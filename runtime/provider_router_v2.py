"""
Provider Router v2

Multi-factor provider selection with health awareness, circuit breakers, and cost/latency optimization.
"""

import os
import time
import asyncio
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from runtime.runtime_contracts import CapabilityName, ProviderName, RuntimeContext
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# Provider Registry
# ============================================================================

@dataclass
class ProviderConfig:
    """Configuration for a provider."""
    capabilities: List[CapabilityName]
    model: str
    endpoint: str
    auth_env: str
    cost_per_1k_tokens: Dict[str, float]
    max_context: int
    avg_latency_ms: int
    reliability_score: float
    rate_limit_rpm: int
    health_endpoint: str
    fallback_priority: int
    executor: Optional[Callable] = None


PROVIDER_REGISTRY: Dict[ProviderName, ProviderConfig] = {
    ProviderName.PERPLEXITY: ProviderConfig(
        capabilities=[CapabilityName.RESEARCH],
        model="sonar-pro",
        endpoint="https://api.perplexity.ai/chat/completions",
        auth_env="PERPLEXITY_API_KEY",
        cost_per_1k_tokens={"input": 0.001, "output": 0.001},
        max_context=128000,
        avg_latency_ms=3000,
        reliability_score=0.95,
        rate_limit_rpm=60,
        health_endpoint="https://api.perplexity.ai/health",
        fallback_priority=1
    ),
    ProviderName.GPT_4O: ProviderConfig(
        capabilities=[CapabilityName.WRITING, CapabilityName.ANALYSIS, CapabilityName.CODING],
        model="gpt-4o",
        endpoint="https://api.openai.com/v1/chat/completions",
        auth_env="OPENAI_API_KEY",
        cost_per_1k_tokens={"input": 0.005, "output": 0.015},
        max_context=128000,
        avg_latency_ms=2000,
        reliability_score=0.98,
        rate_limit_rpm=500,
        health_endpoint="https://api.openai.com/health",
        fallback_priority=1
    ),
    ProviderName.CLAUDE_35_SONNET: ProviderConfig(
        capabilities=[CapabilityName.WRITING, CapabilityName.ANALYSIS, CapabilityName.CODING],
        model="claude-3-5-sonnet-20241022",
        endpoint="https://api.anthropic.com/v1/messages",
        auth_env="ANTHROPIC_API_KEY",
        cost_per_1k_tokens={"input": 0.003, "output": 0.015},
        max_context=200000,
        avg_latency_ms=2500,
        reliability_score=0.97,
        rate_limit_rpm=100,
        health_endpoint="https://api.anthropic.com/health",
        fallback_priority=2
    ),
    ProviderName.GROQ_LLAMA_31_70B: ProviderConfig(
        capabilities=[CapabilityName.WRITING, CapabilityName.ANALYSIS, CapabilityName.CODING],
        model="llama-3.1-70b-versatile",
        endpoint="https://api.groq.com/openai/v1/chat/completions",
        auth_env="GROQ_API_KEY",
        cost_per_1k_tokens={"input": 0.00059, "output": 0.00079},
        max_context=131072,
        avg_latency_ms=800,
        reliability_score=0.93,
        rate_limit_rpm=30,
        health_endpoint="https://api.groq.com/health",
        fallback_priority=3
    ),
    ProviderName.NVIDIA_NIM: ProviderConfig(
        capabilities=[CapabilityName.WRITING, CapabilityName.ANALYSIS, CapabilityName.CODING],
        model="nvidia/nemotron-3-ultra",
        endpoint="https://integrate.api.nvidia.com/v1/chat/completions",
        auth_env="NVIDIA_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=16384,
        avg_latency_ms=1500,
        reliability_score=0.90,
        rate_limit_rpm=60,
        health_endpoint="https://integrate.api.nvidia.com/health",
        fallback_priority=4
    ),
    ProviderName.FIGMA: ProviderConfig(
        capabilities=[CapabilityName.DESIGN],
        model="figma-api",
        endpoint="https://api.figma.com/v1",
        auth_env="FIGMA_TOKEN",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=500,
        reliability_score=0.99,
        rate_limit_rpm=300,
        health_endpoint="https://api.figma.com/v1/me",
        fallback_priority=1
    ),
    ProviderName.PREMIERE: ProviderConfig(
        capabilities=[CapabilityName.VIDEO_EDITING],
        model="premiere-local",
        endpoint="local",
        auth_env="none",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=30000,
        reliability_score=0.95,
        rate_limit_rpm=1,
        health_endpoint="local",
        fallback_priority=1
    ),
    ProviderName.HEYGEN: ProviderConfig(
        capabilities=[CapabilityName.VIDEO_EDITING],
        model="heygen-avatar",
        endpoint="https://api.heygen.com/v2",
        auth_env="HEYGEN_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=15000,
        reliability_score=0.90,
        rate_limit_rpm=10,
        health_endpoint="https://api.heygen.com/health",
        fallback_priority=2
    ),
    ProviderName.VEED: ProviderConfig(
        capabilities=[CapabilityName.VIDEO_EDITING],
        model="veed-api",
        endpoint="https://api.veed.io/v1",
        auth_env="VEED_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=10000,
        reliability_score=0.88,
        rate_limit_rpm=20,
        health_endpoint="https://api.veed.io/health",
        fallback_priority=3
    ),
    ProviderName.MAKE: ProviderConfig(
        capabilities=[CapabilityName.AUTOMATION],
        model="make-api",
        endpoint="https://api.make.com/v2",
        auth_env="MAKE_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=1000,
        reliability_score=0.96,
        rate_limit_rpm=100,
        health_endpoint="https://api.make.com/health",
        fallback_priority=1
    ),
    ProviderName.N8N: ProviderConfig(
        capabilities=[CapabilityName.AUTOMATION],
        model="n8n-api",
        endpoint="https://api.n8n.io/v1",
        auth_env="N8N_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=800,
        reliability_score=0.94,
        rate_limit_rpm=50,
        health_endpoint="https://api.n8n.io/health",
        fallback_priority=2
    ),
    ProviderName.ZAPIER: ProviderConfig(
        capabilities=[CapabilityName.AUTOMATION],
        model="zapier-api",
        endpoint="https://api.zapier.com/v1",
        auth_env="ZAPIER_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=2000,
        reliability_score=0.95,
        rate_limit_rpm=100,
        health_endpoint="https://api.zapier.com/health",
        fallback_priority=3
    ),
    ProviderName.HUBSPOT: ProviderConfig(
        capabilities=[CapabilityName.CRM],
        model="hubspot-api",
        endpoint="https://api.hubapi.com",
        auth_env="HUBSPOT_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=300,
        reliability_score=0.98,
        rate_limit_rpm=100,
        health_endpoint="https://api.hubapi.com/health",
        fallback_priority=1
    ),
    ProviderName.PIPEDRIVE: ProviderConfig(
        capabilities=[CapabilityName.CRM],
        model="pipedrive-api",
        endpoint="https://api.pipedrive.com/v1",
        auth_env="PIPEDRIVE_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=400,
        reliability_score=0.96,
        rate_limit_rpm=100,
        health_endpoint="https://api.pipedrive.com/health",
        fallback_priority=2
    ),
    ProviderName.AIRTABLE: ProviderConfig(
        capabilities=[CapabilityName.CRM],
        model="airtable-api",
        endpoint="https://api.airtable.com/v0",
        auth_env="AIRTABLE_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=500,
        reliability_score=0.95,
        rate_limit_rpm=50,
        health_endpoint="https://api.airtable.com/health",
        fallback_priority=3
    ),
    ProviderName.GMAIL: ProviderConfig(
        capabilities=[CapabilityName.EMAIL],
        model="gmail-api",
        endpoint="https://gmail.googleapis.com/gmail/v1",
        auth_env="GOOGLE_OAUTH_TOKEN",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=200,
        reliability_score=0.99,
        rate_limit_rpm=250,
        health_endpoint="https://gmail.googleapis.com/health",
        fallback_priority=1
    ),
    ProviderName.SENDGRID: ProviderConfig(
        capabilities=[CapabilityName.EMAIL],
        model="sendgrid-api",
        endpoint="https://api.sendgrid.com/v3",
        auth_env="SENDGRID_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=300,
        reliability_score=0.97,
        rate_limit_rpm=600,
        health_endpoint="https://api.sendgrid.com/health",
        fallback_priority=2
    ),
    ProviderName.MAILGUN: ProviderConfig(
        capabilities=[CapabilityName.EMAIL],
        model="mailgun-api",
        endpoint="https://api.mailgun.net/v3",
        auth_env="MAILGUN_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=400,
        reliability_score=0.95,
        rate_limit_rpm=300,
        health_endpoint="https://api.mailgun.net/health",
        fallback_priority=3
    ),
    ProviderName.BROWSER: ProviderConfig(
        capabilities=[CapabilityName.SEARCH, CapabilityName.RESEARCH],
        model="serper-api",
        endpoint="https://google.serper.dev/search",
        auth_env="SERPER_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=800,
        reliability_score=0.92,
        rate_limit_rpm=100,
        health_endpoint="https://google.serper.dev/health",
        fallback_priority=2
    ),
    ProviderName.EXA: ProviderConfig(
        capabilities=[CapabilityName.SEARCH, CapabilityName.RESEARCH],
        model="exa-api",
        endpoint="https://api.exa.ai/search",
        auth_env="EXA_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=1500,
        reliability_score=0.90,
        rate_limit_rpm=50,
        health_endpoint="https://api.exa.ai/health",
        fallback_priority=3
    ),
    ProviderName.GOOGLE_CALENDAR: ProviderConfig(
        capabilities=[CapabilityName.CALENDAR],
        model="google-calendar-api",
        endpoint="https://www.googleapis.com/calendar/v3",
        auth_env="GOOGLE_OAUTH_TOKEN",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=300,
        reliability_score=0.98,
        rate_limit_rpm=500,
        health_endpoint="https://www.googleapis.com/health",
        fallback_priority=1
    ),
    ProviderName.CALENDLY: ProviderConfig(
        capabilities=[CapabilityName.CALENDAR],
        model="calendly-api",
        endpoint="https://api.calendly.com/v1",
        auth_env="CALENDLY_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=400,
        reliability_score=0.96,
        rate_limit_rpm=100,
        health_endpoint="https://api.calendly.com/health",
        fallback_priority=2
    ),
    ProviderName.GOOGLE_DOCS: ProviderConfig(
        capabilities=[CapabilityName.DOCUMENT],
        model="google-docs-api",
        endpoint="https://docs.googleapis.com/v1",
        auth_env="GOOGLE_OAUTH_TOKEN",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=500,
        reliability_score=0.97,
        rate_limit_rpm=100,
        health_endpoint="https://docs.googleapis.com/health",
        fallback_priority=1
    ),
    ProviderName.NOTION: ProviderConfig(
        capabilities=[CapabilityName.DOCUMENT],
        model="notion-api",
        endpoint="https://api.notion.com/v1",
        auth_env="NOTION_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=600,
        reliability_score=0.95,
        rate_limit_rpm=100,
        health_endpoint="https://api.notion.com/health",
        fallback_priority=2
    ),
    ProviderName.PANDOC: ProviderConfig(
        capabilities=[CapabilityName.DOCUMENT],
        model="pandoc-local",
        endpoint="local",
        auth_env="none",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=1000,
        reliability_score=0.99,
        rate_limit_rpm=10,
        health_endpoint="local",
        fallback_priority=3
    ),
    ProviderName.GOOGLE_DRIVE: ProviderConfig(
        capabilities=[CapabilityName.STORAGE],
        model="google-drive-api",
        endpoint="https://www.googleapis.com/drive/v3",
        auth_env="GOOGLE_OAUTH_TOKEN",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=400,
        reliability_score=0.99,
        rate_limit_rpm=1000,
        health_endpoint="https://www.googleapis.com/health",
        fallback_priority=1
    ),
    ProviderName.DROPBOX: ProviderConfig(
        capabilities=[CapabilityName.STORAGE],
        model="dropbox-api",
        endpoint="https://api.dropboxapi.com/2",
        auth_env="DROPBOX_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=500,
        reliability_score=0.97,
        rate_limit_rpm=100,
        health_endpoint="https://api.dropboxapi.com/health",
        fallback_priority=2
    ),
    ProviderName.CLOUDINARY: ProviderConfig(
        capabilities=[CapabilityName.STORAGE],
        model="cloudinary-api",
        endpoint="https://api.cloudinary.com/v1_1",
        auth_env="CLOUDINARY_API_KEY",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=300,
        reliability_score=0.98,
        rate_limit_rpm=500,
        health_endpoint="https://api.cloudinary.com/health",
        fallback_priority=2
    ),
    ProviderName.S3: ProviderConfig(
        capabilities=[CapabilityName.STORAGE],
        model="aws-s3-api",
        endpoint="https://s3.amazonaws.com",
        auth_env="AWS_ACCESS_KEY_ID",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=200,
        reliability_score=0.999,
        rate_limit_rpm=3500,
        health_endpoint="https://s3.amazonaws.com/health",
        fallback_priority=3
    ),
    ProviderName.PLAYWRIGHT: ProviderConfig(
        capabilities=[CapabilityName.TESTING],
        model="playwright-local",
        endpoint="local",
        auth_env="none",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=30000,
        reliability_score=0.95,
        rate_limit_rpm=5,
        health_endpoint="local",
        fallback_priority=1
    ),
    ProviderName.PYTEST: ProviderConfig(
        capabilities=[CapabilityName.TESTING],
        model="pytest-local",
        endpoint="local",
        auth_env="none",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=10000,
        reliability_score=0.98,
        rate_limit_rpm=10,
        health_endpoint="local",
        fallback_priority=2
    ),
    ProviderName.VITEST: ProviderConfig(
        capabilities=[CapabilityName.TESTING],
        model="vitest-local",
        endpoint="local",
        auth_env="none",
        cost_per_1k_tokens={"input": 0.0, "output": 0.0},
        max_context=0,
        avg_latency_ms=5000,
        reliability_score=0.96,
        rate_limit_rpm=20,
        health_endpoint="local",
        fallback_priority=3
    ),
}


