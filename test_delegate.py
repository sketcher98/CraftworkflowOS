from runtime.organization import discover_organization
from runtime.delegate import delegate

organization = discover_organization()

commercial = organization["Commercial"]

employee = commercial["employees"][0]

report = delegate(
    "Find five qualified agency leads",
    employee
)

print()
print(report)