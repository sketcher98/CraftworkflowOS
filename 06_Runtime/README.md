# 06_Runtime — CraftworkflowOS Runtime Architecture

Canonical runtime specification for transforming the documented organization into an executing AI Operating System.

---

## Runtime Principles

1. **Employees request capabilities, never providers** — Capability router selects providers
2. **Event-driven, never polling** — Employees wake on triggers, execute, emit events
3. **Single convention per runtime object** — Capability names, provider names, tool names, event names, artifact schemas, memory namespaces, checkpoint structure
4. **Provider abstraction** — NVIDIA NIM, Groq, OpenRouter, Local models plug in without changing employees
4. **Tool abstraction** — Composio integrations (HubSpot, Gmail, Notion, etc.) accessed via capability routing
5. **Workflow engine** — Complete client lifecycle modeled as executable workflows with rollback, retries, timeouts
6. **Observability built-in** — Structured logging, metrics, tracing from day one

---

## Directory Structure

```
06_Runtime/
├── README.md                           # This file
├── capability_router.md                # Capability → Provider routing specification
├── provider_router.md                  # Provider selection, fallback, cost/latency optimization
├── tool_router.md                      # Tool → Capability → Provider mapping
├── event_system.md                     # Event schema, bus, subscriptions, dead-letter
├── workflow_engine.md                  # Client lifecycle workflows as executable graphs
├── execution_graph.md                  # DAG execution, parallelism, dependency resolution
├── artifact_registry.md                # Artifact schemas, versioning, validation
├── runtime_contracts.md                # Employee ↔ Runtime interface contracts
├── state_machine.md                    # Employee lifecycle states, transitions
├── orchestration.md                    # Director → Employee delegation, fan-out/fan-in
├── scheduler.md                        # Cron, intervals, one-shots, distributed locking
├── checkpoint_system.md                # Working memory persistence, validation, recovery
├── observability.md                    # Logging, metrics, tracing, alerting
├── IMPLEMENTATION_ROADMAP.md           # Prioritized implementation plan (P0-P3)
```

---

## Canonical Naming Standards

### Capability Names (lowercase, singular)
```
research          # Deep research, ICP matching, market intelligence
writing           # Content generation, outreach, proposals, docs
analysis          # Data analysis, forecasting, margin calc, scoring
coding            # Code generation, review, refactoring
design            # UI/UX, brand, motion specs, Figma assets
video_editing     # Video production, captions, export
automation        # Workflow automation, Make/n8n/Zapier
crm               # CRM operations (create, update, query)
email             # Email send, template, tracking
calendar          # Scheduling, availability, booking
document          # Document generation, PDF, contracts
storage           # File storage, CDN, asset management
search            # Web search, semantic search, knowledge retrieval
monitoring        # System health, uptime, alerting
testing           # Test execution, QA, validation
```

### Provider Names (PascalCase)
```
Perplexity        # Deep research, sonar-pro
GPT-4o            # Writing, analysis, coding
Claude-3.5-Sonnet # Analysis, coding, reasoning
Groq-Llama-3.1-70B # Fast inference, coding
NVIDIA-NIM        # Local/private model hosting
Figma             # Design, prototyping, components
Premiere          # Video editing, export
Make              # Automation workflows
HubSpot           # CRM operations
Gmail             # Email operations
Notion            # Documentation, knowledge
Linear            # Project management
GitHub            # Code, CI/CD, issues
Slack             # Notifications, commands
```

### Tool Names (lowercase, kebab-case)
```
perplexity-research
gpt-writing
claude-analysis
groq-coding
figma-design
premiere-video
make-automation
hubspot-crm
gmail-email
notion-docs
linear-projects
github-code
slack-notify
```

### Event Names (lowercase, dot-notation)
```
employee.triggered
employee.started
employee.completed
employee.failed
employee.escalated
capability.requested
capability.routed
capability.completed
capability.failed
artifact.created
artifact.updated
workflow.started
workflow.transitioned
workflow.completed
workflow.failed
workflow.rolled_back
memory.read
memory.written
checkpoint.saved
checkpoint.restored
director.delegated
director.escalated
```

