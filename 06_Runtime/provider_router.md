# Provider Router Specification

Provider selection, fallback, cost/latency optimization, and health management.

---

## Provider Abstraction Layer

Employees never request providers directly. They request capabilities. The Provider Router selects the optimal provider.

---

## Provider Registry

```python
PROVIDER_REGISTRY = {
    "Perplexity": {
        "capabilities": ["research"],
        "model": "sonar-pro",
        "endpoint": "https://api.perplexity.ai/chat/completions",
        "auth": "PERPLEXITY_API_KEY",
        "cost_per_1k_tokens": {"input": 0.001, "output": 0.001},
        "max_context": 128000,
        "avg_latency_ms": 3000,
        "reliability_score": 0.95,
        "rate_limit_rpm": 60,
        "health_endpoint": "https://api.perplexity.ai/health",
        "fallback_priority": 1
    },
    "GPT-4o": {
        "capabilities": ["writing", "analysis", "coding"],
        "model": "gpt-4o",
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "auth": "OPENAI_API_KEY",
        "cost_per_1k_tokens": {"input": 0.005, "output": 0.015},
        "max_context": 128000,
        "avg_latency_ms": 2000,
        "reliability_score": 0.98,
        "rate_limit_rpm": 500,
        "health_endpoint": "https://api.openai.com/health",
        "fallback_priority": 1
    },
    "Claude-3.5-Sonnet": {
        "capabilities": ["writing", "analysis", "coding"],
        "model": "claude-3-5-sonnet-20241022",
        "endpoint": "https://api.anthropic.com/v1/messages",
        "auth": "ANTHROPIC_API_KEY",
        "cost_per_1k_tokens": {"input": 0.003, "output": 0.015},
        "max_context": 200000,
        "avg_latency_ms": 2500,
        "reliability_score": 0.97,
        "rate_limit_rpm": 100,
        "health_endpoint": "https://api.anthropic.com/health",
        "fallback_priority": 2
    },
    "Groq-Llama-3.1-70B": {
        "capabilities": ["writing", "analysis", "coding"],
        "model": "llama-3.1-70b-versatile",
        "endpoint": "https://api.groq.com/openai/v1/chat/completions",
        "auth": "GROQ_API_KEY",
        "cost_per_1k_tokens": {"input": 0.00059, "output": 0.00079},
        "max_context": 131072,
        "avg_latency_ms": 800,
        "reliability_score": 0.93,
        "rate_limit_rpm": 30,
        "health_endpoint": "https://api.groq.com/health",
        "fallback_priority": 3
    },
    "NVIDIA-NIM": {
        "capabilities": ["writing", "analysis", "coding"],
        "model": "nvidia/nemotron-3-ultra",
        "endpoint": "https://integrate.api.nvidia.com/v1/chat/completions",
        "auth": "NVIDIA_API_KEY",
        "cost_per_1k_tokens": {"input": 0.000, "output": 0.000},
        "max_context": 16384,
        "avg_latency_ms": 1500,
        "reliability_score": 0.90,
        "rate_limit_rpm": 60,
        "health_endpoint": "https://integrate.api.nvidia.com/health",
        "fallback_priority": 4
    },
    "Figma": {
        "capabilities": ["design"],
        "model": "figma-api",
        "endpoint": "https://api.figma.com/v1",
        "auth": "FIGMA_TOKEN",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 500,
        "reliability_score": 0.99,
        "rate_limit_rpm": 300,
        "health_endpoint": "https://api.figma.com/v1/me",
        "fallback_priority": 1
    },
    "Premiere": {
        "capabilities": ["video_editing"],
        "model": "premiere-local",
        "endpoint": "local",
        "auth": "none",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 30000,
        "reliability_score": 0.95,
        "rate_limit_rpm": 1,
        "health_endpoint": "local",
        "fallback_priority": 1
    },
    "HeyGen": {
        "capabilities": ["video_editing"],
        "model": "heygen-avatar",
        "endpoint": "https://api.heygen.com/v2",
        "auth": "HEYGEN_API_KEY",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 15000,
        "reliability_score": 0.90,
        "rate_limit_rpm": 10,
        "health_endpoint": "https://api.heygen.com/health",
        "fallback_priority": 2
    },
    "VEED": {
        "capabilities": ["video_editing"],
        "model": "veed-api",
        "endpoint": "https://api.veed.io/v1",
        "auth": "VEED_API_KEY",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 10000,
        "reliability_score": 0.88,
        "rate_limit_rpm": 20,
        "health_endpoint": "https://api.veed.io/health",
        "fallback_priority": 3
    },
    "Make": {
        "capabilities": ["automation"],
        "model": "make-api",
        "endpoint": "https://api.make.com/v2",
        "auth": "MAKE_API_KEY",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 1000,
        "reliability_score": 0.96,
        "rate_limit_rpm": 100,
        "health_endpoint": "https://api.make.com/health",
        "fallback_priority": 1
    },
    "n8n": {
        "capabilities": ["automation"],
        "model": "n8n-api",
        "endpoint": "https://api.n8n.io/v1",
        "auth": "N8N_API_KEY",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 800,
        "reliability_score": 0.94,
        "rate_limit_rpm": 50,
        "health_endpoint": "https://api.n8n.io/health",
        "fallback_priority": 2
    },
    "Zapier": {
        "capabilities": ["automation"],
        "model": "zapier-api",
        "endpoint": "https://api.zapier.com/v1",
        "auth": "ZAPIER_API_KEY",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 2000,
        "reliability_score": 0.95,
        "rate_limit_rpm": 100,
        "health_endpoint": "https://api.zapier.com/health",
        "fallback_priority": 3
    },
    "HubSpot": {
        "capabilities": ["crm"],
        "model": "hubspot-api",
        "endpoint": "https://api.hubapi.com",
        "auth": "HUBSPOT_API_KEY",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 300,
        "reliability_score": 0.98,
        "rate_limit_rpm": 100,
        "health_endpoint": "https://api.hubapi.com/health",
        "fallback_priority": 1
    },
    "Pipedrive": {
        "capabilities": ["crm"],
        "model": "pipedrive-api",
        "endpoint": "https://api.pipedrive.com/v1",
        "auth": "PIPEDRIVE_API_KEY",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 400,
        "reliability_score": 0.96,
        "rate_limit_rpm": 100,
        "health_endpoint": "https://api.pipedrive.com/health",
        "fallback_priority": 2
    },
    "Airtable": {
        "capabilities": ["crm"],
        "model": "airtable-api",
        "endpoint": "https://api.airtable.com/v0",
        "auth": "AIRTABLE_API_KEY",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 500,
        "reliability_score": 0.95,
        "rate_limit_rpm": 50,
        "health_endpoint": "https://api.airtable.com/health",
        "fallback_priority": 3
    },
    "Gmail": {
        "capabilities": ["email"],
        "model": "gmail-api",
        "endpoint": "https://gmail.googleapis.com/gmail/v1",
        "auth": "GOOGLE_OAUTH_TOKEN",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 200,
        "reliability_score": 0.99,
        "rate_limit_rpm": 250,
        "health_endpoint": "https://gmail.googleapis.com/health",
        "fallback_priority": 1
    },
    "SendGrid": {
        "capabilities": ["email"],
        "model": "sendgrid-api",
        "endpoint": "https://api.sendgrid.com/v3",
        "auth": "SENDGRID_API_KEY",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 300,
        "reliability_score": 0.97,
        "rate_limit_rpm": 600,
        "health_endpoint": "https://api.sendgrid.com/health",
        "fallback_priority": 2
    },
    "Mailgun": {
        "capabilities": ["email"],
        "model": "mailgun-api",
        "endpoint": "https://api.mailgun.net/v3",
        "auth": "MAILGUN_API_KEY",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 400,
        "reliability_score": 0.95,
        "rate_limit_rpm": 300,
        "health_endpoint": "https://api.mailgun.net/health",
        "fallback_priority": 3
    },
    "Browser": {
        "capabilities": ["search", "research"],
        "model": "serper-api",
        "endpoint": "https://google.serper.dev/search",
        "auth": "SERPER_API_KEY",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 800,
        "reliability_score": 0.92,
        "rate_limit_rpm": 100,
        "health_endpoint": "https://google.serper.dev/health",
        "fallback_priority": 2
    },
    "Exa": {
        "capabilities": ["search", "research"],
        "model": "exa-api",
        "endpoint": "https://api.exa.ai/search",
        "auth": "EXA_API_KEY",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 1500,
        "reliability_score": 0.90,
        "rate_limit_rpm": 50,
        "health_endpoint": "https://api.exa.ai/health",
        "fallback_priority": 3
    },
    "Google-Calendar": {
        "capabilities": ["calendar"],
        "model": "google-calendar-api",
        "endpoint": "https://www.googleapis.com/calendar/v3",
        "auth": "GOOGLE_OAUTH_TOKEN",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 300,
        "reliability_score": 0.98,
        "rate_limit_rpm": 500,
        "health_endpoint": "https://www.googleapis.com/health",
        "fallback_priority": 1
    },
    "Calendly": {
        "capabilities": ["calendar"],
        "model": "calendly-api",
        "endpoint": "https://api.calendly.com/v1",
        "auth": "CALENDLY_API_KEY",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 400,
        "reliability_score": 0.96,
        "rate_limit_rpm": 100,
        "health_endpoint": "https://api.calendly.com/health",
        "fallback_priority": 2
    },
    "Google-Docs": {
        "capabilities": ["document"],
        "model": "google-docs-api",
        "endpoint": "https://docs.googleapis.com/v1",
        "auth": "GOOGLE_OAUTH_TOKEN",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 500,
        "reliability_score": 0.97,
        "rate_limit_rpm": 100,
        "health_endpoint": "https://docs.googleapis.com/health",
        "fallback_priority": 1
    },
    "Notion": {
        "capabilities": ["document"],
        "model": "notion-api",
        "endpoint": "https://api.notion.com/v1",
        "auth": "NOTION_API_KEY",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 600,
        "reliability_score": 0.95,
        "rate_limit_rpm": 100,
        "health_endpoint": "https://api.notion.com/health",
        "fallback_priority": 2
    },
    "Pandoc": {
        "capabilities": ["document"],
        "model": "pandoc-local",
        "endpoint": "local",
        "auth": "none",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 1000,
        "reliability_score": 0.99,
        "rate_limit_rpm": 10,
        "health_endpoint": "local",
        "fallback_priority": 3
    },
    "Google-Drive": {
        "capabilities": ["storage"],
        "model": "google-drive-api",
        "endpoint": "https://www.googleapis.com/drive/v3",
        "auth": "GOOGLE_OAUTH_TOKEN",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 400,
        "reliability_score": 0.99,
        "rate_limit_rpm": 1000,
        "health_endpoint": "https://www.googleapis.com/health",
        "fallback_priority": 1
    },
    "Dropbox": {
        "capabilities": ["storage"],
        "model": "dropbox-api",
        "endpoint": "https://api.dropboxapi.com/2",
        "auth": "DROPBOX_API_KEY",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 500,
        "reliability_score": 0.97,
        "rate_limit_rpm": 100,
        "health_endpoint": "https://api.dropboxapi.com/health",
        "fallback_priority": 2
    },
    "Cloudinary": {
        "capabilities": ["storage"],
        "model": "cloudinary-api",
        "endpoint": "https://api.cloudinary.com/v1_1",
        "auth": "CLOUDINARY_API_KEY",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 300,
        "reliability_score": 0.98,
        "rate_limit_rpm": 500,
        "health_endpoint": "https://api.cloudinary.com/health",
        "fallback_priority": 2
    },
    "S3": {
        "capabilities": ["storage"],
        "model": "aws-s3-api",
        "endpoint": "https://s3.amazonaws.com",
        "auth": "AWS_ACCESS_KEY_ID",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 200,
        "reliability_score": 0.999,
        "rate_limit_rpm": 3500,
        "health_endpoint": "https://s3.amazonaws.com/health",
        "fallback_priority": 3
    },
    "Playwright": {
        "capabilities": ["testing"],
        "model": "playwright-local",
        "endpoint": "local",
        "auth": "none",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 30000,
        "reliability_score": 0.95,
        "rate_limit_rpm": 5,
        "health_endpoint": "local",
        "fallback_priority": 1
    },
    "pytest": {
        "capabilities": ["testing"],
        "model": "pytest-local",
        "endpoint": "local",
        "auth": "none",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 10000,
        "reliability_score": 0.98,
        "rate_limit_rpm": 10,
        "health_endpoint": "local",
        "fallback_priority": 2
    },
    "Vitest": {
        "capabilities": ["testing"],
        "model": "vitest-local",
        "endpoint": "local",
        "auth": "none",
        "cost_per_1k_tokens": {"input": 0.0, "output": 0.0},
        "max_context": 0,
        "avg_latency_ms": 5000,
        "reliability_score": 0.96,
        "rate_limit_rpm": 20,
        "health_endpoint": "local",
        "fallback_priority": 3
    }
}
```

