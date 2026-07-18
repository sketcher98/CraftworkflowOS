"""
Playbook Loader

Loads department playbooks directly from Markdown.
"""

from pathlib import Path
import re

ROOT = Path(__file__).parent.parent


def load_playbook(department: str):
    """
    Load playbook for a department.
    Maps section titles to employee names.
    """
    path = (
        ROOT /
        "03_Departments" /
        department /
        "Playbook.md"
    )

    if not path.exists():
        return {}

    text = path.read_text(encoding="utf-8")

    sections = {}

    matches = re.findall(
        r"## (.*?)\n(.*?)(?=\n## |\Z)",
        text,
        flags=re.S
    )

    # Map playbook section titles to employee names
    employee_map = {
        "Discovery": "Discovery",
        "Lead Intelligence": "Lead Intelligence",
        "Outreach": "Outreach",
        "Pipeline": "Pipeline",
        "Proposal": "Proposal",
        "Prospecting": "Prospecting",
    }

    for title, body in matches:
        title = title.strip()
        if title in employee_map:
            sections[employee_map[title]] = body.strip()

    return sections