# ============================================================================
# Routing Rules
# ============================================================================

ROUTING_RULES: Dict[CapabilityName, Dict[str, ProviderName]] = {
    CapabilityName.RESEARCH: {
        "deep_research": ProviderName.PERPLEXITY,
        "quick_search": ProviderName.BROWSER,
        "academic": ProviderName.EXA
    },
    CapabilityName.WRITING: {
        "outreach": ProviderName.GPT_4O,
        "proposal": ProviderName.GPT_4O,
        "technical_docs": ProviderName.CLAUDE_35_SONNET,
        "code": ProviderName.GROQ_LLAMA_31_70B
    },
    CapabilityName.ANALYSIS: {
        "financial": ProviderName.CLAUDE_35_SONNET,
        "statistical": ProviderName.GPT_4O,
        "code_analysis": ProviderName.GROQ_LLAMA_31_70B
    },
    CapabilityName.CODING: {
        "fast": ProviderName.GROQ_LLAMA_31_70B,
        "complex": ProviderName.CLAUDE_35_SONNET,
        "review": ProviderName.GPT_4O
    },
    CapabilityName.DESIGN: {
        "ui": ProviderName.FIGMA,
        "brand": ProviderName.FIGMA
    },
    CapabilityName.VIDEO_EDITING: {
        "professional": ProviderName.PREMIERE,
        "avatar": ProviderName.HEYGEN,
        "quick": ProviderName.VEED
    },
    CapabilityName.AUTOMATION: {
        "workflow": ProviderName.MAKE,
        "complex": ProviderName.N8N,
        "simple": ProviderName.ZAPIER
    },
    CapabilityName.CRM: {
        "enterprise": ProviderName.HUBSPOT,
        "sales": ProviderName.PIPEDRIVE,
        "custom": ProviderName.AIRTABLE
    },
    CapabilityName.EMAIL: {
        "transactional": ProviderName.GMAIL,
        "marketing": ProviderName.SENDGRID,
        "developer": ProviderName.MAILGUN
    },
    CapabilityName.SEARCH: {
        "quick": ProviderName.BROWSER,
        "deep": ProviderName.PERPLEXITY,
        "academic": ProviderName.EXA
    },
    CapabilityName.CALENDAR: {
        "scheduling": ProviderName.GOOGLE_CALENDAR,
        "booking": ProviderName.CALENDLY
    },
    CapabilityName.DOCUMENT: {
        "collaborative": ProviderName.GOOGLE_DOCS,
        "knowledge": ProviderName.NOTION,
        "conversion": ProviderName.PANDOC
    }
}


