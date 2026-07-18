"""
Executive Loop

Every request passes through this file.

This is the brain of CraftworkflowOS.
"""

from runtime.loader import load_company, refresh_runtime
from runtime.refresh import refresh_for_task
from runtime.mission import run_mission
from runtime.reflection import reflect
from runtime.checkpoint import save_checkpoint, load_checkpoint, is_checkpoint_valid
from runtime.planner import collect_context
from runtime.priority import choose_priority
from runtime.briefing import create_briefing
from runtime.commercial_briefing import run_commercial_briefing
from runtime.memory.manager import MemoryManager


def execute(task: str, runtime):
    # Initialize memory manager if not present
    if not hasattr(runtime, 'memory_manager'):
        runtime.memory_manager = MemoryManager()
    
    mm = runtime.memory_manager
    
    # Phase 10: Load Memory System (if not already loaded)
    if not hasattr(runtime, 'identity_loaded') or not runtime.identity_loaded:
        # Load identity memory
        runtime.identity_memory = mm.load_identity()
        runtime.identity_loaded = True
        
        # Initialize working memory (will be restored from checkpoint in Phase 11)
        runtime.working_memory = mm.load_working()
        
        # Load skills index
        runtime.skills_index = {}
        for category in ["outreach", "discovery", "proposal", "onboarding", "internal"]:
            skills = mm.list_skills(category)
            if skills:
                runtime.skills_index[category] = skills
        
        # Load preferences
        runtime.preferences = mm.get_all_preferences()
        runtime.preferences_loaded = True
    
    # Phase 11: Restore Working Memory from Checkpoint
    checkpoint = load_checkpoint()
    if checkpoint and is_checkpoint_valid(checkpoint, mm):
        # Valid checkpoint - restore working memory
        runtime.working_memory = mm.load_working(checkpoint)
        runtime = load_company(runtime)  # Reload docs
        runtime = refresh_runtime(runtime, tier="warm")  # Refresh dynamic context
        print(f"Working memory restored from checkpoint. Objective: {runtime.working_memory.current_objective}")
    else:
        # No valid checkpoint - fresh start
        runtime = load_company(runtime)
        runtime = refresh_runtime(runtime, tier="warm")
        # Set initial objective from company state
        if hasattr(runtime, 'working_memory') and not runtime.working_memory.current_objective:
            runtime.working_memory.current_objective = "Land the next paying client"
    
    # Phase 12: Activate Runtime (Mission Loop)
    # Smart refresh based on task requirements
    if task.lower() == "what should i work on today?":
        # Need inbox and projects for prioritization
        runtime = refresh_for_task(runtime, required_info=["inbox", "projects"])
        
        context = collect_context(runtime)
        priority = choose_priority(context)
        result = create_briefing(priority)
        
    elif task.lower().startswith("commercial briefing") or task.lower().startswith("daily briefing"):
        # Need full commercial pipeline context
        runtime = refresh_for_task(runtime, required_info=["inbox", "projects", "client"])
        result = run_commercial_briefing(runtime)
        
    else:
        # General task - load warm cache
        runtime = refresh_for_task(runtime, required_info=["inbox", "projects"])
        result = run_mission(task, runtime)
    
    # Reflection and checkpoint
    reflect(task, result, runtime)
    
    # Save checkpoint with working memory
    if hasattr(runtime, 'working_memory'):
        save_checkpoint(runtime.to_dict(), runtime.working_memory)
    else:
        save_checkpoint(runtime.to_dict())
    
    return result