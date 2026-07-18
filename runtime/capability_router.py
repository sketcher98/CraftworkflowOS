"""
Capability Router

Employees never call tools directly.
Instead they request a capability.

The router decides which provider
should execute the work.

Routes capabilities to real providers using Provider Registry.
"""

from runtime.capabilities import CAPABILITIES
from runtime.provider_registry import get_registry

# Import providers to trigger registration
from runtime.providers import browser, gpt, perplexity


def request(capability: str, objective: str = ""):
    """
    Route a capability request to the appropriate provider(s).
    
    Args:
        capability: The capability name (e.g., "research", "writing", "automation")
        objective: The task objective/description
        
    Returns:
        Dict with capability, providers results, and status
    """
    
    # Get provider names from capability registry
    provider_names = CAPABILITIES.get(capability, [])
    
    # Filter to only registered providers
    registry = get_registry()
    registered_providers = [p for p in provider_names if registry.get_provider(p)]
    
    print(f"\nCapability: {capability}")
    print(f"Available providers: {registered_providers}")
    
    completed = []
    
    for provider_name in registered_providers:
        try:
            artifact = registry.get_provider(provider_name)(objective)
            completed.append(artifact)
        except Exception as e:
            print(f"      Provider {provider_name} failed: {e}")
            # Add error artifact
            from runtime.artifacts import Artifact
            completed.append(Artifact(
                type="Error",
                title=f"{provider_name} Error",
                content=str(e),
                created_by=provider_name,
                metadata={"error": True}
            ))
    
    return {
        "capability": capability,
        "providers": completed,
        "status": "completed"
    }