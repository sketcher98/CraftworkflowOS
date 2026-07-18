"""
Capability Registry

Every business capability maps to one or more providers.

Providers can change.
Capabilities stay forever.
"""

from runtime.provider_registry import list_capabilities, get_providers_for_capability


# Static capability definitions (capabilities that exist regardless of providers)
CAPABILITIES = {
    "research": ["Perplexity", "Browser"],
    "writing": ["GPT-4o"],
    "coding": ["OpenClaw", "Codex"],
    "design": ["OpenDesign", "Figma"],
    "video": ["HeyGen", "VEED"],
    "automation": ["Make", "n8n"],
    "crm": ["HubSpot"]
}


def get_provider(capability):
    """Get the first available provider for a capability from registry."""
    providers = get_providers_for_capability(capability)
    if providers:
        return providers[0]
    # Fallback to static definition
    providers = CAPABILITIES.get(capability.lower(), [])
    if providers:
        return providers[0]
    return None


def get_providers(capability):
    """Get all available providers for a capability."""
    providers = get_providers_for_capability(capability)
    if providers:
        return providers
    return CAPABILITIES.get(capability.lower(), [])


def list_available_capabilities():
    """List capabilities that have at least one registered provider."""
    registry_caps = list_capabilities()
    static_caps = set(CAPABILITIES.keys())
    return list(registry_caps | static_caps)