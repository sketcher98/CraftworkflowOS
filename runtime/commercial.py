"""
Commercial Department

Coordinates the Commercial team.
"""

from runtime.execution_engine import execute
from runtime.scoring_engine import score


def discovery(task):

    print("\n========== DISCOVERY ==========")

    return execute(task)


def lead_intelligence(artifacts):

    print("\n========== LEAD INTELLIGENCE ==========")

    qualified = []

    for artifact in artifacts:

        if artifact.type != "LeadList":
            continue

        for row in artifact.content.splitlines():

            row = row.strip()

            if not row:
                continue

            company, industry, city, size = row.split("|")

            employees = int(size.split()[0])

            qualified.append(

                score({

                    "company": company,

                    "industry": industry,

                    "city": city,

                    "employees": employees,

                })

            )

    qualified.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    return qualified

