from runtime.context import OperatingContext
from runtime.executive import execute

ctx = OperatingContext(
    company_loaded=True,
    identity_loaded=True,
    principles_loaded=True,
    company_state_loaded=True,
    current_project="CraftworkflowOS",
    current_objective="Build Hermes COO",
)

result = execute(
    "Improve the client onboarding process",
    ctx
)

print(result)