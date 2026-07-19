# Capability Router Specification

Canonical interface for routing capability requests to providers.

---

## Interface

```python
def request(capability: str, objective: str, context: RuntimeContext = None) -> CapabilityResult:
    """
    Route a capability request to the optimal provider(s).
    
    Args:
        capability: Canonical capability name (e.g., "research", "writing", "analysis")
        objective: Task description/objective
        context: Optional runtime context for routing decisions
        
    Returns:
        CapabilityResult with artifacts, provider metadata, and status
    """
```

---

## Capability Registry

Single source of truth for capability → provider mappings.

```python
CAPABILITY_REGISTRY = {
    "research": {
        "description": "Deep research, ICP matching, market intelligence",
        "providers": ["Perplexity", "Browser", "Exa"],
        "default": "Perplexity",
        "fallback_order": ["Perplexity", "Browser", "Exa"],
        "routing_rules": {
            "deep_research": "Perplexity",
            "quick_search": "Browser",
            "academic": "Exa"
        }
    },
    "writing": {
        "description": "Content generation, outreach, proposals, docs",
        "providers": ["GPT-4o", "Claude-3.5-Sonnet", "Groq-Llama-3.1-70B"],
        "default": "GPT-4o",
        "fallback_order": ["GPT-4o", "Claude-3.5-Sonnet", "Groq-Llama-3.1-70B"],
        "routing_rules": {
            "outreach": "GPT-4o",
            "proposal": "GPT-4o",
            "technical_docs": "Claude-3.5-Sonnet",
            "code": "Groq-Llama-3.1-70B"
        }
    },
    "analysis": {
        "description": "Data analysis, forecasting, margin calc, scoring",
        "providers": ["GPT-4o", "Claude-3.5-Sonnet", "Groq-Llama-3.1-70B"],
        "default": "GPT-4o",
        "fallback_order": ["GPT-4o", "Claude-3.5-Sonnet", "Groq-Llama-3.1-70B"],
        "routing_rules": {
            "financial": "Claude-3.5-Sonnet",
            "statistical": "GPT-4o",
            "code_analysis": "Groq-Llama-3.1-70B"
        }
    },
    "coding": {
        "description": "Code generation, review, refactoring",
        "providers": ["Groq-Llama-3.1-70B", "Claude-3.5-Sonnet", "GPT-4o"],
        "default": "Groq-Llama-3.1-70B",
        "fallback_order": ["Groq-Llama-3.1-70B", "Claude-3.5-Sonnet", "GPT-4o"]
    },
    "design": {
        "description": "UI/UX, brand, motion specs, Figma assets",
        "providers": ["Figma", "OpenDesign"],
        "default": "Figma",
        "fallback_order": ["Figma", "OpenDesign"]
    },
    "video_editing": {
        "description": "Video production, captions, export",
        "providers": ["Premiere", "HeyGen", "VEED"],
        "default": "Premiere",
        "fallback_order": ["Premiere", "HeyGen", "VEED"]
    },
    "automation": {
        "description": "Workflow automation, Make/n8n/Zapier",
        "providers": ["Make", "n8n", "Zapier"],
        "default": "Make",
        "fallback_order": ["Make", "n8n", "Zapier"]
    },
    "crm": {
        "description": "CRM operations (create, update, query)",
        "providers": ["HubSpot", "Pipedrive", "Airtable"],
        "default": "HubSpot",
        "fallback_order": ["HubSpot", "Pipedrive", "Airtable"]
    },
    "email": {
        "description": "Email send, template, tracking",
        "providers": ["Gmail", "SendGrid", "Mailgun"],
        "default": "Gmail",
        "fallback_order": ["Gmail", "SendGrid", "Mailgun"]
    },
    "calendar": {
        "description": "Scheduling, availability, booking",
        "providers": ["Google Calendar", "Calendly", "Outlook"],
        "default": "Google Calendar",
        "fallback_order": ["Google Calendar", "Calendly", "Outlook"]
    },
    "document": {
        "description": "Document generation, PDF, contracts",
        "providers": ["Google Docs", "Notion", "Pandoc"],
        "default": "Google Docs",
        "fallback_order": ["Google Docs", "Notion", "Pandoc"]
    },
    "storage": {
        "description": "File storage, CDN, asset management",
        "providers": ["Google Drive", "Dropbox", "Cloudinary", "S3"],
        "default": "Google Drive",
        "fallback_order": ["Google Drive", "Dropbox", "Cloudinary", "S3"]
    },
    "search": {
        "description": "Web search, semantic search, knowledge retrieval",
        "providers": ["Browser", "Perplexity", "Exa", "Google Search"],
        "default": "Browser",
        "fallback_order": ["Browser", "Perplexity", "Exa", "Google Search"]
    },
    "monitoring": {
        "description": "System health, uptime, alerting",
        "providers": ["Datadog", "Grafana", "Prometheus"],
        "default": "Datadog",
        "fallback_order": ["Datadog", "Grafana", "Prometheus"]
    },
    "testing": {
        "description": "Test execution, QA, validation",
        "providers": ["Playwright", "pytest", "Vitest"],
        "default": "Playwright",
        "fallback_order": ["Playwright", "pytest", "Vitest"]
    }
}
```

