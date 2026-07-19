# Implementation Roadmap - Phase 7 (Tool Integration)

**Updated:** 2025-07-19
**Status:** P0 Complete, P1 In Progress

---

## P0 — Critical Path (Week 1-2) ✅ COMPLETED

### 1. Runtime Contracts & Interfaces
**File:** `runtime/runtime_contracts.py`
- `EmployeeRuntime` abstract base class
- `RuntimeContext` typed dict
- `CapabilityRequest` / `CapabilityResult` schemas
- `Task` / `ExecutionResult` schemas
- `Event` / `EventResult` schemas
- **Status**: ✅ Complete, tested

### 2. Capability Router v2
**File:** `runtime/capability_router_v2.py`
- Canonical capability registry
- Multi-provider routing with fallback
- Health-aware provider selection
- Cost/latency optimization
- Circuit breaker integration
- **Status**: ✅ Complete, tested (20/20 tests passing)

### 3. Provider Router v2
**File:** `runtime/provider_router_v2.py`
- Provider registry with 30+ providers
- Multi-factor selection algorithm
- Circuit breaker pattern
- Background health checks
- Cost tracking
- **Status**: ✅ Complete, tested
- **Added**: Groq, OpenRouter, NVIDIA NIM
- **Updated**: CRM routing → Notion (primary), Airtable (fallback)

### 4. Event System
**File:** `runtime/event_system.py`
- `EventBus` with pattern matching
- Priority-based subscription
- Dead-letter queue
- Event replay
- Structured logging integration
- **Status**: ✅ Complete, tested

### 5. CRM Configuration
- HubSpot: ❌ DISABLED (legacy FyreStrokeDigital account)
- Notion: ✅ PRIMARY CRM (capability: `crm`)
- Airtable: ✅ FALLBACK CRM
- **Status**: ✅ Complete

---

## P1 — Core Integrations & Workflows (Week 2-4) 🔄 IN PROGRESS

### 6. Notion CRM Schemas ✅ COMPLETED
**File:** `runtime/notion_crm_schemas.py`
- 12 database schemas (Leads, Companies, Contacts, Opportunities, Sales Calls, Proposals, Clients, Projects, Tasks, Knowledge Base, SOPs, Executive Dashboard)
- Properties, relationships, status values, views, templates, automations
- Owning department & employee for each
- HubSpot ID fields for migration
- **Status**: ✅ Complete

### 7. Notion CRM Client ✅ COMPLETED
**File:** `runtime/notion_crm_client.py`
- Full CRUD for all 12 databases
- `CRMManager` with provider selection
- Graceful degradation (Notion-only mode)
- Query/filter support
- **Status**: ✅ Complete

### 8. Composio Notion Integration
**File:** `runtime/integrations/composio_notion.py`
- OAuth flow for Notion
- Connection management
- Action execution wrapper
- Rate limiting
- **Status**: ⬜ TODO

### 9. Composio Gmail Integration
**File:** `runtime/integrations/composio_gmail.py`
- OAuth flow for Gmail
- Send/read/search emails
- Thread management
- **Status**: ⬜ TODO

### 10. Composio Google Calendar Integration
**File:** `runtime/integrations/composio_calendar.py`
- OAuth flow for Calendar
- Create/read/update events
- Availability checking
- **Status**: ⬜ TODO

### 11. Composio GitHub Integration
**File:** `runtime/integrations/composio_github.py`
- OAuth flow for GitHub
- Repo/file/issue/PR operations
- CI/CD triggers
- **Status**: ⬜ TODO

### 12. Database Creation Script
**File:** `scripts/create_notion_databases.py`
- Creates all 12 databases via Notion API
- Sets up relations between databases
- Creates default views
- Populates templates
- **Status**: ⬜ TODO

### 13. Workflow Engine
**File:** `runtime/workflow_engine.py`
- DAG-based workflow execution
- State machine with transitions
- Compensation/rollback support
- Timeout monitoring
- Persistence layer
- **Status**: ⬜ TODO

### 14. Workflow Implementations (10 workflows)
| Workflow | File | Status |
|----------|------|--------|
| WF-01: Lead Discovery | `runtime/workflows/lead_discovery.py` | ⬜ TODO |
| WF-02: Outbound Outreach | `runtime/workflows/outbound_outreach.py` | ⬜ TODO |
| WF-03: Discovery Call | `runtime/workflows/discovery_call.py` | ⬜ TODO |
| WF-04: Proposal Generation | `runtime/workflows/proposal_generation.py` | ⬜ TODO |
| WF-05: Deal Close → Onboarding | `runtime/workflows/deal_close_onboarding.py` | ⬜ TODO |
| WF-06: Project Delivery | `runtime/workflows/project_delivery.py` | ⬜ TODO |
| WF-07: Client Health | `runtime/workflows/client_health.py` | ⬜ TODO |
| WF-08: Expansion/Referral | `runtime/workflows/expansion_referral.py` | ⬜ TODO |
| WF-09: Executive Dashboard | `runtime/workflows/exec_dashboard.py` | ⬜ TODO |
| WF-10: KB Maintenance | `runtime/workflows/kb_maintenance.py` | ⬜ TODO |

