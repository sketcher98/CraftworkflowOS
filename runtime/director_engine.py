"""
Director Engine

Coordinates department employees.
"""

from runtime.delegate import delegate
from runtime.playbook_loader import load_playbook


def run_department(task: str, department: dict):
    """
    Run a department's workflow.
    
    Args:
        task: The objective for the department
        department: Dict with 'director' and 'employees' keys
    """
    
    reports = []
    
    dept_name = department["director"]["name"]
    
    playbook = load_playbook(dept_name)
    
    for employee in department["employees"]:
        employee_name = employee["name"]
        employee_task = playbook.get(employee_name, task)
        
        reports.append(
            delegate(employee_task, employee)
        )
    
    return {
        "department": dept_name,
        "reports": reports
    }