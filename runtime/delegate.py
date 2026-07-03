"""
Delegation Engine

Allows Directors to delegate work to Employees.
"""


def delegate(task: str, employee: dict):

    print(f"\nDelegating to {employee['name']}...")
    print(f"Task: {task}")

    return {
        "employee": employee["name"],
        "task": task,
        "status": "Completed",
        "recommendation":
            f"{employee['name']} completed assigned objective."
    }