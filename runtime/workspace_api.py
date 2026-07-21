"""
Workspace API

REST/CLI interface for external tools to interact with CraftworkflowOS.
Provides programmatic access to:
- Operating Context (read company knowledge)
- Task Management (CRUD operations)
- Artifact Store (store/retrieve work products)
- Commercial Pipeline (run briefings, get leads)
- Project Management (projects, epics, tasks)
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import json
import time
from datetime import datetime

# Runtime imports
from runtime.context import OperatingContext
from runtime.loader import load_company, refresh_runtime
from runtime.executive import execute
from runtime.commercial_briefing import run_commercial_briefing
from runtime.task import Task
from runtime.task_manager import TaskManager
from runtime.checkpoint import load_checkpoint, save_checkpoint
from runtime.notion_workspace_index import get_notion_workspace_index


@dataclass
class APIResponse:
    """Standard API response format."""
    success: bool
    data: Any = None
    error: str = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class WorkspaceAPI:
    """
    Main Workspace API class.
    
    Provides external interface for tools/agents to interact with CraftworkflowOS.
    """
    
    def __init__(self, workspace_root: str = None):
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent
        self.workspace_root = Path(workspace_root)
        self.runtime = None
        self.task_manager = TaskManager()
        self.notion_workspace_index = get_notion_workspace_index(self.workspace_root)
        self._initialized = False
    
    def initialize(self, force_refresh: bool = False) -> APIResponse:
        """Initialize the runtime context."""
        try:
            self.runtime = OperatingContext()
            self.runtime = load_company(self.runtime)
            self.notion_workspace_index = self.runtime.notion_workspace_index
            
            # Always load warm cache for immediate usability
            self.runtime = refresh_runtime(self.runtime, tier="warm")
            
            if force_refresh:
                self.runtime = refresh_runtime(self.runtime, tier="warm")
            
            self._initialized = True
            return APIResponse(
                success=True,
                data={"status": "initialized", "hot_loaded": self.runtime.hot_loaded, "warm_loaded": self.runtime.warm_loaded}
            )
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    def _ensure_initialized(self):
        """Lazy initialization."""
        if not self._initialized:
            self.initialize()
    
    def _find_project_path(self, project_name: str):
        """Find the directory path for a project by name."""
        if not self.runtime.warm_loaded:
            self.runtime = refresh_runtime(self.runtime, tier="warm")
        
        for path in self.runtime.projects.get("files", {}):
            if project_name in path:
                # path is like "07_Projects/TestProject/README.md"
                # We need the directory: "07_Projects/TestProject"
                project_dir = self.workspace_root / Path(path).parent
                return project_dir
        return None
    
    # =========================================================================
    # CONTEXT QUERIES
    # =========================================================================
    
    def get_company(self) -> APIResponse:
        """Get company mission, vision, services, ICP."""
        self._ensure_initialized()
        return APIResponse(
            success=True,
            data={
                "company": self.runtime.company.get("content", ""),
                "identity": self.runtime.identity.get("content", ""),
                "principles": self.runtime.principles.get("content", ""),
                "company_state": self.runtime.company_state.get("content", ""),
            }
        )
    
    def get_organization(self) -> APIResponse:
        """Get full organization structure."""
        self._ensure_initialized()
        return APIResponse(
            success=True,
            data=self.runtime.organization
        )
    
    def get_inbox(self) -> APIResponse:
        """Get current inbox tasks."""
        self._ensure_initialized()
        if not self.runtime.warm_loaded:
            self.runtime = refresh_runtime(self.runtime, tier="warm")
        return APIResponse(
            success=True,
            data=self.runtime.inbox_tasks
        )
    
    def get_projects(self) -> APIResponse:
        """Get active projects."""
        self._ensure_initialized()
        if not self.runtime.warm_loaded:
            self.runtime = refresh_runtime(self.runtime, tier="warm")
        return APIResponse(
            success=True,
            data=self.runtime.projects
        )
    
    def get_current_client(self) -> APIResponse:
        """Get current client info."""
        self._ensure_initialized()
        if not self.runtime.warm_loaded:
            self.runtime = refresh_runtime(self.runtime, tier="warm")
        return APIResponse(
            success=True,
            data=self.runtime.current_client_docs
        )
    
    def get_context_status(self) -> APIResponse:
        """Get current runtime context status (cache tiers, loaded state)."""
        self._ensure_initialized()
        from runtime.refresh import get_refresh_status
        return APIResponse(
            success=True,
            data={
                "status": get_refresh_status(self.runtime),
                "hot_loaded": self.runtime.hot_loaded,
                "warm_loaded": self.runtime.warm_loaded,
                "last_refresh": getattr(self.runtime, 'last_refresh', 'Never'),
            }
        )
    
    # =========================================================================
    # TASK MANAGEMENT
    # =========================================================================
    
    def create_task(self, objective: str, department: str = "", 
                    priority: str = "Normal", owner: str = "") -> APIResponse:
        """Create a new task."""
        self._ensure_initialized()
        try:
            task = Task(
                objective=objective,
                department=department,
                owner=owner,
                priority=priority
            )
            self.task_manager.add(task)
            return APIResponse(success=True, data=task.to_dict())
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    def get_tasks(self, status: str = None, department: str = None) -> APIResponse:
        """Get all tasks, optionally filtered."""
        self._ensure_initialized()
        tasks = self.task_manager.get_tasks(status=status, department=department)
        return APIResponse(success=True, data=[t.to_dict() for t in tasks])
    
    def complete_task(self, task_id: str) -> APIResponse:
        """Mark a task as complete."""
        self._ensure_initialized()
        tasks = self.task_manager.get_tasks()
        task = next((t for t in tasks if t.id == task_id), None)
        if task:
            task.complete()
            return APIResponse(success=True, data=task.to_dict())
        return APIResponse(success=False, error=f"Task {task_id} not found")
    
    # =========================================================================
    # EXECUTION
    # =========================================================================
    
    def execute(self, task: str) -> APIResponse:
        """Execute a task through the executive loop."""
        self._ensure_initialized()
        try:
            result = execute(task, self.runtime)
            return APIResponse(success=True, data={"result": result})
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    def ask_priority(self) -> APIResponse:
        """Ask 'what should I work on today?'"""
        return self.execute("what should i work on today?")
    
    def run_commercial_briefing(self) -> APIResponse:
        """Run the full commercial pipeline and return formatted briefing."""
        self._ensure_initialized()
        if not self.runtime.warm_loaded:
            self.runtime = refresh_runtime(self.runtime, tier="warm")
        
        try:
            briefing, qualified, messages = run_commercial_briefing(self.runtime)
            return APIResponse(success=True, data={
                "briefing": briefing,
                "qualified_leads": qualified,
                "outreach_messages": messages
            })
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    # =========================================================================
    # ARTIFACTS & CHECKPOINTS
    # =========================================================================
    
    def save_checkpoint(self) -> APIResponse:
        """Save current runtime state."""
        self._ensure_initialized()
        try:
            save_checkpoint(self.runtime.to_dict())
            return APIResponse(success=True, data={"status": "checkpoint saved"})
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    def load_checkpoint(self) -> APIResponse:
        """Load last checkpoint."""
        try:
            data = load_checkpoint()
            if data:
                self.runtime = OperatingContext.from_dict(data)
                self._initialized = True
                return APIResponse(success=True, data={"status": "checkpoint loaded"})
            return APIResponse(success=False, error="No checkpoint found")
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    def get_artifacts(self) -> APIResponse:
        """Get all artifacts from current session."""
        self._ensure_initialized()
        # This would be populated during execution
        return APIResponse(success=True, data={"artifacts": []})
    
    # =========================================================================
    # PROJECT MANAGEMENT
    # =========================================================================
    
    def create_project(self, name: str, description: str = "", 
                       objective: str = "") -> APIResponse:
        """Create a new project."""
        self._ensure_initialized()
        try:
            # Store project in 07_Projects folder
            project_path = self.workspace_root / "07_Projects" / name
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Create README.md
            readme = project_path / "README.md"
            readme_content = f"""# {name}

