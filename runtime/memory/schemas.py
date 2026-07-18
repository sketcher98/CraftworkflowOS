"""
Memory Data Structures

Core data classes for CraftworkflowOS memory system.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


@dataclass
class IdentityMemory:
    """Hermes identity - static, defines who Hermes is."""
    role: str = "Chief Operating Officer"
    company: str = "CraftedWorkflows"
    mission: str = ""
    principles: List[str] = field(default_factory=list)
    authority: List[str] = field(default_factory=list)
    never_do: List[str] = field(default_factory=list)
    communication_style: str = "Clear, direct, executive"
    success_metrics: List[str] = field(default_factory=list)
    updated: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)


@dataclass
class WorkingMemory:
    """Session-scoped working memory - active context."""
    current_objective: str = ""
    active_project: Optional[str] = None
    active_client: Optional[str] = None
    session_notes: str = ""
    inbox_snapshot: Dict = field(default_factory=dict)
    priorities: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    active_skills: List[str] = field(default_factory=list)
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)


@dataclass
class ClientProfile:
    """Long-term client memory."""
    name: str
    company: str = ""
    industry: str = ""
    size: str = ""
    contacts: List[Dict] = field(default_factory=list)
    pain_points: List[str] = field(default_factory=list)
    buying_signals: List[str] = field(default_factory=list)
    communication_preferences: Dict = field(default_factory=dict)
    engagement_history: List[Dict] = field(default_factory=list)
    proposals_sent: List[Dict] = field(default_factory=list)
    status: str = "prospect"  # prospect, active, past, dormant
    tags: List[str] = field(default_factory=list)
    created: str = field(default_factory=lambda: datetime.now().isoformat())
    updated: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Episode:
    """Episodic memory - specific events with outcomes."""
    id: str
    title: str
    date: str
    context: str
    action: str
    outcome: str
    learning: str
    tags: List[str] = field(default_factory=list)
    related_entities: List[str] = field(default_factory=list)
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Skill:
    """Reusable skill/playbook."""
    name: str
    category: str
    description: str
    steps: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    examples: List[Dict] = field(default_factory=list)
    success_metrics: List[str] = field(default_factory=list)
    version: int = 1
    created: str = field(default_factory=lambda: datetime.now().isoformat())
    updated: str = field(default_factory=lambda: datetime.now().isoformat())
    usage_count: int = 0
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Reflection:
    """Post-action reflection/learning."""
    date: str
    period: str  # daily, weekly, project, strategic
    context: str
    what_worked: List[str] = field(default_factory=list)
    what_didnt: List[str] = field(default_factory=list)
    adjustments: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Decision:
    """Record of a significant decision."""
    id: str
    topic: str
    timestamp: str
    context: str
    options: List[Dict] = field(default_factory=list)
    chosen: str = ""
    rationale: str = ""
    outcome: str = "pending"  # pending, confirmed, reversed
    reversibility: str = "medium"  # low, medium, high
    review_date: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Preference:
    """Learned preference/default."""
    category: str
    key: str
    value: Any
    confidence: float = 0.5  # 0-1, how confident we are
    source: str = "observed"  # observed, explicit, inferred
    updated: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Pattern:
    """Recognized business pattern."""
    name: str
    description: str
    contexts: List[str] = field(default_factory=list)
    indicators: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    success_rate: float = 0.0
    occurrences: int = 0
    last_seen: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return asdict(self)