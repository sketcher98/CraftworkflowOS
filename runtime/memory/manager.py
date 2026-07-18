"""
Memory Manager

Central memory management for Hermes.
Provides unified interface to all memory layers.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import uuid

from runtime.memory.schemas import (
    IdentityMemory, WorkingMemory, ClientProfile, Episode,
    Skill, Reflection, Decision, Preference, Pattern
)


class MemoryManager:
    """
    Central memory management for Hermes.
    
    Provides unified interface to all memory layers:
    - Identity: Who Hermes is (role, mission, principles, authority)
    - Working: Current session context (objectives, projects, client)
    - Long-term: Accumulated knowledge (clients, patterns, relationships)
    - Episodic: Experience history (what happened when)
    - Skills: Reusable procedures (playbooks, templates)
    - Reflections: Learning record (what worked, what didn't)
    - Decisions: Audit trail (why we chose X over Y)
    - Preferences: Learned defaults (communication, scheduling, etc.)
    """
    
    def __init__(self, workspace_root: str = None):
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent.parent
        else:
            workspace_root = Path(workspace_root)
            
        self.workspace_root = workspace_root
        self.memory_root = workspace_root / "memory"
        
        # Layer paths
        self.identity_path = self.memory_root / "identity"
        self.working_path = self.memory_root / "working"
        self.longterm_path = self.memory_root / "longterm"
        self.episodic_path = self.memory_root / "episodic"
        self.skills_path = self.memory_root / "skills"
        self.reflections_path = self.memory_root / "reflections"
        self.decisions_path = self.memory_root / "decisions"
        self.preferences_path = self.memory_root / "preferences"
        self.cache_path = workspace_root / "runtime" / "cache"
        
        # Ensure directories exist
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create all memory directories if they don't exist."""
        dirs = [
            self.identity_path,
            self.working_path,
            self.longterm_path / "clients",
            self.longterm_path / "patterns",
            self.longterm_path / "relationships",
            self.longterm_path / "market_intelligence",
            self.episodic_path,
            self.skills_path / "outreach",
            self.skills_path / "discovery",
            self.skills_path / "proposal",
            self.skills_path / "onboarding",
            self.skills_path / "internal",
            self.reflections_path / "daily",
            self.reflections_path / "weekly",
            self.reflections_path / "project",
            self.reflections_path / "strategic",
            self.decisions_path,
            self.preferences_path,
            self.cache_path,
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
    
    # ================================================================
    # IDENTITY LAYER
    # ================================================================
    
    def load_identity(self) -> IdentityMemory:
        """Load all identity documents."""
        identity = IdentityMemory()
        
        # Load from files
        for doc_file in self.identity_path.glob("*.md"):
            key = doc_file.stem
            content = doc_file.read_text(encoding="utf-8")
            if hasattr(identity, key):
                setattr(identity, key, content)
        
        return identity
    
    def save_identity(self, identity: IdentityMemory):
        """Save identity documents."""
        identity.updated = datetime.now().isoformat()
        
        # Only save markdown files, not the structured fields
        for doc_name in ["role", "mission", "principles", "authority"]:
            content = getattr(identity, doc_name, "")
            if content:
                path = self.identity_path / f"{doc_name}.md"
                path.write_text(content, encoding="utf-8")
    
    # ================================================================
    # WORKING MEMORY
    # ================================================================
    
    def load_working(self, checkpoint: Dict = None) -> WorkingMemory:
        """Load working memory from checkpoint or files."""
        working = WorkingMemory()
        
        # Try checkpoint first
        if checkpoint and "working_memory" in checkpoint:
            wm_data = checkpoint["working_memory"]
            working.current_objective = wm_data.get("current_objective", "")
            working.active_project = wm_data.get("active_project", "")
            working.active_client = wm_data.get("active_client", "")
            working.session_notes = wm_data.get("session_notes", "")
            working.inbox_snapshot = wm_data.get("inbox_snapshot", {})
            working.priorities = wm_data.get("priorities", [])
            working.blockers = wm_data.get("blockers", [])
            working.active_skills = wm_data.get("active_skills", [])
            working.last_updated = wm_data.get("last_updated", datetime.now().isoformat())
            return working
        
        # Fallback to files
        obj_file = self.working_path / "current_objective.md"
        if obj_file.exists():
            working.current_objective = obj_file.read_text(encoding="utf-8").strip()
        
        proj_file = self.working_path / "active_project.md"
        if proj_file.exists():
            working.active_project = proj_file.read_text(encoding="utf-8").strip()
        
        client_file = self.working_path / "current_client.md"
        if client_file.exists():
            working.active_client = client_file.read_text(encoding="utf-8").strip()
        
        notes_file = self.working_path / "session_notes.md"
        if notes_file.exists():
            working.session_notes = notes_file.read_text(encoding="utf-8").strip()
        
        inbox_file = self.working_path / "inbox_snapshot.json"
        if inbox_file.exists():
            working.inbox_snapshot = json.loads(inbox_file.read_text(encoding="utf-8"))
        
        priorities_file = self.working_path / "priorities.json"
        if priorities_file.exists():
            working.priorities = json.loads(priorities_file.read_text(encoding="utf-8"))
        
        blockers_file = self.working_path / "blockers.json"
        if blockers_file.exists():
            working.blockers = json.loads(blockers_file.read_text(encoding="utf-8"))
        
        skills_file = self.working_path / "active_skills.json"
        if skills_file.exists():
            working.active_skills = json.loads(skills_file.read_text(encoding="utf-8"))
        
        return working
    
    def save_working(self, working: WorkingMemory):
        """Save working memory to files."""
        working.last_updated = datetime.now().isoformat()
        
        (self.working_path / "current_objective.md").write_text(
            working.current_objective, encoding="utf-8"
        )
        (self.working_path / "active_project.md").write_text(
            working.active_project or "", encoding="utf-8"
        )
        (self.working_path / "current_client.md").write_text(
            working.active_client or "", encoding="utf-8"
        )
        (self.working_path / "session_notes.md").write_text(
            working.session_notes, encoding="utf-8"
        )
        (self.working_path / "inbox_snapshot.json").write_text(
            json.dumps(working.inbox_snapshot, indent=2), encoding="utf-8"
        )
        (self.working_path / "priorities.json").write_text(
            json.dumps(working.priorities, indent=2), encoding="utf-8"
        )
        (self.working_path / "blockers.json").write_text(
            json.dumps(working.blockers, indent=2), encoding="utf-8"
        )
        (self.working_path / "active_skills.json").write_text(
            json.dumps(working.active_skills, indent=2), encoding="utf-8"
        )
    
    # ================================================================
    # LONG-TERM MEMORY
    # ================================================================
    
    def get_client(self, name: str) -> Optional[ClientProfile]:
        """Load client profile."""
        path = self.longterm_path / "clients" / f"{name}.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return ClientProfile(**data)
        return None
    
    def save_client(self, client: ClientProfile):
        """Save client profile."""
        path = self.longterm_path / "clients" / f"{client.name}.json"
        client.updated = datetime.now().isoformat()
        path.write_text(json.dumps(client.__dict__, indent=2), encoding="utf-8")
    
    def list_clients(self) -> List[str]:
        """List all known clients."""
        clients_dir = self.longterm_path / "clients"
        return [f.stem for f in clients_dir.glob("*.json")]
    
    def add_pattern(self, pattern: Pattern):
        """Record a discovered pattern."""
        path = self.longterm_path / "patterns" / f"{pattern.name}.json"
        path.write_text(json.dumps(pattern.__dict__, indent=2), encoding="utf-8")
    
    def get_patterns(self, category: str = None) -> List[Pattern]:
        """Get all patterns, optionally filtered by category."""
        patterns = []
        for path in (self.longterm_path / "patterns").glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            pattern = Pattern(**data)
            if category is None or pattern.category == category:
                patterns.append(pattern)
        return patterns
    
    def add_relationship(self, relationship: Dict):
        """Record a relationship (person, org, connection)."""
        path = self.longterm_path / "relationships" / f"{relationship['id']}.json"
        relationship["created_at"] = datetime.now().isoformat()
        path.write_text(json.dumps(relationship, indent=2), encoding="utf-8")
    
    def get_market_intel(self, topic: str) -> Optional[Dict]:
        """Get market intelligence on a topic."""
        path = self.longterm_path / "market_intelligence" / f"{topic}.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None
    
    def save_market_intel(self, intel: Dict):
        """Save market intelligence."""
        path = self.longterm_path / "market_intelligence" / f"{intel['topic']}.json"
        intel["updated_at"] = datetime.now().isoformat()
        path.write_text(json.dumps(intel, indent=2), encoding="utf-8")
    
    # ================================================================
    # EPISODIC MEMORY
    # ================================================================
    
    def record_episode(self, episode: Episode):
        """Record an episodic memory (what happened)."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        time_str = datetime.now().strftime("%H-%M-%S")
        path = self.episodic_path / f"{date_str}-{time_str}-{episode.id}.json"
        
        episode_dict = episode.__dict__.copy()
        episode_dict["timestamp"] = datetime.now().isoformat()
        path.write_text(json.dumps(episode_dict, indent=2), encoding="utf-8")
    
    def get_episodes(self, since: datetime = None, type_filter: str = None) -> List[Episode]:
        """Get episodes, optionally filtered."""
        episodes = []
        for path in sorted(self.episodic_path.glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            if since and datetime.fromisoformat(data["timestamp"]) < since:
                continue
            if type_filter and data.get("type") != type_filter:
                continue
            episodes.append(Episode(**data))
        return episodes
    
    # ================================================================
    # SKILLS
    # ================================================================
    
    def load_skill(self, category: str, name: str) -> Optional[Skill]:
        """Load a skill from the registry."""
        path = self.skills_path / category / f"{name}.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return Skill(**data)
        return None
    
    def list_skills(self, category: str = None) -> List[str]:
        """List available skills."""
        if category:
            path = self.skills_path / category
            if path.exists():
                return [f.stem for f in path.glob("*.json")]
            return []
        
        skills = []
        for cat_dir in self.skills_path.iterdir():
            if cat_dir.is_dir():
                for f in cat_dir.glob("*.json"):
                    skills.append(f"{cat_dir.name}/{f.stem}")
        return skills
    
    def save_skill(self, category: str, name: str, skill: Skill):
        """Save a skill."""
        path = self.skills_path / category / f"{name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        skill.updated = datetime.now().isoformat()
        path.write_text(json.dumps(skill.__dict__, indent=2), encoding="utf-8")
    
    def increment_skill_usage(self, category: str, name: str):
        """Increment skill usage count."""
        skill = self.load_skill(category, name)
        if skill:
            skill.usage_count += 1
            self.save_skill(category, name, skill)
    
    # ================================================================
    # REFLECTIONS
    # ================================================================
    
    def add_reflection(self, reflection: Reflection):
        """Add a reflection."""
        category = reflection.period
        date_str = datetime.now().strftime("%Y-%m-%d")
        time_str = datetime.now().strftime("%H-%M-%S")
        path = self.reflections_path / category / f"{date_str}-{time_str}.json"
        
        reflection_dict = reflection.__dict__.copy()
        reflection_dict["timestamp"] = datetime.now().isoformat()
        path.write_text(json.dumps(reflection_dict, indent=2), encoding="utf-8")
    
    def get_recent_reflections(self, days: int = 7, category: str = None) -> List[Reflection]:
        """Get recent reflections."""
        cutoff = datetime.now().replace(hour=0, minute=0, second=0)
        cutoff = cutoff.replace(day=cutoff.day - days)
        
        reflections = []
        search_dirs = [self.reflections_path / category] if category else self.reflections_path.iterdir()
        
        for cat_dir in search_dirs:
            if not cat_dir.is_dir():
                continue
            for path in cat_dir.glob("*.json"):
                data = json.loads(path.read_text(encoding="utf-8"))
                if datetime.fromisoformat(data.get("timestamp", "")) >= cutoff:
                    reflections.append(Reflection(**data))
        return reflections
    
    # ================================================================
    # DECISIONS
    # ================================================================
    
    def record_decision(self, decision: Decision):
        """Record a significant decision."""
        path = self.decisions_path / f"{decision.id}.json"
        path.write_text(json.dumps(decision.__dict__, indent=2), encoding="utf-8")
        
        # Update index
        index_path = self.decisions_path / "index.json"
        index = []
        if index_path.exists():
            index = json.loads(index_path.read_text(encoding="utf-8"))
        index.append({
            "id": decision.id,
            "topic": decision.topic,
            "timestamp": decision.timestamp,
            "outcome": decision.outcome,
            "chosen": decision.chosen
        })
        index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")
    
    def get_decisions(self, topic: str = None) -> List[Decision]:
        """Get decisions, optionally filtered by topic."""
        decisions = []
        for path in self.decisions_path.glob("*.json"):
            if path.name == "index.json":
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            decision = Decision(**data)
            if topic is None or topic.lower() in decision.topic.lower():
                decisions.append(decision)
        return decisions
    
    def get_decision_index(self) -> List[Dict]:
        """Get decision index."""
        index_path = self.decisions_path / "index.json"
        if index_path.exists():
            return json.loads(index_path.read_text(encoding="utf-8"))
        return []
    
    # ================================================================
    # PREFERENCES
    # ================================================================
    
    def get_preference(self, category: str, key: str) -> Optional[Any]:
        """Get a specific preference."""
        path = self.preferences_path / category / f"{key}.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return data.get("value")
        return None
    
    def set_preference(self, category: str, key: str, value: Any, confidence: float = 0.5, source: str = "observed"):
        """Set a preference."""
        path = self.preferences_path / category / f"{key}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        
        pref = Preference(
            category=category,
            key=key,
            value=value,
            confidence=confidence,
            source=source
        )
        path.write_text(json.dumps(pref.__dict__, indent=2), encoding="utf-8")
    
    def get_all_preferences(self) -> Dict[str, Dict[str, Any]]:
        """Get all preferences."""
        prefs = {}
        for cat_dir in self.preferences_path.iterdir():
            if cat_dir.is_dir():
                prefs[cat_dir.name] = {}
                for pref_file in cat_dir.glob("*.json"):
                    data = json.loads(pref_file.read_text(encoding="utf-8"))
                    prefs[cat_dir.name][data["key"]] = data["value"]
        return prefs
    
    # ================================================================
    # CHECKPOINTS
    # ================================================================
    
    def save_checkpoint(self, runtime_state: Dict, working: WorkingMemory):
        """Save runtime state + working memory to checkpoint."""
        checkpoint_data = {
            **runtime_state,
            "working_memory": working.__dict__
        }
        path = self.cache_path / "runtime_cache.json"
        path.write_text(json.dumps(checkpoint_data, indent=4), encoding="utf-8")
    
    def load_checkpoint(self) -> Optional[Dict]:
        """Load checkpoint if exists."""
        path = self.cache_path / "runtime_cache.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None
    
    def is_checkpoint_valid(self, checkpoint: Dict) -> bool:
        """Verify checkpoint matches current critical docs."""
        # Check if critical files have changed since checkpoint
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
            full_path = self.workspace_root / rel_path
            if full_path.exists():
                mtime = datetime.fromtimestamp(full_path.stat().st_mtime)
                if mtime > checkpoint_dt:
                    return False
        return True
    
    # ================================================================
    # INITIALIZATION
    # ================================================================
    
    def initialize_from_docs(self):
        """Initialize identity from existing documentation."""
        identity = IdentityMemory()
        
        # Load from 02_COO/identity.md
        identity_path = self.workspace_root / "02_COO" / "identity.md"
        if identity_path.exists():
            identity.role = identity_path.read_text(encoding="utf-8")
        
        # Load from 01_CEO/company.md
        company_path = self.workspace_root / "01_CEO" / "company.md"
        if company_path.exists():
            identity.mission = company_path.read_text(encoding="utf-8")
        
        # Load from 01_CEO/decision_principles.md
        principles_path = self.workspace_root / "01_CEO" / "decision_principles.md"
        if principles_path.exists():
            identity.principles = principles_path.read_text(encoding="utf-8")
        
        # Load from 02_COO/identity.md for authority
        if identity_path.exists():
            identity.authority = identity_path.read_text(encoding="utf-8")
        
        self.save_identity(identity)
        return identity