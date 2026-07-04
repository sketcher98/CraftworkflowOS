from runtime.task import Task
from runtime.commercial import discovery, lead_intelligence
from runtime.outreach import create_messages


task = Task(
    objective="Find five agency owners",
    department="Commercial"
)

result = discovery(task)

artifacts = []

for step in result["steps"]:
    artifacts.extend(step["providers"])

qualified = lead_intelligence(artifacts)

print("\n==============================")
print("QUALIFIED LEADS")
print("==============================")

for lead in qualified:

    print(

        f"{lead['company']} | "

        f"{lead['industry']} | "

        f"{lead['city']} | "

        f"{lead['employees']} Employees | "

        f"Score {lead['score']}"

    )

messages = create_messages(qualified)

print("\n==============================")
print("COMMERCIAL BRAIN")
print("==============================")

for message in messages:

    print()

    print(message["company"])

    print("Playbook :", message["strategy"]["playbook"])

    print("Flow     :", message["strategy"]["flow"])

    print("Platform :", message["strategy"]["platform"])

    print("Priority :", message["strategy"]["priority"])

    print("--------------------------------")

    print(message["message"])