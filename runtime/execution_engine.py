"""
Execution Engine

Every employee executes work through here.
"""

from runtime.capability_router import request


def execute(task):

    print(f"\nExecuting: {task.objective}\n")

    steps = []

    if task.department == "Commercial":

        steps = [
            ("research", task.objective),
            ("writing", task.objective),
        ]

    elif task.department == "Marketing":

        steps = [
            ("research", task.objective),
            ("writing", task.objective),
            ("design", task.objective),
        ]

    elif task.department == "Operations":

        steps = [
            ("automation", task.objective),
        ]

    results = []

    for capability, objective in steps:

        result = request(
            capability,
            objective
        )

        results.append(result)

    return {
        "task": task.objective,
        "steps": results,
        "status": "completed"
    }