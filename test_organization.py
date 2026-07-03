from runtime.organization import discover_organization

organization = discover_organization()

for department, info in organization.items():

    print()
    print("=" * 50)
    print(department)
    print("=" * 50)

    director = info["director"]

    if director:
        print("Director:")
        print(director["name"])

    print()

    print("Employees:")

    for employee in info["employees"]:
        print("-", employee["name"])