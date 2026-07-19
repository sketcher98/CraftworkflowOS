# Event System Specification

Typed event schemas, bus implementation, subscriptions, dead-letter handling, and replay.

---

## Event Schema

All events follow a canonical envelope:

```json
{
  "event_id": "evt_abc123",
  "event_type": "capability.completed",
  "timestamp": "2025-01-19T10:30:00.123Z",
  "source": "runtime.capability_router",
  "correlation_id": "corr_xyz789",
  "causation_id": "evt_def456",
  "payload": {...},
  "metadata": {
    "retry_count": 0,
    "priority": "normal",
    "ttl_seconds": 3600
  }
}
```

---

## Canonical Event Types

### Employee Lifecycle
```
employee.triggered        # Employee received task
employee.started          # Employee began execution
employee.completed        # Employee finished successfully
employee.failed           # Employee execution failed
employee.escalated        # Employee escalated to director
employee.waiting          # Employee waiting for external input
employee.resumed          # Employee resumed after wait
```

### Capability Routing
```
capability.requested      # Capability requested by employee
capability.routed         # Provider selected
capability.started        # Provider began execution
capability.completed      # Provider returned result
capability.failed         # Provider execution failed
capability.fallback       # Fallback to next provider
```

### Artifact Lifecycle
```
artifact.created          # New artifact produced
artifact.updated          # Artifact modified
artifact.archived         # Artifact moved to cold storage
artifact.validated        # Artifact passed schema validation
artifact.failed_validation # Artifact failed validation
```

### Workflow Engine
```
workflow.started          # Workflow instance created
workflow.transitioned     # State transition occurred
workflow.completed        # Workflow reached terminal state
workflow.failed           # Workflow failed (non-recoverable)
workflow.rolled_back      # Workflow rolled back to previous state
workflow.compensated      # Compensation transaction executed
workflow.paused           # Workflow paused (waiting)
workflow.resumed          # Workflow resumed
```

### Memory & Checkpoint
```
memory.read               # Memory layer read
memory.written            # Memory layer write
checkpoint.saved          # Checkpoint persisted
checkpoint.restored       # Checkpoint loaded
checkpoint.failed         # Checkpoint save/load failed
```

### Director & Orchestration
```
director.delegated        # Director delegated to employee
director.escalated        # Director escalated issue
director.compensated      # Director initiated compensation
director.reassigned       # Director reassigned task
```

### Scheduler
```
scheduler.triggered       # Scheduled job fired
scheduler.completed       # Scheduled job completed
scheduler.failed          # Scheduled job failed
scheduler.misfire         # Job missed its window
```

---

## Event Bus Implementation

