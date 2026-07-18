"""
Executive Loop

Every request passes through this file.

This is the brain of CraftworkflowOS.
"""

from runtime.loader import load_company, refresh_runtime
from runtime.mission import run_mission
from runtime.reflection import reflect
from runtime.checkpoint import save_checkpoint
from runtime.planner import collect_context
from runtime.priority import choose_priority
from runtime.briefing import create_briefing


def execute(task: str, runtime):

    # Load hot cache (static context) - once per session
    runtime = load_company(runtime)

    # Refresh warm cache (dynamic context) for current task
    runtime = refresh_runtime(runtime, tier="warm")

    if task.lower() == "what should i work on today?":

        context = collect_context(runtime)

        priority = choose_priority(context)

        result = create_briefing(priority)

    else:

        result = run_mission(task, runtime)

    reflect(task, result, runtime)

    save_checkpoint(runtime.to_dict())

    return result