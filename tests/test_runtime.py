"""Runtime tests for CraftworkflowOS"""

import pytest
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from runtime.runtime_contracts import (
    RuntimeContext, CapabilityName, ProviderName, CapabilityRequest, CapabilityResult,
    Task, ExecutionResult, Event, Artifact, EmployeeProfile, CapabilityDeclaration
)
from runtime.capability_router_v2 import request_capability
from runtime.provider_router_v2 import (
    select_provider, get_providers_for_capability, is_healthy,
    track_provider_cost, PROVIDER_REGISTRY, ROUTING_RULES
)
from runtime.event_system import EventBus, Event, EventPriority, emit, subscribe


class TestRuntimeContext:
    """Test runtime context creation and structure."""
    
    def test_runtime_context_creation(self):
        ctx = RuntimeContext()
        assert hasattr(ctx, 'commercial')
        assert hasattr(ctx, 'marketing')
        assert hasattr(ctx, 'operations')
        assert hasattr(ctx, 'delivery')
        assert hasattr(ctx, 'finance')
        assert hasattr(ctx, 'creative')
        assert hasattr(ctx, 'engineering')
        assert hasattr(ctx, 'memory')
        assert hasattr(ctx, 'checkpoint')
    
    def test_runtime_context_with_data(self):
        ctx = RuntimeContext(
            commercial={'pipeline': []},
            marketing={'campaigns': {}}
        )
        assert ctx.commercial == {'pipeline': []}
        assert ctx.marketing == {'campaigns': {}}


class TestCapabilityRouter:
    """Test capability routing."""
    
    def test_capability_names(self):
        assert CapabilityName.RESEARCH == "research"
        assert CapabilityName.WRITING == "writing"
        assert CapabilityName.ANALYSIS == "analysis"
        assert CapabilityName.CODING == "coding"
        assert CapabilityName.DESIGN == "design"
        assert CapabilityName.VIDEO_EDITING == "video_editing"
        assert CapabilityName.AUTOMATION == "automation"
        assert CapabilityName.CRM == "crm"
        assert CapabilityName.EMAIL == "email"
    
    def test_provider_names(self):
        assert ProviderName.PERPLEXITY == "Perplexity"
        assert ProviderName.GPT_4O == "GPT-4o"
        assert ProviderName.CLAUDE_35_SONNET == "Claude-3.5-Sonnet"
        assert ProviderName.GROQ_LLAMA_31_70B == "Groq-Llama-3.1-70B"
        assert ProviderName.FIGMA == "Figma"
        assert ProviderName.MAKE == "Make"
        assert ProviderName.HUBSPOT == "HubSpot"
    
    def test_get_providers_for_capability(self):
        providers = get_providers_for_capability(CapabilityName.RESEARCH)
        assert "Perplexity" in [p.value for p in providers]
        assert "Browser" in [p.value for p in providers]
        assert "Exa" in [p.value for p in providers]
        
        providers = get_providers_for_capability(CapabilityName.WRITING)
        assert "GPT-4o" in [p.value for p in providers]
        assert "Claude-3.5-Sonnet" in [p.value for p in providers]
        assert "Groq-Llama-3.1-70B" in [p.value for p in providers]
    
    def test_select_provider_routing_rules(self):
        # Deep research -> Perplexity
        provider = select_provider(CapabilityName.RESEARCH, "deep research on ICP")
        assert provider == ProviderName.PERPLEXITY
        
        # Quick search -> Browser
        provider = select_provider(CapabilityName.RESEARCH, "quick search")
        assert provider == ProviderName.BROWSER
        
        # Outreach -> GPT-4o
        provider = select_provider(CapabilityName.WRITING, "outreach message")
        assert provider == ProviderName.GPT_4O
        
        # Financial analysis -> Claude
        provider = select_provider(CapabilityName.ANALYSIS, "financial analysis")
        assert provider == ProviderName.CLAUDE_35_SONNET
    
    def test_capability_execution(self):
        # Research
        result = request_capability(CapabilityName.RESEARCH, "deep research on agency founders")
        assert result.status == "completed"
        assert result.provider == ProviderName.PERPLEXITY
        
        # Writing
        result = request_capability(CapabilityName.WRITING, "outreach message")
        assert result.status == "completed"
        assert result.provider == ProviderName.GPT_4O
        
        # Analysis
        result = request_capability(CapabilityName.ANALYSIS, "margin analysis")
        assert result.status == "completed"


class TestProviderRouter:
    """Test provider routing and health."""
    
    def test_provider_registry(self):
        assert "Perplexity" in [p.value for p in PROVIDER_REGISTRY.keys()]
        assert "GPT-4o" in [p.value for p in PROVIDER_REGISTRY.keys()]
        assert "Claude-3.5-Sonnet" in [p.value for p in PROVIDER_REGISTRY.keys()]
        assert "Groq-Llama-3.1-70B" in [p.value for p in PROVIDER_REGISTRY.keys()]
        assert "Figma" in [p.value for p in PROVIDER_REGISTRY.keys()]
        assert "Make" in [p.value for p in PROVIDER_REGISTRY.keys()]
        assert "HubSpot" in [p.value for p in PROVIDER_REGISTRY.keys()]
    
    def test_provider_config(self):
        config = PROVIDER_REGISTRY[ProviderName.PERPLEXITY]
        assert CapabilityName.RESEARCH in config.capabilities
        assert config.fallback_priority == 1
        
        config = PROVIDER_REGISTRY[ProviderName.GPT_4O]
        assert CapabilityName.WRITING in config.capabilities
        assert CapabilityName.ANALYSIS in config.capabilities
        assert CapabilityName.CODING in config.capabilities
    
    def test_health_check(self):
        # Should return True for unknown (assumed healthy)
        assert is_healthy(ProviderName.PERPLEXITY) == True
        assert is_healthy(ProviderName.GPT_4O) == True
    
    def test_cost_tracking(self):
        result = track_provider_cost(ProviderName.GPT_4O, 1000, 500)
        assert "cost_usd" in result
        assert result["cost_usd"] > 0


