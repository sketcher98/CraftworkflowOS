"""
Hermes Decision Schemas
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Decision:

    employee: str

    playbook: str

    reason: str

    steps: List[str]