"""
Checkpoint Manager

Responsible for saving and restoring the active
CraftworkflowOS runtime session.
"""

import json
from pathlib import Path
from datetime import datetime


CACHE_FILE = Path(__file__).parent / "cache" / "runtime_cache.json"


def save_checkpoint(data: dict):
    """
    Save runtime state to disk.
    """

    data["saved_at"] = datetime.now().isoformat()

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_checkpoint():
    """
    Load runtime state.

    Returns None if no checkpoint exists.
    """

    if not CACHE_FILE.exists():
        return None

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)