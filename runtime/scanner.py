"""
Workspace Scanner

Discovers active work across CraftworkflowOS.
"""

from pathlib import Path

ROOT = Path(__file__).parent.parent


def scan_folder(path: Path, ignore: set[str]) -> list[str]:
    """
    Return only active folders.
    """

    items = []

    if not path.exists():
        return items

    for item in path.iterdir():

        if not item.is_dir():
            continue

        if item.name.startswith("."):
            continue

        if item.name in ignore:
            continue

        items.append(item.name)

    return sorted(items)


def scan_workspace():

    workspace = {}

    workspace["projects"] = scan_folder(
        ROOT / "07_Projects",
        ignore={
            "Projects_Archive",
        },
    )

    workspace["clients"] = scan_folder(
        ROOT / "06_Clients",
        ignore={
            "Clients_Archive",
            "Leads",
            "Meetings",
        },
    )

    workspace["tasks"] = []

    inbox = ROOT / "08_Command Center" / "Inbox" / "New"

    if inbox.exists():

        for file in sorted(inbox.glob("*.md")):

            workspace["tasks"].append(file.stem)

    return workspace