---

## Provider Selection Algorithm

```python
def select_provider(capability: str, objective: str, context: RuntimeContext = None) -> ProviderSelection:
    """
    Multi-factor provider selection:
    1. Capability match
    2. Routing rules (explicit)
    3. Health status
    3. Latency budget
    4. Cost budget
    5. Context length requirement
    6. Reliability score
    7. Fallback priority
    """
    
    candidates = get_providers_for_capability(capability)
    if not candidates:
        raise NoProviderForCapabilityError(capability)
    
    # Filter unhealthy
    healthy = [p for p in candidates if is_healthy(p)]
    if not healthy:
        raise AllProvidersUnhealthyError(capability)
    
    # Apply routing rules
    for rule, provider in CAPABILITY_REGISTRY[capability]["routing_rules"].items():
        if provider in healthy and rule_matches(rule, objective, context):
            return ProviderSelection(provider, "routing_rule")
    
    # Score remaining candidates
    scored = []
    for provider in healthy:
        score = calculate_score(provider, context)
        scored.append((score, provider))
    
    scored.sort(reverse=True, key=lambda x: x[0])
    return ProviderSelection(scored[0][1], "scored")


def calculate_score(provider: str, context: RuntimeContext) -> float:
    """Weighted scoring for provider selection."""
    p = PROVIDER_REGISTRY[provider]
    
    # Latency score (lower is better)
    latency_score = 1.0 - min(p["avg_latency_ms"] / 30000, 1.0)
    
    # Cost score (lower is better) 
    cost_score = 1.0 - min(p["cost_per_1k_tokens"]["output"] / 0.02, 1.0)
    
    # Reliability score
    reliability_score = p["reliability_score"]
    
    # Context length score
    context_score = 1.0 if p["max_context"] >= (context.max_context_needed or 0) else 0.5
    
    # Fallback priority (lower is better)
    fallback_score = 1.0 - (p["fallback_priority"] - 1) * 0.1
    
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
```

