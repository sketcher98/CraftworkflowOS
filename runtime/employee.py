"""
Employee Loader

Loads employee manuals.
"""

from pathlib import Path

ROOT = Path(__file__).parent.parent


def load_employee(department, employee):

    file = (
        ROOT
        / "03_Departments"
        / department
        / "Employees"
        / f"{employee}.md"
    )

    if not file.exists():
        return ""

    return file.read_text(
        encoding="utf-8"
    )