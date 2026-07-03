"""
Department Delegator

Routes work to the correct department.
"""

def choose_department(task: str):

    task = task.lower()

    commercial_keywords = [
        "client",
        "lead",
        "prospect",
        "outreach",
        "proposal",
        "pipeline",
        "crm",
        "discovery",
        "sales",
        "linkedin",
        "twitter",
        "x",
        "email",
        "follow up",
    ]

    for keyword in commercial_keywords:
        if keyword in task:
            return "Commercial"

    return "Executive"