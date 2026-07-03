"""
Department Director

Loads the correct department.
"""

from pathlib import Path

ROOT = Path(__file__).parent.parent


def load_department(name: str):

    path = ROOT / "03_Departments" / name

    return {
        "name": name,
        "path": path
    }