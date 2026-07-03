"""
Capability Router

Employees never call tools directly.

Instead they request a capability.

The router decides which provider
should execute the work.

Routes capabilities to real providers.
"""

from runtime.capabilities import CAPABILITIES

from runtime.providers import (
    browser,
    gpt,
    perplexity,
    opendesign,
    heygen,
    make,
)

PROVIDERS = {
    "Browser": browser.execute,
    "GPT-5": gpt.execute,
    "Perplexity": perplexity.execute,
    "OpenDesign": opendesign.execute,
    "HeyGen": heygen.execute,
    "Make": make.execute,
}


def request(capability: str, objective: str = ""):

    providers = CAPABILITIES.get(
        capability,
        []
    )

    print(f"\nCapability: {capability}")

    completed = []

    for provider in providers:

        executor = PROVIDERS.get(provider)

        if executor is None:
            continue

        completed.append(
            executor(objective)
        )

    return {
        "capability": capability,
        "providers": completed,
        "status": "completed"
    }