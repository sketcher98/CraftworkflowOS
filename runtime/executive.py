"""
Executive Loop

Every request passes through this file.

This is the brain of CraftworkflowOS.
"""

from runtime.loader import load_company, refresh_runtime
from runtime.refresh import refresh_for_task
from runtime.mission import run_mission
from runtime.reflection import reflect
from runtime.checkpoint import save_checkpoint
from runtime.planner import collect_context
from runtime.priority import choose_priority
from runtime.briefing import create_briefing
from runtime.commercial_briefing import run_commercial_briefing


def execute(task: str, runtime):

    # Load hot cache (static context) - once per session
    runtime = load_company(runtime)

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

    reflect(task, result, runtime)

    save_checkpoint(runtime.to_dict())

    return result