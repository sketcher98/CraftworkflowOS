"""
Task Manager

Central queue for Hermes.
"""

from runtime.task import Task


class TaskManager:

    def __init__(self):

        self.tasks = []

    def add(self, task: Task):

        self.tasks.append(task)

    def pending(self):

        return [
            t
            for t in self.tasks
            if t.status == "Pending"
        ]

    def completed(self):

        return [
            t
            for t in self.tasks
            if t.status == "Completed"
        ]

    def next(self):

        pending = self.pending()

        if not pending:
            return None

        priorities = {
            "Critical": 4,
            "High": 3,
            "Normal": 2,
            "Low": 1
        }

        pending.sort(
            key=lambda t: priorities.get(
                t.priority,
                0
            ),
            reverse=True
        )

        return pending[0]