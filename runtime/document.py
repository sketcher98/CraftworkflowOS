"""
Document Parser

Converts markdown documents into structured data
that Hermes can reason about.
"""

from pathlib import Path


def parse_markdown(path: Path):

    """
    Reads a markdown document and extracts tasks.

    Returns:
        {
            "title": filename,
            "tasks": [...]
        }
    """

    document = {
        "title": path.stem,
        "tasks": []
    }

    if not path.exists():
        return document

    current_priority = "NORMAL"

    with open(path, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            # Ignore headings

            if line.startswith("#"):

                heading = line.replace("#", "").strip().upper()

                if heading in [
                    "URGENT",
                    "HIGH",
                    "MEDIUM",
                    "LOW"
                ]:
                    current_priority = heading

                continue

            # Task

            if line.startswith("-"):

                task = line[1:].strip()

                document["tasks"].append({

                    "title": task,

                    "priority": current_priority,

                    "completed": False

                })

    return document