"""
Executive Briefing
"""


def create_briefing(priority):

    return f"""
==========================
Executive Briefing
==========================

Today's Highest Leverage Task

{priority['task']}

Why?

{priority['reason']}
"""