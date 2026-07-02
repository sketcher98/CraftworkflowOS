from runtime.context import OperatingContext
from runtime.executive import execute

ctx = OperatingContext()

result = execute(
    "What should I work on today?",
    ctx
)

print(result)

print()
print("----- Loader Test -----")
print()

print("Company characters:",
      len(ctx.company["content"]))

print("Identity characters:",
      len(ctx.identity["content"]))

print("Principles characters:",
      len(ctx.principles["content"]))

print("Company State characters:",
      len(ctx.company_state["content"]))