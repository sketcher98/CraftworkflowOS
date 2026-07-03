from runtime.execution_engine import execute
from runtime.task import Task

task = Task(
    objective="Find five agency owners",
    department="Commercial"
)

result = execute(task)

print()
print(result)