### Artifact Schemas (lowercase, kebab-case)
```
proposal-draft
outreach-message
research-report
design-spec
video-asset
ui-spec
code-module
test-result
invoice-pdf
contract-signed
case-study
onboarding-deck
qbr-deck
health-report
expansion-proposal
```

### Working Memory Namespaces (lowercase, dot-notation)
```
commercial.leads
commercial.pipeline
commercial.proposals
marketing.content
marketing.campaigns
operations.sops
operations.automations
delivery.projects
delivery.clients
delivery.quality
finance.invoices
finance.cashflow
finance.forecasts
creative.assets
creative.templates
engineering.code
engineering.deploys
```

### Runtime Context Keys (lowercase, dot-notation)
```
context.company
context.commercial
context.marketing
context.operations
context.delivery
context.finance
context.creative
context.engineering
context.memory
context.checkpoint
```

### Checkpoint Structure (lowercase, kebab-case)
```
runtime-cache.json
working-memory.json
employee-states.json
workflow-states.json
artifact-index.json
```

---

## Runtime Components Overview

### 1. Capability Router (`runtime/capability_router.py`)
- Single entry point: `request(capability, objective, context)`
- Returns: `{capability, providers: [], status, artifacts: []}`
- Routes to Provider Router for provider selection

### 2. Provider Router (`runtime/provider_router.py`)
- Selects provider based on: capability, latency, availability, cost, context_length, reliability, fallback_priority
- Supports: NVIDIA NIM, Groq, OpenRouter, Local models
- Falls back gracefully with circuit breaker pattern

### 3. Tool Router (`runtime/tool_router.py`)
- Maps tool → capability → provider
- Composio integrations: HubSpot, Gmail, Notion, Google Calendar, Slack, Make, Figma, Perplexity, Exa, Calendly, Typeform, Google Docs/Sheets, GitHub, Linear, Dropbox, Cloudinary, etc.
- Future integrations plug in without changing employees

### 4. Event System (`runtime/event_system.py`)
- Event bus with typed schemas
- Subscriptions: `subscribe(event_pattern, handler)`
- Dead-letter queue for failed deliveries
- Event replay for debugging

### 5. Workflow Engine (`runtime/workflow_engine.py`)
- Client lifecycle as executable DAG
- Each transition: owner, trigger, artifacts, events, rollback, retries, timeout, escalation
- State persistence, resume from checkpoint

### 6. Execution Graph (`runtime/execution_graph.py`)
- DAG execution with parallelism
- Dependency resolution, fan-out/fan-in
- Timeout and retry policies per node

### 7. Artifact Registry (`runtime/artifact_registry.py`)
- Schema validation (JSON Schema)
- Versioning, lineage, immutability
- Artifact search and retrieval

### 8. Runtime Contracts (`runtime/runtime_contracts.py`)
- Employee ↔ Runtime interface
- Required methods: `execute(task, context)`, `handle_event(event)`, `get_state()`
- Input/output validation

### 9. State Machine (`runtime/state_machine.py`)
- Employee states: IDLE, TRIGGERED, EXECUTING, WAITING, COMPLETED, FAILED, ESCALATED
- Valid transitions, guards, actions

### 10. Orchestration (`runtime/orchestration.py`)
- Director delegation: fan-out to employees, fan-in results
- Priority queues, load balancing
- Cross-department coordination

### 11. Scheduler (`runtime/scheduler.py`)
- Cron, intervals, one-shots
- Distributed locking (Redis-based)
- Job persistence, resume on restart

### 12. Checkpoint System (`runtime/checkpoint_system.py`)
- Working memory serialization
- Validation against critical docs
- Recovery with state reconstruction

### 13. Observability (`runtime/observability.py`)
- Structured logging (JSON)
- Metrics (Prometheus format)
- Distributed tracing (OpenTelemetry)
- Alerting rules

---

## Employee Runtime Interface

Every employee implements:

```python
class EmployeeRuntime:
    def execute(self, task: Task, context: RuntimeContext) -> ExecutionResult:
        """Main execution entry point. Called by workflow engine."""
    
    def handle_event(self, event: Event) -> EventResult:
        """Handle incoming events (capability completion, escalation, etc.)"""
    
    def get_state(self) -> EmployeeState:
        """Return current state for checkpointing."""
    
    def get_capabilities(self) -> List[CapabilityDeclaration]:
        """Declare required capabilities (from profile)."""
    
    def get_required_context(self) -> List[str]:
        """Runtime context keys this employee needs."""
```

