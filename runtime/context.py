"""
Operating Context

Represents Hermes' current understanding of
CraftedWorkflows during this session.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class OperatingContext:

    company_loaded: bool = False
    identity_loaded: bool = False
    principles_loaded: bool = False
    company_state_loaded: bool = False

    current_project: str | None = None
    current_client: str | None = None
    current_objective: str | None = None

    company: dict = field(default_factory=dict)
    identity: dict = field(default_factory=dict)
    principles: dict = field(default_factory=dict)
    company_state: dict = field(default_factory=dict)

    saved_at: str | None = None
    
    last_refresh: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)