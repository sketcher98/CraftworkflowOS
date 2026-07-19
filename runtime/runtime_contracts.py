"""
Runtime Contracts

Canonical interfaces for the CraftworkflowOS runtime.
All components must adhere to these contracts.
"""

from typing import Dict, List, Optional, Any, Literal, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod
import uuid


# ============================================================================
# Enums
# ============================================================================

class CapabilityName(str, Enum):
    """Canonical capability names."""
    RESEARCH = "research"
    WRITING = "writing"
    ANALYSIS = "analysis"
    CODING = "coding"
    DESIGN = "design"
    VIDEO_EDITING = "video_editing"
    AUTOMATION = "automation"
    CRM = "crm"
    EMAIL = "email"
    CALENDAR = "calendar"
    DOCUMENT = "document"
    STORAGE = "storage"
    SEARCH = "search"
    MONITORING = "monitoring"
    TESTING = "testing"


class ProviderName(str, Enum):
    """Canonical provider names."""
    PERPLEXITY = "Perplexity"
    GPT_4O = "GPT-4o"
    CLAUDE_35_SONNET = "Claude-3.5-Sonnet"
    GROQ_LLAMA_31_70B = "Groq-Llama-3.1-70B"
    NVIDIA_NIM = "NVIDIA-NIM"
    FIGMA = "Figma"
    PREMIERE = "Premiere"
    HEYGEN = "HeyGen"
    VEED = "VEED"
    MAKE = "Make"
    N8N = "n8n"
    ZAPIER = "Zapier"
    HUBSPOT = "HubSpot"
    PIPEDRIVE = "Pipedrive"
    AIRTABLE = "Airtable"
    GMAIL = "Gmail"
    SENDGRID = "SendGrid"
    MAILGUN = "Mailgun"
    BROWSER = "Browser"
    EXA = "Exa"
    GOOGLE_CALENDAR = "Google-Calendar"
    CALENDLY = "Calendly"
    GOOGLE_DOCS = "Google-Docs"
    NOTION = "Notion"
    PANDOC = "Pandoc"
    GOOGLE_DRIVE = "Google-Drive"
    DROPBOX = "Dropbox"
    CLOUDINARY = "Cloudinary"
    S3 = "S3"
    PLAYWRIGHT = "Playwright"
    PYTEST = "pytest"
    VITEST = "Vitest"


class EmployeeState(str, Enum):
    """Employee lifecycle states."""
    IDLE = "IDLE"
    TRIGGERED = "TRIGGERED"
    EXECUTING = "EXECUTING"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ESCALATED = "ESCALATED"


class WorkflowStatus(str, Enum):
    """Workflow instance status."""
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    COMPENSATING = "COMPENSATING"
    COMPENSATED = "COMPENSATED"
    PAUSED = "PAUSED"


