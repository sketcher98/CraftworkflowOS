"""
Capability Router v2

Routes capability requests to optimal providers with health awareness, fallback, and cost/latency optimization.
"""

import os
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from runtime.runtime_contracts import CapabilityName, ProviderName, RuntimeContext, CapabilityRequest, CapabilityResult, Artifact
from runtime.provider_router_v2 import (
    select_provider, 
    execute_with_fallback, 
    get_providers_for_capability,
    is_healthy,
    track_provider_cost,
    PROVIDER_REGISTRY
)
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# Provider Executors (Mock implementations - replace with real API calls)
# ============================================================================

def _execute_perplexity(objective: str) -> Artifact:
    """Execute Perplexity research."""
    api_key = os.getenv("PERPLEXITY_API_KEY")
    
    if not api_key:
        logger.warning("PERPLEXITY_API_KEY not set, using mock")
        return Artifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            artifact_type="research-report",
            version="1.0.0",
            title="ICP Research Results",
            content={
                "objective": objective,
                "findings": [
                    {"company": "Creative Agency Ltd", "industry": "Creative Agency", "location": "London, UK", "size": "10-15 employees", "signals": ["Hiring: Senior Designer", "Posted: 'Booked out for Q1'"], "linkedin_url": "https://linkedin.com/company/creative-agency"},
                    {"company": "Growth Marketing Co", "industry": "Marketing Agency", "location": "Manchester, UK", "size": "5-10 employees", "signals": ["Posted: 'Scaling delivery team'", "Hiring: Account Manager"], "linkedin_url": "https://linkedin.com/company/growth-marketing"}
                ],
                "recommendations": ["Target Creative Agency Ltd - high urgency signals", "Engage Growth Marketing Co - scaling delivery"]
            },
            created_by="Perplexity",
            created_at=datetime.now()
        )
    
    # Real API call would go here
    import requests
    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": "sonar-pro",
                "messages": [
                    {"role": "system", "content": "You are a lead intelligence specialist. Find high-quality agency founders matching ICP."},
                    {"role": "user", "content": objective}
                ],
                "max_tokens": 2000,
                "temperature": 0.2
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        
        return Artifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            artifact_type="research-report",
            version="1.0.0",
            title="ICP Research Results",
            content={"objective": objective, "raw_response": content},
            created_by="Perplexity"
        )
    except Exception as e:
        logger.error(f"Perplexity error: {e}")
        return Artifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            artifact_type="research-report",
            version="1.0.0",
            title="ICP Research Results (Error)",
            content={"objective": objective, "error": str(e)},
            created_by="Perplexity"
        )


def _execute_gpt4o(objective: str) -> Artifact:
    """Execute GPT-4o writing."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        logger.warning("OPENAI_API_KEY not set, using mock")
        return Artifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            artifact_type="draft",
            version="1.0.0",
            title="Outreach Message",
            content={
                "objective": objective,
                "message": "Hey,\n\nQuick question—has workload started growing faster than operational freedom recently?\n\n—Precious"
            },
            created_by="GPT-4o"
        )
    
    from openai import OpenAI
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are Precious, founder of CraftedWorkflows. Write concise, respectful outreach messages."},
                {"role": "user", "content": objective}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        content = response.choices[0].message.content.strip()
        tokens_used = response.usage.total_tokens if response.usage else 0
        
        return Artifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            artifact_type="draft",
            version="1.0.0",
            title="Outreach Message",
            content={"objective": objective, "message": content, "tokens_used": tokens_used},
            created_by="GPT-4o",
            metadata={"tokens_used": tokens_used}
        )
    except Exception as e:
        logger.error(f"GPT-4o error: {e}")
        return Artifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            artifact_type="draft",
            version="1.0.0",
            title="Outreach Message (Error)",
            content={"objective": objective, "error": str(e)},
            created_by="GPT-4o"
        )


def _execute_claude(objective: str) -> Artifact:
    """Execute Claude analysis."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        logger.warning("ANTHROPIC_API_KEY not set, using mock")
        return Artifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            artifact_type="analysis",
            version="1.0.0",
            title="Financial Analysis",
            content={"objective": objective, "analysis": "Mock financial analysis - margin 72%, recommended price $9,500"},
            created_by="Claude-3.5-Sonnet"
        )
    
    import anthropic
    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            temperature=0.3,
            messages=[{"role": "user", "content": objective}]
        )
        
        content = response.content[0].text if response.content else ""
        
        return Artifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            artifact_type="analysis",
            version="1.0.0",
            title="Analysis Result",
            content={"objective": objective, "analysis": content},
            created_by="Claude-3.5-Sonnet"
        )
    except Exception as e:
        logger.error(f"Claude error: {e}")
        return Artifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            artifact_type="analysis",
            version="1.0.0",
            title="Analysis Result (Error)",
            content={"objective": objective, "error": str(e)},
            created_by="Claude-3.5-Sonnet"
        )


