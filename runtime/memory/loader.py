"""
Memory Loader

Loads memory into the runtime context during boot sequence.
Integrates with existing loader and refresh system.
"""

from runtime.memory.manager import MemoryManager
from runtime.memory.schemas import IdentityMemory, WorkingMemory


def load_memory(runtime):
    """
    Load all memory layers into runtime during boot.
    
    This is called during Phase 10 of the boot sequence.
    """
    if not hasattr(runtime, 'memory_manager'):
        runtime.memory_manager = MemoryManager()
    
    mm = runtime.memory_manager
    
    # Load identity (static, once per session)
    if not getattr(runtime, 'identity_loaded', False):
        runtime.identity_memory = mm.load_identity()
        runtime.identity_loaded = True
        print("Identity memory loaded.")
    
    # Initialize working memory (will be restored from checkpoint in Phase 11)
    if not getattr(runtime, 'working_memory', None):
        runtime.working_memory = mm.load_working()
        print("Working memory initialized.")
    
    # Load available skills index
    if not getattr(runtime, 'skills_index', None):
        runtime.skills_index = {}
        for category in ["outreach", "discovery", "proposal", "onboarding", "internal"]:
            skills = mm.list_skills(category)
            if skills:
                runtime.skills_index[category] = skills
        print(f"Skills index loaded: {sum(len(v) for v in runtime.skills_index.values())} skills.")
    
    # Load preferences
    if not getattr(runtime, 'preferences_loaded', False):
        runtime.preferences = mm.get_all_preferences()
        runtime.preferences_loaded = True
        print("Preferences loaded.")
    
    return runtime


def refresh_memory(runtime, tier: str = "warm"):
    """
    Refresh memory layers based on tier.
    
    Called during Phase 11 and when task requires fresh context.
    """
    if not hasattr(runtime, 'memory_manager'):
        return runtime
    
    mm = runtime.memory_manager
    
    if tier in ("cold", "all"):
        # Refresh long-term memory (clients, patterns, relationships)
        print("Refreshing long-term memory...")
        # Long-term is file-based, auto-refreshed on access
    
    if tier in ("warm", "all"):
        # Refresh working memory from files
        print("Refreshing working memory...")
        mm = runtime.memory_manager
        working = mm.load_working()
        runtime.working_memory = working
    
    if tier in ("hot", "all"):
        # Refresh identity (rarely needed)
        print("Refreshing identity...")
        runtime.identity_memory = runtime.memory_manager.load_identity()
    
    return runtime


def load_skills_for_objective(runtime, objective: str):
    """
    Load skills relevant to current objective.
    
    Called when starting a task that needs specific skills.
    """
    mm = runtime.memory_manager
    
    # Determine relevant skills from objective keywords
    objective_lower = objective.lower()
    relevant_skills = []
    
    skill_keywords = {
        "outreach": ["outreach", "message", "dm", "linkedin", "twitter", "cold", "prospect"],
        "discovery": ["discovery", "call", "meeting", "diagnose", "qualify"],
        "proposal": ["proposal", "quote", "pricing", "contract", "close"],
        "onboarding": ["onboard", "kickoff", "setup", "implementation"],
        "internal": ["plan", "review", "reflect", "decide", "prioritize"]
    }
    
    for category, keywords in skill_keywords.items():
        if any(kw in objective_lower for kw in keywords):
            skills = runtime.memory_manager.list_skills(category)
            relevant_skills.extend([f"{category}/{s}" for s in skills])
    
    # Load the actual skill objects
    active_skills = []
    for skill_ref in relevant_skills:
        category, name = skill_ref.split("/", 1)
        skill = runtime.memory_manager.load_skill(category, name)
        if skill:
            active_skills.append(skill)
    
    # Update working memory
    runtime.working_memory.active_skills = [f"{s.category}/{s.name}" for s in active_skills]
    
    print(f"Loaded {len(active_skills)} skills for objective: {objective[:50]}...")
    return active_skills


def get_relevant_memory(runtime, query: str) -> Dict:
    """
    Get memory relevant to a query.
    
    Used by executive loop for context-aware decisions.
    """
    mm = runtime.memory_manager
    query_lower = query.lower()
    
    relevant = {
        "clients": [],
        "patterns": [],
        "episodes": [],
        "skills": [],
        "preferences": {},
        "reflections": [],
        "decisions": []
    }
    
    # Check clients
    for client_name in mm.list_clients():
        if client_name.lower() in query_lower:
            client = mm.get_client(client_name)
            if client:
                relevant["clients"].append(client)
    
    # Check patterns
    patterns = mm.get_patterns()
    for pattern in patterns:
        if any(indicator.lower() in query_lower for indicator in pattern.indicators):
            relevant["patterns"].append(pattern)
    
    # Check recent episodes
    episodes = mm.get_episodes(since=datetime.now().replace(day=datetime.now().day - 30))
    for episode in episodes:
        if any(tag.lower() in query_lower for tag in episode.tags):
            relevant["episodes"].append(episode)
    
    # Check skills
    for skill_ref in runtime.working_memory.active_skills:
        category, name = skill_ref.split("/", 1)
        skill = runtime.memory_manager.load_skill(category, name)
        if skill:
            relevant["skills"].append(skill)
    
    # Check preferences
    prefs = runtime.memory_manager.get_all_preferences()
    for category, prefs in prefs.items():
        for key, value in prefs.items():
            if key.lower() in query_lower:
                relevant["preferences"][f"{category}.{key}"] = value
    
    # Check recent reflections
    reflections = mm.get_recent_reflections(days=7)
    for reflection in reflections:
        if any(tag.lower() in query_lower for tag in reflection.tags):
            relevant["reflections"].append(reflection)
    
    # Check decisions
    decisions = mm.get_decisions()
    for decision in decisions:
        if any(tag.lower() in query_lower for tag in decision.tags):
            relevant["decisions"].append(decision)
    
    return relevant