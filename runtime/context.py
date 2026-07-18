"""
Operating Context

Represents Hermes' current understanding of
CraftedWorkflows during this session.

Cache Tiers:
- Hot: Static context (loaded once)
- Warm: Dynamic context (refreshed on demand)
- Cold: Reference context (loaded on request)
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class OperatingContext:

    # Hot Cache (Static - loaded once)
    hot_loaded: bool = False
    company: dict = field(default_factory=dict)
    identity: dict = field(default_factory=dict)
    principles: dict = field(default_factory=dict)
    company_state: dict = field(default_factory=dict)
    boot_sequence: dict = field(default_factory=dict)
    mission_loop: dict = field(default_factory=dict)
    refresh_policy: dict = field(default_factory=dict)
    cache_rules: dict = field(default_factory=dict)
    session_manager: dict = field(default_factory=dict)
    runtime_context: dict = field(default_factory=dict)
    organization: dict = field(default_factory=dict)

    # Warm Cache (Dynamic - refreshed on demand)
    warm_loaded: bool = False
    force_warm_refresh: bool = False
    inbox_tasks: dict = field(default_factory=dict)
    projects: dict = field(default_factory=dict)
    current_client_docs: dict = field(default_factory=dict)
    recent_logs: dict = field(default_factory=dict)

    # Cold Cache (Reference - on request)
    archive: dict = field(default_factory=dict)
    knowledge_base: dict = field(default_factory=dict)

    # Current focus
    current_project: str | None = None
    current_client: str | None = None
    current_objective: str | None = None

    # Runtime metadata
    saved_at: str | None = None
    last_refresh: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    def to_dict(self):
        return {
            "hot_loaded": self.hot_loaded,
            "warm_loaded": self.warm_loaded,
            "force_warm_refresh": self.force_warm_refresh,
            "current_project": self.current_project,
            "current_client": self.current_client,
            "current_objective": self.current_objective,
            "company": self.company,
            "identity": self.identity,
            "principles": self.principles,
            "company_state": self.company_state,
            "boot_sequence": self.boot_sequence,
            "mission_loop": self.mission_loop,
            "refresh_policy": self.refresh_policy,
            "cache_rules": self.cache_rules,
            "session_manager": self.session_manager,
            "runtime_context": self.runtime_context,
            "organization": self.organization,
            "inbox_tasks": self.inbox_tasks,
            "projects": self.projects,
            "current_client_docs": self.current_client_docs,
            "recent_logs": self.recent_logs,
            "archive": self.archive,
            "knowledge_base": self.knowledge_base,
            "saved_at": self.saved_at,
            "last_refresh": self.last_refresh,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)