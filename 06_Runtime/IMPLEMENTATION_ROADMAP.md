# Implementation Roadmap

Prioritized implementation plan for Phase 6 Runtime Architecture.

---

## P0 — Critical Path (Week 1-2)

### 1. Runtime Contracts & Interfaces
**File:** `runtime/runtime_contracts.py`
- `EmployeeRuntime` abstract base class
- `RuntimeContext` typed dict
- `CapabilityRequest` / `CapabilityResult` schemas
- `Task` / `ExecutionResult` schemas
- `Event` / `EventResult` schemas

### 2. Capability Router Refactor
**File:** `runtime/capability_router_v2.py`
- Canonical capability registry (from `capability_router.md`)
- Multi-provider routing with fallback
- Health-aware provider selection
- Cost/latency optimization
- Circuit breaker integration

### 3. Provider Router Refactor
**File:** `runtime/provider_router_v2.py`
- Provider registry with 30+ providers (from `provider_router.md`)
- Multi-factor selection algorithm
- Circuit breaker pattern
- Background health checks
- Cost tracking

### 4. Event System Implementation
**File:** `runtime/event_system.py`
- `EventBus` with pattern matching
- Priority-based subscription
- Dead-letter queue
- Event replay
- Structured logging integration

### 5. Memory Manager Integration
**File:** `runtime/memory/manager.py` (existing - enhance)
- Verify 9-layer integration
- Add checkpoint validation
- Add preference application
- Add reflection storage

---

## P1 — Core Workflow & Orchestration (Week 2-3)

### 6. Workflow Engine
**File:** `runtime/workflow_engine.py`
- DAG-based workflow execution
- State machine with transitions
- Compensation/rollback support
- Timeout monitoring
- Persistence layer

### 7. Execution Graph
**File:** `runtime/execution_graph.py`
- DAG executor with parallelism
- Dependency resolution
- Fan-out/fan-in for director delegation
- Retry policies per node

### 8. Orchestration Layer
**File:** `runtime/orchestration.py`
- Director → Employee delegation
- Priority queue for task scheduling
- Cross-department coordination
- Load balancing

### 9. Scheduler
**File:** `runtime/scheduler.py`
- Cron, interval, one-shot jobs
- Distributed locking (Redis)
- Job persistence and resume

---

## P2 — Integration & Observability (Week 3-4)

### 10. Composio Integration
**File:** `runtime/integrations/composio.py`
- Tool registry from `tool_router.md`
- OAuth flow management
- Action execution wrapper
- Rate limiting per tool

### 11. Direct API Integrations
**File:** `runtime/integrations/direct.py`
- GitHub, GitLab, Linear, Jira
- Stripe, QuickBooks, Supabase
- All tools from `tool_router.md` DIRECT_TOOLS

### 12. Checkpoint System v2
**File:** `runtime/checkpoint_system_v2.py`
- Working memory serialization
- Employee state persistence
- Workflow state persistence
- Validation against critical docs
- Recovery with state reconstruction

### 13. Observability
**File:** `runtime/observability.py`
- Structured logging (structlog)
- Prometheus metrics
- OpenTelemetry tracing
- Alerting rules

---

## P3 — Autonomous Operation (Week 4-5)

### 14. Autonomous Execution Loop
**File:** `runtime/autonomous.py`
- Continuous event processing
- Self-healing workflows
- Reflection-driven improvement
- Preference learning

### 15. Reflection & Learning
**File:** `runtime/reflection_loop.py`
- Post-execution reflection
- Pattern extraction
- Preference updates
- Skill/knowledge persistence

### 16. Self-Optimization
**File:** `runtime/optimizer.py`
- Routing optimization (cost/latency)
- Workflow bottleneck detection
- Provider performance analysis
- Automatic scaling hints

---

## Migration Strategy

### Phase 1: Parallel Implementation
1. Build new components alongside existing
2. Route 10% of traffic to new capability router
3. Compare results, fix discrepancies

### Phase 2: Gradual Migration
1. Migrate Commercial department employees first
2. Then Marketing, Operations, Delivery
3. Then Engineering, Finance, Creative

### Phase 3: Cutover
1. All traffic through new runtime
2. Deprecate old modules
3. Clean up technical debt

---

## Testing Requirements

Each component must have:
- Unit tests (>80% coverage)
- Integration tests with real providers (mocked)
- End-to-end workflow tests
- Chaos testing (provider failures, timeouts)
- Load testing (concurrent workflows)

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
- HubSpot OAuth credentials
- Gmail OAuth credentials
- Notion OAuth credentials
- Figma personal token
- Perplexity API key
- Exa API key
- Make API key
- N8N API key
- HubSpot API key
- SendGrid API key
- Mailgun API key
- Google OAuth credentials
- Calendly API key
- Typefully API key
- Cloudinary API key
- TinyPNG API key
- Giphy API key
- HTML to Image API key
- ImgBB API key
- Tally Forms API key
- Lemonsqueezy API key
- Gumroad API key
- Canva OAuth credentials
- Vapi API key
- Groq API key
- Paystack API key
- Supabase API key
- Daytona API key
- Facebook OAuth credentials

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