def _execute_groq(objective: str) -> Artifact:
    """Execute Groq coding."""
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        logger.warning("GROQ_API_KEY not set, using mock")
        return Artifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            artifact_type="code",
            version="1.0.0",
            title="Code Implementation",
            content={"objective": objective, "code": "# Mock implementation\nclass Handler:\n    def process(self, data):\n        return {'status': 'ok'}"},
            created_by="Groq-Llama-3.1-70B"
        )
    
    from groq import Groq
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert Python developer. Write clean, typed, production-ready code."},
                {"role": "user", "content": objective}
            ],
            max_tokens=4000,
            temperature=0.2
        )
        
        content = response.choices[0].message.content
        
        return Artifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            artifact_type="code",
            version="1.0.0",
            title="Code Implementation",
            content={"objective": objective, "code": content},
            created_by="Groq-Llama-3.1-70B"
        )
    except Exception as e:
        logger.error(f"Groq error: {e}")
        return Artifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            artifact_type="code",
            version="1.0.0",
            title="Code Implementation (Error)",
            content={"objective": objective, "error": str(e)},
            created_by="Groq-Llama-3.1-70B"
        )


def _execute_figma(objective: str) -> Artifact:
    """Execute Figma design."""
    token = os.getenv("FIGMA_TOKEN")
    
    if not token:
        logger.warning("FIGMA_TOKEN not set, using mock")
        return Artifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            artifact_type="design-spec",
            version="1.0.0",
            title="Design Specification",
            content={"objective": objective, "spec": {"components": ["Button", "Card", "Table"], "tokens": {"colors": {"primary": "#6B46C1"}}}},
            created_by="Figma"
        )
    
    # Real Figma API call would go here
    return Artifact(
        artifact_id=f"art_{uuid.uuid4().hex[:8]}",
        artifact_type="design-spec",
        version="1.0.0",
        title="Design Specification",
        content={"objective": objective, "spec": "Figma file created", "file_key": "mock_key"},
        created_by="Figma"
    )


def _execute_browser(objective: str) -> Artifact:
    """Execute Browser search."""
    api_key = os.getenv("SERPER_API_KEY")
    
    if not api_key:
        logger.warning("SERPER_API_KEY not set, using mock")
        return Artifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            artifact_type="search-results",
            version="1.0.0",
            title="Search Results",
            content={"objective": objective, "results": [{"title": "Agency Founder - LinkedIn", "url": "https://linkedin.com/in/founder", "snippet": "Founder at AgencyCo"} ]},
            created_by="Browser"
        )
    
    import requests
    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json={"q": objective, "num": 10},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        return Artifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            artifact_type="search-results",
            version="1.0.0",
            title="Search Results",
            content={"objective": objective, "results": data.get("organic", [])},
            created_by="Browser"
        )
    except Exception as e:
        logger.error(f"Browser error: {e}")
        return Artifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            artifact_type="search-results",
            version="1.0.0",
            title="Search Results (Error)",
            content={"objective": objective, "error": str(e)},
            created_by="Browser"
        )


# ============================================================================
# Provider Executor Mapping
# ============================================================================

