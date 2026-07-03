"""
Task Object

Every piece of work inside Hermes
is represented as a Task.
"""

from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Task:

    id: str = field(
        default_factory=lambda: str(uuid.uuid4())[:8]
    )

    objective: str = ""

    department: str = ""

    owner: str = ""

    priority: str = "Normal"

    status: str = "Pending"

    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    completed_at: str | None = None

    notes: str = ""

    artifacts: list = field(default_factory=list)

    dependencies: list = field(default_factory=list)

    def complete(self):

        self.status = "Completed"

        self.completed_at = datetime.now().isoformat()

    def to_dict(self):

        return self.__dict__