class TestEventSystem:
    """Test event bus functionality."""
    
    @pytest.mark.asyncio
    async def test_basic_emit_subscribe(self):
        bus = EventBus()
        received = []
        
        async def handler(event):
            received.append(event)
        
        bus.subscribe('test.*', handler)
        await bus.emit(Event(event_type='test.event', payload={'foo': 'bar'}, source='test'))
        await asyncio.sleep(0.1)
        
        assert len(received) == 1
        assert received[0].payload['foo'] == 'bar'
    
    @pytest.mark.asyncio
    async def test_pattern_matching(self):
        bus = EventBus()
        received = []
        
        async def handler(event):
            received.append(event)
        
        bus.subscribe('test.*', handler)
        await bus.emit(Event(event_type='test.other', payload={'baz': 'qux'}, source='test'))
        await asyncio.sleep(0.1)
        
        assert len(received) == 1
    
    @pytest.mark.asyncio
    async def test_filter_function(self):
        bus = EventBus()
        received = []
        
        async def handler(event):
            received.append(event)
        
        bus.subscribe('filtered.*', handler, filter_fn=lambda e: e.payload.get('important'))
        await bus.emit(Event(event_type='filtered.a', payload={'important': True}, source='test'))
        await bus.emit(Event(event_type='filtered.b', payload={'important': False}, source='test'))
        await asyncio.sleep(0.1)
        
        assert len(received) == 1
        assert received[0].payload['important'] == True
    
    @pytest.mark.asyncio
    async def test_priority_ordering(self):
        bus = EventBus()
        high_priority = []
        low_priority = []
        
        async def high_handler(e):
            high_priority.append(e)
        
        async def low_handler(e):
            low_priority.append(e)
        
        bus.subscribe('priority.*', high_handler, priority=EventPriority.HIGH)
        bus.subscribe('priority.*', low_handler, priority=EventPriority.LOW)
        
        await bus.emit(Event(event_type='priority.test', payload={}, source='test'))
        await asyncio.sleep(0.1)
        
        assert len(high_priority) == 1
        assert len(low_priority) == 1
    
    @pytest.mark.asyncio
    async def test_dead_letter_queue(self):
        bus = EventBus()
        
        async def failing_handler(e):
            raise ValueError('intentional failure')
        
        bus.subscribe('fail.*', failing_handler)
        await bus.emit(Event(event_type='fail.test', payload={}, source='test'))
        await asyncio.sleep(0.1)
        
        dead_letters = bus.get_dead_letters()
        assert len(dead_letters) == 1
        assert 'intentional failure' in dead_letters[0].error
    
    @pytest.mark.asyncio
    async def test_replay(self):
        bus = EventBus()
        replayed = []
        
        async def handler(e):
            replayed.append(e)
        
        await bus.emit(Event(event_type='replay.test', payload={}, source='test'))
        await asyncio.sleep(0.1)
        
        count = bus.replay('replay.*', handler=lambda e: replayed.append(e))
        assert count == 1
        assert len(replayed) == 1


class TestExecutiveLoop:
    """Test the executive loop integration."""
    
    def test_full_system_integration(self):
        from runtime.context import OperatingContext
        from runtime.loader import load_company, refresh_runtime
        from runtime.executive import execute
        
        runtime = OperatingContext()
        runtime = load_company(runtime)
        runtime = refresh_runtime(runtime, tier='warm')
        
        # Test commercial briefing
        result = execute('commercial briefing', runtime)
        if isinstance(result, tuple):
            briefing, leads, messages = result
            assert len(leads) == 5
            assert len(messages) == 5
        
        # Test work guidance
        result = execute('what should i work on today?', runtime)
        assert len(result) > 0


class TestArtifactSchema:
    """Test artifact schemas."""
    
    def test_artifact_creation(self):
        artifact = Artifact(
            artifact_type="proposal-draft",
            title="Test Proposal",
            content={"client_id": "client_123", "tier": "goldilocks", "amount": 9500},
            created_by="Commercial.Proposal"
        )
        assert artifact.artifact_type == "proposal-draft"
        assert artifact.content["amount"] == 9500
        assert artifact.checksum is not None


class TestEmployeeProfile:
    """Test employee profile structure."""
    
    def test_employee_profile_creation(self):
        profile = EmployeeProfile(
            name="Test Employee",
            department="Test",
            role="Specialist",
            reports_to="Director",
            capability_tier="Specialist",
            mission="Test mission"
        )
        assert profile.name == "Test Employee"
        assert profile.department == "Test"
        assert profile.mission == "Test mission"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])