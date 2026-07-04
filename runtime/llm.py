"""
Hermes LLM Interface

Every department thinks through here.

Today:
    Mock

Tomorrow:
    GPT-5
    Claude
    Gemini
    OpenRouter
    Local Models
"""

from textwrap import shorten


def think(prompt: str):

    print()

    print("=" * 60)
    print("HERMES THINKING")
    print("=" * 60)

    print()

    print(
        shorten(
            prompt,
            width=350,
            placeholder=" ..."
        )
    )

    print()

    return {
        "employee": "Outreach",
        "reason":
        "Lead is highly qualified and ready for first contact.",

        "playbook":
        "Founder Mirror",

        "steps": [

            "Personalize opening",

            "Send LinkedIn DM",

            "Schedule follow-up in 2 days"

        ]
    }