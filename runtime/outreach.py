"""
Outreach Employee
"""

from runtime.commercial_brain import choose_strategy


def create_messages(leads):

    messages = []

    for lead in leads:

        strategy = choose_strategy(lead)

        if strategy["flow"] == 1:

            text = f"""Hey {lead['company']},

Quick question—

Has workload started growing faster than operational freedom recently?

—Precious"""

        elif strategy["flow"] == 5:

            text = f"""Quick question—

What breaks inside {lead['company']} if you disappear for four days?

—Precious"""

        elif strategy["flow"] == 4:

            text = f"""Hey—

I've seen {lead['company']} around.

Are you mainly focused on getting more clients right now?

—Precious"""

        else:

            text = f"""Mind if I'm direct for 30 seconds?

—Precious"""

        messages.append({

            "company": lead["company"],

            "strategy": strategy,

            "message": text

        })

    return messages