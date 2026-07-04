from runtime.knowledge import load_department

commercial = load_department("Commercial")

print()

print("=" * 50)
print("DIRECTOR")
print("=" * 50)

print(commercial["director"][:300])

print()

print("=" * 50)
print("EMPLOYEES")
print("=" * 50)

for employee in commercial["employees"]:

    print(employee)

print()

print("=" * 50)
print("PLAYBOOK")
print("=" * 50)

print(commercial["playbook"][:300])