"""
Executive Scoring Engine
"""


def score(task):

    points = 0

    priority = task["priority"]

    if priority == "URGENT":
        points += 100

    elif priority == "HIGH":
        points += 70

    elif priority == "MEDIUM":
        points += 40

    elif priority == "LOW":
        points += 10

    return points