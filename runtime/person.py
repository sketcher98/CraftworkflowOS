"""
Person Loader

Loads Directors and Employees into structured objects.
"""

from pathlib import Path

ROOT = Path(__file__).parent.parent


def load_person(path: Path):

    if not path.exists():
        return None

    text = path.read_text(
        encoding="utf-8"
    )

    # Use parent directory name for employee (e.g., "Discovery" from "Employees/Discovery/Profile.md")
    # For directors, the file is named like "Commercial_Director.md" so use stem
    if path.parent.name == "Employees":
        name = path.parent.parent.name  # e.g., "Discovery"
    else:
        name = path.stem.replace("_", " ")

    return {
        "name": name,
        "content": text
    }