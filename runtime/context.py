"""
Operating Context

Represents Hermes' current understanding of
CraftedWorkflows during this session.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class OperatingContext:

    # Runtime status
    company_loaded: bool = False
    identity_loaded: bool = False
    principles_loaded: bool = False
    company_state_loaded: bool = False

    # Current focus
    current_project: str | None = None
    current_client: str | None = None
    current_objective: str | None = None

    # Loaded knowledge
    company: dict = field(default_factory=dict)
    identity: dict = field(default_factory=dict)
    principles: dict = field(default_factory=dict)
    company_state: dict = field(default_factory=dict)
    organization: dict = field(default_factory=dict)

    # Runtime metadata
    saved_at: str | None = None
    last_refresh: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    def to_dict(self):
        return {
            "company_loaded": self.company_loaded,
            "identity_loaded": self.identity_loaded,
            "principles_loaded": self.principles_loaded,
            "company_state_loaded": self.company_state_loaded,
            "current_project": self.current_project,
            "current_client": self.current_client,
            "current_objective": self.current_objective,
            "company": self.company,
            "identity": self.identity,
            "principles": self.principles,
            "company_state": self.company_state,
            "organization": self.organization,
            "saved_at": self.saved_at,
            "last_refresh": self.last_refresh,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)