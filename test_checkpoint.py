from runtime.context import OperatingContext
from runtime.checkpoint import save_checkpoint, load_checkpoint


ctx = OperatingContext()

ctx.company_loaded = True
ctx.identity_loaded = True
ctx.principles_loaded = True
ctx.company_state_loaded = True

ctx.current_project = "CraftworkflowOS"
ctx.current_objective = "Build Hermes COO"


save_checkpoint(ctx.to_dict())


loaded = load_checkpoint()

new_ctx = OperatingContext.from_dict(loaded)

print(new_ctx)