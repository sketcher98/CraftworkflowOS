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

    return {
        "name": path.stem.replace("_", " "),
        "content": text
    }