---

## Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, provider: str, failure_threshold: int = 5, timeout: int = 60):
        self.provider = provider
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    def call(self, executor, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
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
```

---

## Health Check System

```python
async def check_provider_health(provider: str) -> HealthStatus:
    """Check provider health with timeout."""
    p = PROVIDER_REGISTRY[provider]
    endpoint = p["health_endpoint"]
    
    if endpoint == "local":
        return HealthStatus(provider, "healthy", latency_ms=1)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, timeout=5) as resp:
                latency = time.time() - start
                if resp.status == 200:
                    return HealthStatus(provider, "healthy", latency_ms=latency)
                else:
                    return HealthStatus(provider, "degraded", latency_ms=latency)
    except asyncio.TimeoutError:
        return HealthStatus(provider, "unhealthy", error="timeout")
    except Exception as e:
        return HealthStatus(provider, "unhealthy", error=str(e))


async def health_check_loop():
    """Background health checks every 30 seconds."""
    while True:
        for provider in PROVIDER_REGISTRY:
            status = await check_provider_health(provider)
            update_health_cache(provider, status)
        await asyncio.sleep(30)
```

---

## Cost Tracking

```python
def track_provider_cost(provider: str, tokens_in: int, tokens_out: int) -> CostRecord:
    """Track cost per provider call."""
    p = PROVIDER_REGISTRY[provider]
    cost = (tokens_in * p["cost_per_1k_tokens"]["input"] + 
            tokens_out * p["cost_per_1k_tokens"]["output"]) / 1000
    
    record = CostRecord(
        provider=provider,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        cost_usd=cost,
        timestamp=time.time()
    )
    
    append_to_cost_ledger(record)
    return record
