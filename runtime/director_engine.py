"""
Director Engine

Coordinates department employees.
"""

from runtime.delegate import delegate
from runtime.playbook_loader import load_playbook


def run_department(task: str, department: dict):

    reports = []

    playbook = load_playbook(
        department["name"]
    )

    for employee in department["employees"]:

        employee_task = playbook.get(
            employee["name"],
            task
        )

        reports.append(
            delegate(
                employee_task,
                employee
            )
        )

    return {
        "department": department["director"]["name"],
        "reports": reports
    }