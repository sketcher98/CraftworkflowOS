"""
Checkpoint Manager

Responsible for saving and restoring the active
CraftworkflowOS runtime session.
Integrates with MemoryManager for working memory persistence.
"""

import json
from pathlib import Path
from datetime import datetime

from runtime.memory.manager import MemoryManager


CACHE_FILE = Path(__file__).parent / "cache" / "runtime_cache.json"


def save_checkpoint(runtime_state: dict, working_memory=None):
    """
    Save runtime state to disk.
    
    If working_memory is provided (MemoryManager.WorkingMemory),
    it will be included in the checkpoint.
    """
    if working_memory:
        runtime_state["working_memory"] = working_memory.__dict__
    
    runtime_state["saved_at"] = datetime.now().isoformat()
    
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(runtime_state, f, indent=4)


def load_checkpoint():
    """
    Load runtime state.
    
    Returns None if no checkpoint exists.
    """
    if not CACHE_FILE.exists():
        return None
    
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def is_checkpoint_valid(checkpoint: dict, memory_manager: MemoryManager = None) -> bool:
    """
    Verify checkpoint matches current critical docs.
    """
    if memory_manager:
        return memory_manager.is_checkpoint_valid(checkpoint)
    
    # Fallback validation
    critical_files = [
        "01_CEO/company.md",
        "02_COO/identity.md", 
        "01_CEO/decision_principles.md",
        "02_COO/company_state.md"
    ]
    
    checkpoint_time = checkpoint.get("last_refresh", "")
    if not checkpoint_time:
        return False
    
    checkpoint_dt = datetime.fromisoformat(checkpoint_time)
    
    for rel_path in critical_files:
        full_path = Path(__file__).parent.parent / rel_path
        if full_path.exists():
            mtime = datetime.fromtimestamp(full_path.stat().st_mtime)
            if mtime > checkpoint_dt:
                return False
    return True