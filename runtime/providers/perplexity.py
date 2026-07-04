from runtime.artifacts import Artifact


def execute(objective):

    print("      Perplexity researching...")

    artifact = Artifact(
        type="Research",
        title="ICP Research",
        content=f"""
Research summary for:

{objective}

Recommended targets:

• Creative agencies
• Marketing agencies
• Automation consultancies
""",
        created_by="Perplexity"
    )

    return artifact