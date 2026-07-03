"""
Priority Engine

Ranks today's work using executive rules.
"""


from runtime.tasks import collect_tasks
from runtime.scoring import score


def choose_priority(context):

    tasks = collect_tasks()

    if not tasks:

        return {
            "task": "Review company_state.md",
            "reason": "No work was found."
        }

    best = max(tasks, key=score)

    return {

        "task": best["title"],

        "reason": f"Priority: {best['priority']}"

    }