```

---

## Fallback Chain Execution

```python
def execute_with_fallback(capability: str, objective: str, context: RuntimeContext) -> CapabilityResult:
    """Execute capability with automatic fallback."""
    providers = get_fallback_chain(capability)
    last_error = None
    
    for provider in providers:
        if not is_healthy(provider):
            continue
            
        try:
            result = execute_provider(provider, objective)
            emit_event("capability.completed", {
                "capability": capability,
                "provider": provider,
                "latency_ms": result.latency_ms
            })
            return result
        except Exception as e:
            last_error = e
            emit_event("capability.failed", {
                "capability": capability,
                "provider": provider,
                "error": str(e)
            })
            continue
    
    raise AllProvidersFailedError(f"All providers failed for {capability}: {last_error}")
```

---

## Configuration

Provider registry can be extended via config file:

```yaml
# config/providers.yaml
providers:
  - name: "Custom-LLM"
    capabilities: ["writing", "analysis"]
    endpoint: "https://custom-llm.example.com/v1"
    auth: "CUSTOM_API_KEY"
    cost_per_1k_tokens: {input: 0.002, output: 0.006}
    max_context: 32000
    fallback_priority: 5
```

---

## Testing Requirements

```python
def test_provider_router():
    # Test capability -> provider mapping
    for cap in CAPABILITY_REGISTRY:
        providers = get_providers_for_capability(cap)
        assert len(providers) > 0
    
    # Test routing rules
    sel = select_provider("research", "deep research on ICP")
    assert sel.provider == "Perplexity"
    
    sel = select_provider("research", "quick search")
    assert sel.provider == "Browser"
    
    # Test fallback
    mock_unhealthy("Perplexity")
    sel = select_provider("research", "deep research")
    assert sel.provider == "Browser"
    
    # Test cost optimization
    context = RuntimeContext(cost_budget="low")
    sel = select_provider("writing", "outreach", context)
    # Should prefer cheaper provider
    
    # Test latency optimization
    context = RuntimeContext(latency_budget=1000)
    sel = select_provider("coding", "quick fix", context)
    # Should prefer Groq
```