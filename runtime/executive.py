"""
Executive Loop

Every request passes through this file.

This is the brain of CraftworkflowOS.
"""

from runtime.loader import load_company
from runtime.refresh import refresh_runtime
from runtime.mission import run_mission
from runtime.reflection import reflect
from runtime.checkpoint import save_checkpoint


def execute(task: str, runtime):

    runtime = load_company(runtime)

    runtime = refresh_runtime(runtime)

    result = run_mission(task, runtime)

    reflect(task, result, runtime)

    save_checkpoint(runtime.to_dict())

    return result