class EventPriority(int, Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


# ============================================================================
# Core Data Classes
# ============================================================================

@dataclass
class RuntimeContext:
    """Context passed to all runtime operations."""
    company: Dict[str, Any] = field(default_factory=dict)
    commercial: Dict[str, Any] = field(default_factory=dict)
    marketing: Dict[str, Any] = field(default_factory=dict)
    operations: Dict[str, Any] = field(default_factory=dict)
    delivery: Dict[str, Any] = field(default_factory=dict)
    finance: Dict[str, Any] = field(default_factory=dict)
    creative: Dict[str, Any] = field(default_factory=dict)
    engineering: Dict[str, Any] = field(default_factory=dict)
    memory: Dict[str, Any] = field(default_factory=dict)
    checkpoint: Dict[str, Any] = field(default_factory=dict)
    latency_budget_ms: Optional[int] = None
    cost_budget: Optional[str] = None  # "low", "medium", "high"
    max_context_needed: Optional[int] = None
    correlation_id: Optional[str] = None


@dataclass
class CapabilityDeclaration:
    """Employee capability declaration from profile."""
    name: CapabilityName
    description: str
    provider_preference: Optional[ProviderName] = None
    required_context: List[str] = field(default_factory=list)
    output_format: str = "markdown"
    memory_write: str = ""


@dataclass
class CapabilityRequest:
    """Request for capability execution."""
    capability: CapabilityName
    objective: str
    context: Optional[RuntimeContext] = None
    priority: EventPriority = EventPriority.NORMAL
    timeout_seconds: Optional[int] = None


@dataclass
class CapabilityResult:
    """Result of capability execution."""
    capability: CapabilityName
    provider: ProviderName
    status: Literal["completed", "failed", "fallback"]
    artifacts: List[Any] = field(default_factory=list)
    routing_metadata: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    latency_ms: int = 0


@dataclass
class Task:
    """Executable task from workflow or director."""
    task_id: str
    name: str
    description: str
    assignee: str  # Employee identifier
    capabilities_required: List[CapabilityName] = field(default_factory=list)
    inputs: Dict[str, Any] = field(default_factory=dict)
    expected_outputs: List[str] = field(default_factory=list)
    timeout_seconds: int = 3600
    retry_policy: Dict[str, Any] = field(default_factory=dict)
    correlation_id: str = ""


@dataclass
class ExecutionResult:
    """Result of task/workflow execution."""
    task_id: str
    status: Literal["completed", "failed", "partial"]
    outputs: Dict[str, Any] = field(default_factory=dict)
    artifacts: List[Any] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    latency_ms: int = 0
    next_actions: List[str] = field(default_factory=list)


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
        import json
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


@dataclass
class Artifact:
    """Canonical artifact envelope."""
    artifact_id: str = field(default_factory=lambda: f"art_{uuid.uuid4().hex[:8]}")
    artifact_type: str = ""
    version: str = "1.0.0"
    title: str = ""
    content: Dict[str, Any] = field(default_factory=dict)
    created_by: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    schema_version: str = "1.0"
    checksum: Optional[str] = None
    
    def __post_init__(self):
        if self.checksum is None and self.content:
            import hashlib
            import json
            content_str = json.dumps(self.content, sort_keys=True, default=str)
            self.checksum = f"sha256:{hashlib.sha256(content_str.encode()).hexdigest()}"


@dataclass
class EmployeeProfile:
    """Employee profile from 03_Departments."""
    name: str
    department: str
    role: str
    reports_to: str
    capability_tier: str
    mission: str
    responsibilities: Dict[str, List[str]] = field(default_factory=dict)
    inputs: Dict[str, List[str]] = field(default_factory=dict)
    outputs: Dict[str, List[str]] = field(default_factory=dict)
    kpis: Dict[str, List[str]] = field(default_factory=dict)
    decision_authority: Dict[str, List[str]] = field(default_factory=dict)
    escalation_rules: List[Dict[str, str]] = field(default_factory=list)
    memory_usage: Dict[str, List[str]] = field(default_factory=dict)
    capability_declarations: List[CapabilityDeclaration] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    playbooks: List[str] = field(default_factory=list)
    dynamic_decision_logic: str = ""
    handoff_rules: List[Dict[str, str]] = field(default_factory=list)
    success_metrics: Dict[str, List[str]] = field(default_factory=dict)
    communication_style: List[str] = field(default_factory=list)
    entry_conditions: List[str] = field(default_factory=list)
    exit_conditions: List[str] = field(default_factory=list)
    failure_conditions: List[str] = field(default_factory=list)


# ============================================================================
# Abstract Interfaces
# ============================================================================

class EmployeeRuntime(ABC):
    """Abstract base class for all employee runtimes."""
    
    @abstractmethod
    def execute(self, task: Task, context: RuntimeContext) -> ExecutionResult:
        """Main execution entry point. Called by workflow engine."""
        pass
    
    @abstractmethod
    def handle_event(self, event: Event) -> Dict[str, Any]:
        """Handle incoming events (capability completion, escalation, etc.)"""
        pass
    
    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        """Return current state for checkpointing."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[CapabilityDeclaration]:
        """Declare required capabilities (from profile)."""
        pass
    
    @abstractmethod
    def get_required_context(self) -> List[str]:
        """Runtime context keys this employee needs."""
        pass


class CapabilityRouter(ABC):
    """Abstract capability router interface."""
    
    @abstractmethod
    def request(self, request: CapabilityRequest) -> CapabilityResult:
        """Route capability request to provider."""
        pass
    
    @abstractmethod
    def get_available_capabilities(self) -> List[CapabilityName]:
        """List all registered capabilities."""
        pass
    
    @abstractmethod
    def register_provider(
        self, 
        name: ProviderName, 
        executor: callable, 
        capabilities: List[CapabilityName],
        metadata: Dict[str, Any] = None
    ):
        """Register a provider."""
        pass


class ProviderRouter(ABC):
    """Abstract provider router interface."""
    
    @abstractmethod
    def select_provider(
        self, 
        capability: CapabilityName, 
        objective: str, 
        context: Optional[RuntimeContext] = None
    ) -> ProviderName:
        """Select optimal provider for capability."""
        pass
    
    @abstractmethod
    def execute_provider(
        self, 
        provider: ProviderName, 
        objective: str
    ) -> Any:
        """Execute specific provider."""
        pass
    
    @abstractmethod
    def get_provider_health(self, provider: ProviderName) -> Dict[str, Any]:
        """Get provider health status."""
        pass


class EventBus(ABC):
    """Abstract event bus interface."""
    
    @abstractmethod
    async def emit(self, event: Event) -> Event:
        """Emit event to subscribers."""
        pass
    
    @abstractmethod
    def subscribe(
        self,
        pattern: str,
        handler: callable,
        priority: EventPriority = EventPriority.NORMAL,
        filter_fn: Optional[callable] = None
    ) -> str:
        """Subscribe to event pattern. Returns subscription ID."""
        pass
    
    @abstractmethod
    async def replay(
        self,
        event_type_pattern: str = "*",
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        handler: Optional[callable] = None
    ) -> int:
        """Replay historical events."""
        pass


class WorkflowEngine(ABC):
    """Abstract workflow engine interface."""
    
    @abstractmethod
    def register_definition(self, definition: Any):
        """Register workflow definition."""
        pass
    
    @abstractmethod
    def start_workflow(
        self, 
        workflow_name: str, 
        correlation_id: str, 
        context: Dict[str, Any]
    ) -> Any:
        """Start workflow instance."""
        pass
    
    @abstractmethod
    async def on_event(self, event: Event):
        """Handle events that may trigger transitions."""
        pass
    
    @abstractmethod
    async def rollback_workflow(self, instance_id: str, to_state: str = None):
        """Rollback workflow to previous state."""
        pass


class MemoryManager(ABC):
    """Abstract memory manager interface (9-layer memory system)."""
    
    @abstractmethod
    def load_identity(self) -> Dict[str, Any]:
        """Load identity layer."""
        pass
    
    @abstractmethod
    def load_working(self, checkpoint: Optional[Any] = None) -> Any:
        """Load working memory."""
        pass
    
    @abstractmethod
    def save_working(self, working_memory: Any):
        """Save working memory."""
        pass
    
    @abstractmethod
    def get_longterm(self, key: str) -> Optional[Any]:
        """Get long-term memory."""
        pass
    
    @abstractmethod
    def set_longterm(self, key: str, value: Any):
        """Set long-term memory."""
        pass
    
    @abstractmethod
    def append_episodic(self, category: str, event: Dict[str, Any]):
        """Append episodic memory."""
        pass
    
    @abstractmethod
    def get_episodic(self, category: str) -> List[Dict[str, Any]]:
        """Get episodic memories."""
        pass
    
    @abstractmethod
    def get_preference(self, key: str) -> Optional[Any]:
        """Get preference."""
        pass
    
    @abstractmethod
    def set_preference(self, key: str, value: Any):
        """Set preference."""
        pass
    
    @abstractmethod
    def is_checkpoint_valid(self, checkpoint: Dict[str, Any]) -> bool:
        """Validate checkpoint against critical docs."""
        pass


class CheckpointSystem(ABC):
    """Abstract checkpoint system."""
    
    @abstractmethod
    def save(self, runtime_state: Dict[str, Any], working_memory: Any = None):
        """Save checkpoint."""
        pass
    
    @abstractmethod
    def load(self) -> Optional[Dict[str, Any]]:
        """Load latest checkpoint."""
        pass
    
    @abstractmethod
    def validate(self, checkpoint: Dict[str, Any], memory_manager: MemoryManager) -> bool:
        """Validate checkpoint."""
        pass


# ============================================================================
# Factory Functions
# ============================================================================

def create_runtime_context() -> RuntimeContext:
    """Create empty runtime context."""
    return RuntimeContext()


def create_capability_request(
    capability: CapabilityName,
    objective: str,
    context: Optional[RuntimeContext] = None
) -> CapabilityRequest:
    """Create capability request."""
    return CapabilityRequest(capability=capability, objective=objective, context=context)


def create_task(
    name: str,
    description: str,
    assignee: str,
    capabilities_required: List[CapabilityName] = None,
    correlation_id: str = None
) -> Task:
    """Create executable task."""
    return Task(
        task_id=f"task_{uuid.uuid4().hex[:8]}",
        name=name,
        description=description,
        assignee=assignee,
        capabilities_required=capabilities_required or [],
        correlation_id=correlation_id or f"corr_{uuid.uuid4().hex[:8]}"
    )


def create_artifact(
    artifact_type: str,
    title: str,
    content: Dict[str, Any],
    created_by: str,
    version: str = "1.0.0"
) -> Artifact:
    """Create artifact."""
    return Artifact(
        artifact_type=artifact_type,
        title=title,
        content=content,
        created_by=created_by,
        version=version
    )


def create_event(
    event_type: str,
    payload: Dict[str, Any],
    source: str,
    correlation_id: Optional[str] = None,
    causation_id: Optional[str] = None
) -> Event:
    """Create event."""
    return Event(
        event_type=event_type,
        payload=payload,
        source=source,
        correlation_id=correlation_id,
        causation_id=causation_id
    )