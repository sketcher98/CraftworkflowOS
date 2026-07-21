"""
CraftworkflowOS Loader

Loads all company knowledge into the OperatingContext
using tiered caching (Hot/Warm/Cold).

Version: 1.0
"""

from pathlib import Path
from runtime.org import load_org

ROOT = Path(__file__).parent.parent


def read_markdown(relative_path: str) -> str:
    """
    Read a markdown file.

    Returns an empty string if the file doesn't exist.
    """

    path = ROOT / relative_path

    if not path.exists():
        print(f"WARNING: Missing {relative_path}")
        return ""

    return path.read_text(encoding="utf-8")


def load_hot_cache(runtime):
    """
    Load Hot Cache (Static Context) - loaded once per session.
    
    Contains: Company, Identity, Principles, Company State, 
    Boot Sequence, Mission Loop, Refresh Policy, Cache Rules,
    Session Manager, Runtime Context, Organization.
    """

    if runtime.hot_loaded:
        print("Hot cache already loaded.")
        return runtime

    # 01_CEO
    runtime.company["content"] = read_markdown("01_CEO/company.md")
    runtime.principles["content"] = read_markdown("01_CEO/decision_principles.md")

    # 02_COO
    runtime.identity["content"] = read_markdown("02_COO/identity.md")
    runtime.company_state["content"] = read_markdown("02_COO/company_state.md")

    # 00_Systems
    runtime.boot_sequence["content"] = read_markdown("00_Systems/boot_sequence.md")
    runtime.mission_loop["content"] = read_markdown("00_Systems/mission_loop.md")
    runtime.refresh_policy["content"] = read_markdown("00_Systems/Session/refresh_policy.md")
    runtime.cache_rules["content"] = read_markdown("00_Systems/Session/cache_rules.md")
    runtime.session_manager["content"] = read_markdown("00_Systems/Session/session_manager.md")
    runtime.runtime_context["content"] = read_markdown("00_Systems/Session/runtime_context.md")

    # 03_Departments - Organization structure
    runtime.organization = load_org()

    # Canonical local Notion index: load once for this session.
    from runtime.notion_workspace_index import get_notion_workspace_index
    runtime.notion_workspace_index = get_notion_workspace_index(ROOT)

    runtime.hot_loaded = True
    print("Hot cache loaded (static context).")

    return runtime


def load_warm_cache(runtime, force=False):
    """
    Load Warm Cache (Dynamic Context) - refreshed on demand.
    
    Contains: Inbox tasks, Active Projects, Current Client docs, Recent Logs.
    """

    if runtime.warm_loaded and not force and not runtime.force_warm_refresh:
        print("Warm cache already loaded (use force=True or set force_warm_refresh to refresh).")
        return runtime

    # 08_Command_Center - Inbox
    inbox_path = ROOT / "08_Command Center" / "Inbox" / "New"
    runtime.inbox_tasks["files"] = {}
    if inbox_path.exists():
        for file in inbox_path.glob("*.md"):
            runtime.inbox_tasks["files"][file.name] = file.read_text(encoding="utf-8")

    # 07_Projects - Active projects
    projects_path = ROOT / "07_Projects"
    runtime.projects["files"] = {}
    if projects_path.exists():
        for file in projects_path.rglob("*.md"):
            rel_path = file.relative_to(ROOT)
            runtime.projects["files"][str(rel_path)] = file.read_text(encoding="utf-8")

    # 06_Clients - Current client (if any)
    clients_path = ROOT / "06_Clients"
    runtime.current_client_docs["files"] = {}
    if clients_path.exists():
        for file in clients_path.rglob("*.md"):
            rel_path = file.relative_to(ROOT)
            runtime.current_client_docs["files"][str(rel_path)] = file.read_text(encoding="utf-8")

    # 05_Operations - Recent logs
    ops_path = ROOT / "05_Operations"
    runtime.recent_logs["files"] = {}
    if ops_path.exists():
        for file in ops_path.rglob("*.md"):
            rel_path = file.relative_to(ROOT)
            runtime.recent_logs["files"][str(rel_path)] = file.read_text(encoding="utf-8")

    runtime.warm_loaded = True
    runtime.force_warm_refresh = False
    print("Warm cache loaded (dynamic context).")

    return runtime


def load_cold_cache(runtime):
    """
    Load Cold Cache (Reference Context) - loaded on request.
    
    Contains: Archive, Knowledge Base (04_Knowledge, 09_Archive).
    """

    # 04_Knowledge
    knowledge_path = ROOT / "04_Knowledge"
    runtime.knowledge_base["files"] = {}
    if knowledge_path.exists():
        for file in knowledge_path.rglob("*.md"):
            rel_path = file.relative_to(ROOT)
            runtime.knowledge_base["files"][str(rel_path)] = file.read_text(encoding="utf-8")

    # 09_Archive
    archive_path = ROOT / "09_Archive"
    runtime.archive["files"] = {}
    if archive_path.exists():
        for file in archive_path.rglob("*.md"):
            rel_path = file.relative_to(ROOT)
            runtime.archive["files"][str(rel_path)] = file.read_text(encoding="utf-8")

    print("Cold cache loaded (reference context).")

    return runtime


def load_company(runtime):
    """
    Main entry point - loads hot cache (static context).
    Only runs once per session.
    """
    return load_hot_cache(runtime)


def refresh_runtime(runtime, tier="warm"):
    """
    Refresh specified cache tier.
    
    Tiers: hot, warm, cold, all
    """
    if tier in ("hot", "all"):
        runtime.hot_loaded = False
        runtime = load_hot_cache(runtime)

    if tier in ("warm", "all"):
        runtime.force_warm_refresh = True
        runtime = load_warm_cache(runtime, force=True)

    if tier in ("cold", "all"):
        runtime = load_cold_cache(runtime)

    return runtime