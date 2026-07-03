"""
Playbook Loader

Loads department playbooks directly from Markdown.
"""

from pathlib import Path
import re

ROOT = Path(__file__).parent.parent


def load_playbook(department: str):

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

    for title, body in matches:
        sections[title.strip()] = body.strip()

    return sections