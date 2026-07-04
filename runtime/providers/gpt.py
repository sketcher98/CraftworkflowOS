from runtime.artifacts import Artifact


def execute(objective):

    print("      GPT writing...")

    artifact = Artifact(
        type="Draft",
        title="Draft",
        content=f"Draft created for:\n\n{objective}",
        created_by="GPT-5"
    )

    return artifact