"""
Organization Loader

Discovers the company automatically.
"""

from pathlib import Path
from runtime.person import load_person

ROOT = Path(__file__).parent.parent

IGNORE = {
    "Agents",
    "Archive",
    "__pycache__"
}


def discover_organization():

    root = ROOT / "03_Departments"

    organization = {}

    for department in sorted(root.iterdir()):

        if not department.is_dir():
            continue

        if department.name in IGNORE:
            continue

        director = load_person(
            department /
            f"{department.name}_Director.md"
        )

        employees = []

        employee_folder = department / "Employees"

        if employee_folder.exists():

            for employee in sorted(
                employee_folder.glob("*.md")
            ):

                employees.append(
                    load_person(employee)
                )

        organization[department.name] = {
            "director": director,
            "employees": employees
        }

    return organization