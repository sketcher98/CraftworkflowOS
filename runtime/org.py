"""
Organization Loader

Loads the executive structure of CraftedWorkflows.
"""

from pathlib import Path

ROOT = Path(__file__).parent.parent


def load_org():
    """
    Load every department director into memory.
    """

    organization = {}

    departments = ROOT / "03_Departments"

    if not departments.exists():
        return organization

    for department in departments.iterdir():

        if not department.is_dir():
            continue

        director_file = department / "Director.md"

        if director_file.exists():

            organization[department.name] = {
                "name": department.name,
                "director": director_file.read_text(
                    encoding="utf-8"
                )
            }

    return organization