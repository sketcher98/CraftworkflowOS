"""In-memory index for the canonical local Notion workspace discovery snapshot."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional


DEFAULT_CACHE_NAME = "notion_workspace_discovery.json"
CACHE_MAX_AGE_SECONDS = 24 * 60 * 60


class NotionWorkspaceIndex:
    """Load and index the local Notion discovery snapshot once per session."""

    def __init__(
        self,
        workspace_root: Optional[str | Path] = None,
        cache_path: Optional[str | Path] = None,
        max_age_seconds: int = CACHE_MAX_AGE_SECONDS,
    ) -> None:
        root = Path(workspace_root) if workspace_root else Path(__file__).parent.parent
        self.cache_path = Path(cache_path) if cache_path else root / DEFAULT_CACHE_NAME
        self.max_age_seconds = max_age_seconds
        self.loaded = False
        self.data: Dict[str, Any] = {}
        self.pages: List[Dict[str, Any]] = []
        self.databases: List[Dict[str, Any]] = []
        self.pages_by_id: Dict[str, Dict[str, Any]] = {}
        self.databases_by_id: Dict[str, Dict[str, Any]] = {}
        self.by_title: Dict[str, List[Dict[str, Any]]] = {}
        self.by_url: Dict[str, Dict[str, Any]] = {}
        self.by_parent_database: Dict[str, List[Dict[str, Any]]] = {}
        self.stale = False
        self.load()

    def load(self) -> "NotionWorkspaceIndex":
        """Load the snapshot and build all indexes; safe to call repeatedly."""
        if self.loaded:
            return self
        if not self.cache_path.exists():
            self.loaded = True
            self.stale = True
            return self
        try:
            self.data = json.loads(self.cache_path.read_text(encoding="utf-8"))
            self.pages = list(self.data.get("pages", []))
            self.databases = list(self.data.get("databases", []))
            self.pages_by_id = {item.get("id"): item for item in self.pages if item.get("id")}
            self.databases_by_id = {item.get("id"): item for item in self.databases if item.get("id")}
            self._build_indexes()
            self.stale = (time.time() - self.cache_path.stat().st_mtime) > self.max_age_seconds
        except (OSError, ValueError, TypeError):
            self.data = {}
            self.pages = []
            self.databases = []
            self.stale = True
        self.loaded = True
        return self

    def _build_indexes(self) -> None:
        self.by_title = {}
        self.by_url = {}
        self.by_parent_database = {}
        for item in (*self.databases, *self.pages):
            title = str(item.get("title", "")).strip().casefold()
            if title:
                self.by_title.setdefault(title, []).append(item)
            if item.get("url"):
                self.by_url[item["url"]] = item
            parent_id = item.get("parent_database_id") or item.get("parent_db_id")
            parent = item.get("parent")
            if not parent_id and isinstance(parent, dict):
                parent_id = parent.get("database_id") or parent.get("id")
            if parent_id:
                self.by_parent_database.setdefault(parent_id, []).append(item)

    def refresh(self, loader: Optional[Callable[[], Dict[str, Any]]] = None) -> "NotionWorkspaceIndex":
        """Explicitly replace the snapshot, optionally using a discovery loader."""
        if loader is None:
            self.loaded = False
            self.data = {}
            return self.load()
        snapshot = loader()
        self.cache_path.write_text(json.dumps(snapshot, indent=2, default=str), encoding="utf-8")
        self.loaded = False
        self.data = {}
        return self.load()

    def needs_refresh(self) -> bool:
        return self.stale or not self.cache_path.exists()

    def find_database(self, database_id: str) -> Optional[Dict[str, Any]]:
        return self.databases_by_id.get(database_id)

    def find_page(self, page_id: str) -> Optional[Dict[str, Any]]:
        return self.pages_by_id.get(page_id)

    def find_by_title(self, title: str, kind: Optional[str] = None) -> List[Dict[str, Any]]:
        matches = list(self.by_title.get(str(title).strip().casefold(), []))
        if kind == "page":
            return [item for item in matches if item in self.pages]
        if kind == "database":
            return [item for item in matches if item in self.databases]
        return matches

    def find_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        return self.by_url.get(url)

    def find_pages_by_database(self, database_id: str) -> List[Dict[str, Any]]:
        return list(self.by_parent_database.get(database_id, []))

    def find_by_id(self, object_id: str) -> Optional[Dict[str, Any]]:
        return self.find_page(object_id) or self.find_database(object_id)

    def all_pages(self) -> List[Dict[str, Any]]:
        return list(self.pages)

    def all_databases(self) -> List[Dict[str, Any]]:
        return list(self.databases)


_default_index: Optional[NotionWorkspaceIndex] = None


def get_notion_workspace_index(workspace_root: Optional[str | Path] = None) -> NotionWorkspaceIndex:
    """Return the process-wide index, loading the discovery file only once."""
    global _default_index
    if _default_index is None:
        _default_index = NotionWorkspaceIndex(workspace_root=workspace_root)
    return _default_index


def request_notion_rediscovery(
    loader: Optional[Callable[[], Dict[str, Any]]] = None,
    workspace_root: Optional[str | Path] = None,
) -> NotionWorkspaceIndex:
    """Explicitly request a rediscovery/reload for the current process."""
    index = get_notion_workspace_index(workspace_root)
    if loader is None:
        script = index.cache_path.parent / "scripts" / "discover_notion_workspace.py"
        def discover() -> Dict[str, Any]:
            env = os.environ.copy()
            subprocess.run([sys.executable, str(script)], cwd=str(index.cache_path.parent), env=env, check=True)
            return json.loads(index.cache_path.read_text(encoding="utf-8"))
        loader = discover
    return index.refresh(loader)


def rediscover_if_needed(workspace_root: Optional[str | Path] = None) -> NotionWorkspaceIndex:
    """Refresh only when the cache is missing or older than 24 hours."""
    index = get_notion_workspace_index(workspace_root)
    if index.needs_refresh():
        return request_notion_rediscovery(workspace_root=workspace_root)
    return index


# Backward-friendly alias for callers that prefer a short name.
get_index = get_notion_workspace_index

__all__ = ["NotionWorkspaceIndex", "get_notion_workspace_index", "request_notion_rediscovery", "rediscover_if_needed", "get_index"]
