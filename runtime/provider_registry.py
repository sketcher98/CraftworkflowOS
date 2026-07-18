"""
Provider Registry

Manages provider registration, discovery, and capability routing.
Providers can be registered dynamically and selected for capabilities.
"""

from typing import Callable, Dict, List, Any
from runtime.artifacts import Artifact


class ProviderRegistry:
    """
    Registry for all external providers.
    
    Providers implement capabilities (research, writing, coding, design, etc.)
    and are registered here for the capability router to discover.
    """
    
    def __init__(self):
        self._providers: Dict[str, Callable] = {}
        self._provider_metadata: Dict[str, Dict] = {}
        self._capability_map: Dict[str, List[str]] = {}
    
    def register(self, name: str, executor: Callable, capabilities: List[str], metadata: Dict = None):
        """
        Register a provider.
        
        Args:
            name: Provider name (e.g., "Perplexity", "GPT-5", "Browser")
            executor: Function that takes objective str and returns Artifact or dict
            capabilities: List of capabilities this provider fulfills
            metadata: Optional metadata (auth, config, rate limits, etc.)
        """
        self._providers[name] = executor
        self._provider_metadata[name] = metadata or {}
        
        for capability in capabilities:
            if capability not in self._capability_map:
                self._capability_map[capability] = []
            if name not in self._capability_map[capability]:
                self._capability_map[capability].append(name)
        
        print(f"Registered provider: {name} -> capabilities: {capabilities}")
    
    def get_provider(self, name: str) -> Callable:
        """Get provider executor by name."""
        return self._providers.get(name)
    
    def get_providers_for_capability(self, capability: str) -> List[str]:
        """Get list of provider names that fulfill a capability."""
        return self._capability_map.get(capability, [])
    
    def get_provider_metadata(self, name: str) -> Dict:
        """Get metadata for a provider."""
        return self._provider_metadata.get(name, {})
    
    def list_providers(self) -> List[str]:
        """List all registered provider names."""
        return list(self._providers.keys())
    
    def list_capabilities(self) -> List[str]:
        """List all registered capabilities."""
        return list(self._capability_map.keys())
    
    def execute_capability(self, capability: str, objective: str) -> List[Any]:
        """
        Execute a capability using all registered providers for it.
        
        Returns list of results from each provider.
        """
        providers = self.get_providers_for_capability(capability)
        results = []
        
        for provider_name in providers:
            executor = self._providers.get(provider_name)
            if executor:
                print(f"      {provider_name} executing...")
                try:
                    result = executor(objective)
                    results.append({
                        "provider": provider_name,
                        "result": result
                    })
                except Exception as e:
                    print(f"      ERROR in {provider_name}: {e}")
                    results.append({
                        "provider": provider_name,
                        "error": str(e)
                    })
        
        return results


# Global registry instance
REGISTRY = ProviderRegistry()


def register_provider(name: str, executor: Callable, capabilities: List[str], metadata: Dict = None):
    """Convenience function to register a provider globally."""
    REGISTRY.register(name, executor, capabilities, metadata)


def get_providers_for_capability(capability: str) -> List[str]:
    """Get list of provider names that fulfill a capability."""
    return REGISTRY.get_providers_for_capability(capability)


def execute_provider(provider_name: str, objective: str) -> Any:
    """Execute a specific provider by name with an objective."""
    executor = REGISTRY.get_provider(provider_name)
    if not executor:
        raise ValueError(f"Provider '{provider_name}' not found in registry")
    return executor(objective)


def list_providers() -> List[str]:
    """List all registered provider names."""
    return REGISTRY.list_providers()


def list_capabilities() -> List[str]:
    """List all registered capabilities."""
    return REGISTRY.list_capabilities()


def get_registry() -> ProviderRegistry:
    """Get the global provider registry instance."""
    return REGISTRY