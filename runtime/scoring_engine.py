"""
Lead Scoring Engine
"""

from runtime.icp import TARGET


def score(lead):

    score = 0

    reasons = []

    if lead["industry"] in TARGET["industries"]:

        score += 40

        reasons.append("Target industry")

    if TARGET["employee_min"] <= lead["employees"] <= TARGET["employee_max"]:

        score += 30

        reasons.append("Ideal company size")

    if lead["city"] in TARGET["cities"]:

        score += 20

        reasons.append("Target geography")

    return {

        **lead,

        "score": score,

        "reasons": reasons

    }