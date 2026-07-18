"""
Refresh Policy Implementation

Implements the documented refresh policy with:
- File change detection via mtimes
- Tiered cache invalidation (Hot/Warm/Cold)
- Refresh triggers: new session, explicit request, file changes, missing info, verification needed
- Priority order: Documentation > Company State > History > Memory > General Knowledge
"""

from pathlib import Path
from datetime import datetime
import json
from runtime.loader import load_hot_cache, load_warm_cache, load_cold_cache

ROOT = Path(__file__).parent.parent

# State file for tracking last refresh times
REFRESH_STATE_FILE = ROOT / "runtime" / "cache" / "refresh_state.json"


def load_refresh_state():
    """Load refresh state from disk."""
    if REFRESH_STATE_FILE.exists():
        with open(REFRESH_STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_refresh_state(state):
    """Save refresh state to disk."""
    REFRESH_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REFRESH_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_file_mtimes(paths):
    """Get modification times for a list of paths relative to ROOT."""
    mtimes = {}
    for path in paths:
        full_path = ROOT / path
        if full_path.exists():
            if full_path.is_file():
                mtimes[str(path)] = full_path.stat().st_mtime
            elif full_path.is_dir():
                for file in full_path.rglob("*.md"):
                    rel = str(file.relative_to(ROOT))
                    mtimes[rel] = file.stat().st_mtime
    return mtimes


# =============================================================================
# CACHE TIER DEFINITIONS
# =============================================================================

HOT_CACHE_PATHS = [
    "01_CEO/company.md",
    "01_CEO/decision_principles.md",
    "02_COO/identity.md",
    "02_COO/company_state.md",
    "00_Systems/boot_sequence.md",
    "00_Systems/mission_loop.md",
    "00_Systems/Session/refresh_policy.md",
    "00_Systems/Session/cache_rules.md",
    "00_Systems/Session/session_manager.md",
    "00_Systems/Session/runtime_context.md",
    "03_Departments",  # Entire org structure
]

WARM_CACHE_PATHS = [
    "08_Command Center/Inbox/New",
    "07_Projects",
    "06_Clients",
    "05_Operations",
]

COLD_CACHE_PATHS = [
    "09_Archive",
    "04_Knowledge",
]


# =============================================================================
# REFRESH TRIGGERS
# =============================================================================

class RefreshTrigger:
    """Enumeration of refresh triggers per documented policy."""
    NEW_SESSION = "new_session"
    EXPLICIT_REQUEST = "explicit_request"
    FILE_CHANGED = "file_changed"
    INFO_MISSING = "info_missing"
    VERIFICATION_NEEDED = "verification_needed"


def should_refresh(runtime, trigger, tier="warm", specific_paths=None):
    """
    Determine if a refresh is needed based on trigger and cache tier.
    
    Per documented policy:
    - New session: refresh all
    - Explicit request: refresh requested tier
    - File changed: refresh affected tier
    - Info missing: load cold cache for specific info
    - Verification needed: refresh warm cache
    """
    
    state = load_refresh_state()
    tier_key = f"{tier}_mtimes"
    
    if trigger == RefreshTrigger.NEW_SESSION:
        return True
    
    if trigger == RefreshTrigger.EXPLICIT_REQUEST:
        return True
    
    if trigger == RefreshTrigger.FILE_CHANGED:
        # Check if any tracked files have changed
        current_mtimes = get_tracked_mtimes(tier, specific_paths)
        last_mtimes = state.get(tier_key, {})
        
        for path, mtime in current_mtimes.items():
            if path not in last_mtimes or last_mtimes[path] < mtime:
                return True
        return False
    
    if trigger == RefreshTrigger.INFO_MISSING:
        # Check if requested info is in cold cache
        if specific_paths:
            for path in specific_paths:
                if path not in getattr(runtime, 'cold_loaded_paths', set()):
                    return True
        return False
    
    if trigger == RefreshTrigger.VERIFICATION_NEEDED:
        # For verification, check warm cache freshness
        if not runtime.warm_loaded:
            return True
        # Also check if warm cache files changed
        return should_refresh(runtime, RefreshTrigger.FILE_CHANGED, "warm")
    
    return False


def get_tracked_mtimes(tier, specific_paths=None):
    """Get mtimes for all tracked paths in a tier."""
    if tier == "hot":
        paths = specific_paths or HOT_CACHE_PATHS
    elif tier == "warm":
        paths = specific_paths or WARM_CACHE_PATHS
    elif tier == "cold":
        paths = specific_paths or COLD_CACHE_PATHS
    else:
        paths = []
    
    return get_file_mtimes(paths)


# =============================================================================
# REFRESH EXECUTION
# =============================================================================

def refresh_runtime(runtime, tier="warm", trigger=RefreshTrigger.EXPLICIT_REQUEST, specific_paths=None):
    """
    Execute refresh for specified tier.
    
    Args:
        runtime: OperatingContext instance
        tier: "hot", "warm", "cold", or "all"
        trigger: RefreshTrigger enum value
        specific_paths: Optional specific paths to check/refresh
    
    Returns:
        Updated runtime
    """
    
    state = load_refresh_state()
    
    if tier in ("hot", "all"):
        if should_refresh(runtime, trigger, "hot", specific_paths):
            print("🔄 Refreshing HOT cache (static context)...")
            runtime = load_hot_cache(runtime)
            state["hot_mtimes"] = get_tracked_mtimes("hot")
        else:
            print("✅ HOT cache up to date.")
    
    if tier in ("warm", "all"):
        if should_refresh(runtime, trigger, "warm", specific_paths):
            print("🔄 Refreshing WARM cache (dynamic context)...")
            runtime = load_warm_cache(runtime, force=True)
            state["warm_mtimes"] = get_tracked_mtimes("warm")
        else:
            print("✅ WARM cache up to date.")
    
    if tier in ("cold", "all"):
        if should_refresh(runtime, trigger, "cold", specific_paths):
            print("🔄 Refreshing COLD cache (reference context)...")
            runtime = load_cold_cache(runtime)
            state["cold_mtimes"] = get_tracked_mtimes("cold")
            # Track which cold paths we've loaded
            if not hasattr(runtime, 'cold_loaded_paths'):
                runtime.cold_loaded_paths = set()
            for path in (specific_paths or COLD_CACHE_PATHS):
                runtime.cold_loaded_paths.add(path)
        else:
            print("✅ COLD cache up to date.")
    
    save_refresh_state(state)
    runtime.last_refresh = datetime.now().isoformat()
    return runtime


def refresh_for_task(runtime, required_info=None):
    """
    Smart refresh based on task requirements.
    
    Args:
        runtime: OperatingContext
        required_info: List of info categories needed (e.g., ["inbox", "projects", "client"])
    
    Returns:
        Updated runtime with necessary context loaded
    """
    
    # Always ensure hot cache is loaded
    if not runtime.hot_loaded:
        runtime = refresh_runtime(runtime, tier="hot", trigger=RefreshTrigger.NEW_SESSION)
    
    # Determine what warm cache components are needed
    needs_warm = False
    warm_paths = []
    
    if required_info:
        for info in required_info:
            if info in ("inbox", "tasks"):
                warm_paths.append("08_Command Center/Inbox/New")
                needs_warm = True
            elif info in ("projects", "active_projects"):
                warm_paths.append("07_Projects")
                needs_warm = True
            elif info in ("client", "clients", "current_client"):
                warm_paths.append("06_Clients")
                needs_warm = True
            elif info in ("logs", "operations", "recent_logs"):
                warm_paths.append("05_Operations")
                needs_warm = True
    
    # Default: refresh all warm cache if nothing specific requested
    if not needs_warm:
        warm_paths = None  # Will use all WARM_CACHE_PATHS
        needs_warm = True
    
    if needs_warm:
        runtime = refresh_runtime(
            runtime, 
            tier="warm", 
            trigger=RefreshTrigger.INFO_MISSING if required_info else RefreshTrigger.VERIFICATION_NEEDED,
            specific_paths=warm_paths
        )
    
    # Check if cold cache needed
    if required_info and any(info in ("archive", "knowledge", "sops", "history") for info in required_info):
        runtime = refresh_runtime(
            runtime,
            tier="cold",
            trigger=RefreshTrigger.INFO_MISSING,
            specific_paths=COLD_CACHE_PATHS
        )
    
    return runtime


def get_refresh_status(runtime):
    """Get human-readable status of all cache tiers."""
    status = []
    status.append("CACHE STATUS:")
    status.append(f"  HOT (static):     {'✅ Loaded' if runtime.hot_loaded else '❌ Not loaded'}")
    status.append(f"  WARM (dynamic):   {'✅ Loaded' if runtime.warm_loaded else '❌ Not loaded'}")
    status.append(f"  COLD (reference): {'✅ Loaded' if hasattr(runtime, 'cold_loaded') and runtime.cold_loaded else '❌ Not loaded'}")
    status.append(f"  Last refresh: {getattr(runtime, 'last_refresh', 'Never')}")
    return "\n".join(status)