```python
import asyncio
import json
from datetime import datetime
from typing import Callable, Dict, List, Pattern, Optional
from dataclasses import dataclass, field
from enum import Enum
import re


class EventPriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class Event:
    event_id: str
    event_type: str
    timestamp: datetime
    source: str
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None
    payload: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    
    def to_json(self) -> str:
        return json.dumps({
            "event_id": self.event_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "payload": self.payload,
            "metadata": self.metadata
        })
    
    @classmethod
    def from_json(cls, data: str) -> "Event":
        obj = json.loads(data)
        obj["timestamp"] = datetime.fromisoformat(obj["timestamp"])
        return cls(**obj)


class Subscription:
    def __init__(
        self,
        pattern: str,
        handler: Callable[[Event], asyncio.coroutine],
        priority: EventPriority = EventPriority.NORMAL,
        filter_fn: Optional[Callable[[Event], bool]] = None
    ):
        self.pattern = pattern
        self.handler = handler
        self.priority = priority
        self.filter_fn = filter_fn
        self.compiled = self._compile_pattern(pattern)
    
    def _compile_pattern(self, pattern: str) -> Pattern:
        """Convert glob-style pattern to regex."""
        # Escape special chars, then replace * with .*
        escaped = re.escape(pattern)
        escaped = escaped.replace(r"\*", ".*")
        return re.compile(f"^{escaped}$")
    
    def matches(self, event_type: str) -> bool:
        return bool(self.compiled.match(event_type))


class DeadLetterQueue:
    def __init__(self, max_size: int = 10000):
        self.queue: List[DeadLetter] = []
        self.max_size = max_size
    
    def add(self, event: Event, error: Exception, retry_count: int):
        if len(self.queue) >= self.max_size:
            self.queue.pop(0)  # FIFO eviction
        self.queue.append(DeadLetter(
            event=event,
            error=str(error),
            retry_count=retry_count,
            failed_at=datetime.utcnow()
        ))
    
    def get_all(self) -> List[DeadLetter]:
        return self.queue.copy()
    
    def retry(self, index: int) -> Optional[Event]:
        if 0 <= index < len(self.queue):
            return self.queue.pop(index).event
        return None


class EventBus:
    def __init__(self):
        self.subscriptions: List[Subscription] = []
        self.dead_letter = DeadLetterQueue()
        self.event_log: List[Event] = []  # For replay
        self.max_log_size = 100000
    
    def subscribe(
        self,
        pattern: str,
        handler: Callable,
        priority: EventPriority = EventPriority.NORMAL,
        filter_fn: Optional[Callable[[Event], bool]] = None
    ) -> str:
        """Subscribe to event pattern. Returns subscription ID."""
        sub = Subscription(pattern, handler, priority, filter_fn)
        self.subscriptions.append(sub)
        # Sort by priority (highest first)
        self.subscriptions.sort(key=lambda s: s.priority.value, reverse=True)
        return f"sub_{len(self.subscriptions)}"
    
    def unsubscribe(self, subscription_id: str) -> bool:
        # Implementation depends on ID format
        pass
    
    async def emit(self, event: Event):
        """Emit event to all matching subscribers."""
        # Log for replay
        self.event_log.append(event)
        if len(self.event_log) > self.max_log_size:
            self.event_log = self.event_log[-self.max_log_size:]
        
        # Find matching subscriptions
        matched = [s for s in self.subscriptions if s.matches(event.event_type)]
        
        # Apply filters
        filtered = [s for s in matched if s.filter_fn is None or s.filter_fn(event)]
        
        # Execute in priority order
        tasks = []
        for sub in filtered:
            try:
                task = asyncio.create_task(sub.handler(event))
                tasks.append(task)
            except Exception as e:
                self.dead_letter.add(event, e, event.metadata.get("retry_count", 0))
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    self.dead_letter.add(event, result, event.metadata.get("retry_count", 0))
    
    async def emit_with_retry(self, event: Event, max_retries: int = 3):
        """Emit with automatic retry on handler failure."""
        for attempt in range(max_retries + 1):
            try:
                await self.emit(event)
                return
            except Exception as e:
                if attempt == max_retries:
                    self.dead_letter.add(event, e, attempt)
                    raise
                event.metadata["retry_count"] = attempt + 1
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    def replay(
        self,
        event_type_pattern: str = "*",
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        handler: Optional[Callable[[Event], asyncio.coroutine]] = None
    ) -> int:
        """Replay historical events to handlers."""
        events = self.event_log
        
        if since:
            events = [e for e in events if e.timestamp >= since]
        if until:
            events = [e for e in events if e.timestamp <= until]
        
        # Filter by pattern
        compiled = self._compile_pattern(event_type_pattern)
        events = [e for e in events if compiled.match(e.event_type)]
        
        count = 0
        for event in events:
            if handler:
                asyncio.run(handler(event))
            count += 1
        
        return count
    
    def _compile_pattern(self, pattern: str) -> Pattern:
        escaped = re.escape(pattern)
        escaped = escaped.replace(r"\*", ".*")
        return re.compile(f"^{escaped}$")


# Global event bus instance
EVENT_BUS = EventBus()


# Convenience functions
async def emit(event_type: str, payload: dict, source: str, **kwargs) -> Event:
    event = Event(
        event_id=f"evt_{uuid.uuid4().hex[:8]}",
        event_type=event_type,
        timestamp=datetime.utcnow(),
        source=source,
        payload=payload,
        **kwargs
    )
    await EVENT_BUS.emit(event)
    return event


def subscribe(pattern: str, handler: Callable, **kwargs) -> str:
    return EVENT_BUS.subscribe(pattern, handler, **kwargs)
```

---

## Subscription Patterns

```python
# Subscribe to all capability events
subscribe("capability.*", handle_capability_event)

# Subscribe to specific employee events
subscribe("employee.completed", handle_completion)

# Subscribe with filter
subscribe(
    "artifact.created",
    handle_artifact,
    filter_fn=lambda e: e.payload.get("type") == "proposal"
)

# Subscribe with priority
subscribe("workflow.failed", handle_critical_failure, priority=EventPriority.CRITICAL)
```

