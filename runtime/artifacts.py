"""
Artifact Store

Every provider returns artifacts.

Artifacts are passed between employees.
"""

from dataclasses import dataclass, field


@dataclass
class Artifact:

    type: str

    title: str

    content: str

    created_by: str

    metadata: dict = field(default_factory=dict)