"""
Provider Initialization

Registers all built-in providers with the Provider Registry.
Run this at application startup to make providers available.
"""

from runtime.provider_registry import register_provider
from runtime.providers import browser, gpt, perplexity


def init_providers():
    """
    Initialize and register all built-in providers.
    Call this once at application startup.
    """
    # Browser - research capability
    register_provider(
        name=browser.PROVIDER_NAME,
        executor=browser.execute,
        capabilities=browser.CAPABILITIES,
        metadata={
            "description": "Web search and scraping",
            "auth": "optional (SERPAPI_KEY for enhanced results)",
            "rate_limit": "respectful"
        }
    )
    
    # GPT-4o - writing capability
    register_provider(
        name=gpt.PROVIDER_NAME,
        executor=gpt.execute,
        capabilities=gpt.CAPABILITIES,
        metadata={
            "description": "OpenAI GPT-4o for writing and content generation",
            "auth": "required (OPENAI_API_KEY)",
            "rate_limit": "tier-based"
        }
    )
    
    # Perplexity - research capability
    register_provider(
        name=perplexity.PROVIDER_NAME,
        executor=perplexity.execute,
        capabilities=perplexity.CAPABILITIES,
        metadata={
            "description": "Perplexity AI for deep research and ICP matching",
            "auth": "required (PERPLEXITY_API_KEY)",
            "rate_limit": "plan-based"
        }
    )
    
    print("All built-in providers registered.")


# Auto-initialize when module is imported
init_providers()