---

## Event Handlers

```python
async def handle_capability_event(event: Event):
    """Route capability events to workflow engine."""
    if event.event_type == "capability.completed":
        await workflow_engine.on_capability_complete(event)
    elif event.event_type == "capability.failed":
        await workflow_engine.on_capability_failed(event)

async def handle_artifact_created(event: Event):
    """Index artifact for search, update registry."""
    artifact = event.payload
    await artifact_registry.index(artifact)
    await workflow_engine.on_artifact_available(artifact)

async def handle_workflow_failed(event: Event):
    """Alert, log, initiate compensation."""
    await alerting.alert("workflow_failed", event.payload)
    await workflow_engine.initiate_compensation(event.correlation_id)
```

---

## Dead Letter Handling

```python
async def process_dead_letters():
    """Process dead letter queue periodically."""
    for dl in EVENT_BUS.dead_letter.get_all():
        # Try to replay
        try:
            await EVENT_BUS.emit(dl.event)
            EVENT_BUS.dead_letter.retry(dl.index)
        except Exception:
            # Alert on persistent failures
            if dl.retry_count >= 3:
                await alerting.alert("dead_letter_persistent", {
                    "event": dl.event.to_json(),
                    "error": dl.error,
                    "retry_count": dl.retry_count
                })
```

---

## Event Replay

```python
# Replay all capability events from last hour
replayed = EVENT_BUS.replay(
    event_type_pattern="capability.*",
    since=datetime.utcnow() - timedelta(hours=1),
    handler=new_handler
)

# Replay specific workflow
replayed = EVENT_BUS.replay(
    event_type_pattern="workflow.*",
    since=datetime.utcnow() - timedelta(days=1),
    handler=workflow_engine.replay
)
```

---

## Observability

### Structured Logging
```python
import structlog

logger = structlog.get_logger()

async def emit(event: Event):
    logger.info(
        "event_emitted",
        event_id=event.event_id,
        event_type=event.event_type,
        source=event.source,
        correlation_id=event.correlation_id,
        latency_ms=event.metadata.get("latency_ms")
    )
```

### Metrics
```python
from prometheus_client import Counter, Histogram

EVENTS_EMITTED = Counter("events_emitted_total", "Total events emitted", ["event_type"])
EVENT_HANDLER_LATENCY = Histogram("event_handler_latency_seconds", "Handler latency", ["event_type"])
EVENTS_FAILED = Counter("events_failed_total", "Failed events", ["event_type", "error_type"])
DEAD_LETTER_SIZE = Gauge("dead_letter_queue_size", "Dead letter queue size")
```

---

## Testing Requirements

```python
def test_event_bus():
    bus = EventBus()
    
    # Test basic emit/subscribe
    received = []
    async def handler(e):
        received.append(e)
    
    sub_id = bus.subscribe("test.*", handler)
    await bus.emit(Event(event_type="test.event", payload={"foo": "bar"}))
    await asyncio.sleep(0.1)  # Allow async processing
    assert len(received) == 1
    assert received[0].payload["foo"] == "bar"
    
    # Test pattern matching
    assert bus.subscriptions[0].matches("test.event")
    assert bus.subscriptions[0].matches("test.other")
    assert not bus.subscriptions[0].matches("other.event")
    
    # Test filter
    filtered = []
    async def filtered_handler(e):
        filtered.append(e)
    
    bus.subscribe("test.*", filtered_handler, filter_fn=lambda e: e.payload.get("important"))
    await bus.emit(Event(event_type="test.a", payload={"important": True}))
    await bus.emit(Event(event_type="test.b", payload={"important": False}))
    assert len(filtered) == 1
    
    # Test dead letter
    async def failing_handler(e):
        raise ValueError("intentional")
    
    bus.subscribe("fail.*", failing_handler)
    await bus.emit(Event(event_type="fail.test", payload={}))
    await asyncio.sleep(0.1)
    assert len(bus.dead_letter.queue) == 1
    
    # Test replay
    replayed = []
    async def replay_handler(e):
        replayed.append(e)
    
    count = bus.replay("test.*", handler=replay_handler)
    assert count == 2  # Two test events emitted
```