"""
Commercial Brain

Decides HOW Hermes should approach a lead.
"""


def choose_strategy(lead):

    score = lead["score"]

    industry = lead["industry"]

    employees = lead["employees"]

    if score >= 90:

        return {

            "playbook": "Founder Mirror",

            "flow": 1,

            "platform": "LinkedIn",

            "priority": "Critical"

        }

    if employees >= 10:

        return {

            "playbook": "Risk Audit",

            "flow": 5,

            "platform": "LinkedIn",

            "priority": "High"

        }

    if industry == "Creative Agency":

        return {

            "playbook": "Conversational",

            "flow": 4,

            "platform": "X",

            "priority": "High"

        }

    return {

        "playbook": "Permission Based",

        "flow": 2,

        "platform": "LinkedIn",

        "priority": "Medium"

    }