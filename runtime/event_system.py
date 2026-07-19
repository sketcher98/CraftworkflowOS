"""
Event System Implementation

Typed event schemas, bus implementation, subscriptions, dead-letter handling, and replay.
"""

import asyncio
import json
import re
import uuid
from datetime import datetime
from typing import Callable, Dict, List, Optional, Pattern, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# Event Priority
# ============================================================================

class EventPriority(int, Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


# ============================================================================
# Event Dataclass
# ============================================================================

@dataclass
class Event:
    """Canonical event envelope."""
    event_id: str = field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:8]}")
    event_type: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
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
        }, default=str)
    
    @classmethod
    def from_json(cls, data: str) -> "Event":
        obj = json.loads(data)
        obj["timestamp"] = datetime.fromisoformat(obj["timestamp"])
        return cls(**obj)


# ============================================================================
# Subscription
# ============================================================================

@dataclass
class Subscription:
    pattern: str
    handler: Callable[[Event], Any]
    priority: EventPriority = EventPriority.NORMAL
    filter_fn: Optional[Callable[[Event], bool]] = None
    compiled: Pattern = field(init=False)
    subscription_id: str = field(default_factory=lambda: f"sub_{uuid.uuid4().hex[:8]}")
    
    def __post_init__(self):
        self.compiled = self._compile_pattern(self.pattern)
    
    def _compile_pattern(self, pattern: str) -> Pattern:
        """Convert glob-style pattern to regex."""
        escaped = re.escape(pattern)
        escaped = escaped.replace(r"\*", ".*")
        return re.compile(f"^{escaped}$")
    
    def matches(self, event_type: str) -> bool:
        return bool(self.compiled.match(event_type))


# ============================================================================
# Dead Letter Queue
# ============================================================================

@dataclass
class DeadLetter:
    event: Event
    error: str
    retry_count: int
    failed_at: datetime = field(default_factory=datetime.now)


class DeadLetterQueue:
    def __init__(self, max_size: int = 10000):
        self.queue: List[DeadLetter] = []
        self.max_size = max_size
    
    def add(self, event: Event, error: Exception, retry_count: int):
        if len(self.queue) >= self.max_size:
            self.queue.pop(0)
        self.queue.append(DeadLetter(
            event=event,
            error=str(error),
            retry_count=retry_count
        ))
    
    def get_all(self) -> List[DeadLetter]:
        return self.queue.copy()
    
    def retry(self, index: int) -> Optional[Event]:
        if 0 <= index < len(self.queue):
            return self.queue.pop(index).event
        return None
    
    def clear(self):
        self.queue.clear()


# ============================================================================
# Event Bus
# ============================================================================

class EventBus:
    def __init__(self, max_log_size: int = 100000):
        self.subscriptions: List[Subscription] = []
        self.dead_letter = DeadLetterQueue()
        self.event_log: List[Event] = []
        self.max_log_size = max_log_size
    
    def subscribe(
        self,
        pattern: str,
        handler: Callable[[Event], Any],
        priority: EventPriority = EventPriority.NORMAL,
        filter_fn: Optional[Callable[[Event], bool]] = None
    ) -> str:
        """Subscribe to event pattern. Returns subscription ID."""
        sub = Subscription(pattern, handler, priority, filter_fn)
        self.subscriptions.append(sub)
        self.subscriptions.sort(key=lambda s: s.priority.value, reverse=True)
        return sub.subscription_id
    
    def unsubscribe(self, subscription_id: str) -> bool:
        for i, sub in enumerate(self.subscriptions):
            if sub.subscription_id == subscription_id:
                self.subscriptions.pop(i)
                return True
        return False
    
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
                logger.error(f"Failed to create task for {sub.subscription_id}: {e}")
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
                await asyncio.sleep(2 ** attempt)
    
    def replay(
        self,
        event_type_pattern: str = "*",
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        handler: Optional[Callable[[Event], Any]] = None
    ) -> int:
        """Replay historical events."""
        events = self.event_log
        
        if since:
            events = [e for e in events if e.timestamp >= since]
        if until:
            events = [e for e in events if e.timestamp <= until]
        
        compiled = self._compile_pattern(event_type_pattern)
        events = [e for e in events if compiled.match(e.event_type)]
        
        count = 0
        for event in events:
            if handler:
                if asyncio.iscoroutinefunction(handler):
                    asyncio.run(handler(event))
                else:
                    handler(event)
            count += 1
        
        return count
    
    def _compile_pattern(self, pattern: str) -> Pattern:
        escaped = re.escape(pattern)
        escaped = escaped.replace(r"\*", ".*")
        return re.compile(f"^{escaped}$")
    
    def get_dead_letters(self) -> List[DeadLetter]:
        return self.dead_letter.get_all()


# Global event bus
EVENT_BUS = EventBus()


# ============================================================================
# Convenience Functions
# ============================================================================

async def emit(
    event_type: str,
    payload: Dict[str, Any],
    source: str,
    correlation_id: Optional[str] = None,
    causation_id: Optional[str] = None,
    **kwargs
) -> Event:
    """Emit event to bus."""
    event = Event(
        event_type=event_type,
        payload=payload,
        source=source,
        correlation_id=correlation_id,
        causation_id=causation_id,
        metadata=kwargs
    )
    await EVENT_BUS.emit(event)
    return event


def subscribe(
    pattern: str,
    handler: Callable[[Event], Any],
    priority: EventPriority = EventPriority.NORMAL,
    filter_fn: Optional[Callable[[Event], bool]] = None
) -> str:
    """Subscribe to event pattern."""
    return EVENT_BUS.subscribe(pattern, handler, priority, filter_fn)


def unsubscribe(subscription_id: str) -> bool:
    """Unsubscribe from event pattern."""
    return EVENT_BUS.unsubscribe(subscription_id)