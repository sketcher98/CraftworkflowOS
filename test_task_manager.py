from runtime.task import Task
from runtime.task_manager import TaskManager

manager = TaskManager()

manager.add(
    Task(
        objective="Write proposal",
        priority="High"
    )
)

manager.add(
    Task(
        objective="Research agency leads",
        priority="Critical"
    )
)

manager.add(
    Task(
        objective="Update documentation",
        priority="Low"
    )
)

next_task = manager.next()

print()

print("Next Task")

print(next_task)