from runtime.organization import discover_organization
from runtime.director_engine import run_department

organization = discover_organization()

commercial = organization["Commercial"]

report = run_department(
    "Get five new agency clients",
    commercial
)

print()
print("=" * 50)
print(report["department"])
print("=" * 50)

for item in report["reports"]:

    print()
    print(item["employee"])
    print(item["recommendation"])