## Objective
{objective or "To be defined"}

## Description
{description or "No description provided."}

## Status
Active

## Created
{datetime.now().isoformat()}
"""
            readme.write_text(readme_content, encoding="utf-8")
            
            # Refresh warm cache to pick up new project
            self.runtime = refresh_runtime(self.runtime, tier="warm")
            
            return APIResponse(success=True, data={
                "name": name,
                "path": str(project_path),
                "readme": readme_content
            })
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    def get_all_projects(self) -> APIResponse:
        """Get all projects (including archived)."""
        self._ensure_initialized()
        if not self.runtime.warm_loaded:
            self.runtime = refresh_runtime(self.runtime, tier="warm")
        
        # Also load cold cache for archive
        from runtime.loader import load_cold_cache
        self.runtime = load_cold_cache(self.runtime)
        
        all_projects = {}
        all_projects.update(self.runtime.projects.get("files", {}))
        all_projects.update(self.runtime.archive.get("files", {}))
        
        return APIResponse(success=True, data=all_projects)
    
    def get_project(self, project_name: str) -> APIResponse:
        """Get specific project details."""
        self._ensure_initialized()
        if not self.runtime.warm_loaded:
            self.runtime = refresh_runtime(self.runtime, tier="warm")
        
        # Search in active projects
        for path, content in self.runtime.projects.get("files", {}).items():
            if project_name in path:
                return APIResponse(success=True, data={"path": path, "content": content})
        
        # Search in archive
        from runtime.loader import load_cold_cache
        self.runtime = load_cold_cache(self.runtime)
        for path, content in self.runtime.archive.get("files", {}).items():
            if project_name in path:
                return APIResponse(success=True, data={"path": path, "content": content})
        
        return APIResponse(success=False, error=f"Project '{project_name}' not found")
    
    def update_project(self, project_name: str, updates: dict) -> APIResponse:
        """Update project (readme, status, etc.)."""
        self._ensure_initialized()
        try:
            # Ensure re is available for regex operations
            import re
            
            # Find project
            project_path = self._find_project_path(project_name)
            
            if not project_path or not project_path.exists():
                return APIResponse(success=False, error=f"Project '{project_name}' not found")
            
            readme_path = project_path / "README.md"
            if not readme_path.exists():
                return APIResponse(success=False, error="Project README not found")
            
            # Read current content
            content = readme_path.read_text(encoding="utf-8")
            
            # Apply updates
            if "description" in updates:
                # Simple replacement - in production use proper markdown parsing
                content = re.sub(
                    r"## Description\n.*?(?=\n## |\Z)",
                    f"## Description\n{updates['description']}",
                    content,
                    flags=re.S
                )
            if "status" in updates:
                content = re.sub(
                    r"## Status\n.*?(?=\n## |\Z)",
                    f"## Status\n{updates['status']}",
                    content,
                    flags=re.S
                )
            
            readme_path.write_text(content, encoding="utf-8")
            
            # Refresh
            self.runtime = refresh_runtime(self.runtime, tier="warm")
            
            return APIResponse(success=True, data={"status": "updated", "project": project_name})
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    def archive_project(self, project_name: str) -> APIResponse:
        """Archive a project (move to 09_Archive)."""
        self._ensure_initialized()
        try:
            project_path = self._find_project_path(project_name)
            
            if not project_path or not project_path.exists():
                return APIResponse(success=False, error=f"Project '{project_name}' not found")
            
            # Move to archive
            archive_path = self.workspace_root / "09_Archive" / project_path.name
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            
            import shutil
            shutil.move(str(project_path), str(archive_path))
            
            # Refresh both warm and cold
            self.runtime = refresh_runtime(self.runtime, tier="warm")
            from runtime.loader import load_cold_cache
            self.runtime = load_cold_cache(self.runtime)
            
            return APIResponse(success=True, data={"status": "archived", "project": project_name})
        except Exception as e:
            return APIResponse(success=False, error=str(e))

    # =========================================================================
    # NOTION WORKSPACE INDEX LOOKUPS
    # =========================================================================
    #
    # These methods consult the local NotionWorkspaceIndex first (fast, in-memory).
    # Only if an item is not found locally would external Notion search be needed.
    # The index is loaded once at boot from notion_workspace_discovery.json.
    # Rediscovery only happens if cache is missing, >24h old, or explicitly requested.

    def find_notion_database(self, database_id: str) -> APIResponse:
        """Find a Notion database by ID using the local index (fast, in-memory)."""
        self._ensure_initialized()
        db = self.notion_workspace_index.find_database(database_id)
        if db:
            return APIResponse(success=True, data=db, error=None)
        return APIResponse(success=False, error=f"Database '{database_id}' not found in local index")

    def find_notion_page(self, page_id: str) -> APIResponse:
        """Find a Notion page by ID using the local index (fast, in-memory)."""
        self._ensure_initialized()
        page = self.notion_workspace_index.find_page(page_id)
        if page:
            return APIResponse(success=True, data=page, error=None)
        return APIResponse(success=False, error=f"Page '{page_id}' not found in local index")

    def find_notion_by_title(self, title: str, kind: str = None) -> APIResponse:
        """Find Notion pages/databases by title (case-insensitive) using local index."""
        self._ensure_initialized()
        matches = self.notion_workspace_index.find_by_title(title, kind=kind)
        return APIResponse(success=True, data=matches)

    def find_notion_by_url(self, url: str) -> APIResponse:
        """Find a Notion page/database by URL using local index."""
        self._ensure_initialized()
        item = self.notion_workspace_index.find_by_url(url)
        if item:
            return APIResponse(success=True, data=item)
        return APIResponse(success=False, error=f"URL '{url}' not found in local index")

    def find_notion_pages_by_database(self, database_id: str) -> APIResponse:
        """Find all Notion pages belonging to a database using local index."""
        self._ensure_initialized()
        pages = self.notion_workspace_index.find_pages_by_database(database_id)
        return APIResponse(success=True, data=pages)

    def find_notion_by_id(self, object_id: str) -> APIResponse:
        """Find any Notion object (page or database) by ID using local index."""
        self._ensure_initialized()
        item = self.notion_workspace_index.find_by_id(object_id)
        if item:
            return APIResponse(success=True, data=item)
        return APIResponse(success=False, error=f"Object '{object_id}' not found in local index")

    def get_all_notion_databases(self) -> APIResponse:
        """Get all Notion databases from local index."""
        self._ensure_initialized()
        databases = self.notion_workspace_index.all_databases()
        return APIResponse(success=True, data=databases)

    def get_all_notion_pages(self) -> APIResponse:
        """Get all Notion pages from local index."""
        self._ensure_initialized()
        pages = self.notion_workspace_index.all_pages()
        return APIResponse(success=True, data=pages)

    def get_notion_index_status(self) -> APIResponse:
        """Get status of the local Notion workspace index."""
        self._ensure_initialized()
        index = self.notion_workspace_index
        cache_path = index.cache_path
        return APIResponse(success=True, data={
            "loaded": index.loaded,
            "stale": index.needs_refresh(),
            "cache_exists": cache_path.exists(),
            "cache_path": str(cache_path),
            "cache_age_seconds": time.time() - cache_path.stat().st_mtime if cache_path.exists() else None,
            "databases_count": len(index.databases),
            "pages_count": len(index.pages),
            "indexed_at": datetime.fromtimestamp(cache_path.stat().st_mtime).isoformat() if cache_path.exists() else None,
        })

    def request_notion_rediscovery(self) -> APIResponse:
        """Explicitly request a full Notion workspace rediscovery (slow - scans all 7,439+ pages)."""
        self._ensure_initialized()
        from runtime.notion_workspace_index import request_notion_rediscovery
        index = request_notion_rediscovery(workspace_root=self.workspace_root)
        self.notion_workspace_index = index
        self.runtime.notion_workspace_index = index
        return APIResponse(success=True, data={
            "status": "rediscovery completed",
            "databases": len(index.databases),
            "pages": len(index.pages)
        })


# Global API instance
_api_instance = None

def get_api() -> WorkspaceAPI:
    """Get or create the global API instance."""
    global _api_instance
    if _api_instance is None:
        _api_instance = WorkspaceAPI()
    return _api_instance