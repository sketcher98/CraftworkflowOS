"""
Priority Engine

Ranks today's work using executive rules.
"""


def choose_priority(context):

    state = context["company_state"].lower()

    inbox = context["inbox"].lower()

    # Rule 1
    if "urgent" in inbox:

        return {
            "task": "Resolve urgent inbox items",
            "reason": "Urgent work blocks business operations."
        }

    # Rule 2
    if "client" in inbox:

        return {
            "task": "Complete client work",
            "reason": "Client delivery protects revenue."
        }

    # Rule 3
    if "revenue" in state:

        return {
            "task": "Focus on revenue generation",
            "reason": "Revenue has the highest leverage."
        }

    # Rule 4
    if "automation" in state:

        return {
            "task": "Build automation systems",
            "reason": "Automation compounds over time."
        }

    # Default

    return {
        "task": "Review company_state.md",
        "reason": "No higher-priority work was detected."
    }