---

## Routing Algorithm

```python
def route_capability(capability: str, objective: str, context: RuntimeContext = None) -> ProviderSelection:
    """
    Select optimal provider for capability based on:
    1. Explicit routing rule match (objective keywords)
    2. Provider availability (health check)
    3. Latency requirements (context.latency_budget)
    4. Cost optimization (context.cost_budget)
    5. Context length requirements
    6. Reliability score (historical)
    7. Fallback priority order
    """
    
    registry = CAPABILITY_REGISTRY.get(capability)
    if not registry:
        raise CapabilityNotFoundError(f"Capability '{capability}' not registered")
    
    # 1. Check explicit routing rules
    for rule, provider in registry["routing_rules"].items():
        if rule_matches(rule, objective, context):
            if is_provider_healthy(provider):
                return ProviderSelection(provider, reason=f"rule_match:{rule}")
    
    # 2. Use default if healthy
    default = registry["default"]
    if is_provider_healthy(default):
        return ProviderSelection(default, reason="default")
    
    # 3. Fallback chain
    for provider in registry["fallback_order"]:
        if is_provider_healthy(provider):
            return ProviderSelection(provider, reason=f"fallback:{provider}")
    
    # 4. No healthy providers
    raise AllProvidersUnhealthyError(f"No healthy providers for {capability}")
```

---

## Health Checks

```python
PROVIDER_HEALTH = {
    "Perplexity": {"endpoint": "https://api.perplexity.ai/health", "timeout": 5},
    "GPT-4o": {"endpoint": "https://api.openai.com/health", "timeout": 5},
    "Claude-3.5-Sonnet": {"endpoint": "https://api.anthropic.com/health", "timeout": 5},
    "Groq-Llama-3.1-70B": {"endpoint": "https://api.groq.com/health", "timeout": 5},
    "Figma": {"endpoint": "https://api.figma.com/v1/me", "timeout": 5},
    "Premiere": {"endpoint": "local", "timeout": 1},
    "Make": {"endpoint": "https://api.make.com/health", "timeout": 5},
    "HubSpot": {"endpoint": "https://api.hubapi.com/health", "timeout": 5},
    "Gmail": {"endpoint": "https://gmail.googleapis.com/health", "timeout": 5},
    "Browser": {"endpoint": "local", "timeout": 1},
}
```

---

## CapabilityResult Schema

```json
{
  "capability": "research",
  "provider": "Perplexity",
  "objective": "Find high-quality agency founders matching ICP",
  "status": "completed",
  "artifacts": [
    {
      "type": "Research",
      "title": "ICP Research Results",
      "content": "...",
      "created_by": "Perplexity",
      "metadata": {"tokens_used": 1234, "latency_ms": 2341}
    }
  ],
  "routing_metadata": {
    "selected_provider": "Perplexity",
    "fallback_used": false,
    "latency_ms": 2341,
    "tokens_used": 1234,
    "cost_usd": 0.0023
  },
  "errors": []
}
```

---

## Integration Points

### Called By:
- Employee `execute()` method when needing capability
- Workflow engine when transition requires capability
- Director delegation when fan-out to specialists

### Calls:
- Provider Router for provider selection
- Provider executors for actual work
- Event System to emit `capability.requested`, `capability.completed`, `capability.failed`

### Memory:
- Reads: `preferences.routing.*` (learned routing preferences)
- Writes: `episodic.capability_events.*` (execution history)

---

## Error Handling

```python
class CapabilityError(Exception):
    pass

class CapabilityNotFoundError(CapabilityError):
    pass

class AllProvidersUnhealthyError(CapabilityError):
    pass

class ProviderTimeoutError(CapabilityError):
    pass

class ProviderExecutionError(CapabilityError):
    pass
```

---

## Testing Requirements

```python
def test_capability_router():
    # Test all registered capabilities resolve
    for cap in CAPABILITY_REGISTRY:
        result = request(cap, "test objective")
        assert result.status in ["completed", "failed"]
    
    # Test routing rules
    result = request("research", "deep research on ICP matching")
    assert result.provider == "Perplexity"
    
    result = request("research", "quick search for contact")
    assert result.provider == "Browser"
    
    # Test fallback
    mock_unhealthy("Perplexity")
    result = request("research", "deep research")
    assert result.provider == "Browser"
    
    # Test unknown capability
    try:
        request("unknown_capability", "test")
        assert False
    except CapabilityNotFoundError:
        pass
```