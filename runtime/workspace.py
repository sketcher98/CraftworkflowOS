"""
Workspace API

Hermes edits its own workspace through here.
"""

from pathlib import Path

ROOT = Path(__file__).parent.parent


def create_folder(path):

    folder = ROOT / path

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder


def create_file(path, content=""):

    file = ROOT / path

    file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    file.write_text(
        content,
        encoding="utf-8"
    )

    return file


def read_file(path):

    file = ROOT / path

    if not file.exists():

        return ""

    return file.read_text(
        encoding="utf-8"
    )


def update_file(path, content):

    file = ROOT / path

    file.write_text(
        content,
        encoding="utf-8"
    )

    return file


def exists(path):

    return (ROOT / path).exists()