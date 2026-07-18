"""
Person Loader

Loads Directors and Employees into structured objects.
"""

from pathlib import Path

ROOT = Path(__file__).parent.parent


def load_person(path: Path):

    if not path.exists():
        return None

    text = path.read_text(
        encoding="utf-8"
    )

    # For employee: path = 03_Departments/Commercial/Employees/Discovery/Profile.md
    #   path.parent = Discovery/
    #   path.parent.parent = Employees/
    #   path.parent.parent.name = "Employees"
    #   Employee name = path.parent.name = "Discovery"
    #   
    # For director: path = 03_Departments/Commercial/Commercial_Director.md
    #   path.parent = Commercial/
    #   path.parent.name != "Employees"
    #   Director name = path.stem.replace("_", " ") = "Commercial Director"
    
    if path.parent.parent.name == "Employees":
        name = path.parent.name  # e.g., "Discovery"
    else:
        name = path.stem.replace("_", " ")

    return {
        "name": name,
        "content": text
    }