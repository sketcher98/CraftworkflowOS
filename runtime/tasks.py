"""
Task Collector

Collects tasks from CraftworkflowOS.
"""

from pathlib import Path

from runtime.document import parse_markdown

ROOT = Path(__file__).parent.parent


def collect_tasks():

    tasks = []

    inbox = ROOT / "08_Command Center" / "Inbox" / "New"

    if not inbox.exists():
        return tasks

    for file in inbox.glob("*.md"):

        document = parse_markdown(file)

        tasks.extend(document["tasks"])

    return tasks