# ============================================================================
# Health & Circuit Breaker
# ============================================================================

@dataclass
class HealthStatus:
    provider: ProviderName
    status: str  # healthy, degraded, unhealthy
    latency_ms: int = 0
    error: Optional[str] = None
    last_check: float = field(default_factory=time.time)


class CircuitBreaker:
    def __init__(self, provider: ProviderName, failure_threshold: int = 5, timeout: int = 60):
        self.provider = provider
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "closed"  # closed, open, half-open
    
    def call(self, executor: Callable, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
                logger.info(f"Circuit breaker for {self.provider}: half-open")
            else:
                raise CircuitOpenError(f"Circuit open for {self.provider}")
        
        try:
            result = executor(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
    
    def on_success(self):
        self.failure_count = 0
        self.state = "closed"
    
    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
            logger.warning(f"Circuit breaker OPEN for {self.provider}")


class CircuitOpenError(Exception):
    pass


# Health check cache
_health_cache: Dict[ProviderName, HealthStatus] = {}
_circuit_breakers: Dict[ProviderName, CircuitBreaker] = {}


def get_circuit_breaker(provider: ProviderName) -> CircuitBreaker:
    if provider not in _circuit_breakers:
        _circuit_breakers[provider] = CircuitBreaker(provider)
    return _circuit_breakers[provider]


async def check_provider_health(provider: ProviderName) -> HealthStatus:
    """Check provider health with timeout."""
    config = PROVIDER_REGISTRY.get(provider)
    if not config:
        return HealthStatus(provider, "unhealthy", error="Provider not registered")
    
    endpoint = config.health_endpoint
    
    if endpoint == "local":
        return HealthStatus(provider, "healthy", latency_ms=1)
    
    try:
        import aiohttp
        start = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                latency = int((time.time() - start) * 1000)
                if resp.status == 200:
                    return HealthStatus(provider, "healthy", latency_ms=latency)
                else:
                    return HealthStatus(provider, "degraded", latency_ms=latency)
    except asyncio.TimeoutError:
        return HealthStatus(provider, "unhealthy", error="timeout")
    except Exception as e:
        return HealthStatus(provider, "unhealthy", error=str(e))


async def health_check_loop(interval: int = 30):
    """Background health checks."""
    while True:
        for provider in ProviderName:
            if provider in PROVIDER_REGISTRY:
                status = await check_provider_health(provider)
                _health_cache[provider] = status
        await asyncio.sleep(interval)


def is_healthy(provider: ProviderName) -> bool:
    """Quick health check from cache."""
    status = _health_cache.get(provider)
    if not status:
        return True  # Unknown = assume healthy
    return status.status == "healthy"


def get_provider_health(provider: ProviderName) -> Dict[str, Any]:
    """Get detailed health info."""
    status = _health_cache.get(provider)
    breaker = _circuit_breakers.get(provider)
    return {
        "provider": provider.value,
        "status": status.status if status else "unknown",
        "latency_ms": status.latency_ms if status else 0,
        "error": status.error if status else None,
        "last_check": status.last_check if status else None,
        "circuit_state": breaker.state if breaker else "closed",
        "failure_count": breaker.failure_count if breaker else 0
    }


# ============================================================================
# Cost Tracking
# ============================================================================

def track_provider_cost(provider: ProviderName, tokens_in: int, tokens_out: int) -> Dict[str, Any]:
    """Track cost per provider call."""
    config = PROVIDER_REGISTRY.get(provider)
    if not config:
        return {"cost_usd": 0, "error": "Provider not found"}
    
    cost = (tokens_in * config.cost_per_1k_tokens["input"] + 
            tokens_out * config.cost_per_1k_tokens["output"]) / 1000
    
    record = {
        "provider": provider.value,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd": cost,
        "timestamp": time.time()
    }
    
    # Append to cost ledger (in production, write to persistent store)
    return record


# ============================================================================
# Provider Selection
# ============================================================================

@dataclass
class ProviderSelection:
    provider: ProviderName
    reason: str
    score: float = 0.0


def get_providers_for_capability(capability: CapabilityName) -> List[ProviderName]:
    """Get all providers that support a capability."""
    providers = []
    for provider, config in PROVIDER_REGISTRY.items():
        if capability in config.capabilities:
            providers.append(provider)
    return providers


def rule_matches(rule: str, objective: str, context: Optional[RuntimeContext]) -> bool:
    """Check if routing rule matches objective."""
    objective_lower = objective.lower()
    
    if rule == "deep_research":
        return any(kw in objective_lower for kw in ["deep", "comprehensive", "detailed", "research", "icp matching"])
    elif rule == "quick_search":
        return any(kw in objective_lower for kw in ["quick", "search", "find", "contact", "email"])
    elif rule == "academic":
        return any(kw in objective_lower for kw in ["academic", "paper", "study", "citation"])
    elif rule == "outreach":
        return any(kw in objective_lower for kw in ["outreach", "dm", "message", "linkedin", "twitter"])
    elif rule == "proposal":
        return any(kw in objective_lower for kw in ["proposal", "quote", "pricing", "deal"])
    elif rule == "technical_docs":
        return any(kw in objective_lower for kw in ["technical", "documentation", "api", "spec"])
    elif rule == "code":
        return any(kw in objective_lower for kw in ["code", "function", "class", "implement", "refactor"])
    elif rule == "financial":
        return any(kw in objective_lower for kw in ["financial", "margin", "pricing", "profit", "revenue"])
    elif rule == "statistical":
        return any(kw in objective_lower for kw in ["statistical", "analysis", "trend", "forecast"])
    elif rule == "code_analysis":
        return any(kw in objective_lower for kw in ["code review", "analyze code", "bug", "performance"])
    elif rule == "fast":
        return any(kw in objective_lower for kw in ["quick", "fast", "simple", "small"])
    elif rule == "complex":
        return any(kw in objective_lower for kw in ["complex", "architecture", "system", "design"])
    elif rule == "review":
        return any(kw in objective_lower for kw in ["review", "pr", "pull request", "audit"])
    elif rule == "ui":
        return any(kw in objective_lower for kw in ["ui", "interface", "dashboard", "component"])
    elif rule == "brand":
        return any(kw in objective_lower for kw in ["brand", "logo", "identity", "guideline"])
    elif rule == "professional":
        return any(kw in objective_lower for kw in ["professional", "production", "high quality"])
    elif rule == "avatar":
        return any(kw in objective_lower for kw in ["avatar", "talking head", "presenter"])
    elif rule == "quick":
        return any(kw in objective_lower for kw in ["quick", "fast", "social", "short"])
    elif rule == "workflow":
        return any(kw in objective_lower for kw in ["workflow", "automation", "scenario", "make.com"])
    elif rule == "enterprise":
        return any(kw in objective_lower for kw in ["enterprise", "hubspot", "crm"])
    elif rule == "sales":
        return any(kw in objective_lower for kw in ["sales", "pipedrive", "deal"])
    elif rule == "custom":
        return any(kw in objective_lower for kw in ["airtable", "custom", "flexible"])
    elif rule == "transactional":
        return any(kw in objective_lower for kw in ["transactional", "receipt", "confirmation"])
    elif rule == "marketing":
        return any(kw in objective_lower for kw in ["marketing", "campaign", "newsletter", "bulk"])
    elif rule == "developer":
        return any(kw in objective_lower for kw in ["developer", "api", "programmatic"])
    elif rule == "quick":
        return any(kw in objective_lower for kw in ["quick", "search", "find"])
    elif rule == "deep":
        return any(kw in objective_lower for kw in ["deep", "research", "comprehensive"])
    elif rule == "scheduling":
        return any(kw in objective_lower for kw in ["schedule", "calendar", "meeting"])
    elif rule == "booking":
        return any(kw in objective_lower for kw in ["book", "calendly", "appointment"])
    elif rule == "collaborative":
        return any(kw in objective_lower for kw in ["collaborative", "google docs", "shared"])
    elif rule == "knowledge":
        return any(kw in objective_lower for kw in ["notion", "wiki", "knowledge", "documentation"])
    elif rule == "conversion":
        return any(kw in objective_lower for kw in ["convert", "pdf", "pandoc", "format"])
    
    return False


def calculate_score(provider: ProviderName, context: Optional[RuntimeContext] = None) -> float:
    """Weighted scoring for provider selection."""
    config = PROVIDER_REGISTRY[provider]
    
    # Latency score (lower is better)
    latency_score = 1.0 - min(config.avg_latency_ms / 30000, 1.0)
    
    # Cost score (lower is better) 
    cost_score = 1.0 - min(config.cost_per_1k_tokens.get("output", 0) / 0.02, 1.0)
    
    # Reliability score
    reliability_score = config.reliability_score
    
    # Context length score
    context_score = 1.0 if config.max_context >= (context.max_context_needed if context else 0) else 0.5
    
    # Fallback priority (lower is better)
    fallback_score = 1.0 - (config.fallback_priority - 1) * 0.1
    
    weights = {
        "latency": 0.25,
        "cost": 0.20,
        "reliability": 0.25,
        "context": 0.15,
        "fallback": 0.15
    }
    
    return (
        weights["latency"] * latency_score +
        weights["cost"] * cost_score +
        weights["reliability"] * reliability_score +
        weights["context"] * context_score +
        weights["fallback"] * fallback_score
    )


def select_provider(capability: CapabilityName, objective: str, context: Optional[RuntimeContext] = None) -> ProviderName:
    """
    Select optimal provider for capability based on:
    1. Capability match
    2. Routing rules (explicit)
    3. Health status
    4. Latency budget
    5. Cost budget
    6. Context length requirement
    7. Reliability score
    8. Fallback priority
    """
    
    candidates = get_providers_for_capability(capability)
    if not candidates:
        raise ValueError(f"No providers for capability: {capability}")
    
    # Filter unhealthy
    healthy = [p for p in candidates if is_healthy(p)]
    if not healthy:
        # If all unhealthy, use all candidates with warning
        logger.warning(f"All providers unhealthy for {capability}, using all candidates")
        healthy = candidates
    
    # Check routing rules
    rules = ROUTING_RULES.get(capability, {})
    for rule, provider in rules.items():
        if provider in healthy and rule_matches(rule, objective, context):
            return provider
    
    # Score remaining candidates
    scored = [(calculate_score(p, context), p) for p in healthy]
    scored.sort(reverse=True, key=lambda x: x[0])
    
    return scored[0][1]


def execute_with_fallback(capability: CapabilityName, objective: str, context: Optional[RuntimeContext] = None) -> Any:
    """Execute capability with automatic fallback chain."""
    providers = get_providers_for_capability(capability)
    last_error = None
    
    for provider in providers:
        if not is_healthy(provider):
            continue
            
        breaker = get_circuit_breaker(provider)
        config = PROVIDER_REGISTRY[provider]
        
        try:
            if config.executor:
                result = breaker.call(config.executor, objective)
                return result
            else:
                # Mock execution for providers without executor
                return {"provider": provider.value, "result": f"Mock result for: {objective}"}
        except CircuitOpenError:
            logger.warning(f"Circuit open for {provider}, trying next")
            continue
        except Exception as e:
            last_error = e
            logger.warning(f"Provider {provider} failed: {e}")
            continue
    
    raise Exception(f"All providers failed for {capability}: {last_error}")


def get_fallback_chain(capability: CapabilityName) -> List[ProviderName]:
    """Get fallback chain for capability."""
    providers = get_providers_for_capability(capability)
    # Sort by fallback priority
    return sorted(providers, key=lambda p: PROVIDER_REGISTRY[p].fallback_priority)