PROVIDER_EXECUTORS: Dict[ProviderName, Callable] = {
    ProviderName.PERPLEXITY: _execute_perplexity,
    ProviderName.GPT_4O: _execute_gpt4o,
    ProviderName.CLAUDE_35_SONNET: _execute_claude,
    ProviderName.GROQ_LLAMA_31_70B: _execute_groq,
    ProviderName.FIGMA: _execute_figma,
    ProviderName.BROWSER: _execute_browser,
}


# ============================================================================
# Capability Router
# ============================================================================

from runtime.provider_router_v2 import (
    select_provider,
    execute_with_fallback,
    get_providers_for_capability,
    is_healthy,
    track_provider_cost,
    PROVIDER_REGISTRY
)
from runtime.runtime_contracts import CapabilityName, ProviderName, RuntimeContext, CapabilityRequest, CapabilityResult
import logging

logger = logging.getLogger(__name__)


# Register executors with provider registry
for provider_name, executor in PROVIDER_EXECUTORS.items():
    if provider_name in PROVIDER_REGISTRY:
        PROVIDER_REGISTRY[provider_name].executor = executor


class CapabilityRouter:
    """Routes capability requests to optimal providers."""
    
    def __init__(self):
        self.routing_history: List[Dict] = []
    
    def request(self, request: CapabilityRequest) -> CapabilityResult:
        """Route capability request to optimal provider."""
        start_time = time.time()
        
        try:
            # Execute with automatic fallback
            result = execute_with_fallback(
                capability=request.capability,
                objective=request.objective,
                context=request.context
            )
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            # Track cost if tokens available
            tokens_used = 0
            if isinstance(result, Artifact) and result.metadata.get("tokens_used"):
                tokens_used = result.metadata["tokens_used"]
                track_provider_cost(request.capability, tokens_used // 2, tokens_used // 2)
            
            # Determine provider from result
            provider = ProviderName.GPT_4O  # Default
            if isinstance(result, Artifact) and result.created_by:
                try:
                    provider = ProviderName(result.created_by)
                except ValueError:
                    pass
            
            capability_result = CapabilityResult(
                capability=request.capability,
                provider=provider,
                status="completed",
                artifacts=[result] if isinstance(result, Artifact) else [result],
                routing_metadata={
                    "latency_ms": latency_ms,
                    "tokens_used": tokens_used,
                    "fallback_used": False
                },
                latency_ms=latency_ms
            )
            
            # Record routing history
            self.routing_history.append({
                "timestamp": time.time(),
                "capability": request.capability.value,
                "provider": provider.value,
                "latency_ms": latency_ms,
                "status": "completed"
            })
            
            return capability_result
            
        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            logger.error(f"Capability {request.capability} failed: {e}")
            
            error_artifact = Artifact(
                artifact_id=f"art_{uuid.uuid4().hex[:8]}",
                artifact_type="error",
                version="1.0.0",
                title=f"{request.capability.value} Error",
                content={"objective": request.objective, "error": str(e)},
                created_by="CapabilityRouter"
            )
            
            return CapabilityResult(
                capability=request.capability,
                provider=ProviderName.GPT_4O,
                status="failed",
                artifacts=[error_artifact],
                errors=[str(e)],
                latency_ms=latency_ms
            )
    
    def get_available_capabilities(self) -> List[CapabilityName]:
        """List all registered capabilities."""
        return list(CapabilityName)
    
    def register_provider(
        self,
        name: ProviderName,
        executor: Callable,
        capabilities: List[CapabilityName],
        metadata: Dict[str, Any] = None
    ):
        """Register a custom provider."""
        PROVIDER_EXECUTORS[name] = executor
        logger.info(f"Registered custom provider: {name.value}")


# ============================================================================
# Convenience Functions
# ============================================================================

_default_router = None

def get_capability_router() -> CapabilityRouter:
    """Get singleton capability router."""
    global _default_router
    if _default_router is None:
        _default_router = CapabilityRouter()
    return _default_router


def request_capability(
    capability: CapabilityName,
    objective: str,
    context: Optional[RuntimeContext] = None
) -> CapabilityResult:
    """Convenience function for capability requests."""
    router = get_capability_router()
    request = CapabilityRequest(capability=capability, objective=objective, context=context)
    return router.request(request)