### 15. Make/n8n Scenario Templates
**Dir:** `integrations/make/scenarios/`
- One scenario per workflow
- Webhook triggers
- Error handling
- **Status**: ⬜ TODO

---

## P2 — Integration & Observability (Week 4-6)

### 16. Direct API Integrations
**File:** `runtime/integrations/direct.py`
- GitHub, GitLab, Linear, Jira
- Stripe, QuickBooks, Supabase
- All tools from `tool_router.md` DIRECT_TOOLS
- **Status**: ⬜ TODO

### 17. Checkpoint System v2
**File:** `runtime/checkpoint_system_v2.py`
- Working memory serialization
- Employee state persistence
- Workflow state persistence
- Validation against critical docs
- Recovery with state reconstruction
- **Status**: ⬜ TODO

### 18. Observability
**File:** `runtime/observability.py`
- Structured logging (structlog)
- Prometheus metrics
- OpenTelemetry tracing
- Alerting rules
- **Status**: ⬜ TODO

---

## P3 — Autonomous Operation (Week 6-8)

### 19. Autonomous Execution Loop
**File:** `runtime/autonomous.py`
- Continuous event processing
- Self-healing workflows
- Reflection-driven improvement
- Preference learning
- **Status**: ⬜ TODO

### 20. Reflection & Learning
**File:** `runtime/reflection_loop.py`
- Post-execution reflection
- Pattern extraction
- Preference updates
- Skill/knowledge persistence
- **Status**: ⬜ TODO

### 21. Self-Optimization
**File:** `runtime/optimizer.py`
- Routing optimization (cost/latency)
- Workflow bottleneck detection
- Provider performance analysis
- Automatic scaling hints
- **Status**: ⬜ TODO

---

## Migration Strategy

### Phase 1: Parallel Implementation (Current)
1. ✅ Build new components alongside existing
2. ⬜ Route 10% of traffic to new capability router
3. ⬜ Compare results, fix discrepancies

### Phase 2: Gradual Migration
1. ⬜ Migrate Commercial department employees first
2. ⬜ Then Marketing, Operations, Delivery
3. ⬜ Then Engineering, Finance, Creative

### Phase 3: Cutover
1. ⬜ All traffic through new runtime
2. ⬜ Deprecate old modules (`provider_registry.py`, `capability_router.py`, `capabilities.py`)
3. ⬜ Clean up technical debt

---

## Dependencies

### External (Available)
- `structlog` — structured logging
- `prometheus-client` — metrics
- `opentelemetry-api` — tracing
- `redis` — distributed locking, caching
- `aiohttp` — async HTTP
- `pydantic` — validation

### External (Needed)
- Composio SDK — `pip install composio-core`
- Notion OAuth credentials
- Gmail OAuth credentials
- Google Calendar OAuth credentials
- GitHub OAuth credentials

### DO NOT NEED (HubSpot Unavailable)
- HubSpot OAuth credentials
- HubSpot API key

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Capability routing latency | < 50ms (p99) |
| Provider fallback time | < 100ms |
| Workflow transition time | < 200ms |
| Checkpoint save/restore | < 500ms |
| Event bus throughput | > 10,000 eps |
| Dead letter rate | < 0.1% |
| Workflow success rate | > 99% |
| Autonomous cycle time | < 5 min |

---

## Test Results (Current)

```
20 passed, 1 warning in 2.33s
- Runtime Contracts: ✅
- Capability Router v2: ✅
- Provider Router v2: ✅ (30+ providers)
- Event System: ✅
- Executive Loop: ✅
- Artifact Schema: ✅
- Employee Profile: ✅
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Provider API changes | Abstract interface, version pinning |
| Composio rate limits | Local caching, request batching |
| Memory bloat | TTL-based cleanup, size limits |
| Deadlock in workflows | Timeout guards, deadlock detection |
| Data loss on crash | Synchronous checkpointing, WAL |
| Provider cost overrun | Budget guards, alerting |
| Circular dependencies | Strict import ordering, interface segregation |
| HubSpot re-enablement | Router config change only (no code changes) |