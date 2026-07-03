"""
Capability Registry

Every business capability maps to one or more providers.

Providers can change.

Capabilities stay forever.
"""

CAPABILITIES = {

    "research": [
        "Perplexity",
        "Browser"
    ],

    "writing": [
        "GPT-5"
    ],

    "coding": [
        "OpenClaw",
        "Codex"
    ],

    "design": [
        "OpenDesign",
        "Figma"
    ],

    "video": [
        "HeyGen",
        "VEED"
    ],

    "automation": [
        "Make",
        "n8n"
    ],

    "crm": [
        "HubSpot"
    ]
}


def get_provider(capability):

    providers = CAPABILITIES.get(
        capability.lower(),
        []
    )

    if not providers:
        return None

    return providers[0]