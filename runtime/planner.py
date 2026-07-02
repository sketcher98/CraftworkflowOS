"""
Planner

Collects the information required for the
Executive to make decisions.
"""

from pathlib import Path

ROOT = Path(__file__).parent.parent


def read_file(relative_path: str) -> str:
    path = ROOT / relative_path

    if not path.exists():
        return ""

    return path.read_text(encoding="utf-8")


def collect_context(runtime):

    return {
        "company": runtime.company.get("content", ""),
        "identity": runtime.identity.get("content", ""),
        "principles": runtime.principles.get("content", ""),
        "company_state": runtime.company_state.get("content", ""),
        "inbox": read_file("08_Command Center/inbox/new/tasks.md"),
    }