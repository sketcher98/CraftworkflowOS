# Operations Department Comparison Report

**Prepared by:** Chief Organization Architect
**Date:** 2026-07-19
**Sources:**
- SOURCE A: 04_Knowledge (CraftworkflowOS primary)
- SOURCE B: agency-agents (reference only)
- SOURCE C: Current 03_Departments (existing structure)

---

## Executive Summary

SOURCE A (04_Knowledge) has **strong strategic foundations** for Operations: SOPs, Systems, Documentation, Automation, Internal Operations mentioned in Operations_Director.md. But **zero employees** exist in the Operations department directory.

SOURCE B (agency-agents) has **relevant specialist roles** in project-management, design, engineering, testing, security, support — but they're **generic agency roles** not tailored to CraftedWorkflows' specific operational needs.

SOURCE C (Current 03_Departments/Operations) has an **Operations Director** with mission "Continuously improve how CraftedWorkflows operates" and owns SOPs, Systems, Documentation, Automation, Internal Operations — but **zero employees**.

**The Gap:** No operational employees exist. Need to build an Operations department from scratch that coordinates Commercial, Marketing, Delivery, Finance, Creative, and Engineering — avoiding duplication, ensuring explicit handoffs, and improving effectiveness of at least two other departments per employee.

---

## 1. SOURCE A Strengths (04_Knowledge)

| Asset | Location | Relevance |
|-------|----------|-----------|
| **Operations Director Mission** | `Operations_Director.md` | "Continuously improve how CraftedWorkflows operates" |
| **Owned Areas** | `Operations_Director.md` | SOPs, Systems, Documentation, Automation, Internal Operations |
| **Boot Sequence** | `00_Systems/boot_sequence.md` | 13-phase boot with Phase 7: Trust Hierarchy, Phase 8: Assessment |
| **Session Management** | `00_Systems/Session/` | Cache rules, refresh policy, session manager |
| **Memory Architecture** | `MEMORY_ARCHITECTURE.md` | 9-layer persistent memory system |
| **Refresh Policy** | `refresh_policy.md` | Tiered cache invalidation (Hot/Warm/Cold) |
| **Checkpoint System** | `runtime/checkpoint.py` | Session persistence with validation |
| **Commercial Playbooks** | `Playbooks/Sales/`, `Playbooks/Outreach/` | Revenue operations support |
| **Marketing Playbooks** | `Playbooks/Marketing/` | Demand generation operations support |

**Key Insight:** SOURCE A has **excellent operational infrastructure** (boot, memory, refresh, checkpoint, session) but **no human operators** to run it.

---

## 2. SOURCE B Strengths (agency-agents)

| Division | Relevant Agents | Adaptation Needed |
|----------|----------------|-------------------|
| **project-management** | PM specialists, sprint planning, delivery tracking | Adapt to multi-dept coordination |
| **engineering** | DevOps automator, backend architect, SRE, incident response | Internal tools, runtime reliability |
| **design** | Design system, documentation engineer | Internal documentation, templates |
| **testing** | QA engineer, regression testing | Quality gates for internal systems |
| **security** | Security auditor, compliance | Internal compliance, data handling |
| **support** | Support specialist | Internal help desk, employee support |
| **finance** | FP&A analyst, bookkeeper | Internal budgeting, cost tracking |

**Irrelevant:** academic, design, game-development, gis, healthcare, spatial-computing, specialized, paid-media, product, sales (generic)

---

## 3. Current Department Landscape (What Operations Must Support)

| Department | Mission | Key Handoffs Operations Must Enable |
|------------|---------|-------------------------------------|
| **Commercial** | Generate predictable revenue | Pipeline → Delivery, Proposal → Delivery, Forecast → Finance |
| **Marketing** | Generate qualified demand | Lead → Commercial, Content → Sales Enablement, Calendar → All |
| **Delivery** | Deliver client outcomes | Kickoff ← Commercial, QA → Engineering, Success → Commercial |
| **Finance** | Protect cash flow & profitability | Forecast ← Commercial, Invoicing ← Delivery, Budget → All |
| **Creative** | Design visual assets & experiences | Assets ← Marketing, UI/UX ← Engineering, Brand → All |
| **Engineering** | Build software, AI, automation | Runtime ← All, Tools → Operations, Infra → All |
| **Intelligence (Future)** | Research, analytics, forecasting | Insights → All, Forecasting → Finance/Commercial |

---

## 4. Gap Analysis: What Operations Must Provide