---

## Memory Architecture Integration

9-layer memory system integrated at runtime:

| Layer | Runtime Access | Persistence |
|-------|----------------|-------------|
| Identity | `runtime.identity` | Git-tracked, loaded at boot |
| Working | `runtime.working_memory` | Checkpointed every cycle |
| Long-term | `runtime.longterm` | Git-tracked, append-only |
| Episodic | `runtime.episodic` | Git-tracked, time-bounded |
| Skills | `runtime.skills` | Git-tracked, versioned |
| Reflections | `runtime.reflections` | Git-tracked, append-only |
| Decisions | `runtime.decisions` | Git-tracked, append-only |
| Preferences | `runtime.preferences` | Git-tracked, learned |
| Checkpoints | `runtime.checkpoints` | Local file, not git |

---

## Boot Sequence (Runtime)

1. **Load Identity** — Mission, principles, authority from `memory/identity/`
2. **Load Company** — `01_CEO/company.md`, `decision_principles.md`
3. **Load Organization** — Discover departments/employees from `03_Departments/`
4. **Initialize Runtime** — Capability router, provider registry, event bus
5. **Load Providers** — Register all providers with capabilities
6. **Load Working Memory** — Restore from latest valid checkpoint
7. **Load Preferences** — Apply learned preferences to routing
8. **Validate Checkpoint** — Verify against critical doc mtimes
9. **Start Event Loop** — Listen for triggers, execute workflows
10. **Schedule Recurring** — Daily briefing, weekly review, monthly planning

---

## Client Lifecycle Workflow (Executable)

```
LEAD_GENERATION
    → trigger: marketing.content_calendar.ready
    → owner: Marketing.ContentStrategist
    → output: lead_magnet, landing_page, campaign
    
QUALIFICATION
    → trigger: lead.captured
    → owner: Commercial.LeadIntelligence
    → output: icp_score, tier, signals
    
DISCOVERY
    → trigger: lead.qualified
    → owner: Commercial.Discovery
    → output: gap_analysis, stakeholder_map
    
PROPOSAL
    → trigger: discovery.complete
    → owner: Commercial.Proposal
    → output: proposal_draft, pricing, terms
    
CLOSED_WON
    → trigger: proposal.accepted
    → owner: Commercial.Pipeline
    → output: signed_contract, deposit
    
ONBOARDING
    → trigger: contract.signed
    → owner: Delivery.ClientOnboarding
    → output: onboarding_plan, access, kickoff
    
EXECUTION
    → trigger: onboarding.complete
    → owner: Delivery.ProjectManager
    → output: project_plan, milestones
    
QA
    → trigger: milestone.delivered
    → owner: Delivery.QualityEngineer
    → output: test_results, signoff
    
CLIENT_SUCCESS
    → trigger: qa.passed
    → owner: Delivery.ClientSuccess
    → output: health_report, qbr_deck
    
EXPANSION
    → trigger: health_score.high
    → owner: Delivery.Expansion
    → output: expansion_proposal, referral
    
FINANCE
    → trigger: milestone.complete / expansion.accepted
    → owner: Finance.Billing
    → output: invoice, payment_tracking
    
EXECUTIVE_REVIEW
    → trigger: monthly_cycle
    → owner: COO
    → output: executive_dashboard, decisions
```

Each transition defines: trigger, artifacts, events, rollback, retries, timeout, escalation.

---

## Verification Checklist

- [ ] All capability names standardized
- [ ] All provider names standardized
- [ ] All tool names standardized
- [ ] All event names standardized
- [ ] All artifact schemas defined
- [ ] All memory namespaces defined
- [ ] All context keys defined
- [ ] All checkpoint structures defined
- [ ] Provider routing logic documented
- [ ] Tool routing logic documented
- [ ] Event schemas defined
- [ ] Workflow transitions defined
- [ ] Employee runtime interface specified
- [ ] State machine transitions defined
- [ ] Observability standards defined
- [ ] Implementation roadmap prioritized