"""
CraftworkflowOS Loader

Loads the core business documents into the
OperatingContext.

Version: 0.2
"""

from pathlib import Path

ROOT = Path(__file__).parent.parent


def read_markdown(relative_path: str) -> str:
    """
    Read a markdown file.

    Returns an empty string if the file
    doesn't exist.
    """

    path = ROOT / relative_path

    if not path.exists():
        print(f"WARNING: Missing {relative_path}")
        return ""

    return path.read_text(
        encoding="utf-8"
    )


def load_company(runtime):

    # Don't reload if already loaded.
    if runtime.company_loaded:
        print("Company already loaded.")
        return runtime

    runtime.company["content"] = read_markdown(
        "01_CEO/company.md"
    )

    runtime.identity["content"] = read_markdown(
        "02_COO/identity.md"
    )

    runtime.principles["content"] = read_markdown(
        "01_CEO/decision_principles.md"
    )

    runtime.company_state["content"] = read_markdown(
        "02_COO/company_state.md"
    )

    runtime.company_loaded = True
    runtime.identity_loaded = True
    runtime.principles_loaded = True
    runtime.company_state_loaded = True

    print("Core company knowledge loaded.")

    return runtime