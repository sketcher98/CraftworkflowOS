"""
Knowledge Loader

Loads markdown knowledge for Hermes.
"""

from pathlib import Path

ROOT = Path(__file__).parent.parent


def read(path):

    path = ROOT / path

    if not path.exists():
        return ""

    return path.read_text(
        encoding="utf-8"
    )


def load_department(name):

    base = ROOT / "03_Departments" / name

    knowledge = {

        "director": "",

        "playbook": "",

        "readme": "",

        "employees": {}

    }

    director = base / f"{name}_Director.md"

    if director.exists():

        knowledge["director"] = director.read_text(
            encoding="utf-8"
        )

    playbook = base / "Playbook.md"

    if playbook.exists():

        knowledge["playbook"] = playbook.read_text(
            encoding="utf-8"
        )

    readme = base / "README.md"

    if readme.exists():

        knowledge["readme"] = readme.read_text(
            encoding="utf-8"
        )

    employees = base / "Employees"

    if employees.exists():

        for employee in employees.iterdir():

            profile = employee / "Profile.md"

            if profile.exists():

                knowledge["employees"][employee.name] = profile.read_text(
                    encoding="utf-8"
                )

    return knowledge