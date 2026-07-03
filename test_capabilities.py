from runtime.capabilities import get_provider

tests = [
    "research",
    "writing",
    "coding",
    "design",
    "video",
    "automation",
]

for capability in tests:

    print(
        capability,
        "→",
        get_provider(capability)
    )