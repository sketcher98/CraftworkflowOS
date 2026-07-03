from runtime.scanner import scan_workspace

workspace = scan_workspace()

print()

print("Projects")

print(workspace["projects"])

print()

print("Clients")

print(workspace["clients"])

print()

print("Tasks")

print(workspace["tasks"])