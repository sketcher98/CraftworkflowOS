"""
Reasoning Engine

Hermes reasons using company knowledge,
not hardcoded business logic.
"""


def reason(department, lead):

    director = department["director"]

    playbook = department["playbook"]

    employees = department["employees"]

    objective = []

    objective.append(
        f"Lead Score: {lead['score']}"
    )

    objective.append(
        f"Industry: {lead['industry']}"
    )

    objective.append(
        f"Employees: {lead['employees']}"
    )

    objective.append(
        f"Location: {lead['city']}"
    )

    return {

        "director": director,

        "playbook": playbook,

        "employees": employees,

        "context": "\n".join(objective)

    }