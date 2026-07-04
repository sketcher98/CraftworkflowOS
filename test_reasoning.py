from runtime.knowledge import load_department
from runtime.reasoning import reason

department = load_department("Commercial")

lead = {

    "company": "Agency Alpha",

    "industry": "Marketing Agency",

    "employees": 12,

    "city": "London",

    "score": 90

}

brain = reason(
    department,
    lead
)

print()

print("=" * 60)
print("COMMERCIAL BRAIN")
print("=" * 60)

print()

print(brain["context"])

print()

print("=" * 60)
print("DIRECTOR KNOWLEDGE")
print("=" * 60)

print(brain["director"][:250])

print()

print("=" * 60)
print("PLAYBOOK")
print("=" * 60)

print(brain["playbook"][:250])

print()

print("=" * 60)
print("EMPLOYEES")
print("=" * 60)

for employee in brain["employees"]:

    print(employee)