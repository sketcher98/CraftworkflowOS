"""
Refresh Policy

Determines whether Hermes should reload files based on tiered caching.

Tiered Cache System:
- Hot (Static): Company, Identity, Principles, State, Boot Sequence, Mission Loop,
  Refresh Policy, Cache Rules, Session Manager, Runtime Context, Organization
  → Loaded ONCE per session

- Warm (Dynamic): Inbox, Active Projects, Current Client, Recent Logs
  → Refreshed ON DEMAND or when files change

- Cold (Reference): Archive, Knowledge Base
  → Loaded ON REQUEST only
"""

from pathlib import Path
from runtime.loader import load_warm_cache, load_cold_cache, load_hot_cache

ROOT = Path(__file__).parent.parent


def get_file_mtimes(paths):
    """Get modification times for a list of paths."""
    mtimes = {}
    for path in paths:
        full_path = ROOT / path
        if full_path.exists():
            mtimes[str(path)] = full_path.stat().st_mtime
    return mtimes


def check_warm_cache_changes(runtime):
    """Check if warm cache files have changed since last load."""
    # Check inbox
    inbox_path = ROOT / "08_Command Center" / "Inbox" / "New"
    if inbox_path.exists():
        for file in inbox_path.glob("*.md"):
            if file.name not in runtime.inbox_tasks.get("files", {}):
                return True

    # Check projects
    projects_path = ROOT / "07_Projects"
    if projects_path.exists():
        for file in projects_path.rglob("*.md"):
            rel = str(file.relative_to(ROOT))
            if rel not in runtime.projects.get("files", {}):
                return True

    return False


def refresh_runtime(runtime, tier="warm"):
    """
    Refresh specified cache tier.
    
    Args:
        runtime: OperatingContext
        tier: "hot", "warm", "cold", or "all"
    """
    if tier in ("hot", "all"):
        runtime.hot_loaded = False
        runtime = load_hot_cache(runtime)

    if tier in ("warm", "all"):
        # Check if warm cache needs refresh
        if not runtime.warm_loaded or runtime.force_warm_refresh or check_warm_cache_changes(runtime):
            runtime = load_warm_cache(runtime, force=True)
        else:
            print("Warm cache up to date.")

    if tier in ("cold", "all"):
        runtime = load_cold_cache(runtime)

    runtime.last_refresh = __import__("datetime").datetime.now().isoformat()
    return runtime