| Operational Need | Current State | Operations Must Provide |
|------------------|---------------|-------------------------|
| **Cross-dept planning** | Ad-hoc | Quarterly planning rhythm, OKR cascade |
| **SOP management** | Scattered in 04_Knowledge | Central SOP registry, versioning, reviews |
| **System reliability** | Runtime exists, no monitoring | Uptime monitoring, incident response, runbooks |
| **Documentation governance** | 04_Knowledge exists, no standards | Doc standards, review cycles, archival |
| **Automation coordination** | Engineering builds, no central request | Automation intake, prioritization, ROI tracking |
| **Cross-dept communication** | Ad-hoc | Weekly rhythms, escalation paths, decision log |
| **Quality assurance** | Ad-hoc per dept | Quality gates, checklists, audit schedule |
| **Internal tooling** | Engineering builds ad-hoc | Tool intake, prioritization, adoption tracking |
| **Employee onboarding/offboarding** | Ad-hoc | Standardized workflows, checklists |
| **Meeting rhythms** | Ad-hoc | Weekly/dept, monthly/cross-dept, quarterly/strategic |
| **Decision tracking** | None | Decision log, owner, status, review date |
| **Risk management** | None | Risk register, mitigation plans, quarterly review |

---

## 5. Proposed Operations Department Structure

### Director: Operations Director (exists)
Reports to COO. Owns: SOPs, Systems, Documentation, Automation, Internal Operations.

### Employees (6 specialists — each improves ≥2 departments)

| # | Role | Primary Focus | Improves Departments |
|---|------|---------------|---------------------|
| 1 | **Planning Rhythm Coordinator** | Quarterly planning, OKR cascade, meeting rhythms, decision log | All (6+) |
| 2 | **SOP & Documentation Librarian** | SOP registry, doc standards, versioning, review cycles | All (6+) |
| 3 | **Automation & Systems Coordinator** | Automation intake, prioritization, ROI tracking, platform | Engineering, Commercial, Marketing, Operations |
| 4 | **Quality & Reliability Engineer** | Quality gates, SLIs/SLOs, error budgets, incident response | Engineering, Delivery, Commercial, Operations |
| 5 | **Internal Communications & Rhythm Manager** | Meeting rhythms, decision log, escalation paths, onboarding | All (6+) |
| 6 | **Automation & Internal Tools PM** | Tool intake, evaluation, adoption, integration, budget | Engineering, Commercial, Marketing, Operations |

---

## 6. Implementation Order

| Phase | Employees | Rationale |
|-------|-----------|-----------|
| **1** | Planning Rhythm Coordinator, SOP & Documentation Librarian | Foundation: rhythms + knowledge governance |
| **2** | Quality & Reliability Engineer, Automation & Systems Coordinator | Reliability + automation coordination |
| **3** | Internal Communications & Rhythm Manager, Automation & Internal Tools PM | Communication rhythms + tool adoption |

---

## 7. Shared Documentation References (No Duplication)

All Operations employees reference these 04_Knowledge paths:

| Doc | Used By |
|-----|---------|
| `00_Systems/boot_sequence.md` | All (boot process) |
| `00_Systems/Session/` | All (session management) |
| `MEMORY_ARCHITECTURE.md` | All (memory layers) |
| `refresh_policy.md` | All (cache invalidation) |
| `runtime/checkpoint.py` | Planning, Comms (session persistence) |
| `Playbooks/Sales/` | Quality, Automation (revenue ops) |
| `Playbooks/Marketing/` | Quality, Automation (marketing ops) |
| `04_Knowledge/Company/` | All (strategy context) |

---

## 8. Capability Routing (Add to runtime/capabilities.py)

```python
CAPABILITIES = {
    "research": ["Perplexity", "Browser"],
    "writing": ["GPT-4o"],
    "analysis": ["GPT-4o"],
    "design": ["OpenDesign", "Figma"],
    "video": ["HeyGen", "VEED"],
    "automation": ["Make", "n8n"],
    "crm": ["HubSpot"],
    "project_management": ["Linear", "Notion"],    # NEW
    "monitoring": ["Datadog", "Grafana"],          # NEW
    "documentation": ["Notion", "GitBook"],        # NEW
}
```

---

## 9. Next Steps

1. **Create comparison report** (this document) → commit
2. **Build 6 Operations employees** using EMPLOYEE_TEMPLATE
3. **Add capabilities** to runtime/capabilities.py
4. **Verify** org discovery, capability routing, executive loop
5. **Commit & push** as single milestone