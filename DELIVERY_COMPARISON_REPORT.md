# Delivery Department Comparison Report

**Prepared by:** Chief Organization Architect
**Date:** 2026-07-19
**Sources:**
- SOURCE A: 04_Knowledge (CraftworkflowOS primary)
- SOURCE B: agency-agents (reference only)
- SOURCE C: Current 03_Departments (existing structure)

---

## Executive Summary

SOURCE A (04_Knowledge) has **strong strategic foundations** for Delivery: the client lifecycle is well-defined across Commercial → Delivery → Finance handoffs. The Commercial employees already produce outputs that Delivery consumes (proposals, gap analyses, stakeholder maps). But **zero employees** exist in the Delivery department directory.

SOURCE B (agency-agents) has **relevant specialist roles** in project-management, support, engineering, testing — but they're **generic agency roles** not tailored to CraftedWorkflows' specific delivery model (AI systems installation, automation delivery, client success).

SOURCE C (Current 03_Departments/Delivery) has a **Delivery Director** with mission "Deliver outstanding client outcomes on time" and owns Client Delivery, Project Management, QA, Client Success, Documentation — but **zero employees**.

**The Gap:** No operational delivery employees exist. Need to build a Delivery department that transforms signed clients into successful case studies, long-term partners, referrals and expansion opportunities.

---

## Client Lifecycle Mapping

```
MARKETING → COMMERCIAL → OPERATIONS → DELIVERY → FINANCE
    ↓           ↓            ↓           ↓         ↓
  Leads      Signed       Planning    Delivery   Invoicing
  → Audit    Contract     & SOPs      & QA       & Cash
    →        →            →           →          →
  Lead Magnet → Discovery → Proposal → Signed → Onboarding → Execution → QA → Success → Expansion
```

### Detailed Client Journey

| Phase | Owner | Input | Output | Duration |
|-------|-------|-------|--------|----------|
| **Lead Gen** | Marketing | Content, Outreach | Qualified Leads | Ongoing |
| **Discovery** | Commercial (Discovery Specialist) | Lead + Signals | Gap Analysis, Stakeholder Map | 1-2 weeks |
| **Proposal** | Commercial (Proposal Specialist) | Gap Analysis | Signed Proposal + Deposit | 1 week |
| **Onboarding** | **Delivery (Onboarding Specialist)** | Signed Contract | Project Kickoff, Access, Plan | 1-2 weeks |
| **Execution** | **Delivery (Project Manager + Tech Lead)** | Project Plan | Working Systems, Artifacts | 4-12 weeks |
| **Quality Assurance** | **Delivery (QA Engineer)** | Working Systems | Validated Systems, Reports | Ongoing |
| **Client Success** | **Delivery (Client Success Manager)** | Validated Systems | Value Realization, Health Score | Ongoing |
| **Expansion** | **Delivery (Expansion Specialist)** | Success Signals | Upsells, Referrals, Case Studies | Ongoing |
| **Invoicing** | Finance | Delivery Milestones | Cash Collection | Per Contract |

---

## 1. SOURCE A Strengths (04_Knowledge)

| Asset | Location | Relevance |
|-------|----------|-----------|
| **Delivery Director Mission** | `Delivery_Director.md` | "Deliver outstanding client outcomes on time" |
| **Owned Areas** | `Delivery_Director.md` | Client Delivery, Project Management, QA, Client Success, Documentation |
| **Commercial Outputs** | `Playbooks/Sales/` | Gap analyses, proposals, stakeholder maps feed Delivery |
| **Operations Support** | `Operations_Director.md` | SOPs, Systems, Automation, Quality for Delivery |
| **Finance Handoff** | `Finance_Director.md` | Cash flow, invoicing, forecasting from Delivery milestones |
| **Commercial Employees** | `Commercial/Employees/` | Produce gap_analysis, stakeholder_map, proposal, pipeline |

**Key Insight:** SOURCE A has **complete upstream context** — Commercial produces everything Delivery needs to start. But no Delivery employees exist to consume it.

---

## 2. SOURCE B Strengths (agency-agents)

| Division | Relevant Agents | Adaptation Needed |
|----------|----------------|-------------------|
| **project-management** | PM specialists, sprint planning, delivery tracking | Adapt to automation delivery, not generic projects |
| **engineering** | DevOps automator, backend architect, SRE, incident response | Internal tools, runtime reliability |
| **testing** | QA engineer, regression testing | Quality gates for automation delivery |
| **support** | Support specialist | Client support, ticketing |
| **engineering** | DevOps automator, backend architect | Technical architecture for client systems |

**Irrelevant:** academic, design, game-development, gis, healthcare, spatial-computing, specialized, paid-media, product, sales

---

## 3. Gap Analysis: What Delivery Must Provide

| Operational Need | Current State | Delivery Must Provide |
|------------------|---------------|----------------------|
| **Client Onboarding** | Ad-hoc | Standardized onboarding flow, access provisioning, kickoff |
| **Project Management** | Ad-hoc | Structured PM: timeline, deliverables, milestones, risks |
| **Technical Delivery** | Ad-hoc | Architecture, implementation, integration, documentation |
| **Quality Assurance** | Ad-hoc | QA gates, testing, validation, acceptance criteria |
| **Client Success** | Ad-hoc | Health monitoring, value realization, renewal prep |
| **Expansion/Referrals** | Ad-hoc | Upsell identification, referral program, case studies |
| **Documentation** | Ad-hoc | Runbooks, handoff docs, training materials |
| **Cross-dept Coordination** | Ad-hoc | Delivery ↔ Commercial, Operations, Finance, Creative |
| **Client Communication** | Ad-hoc | Status reports, executive summaries, escalation paths |

---

## 4. Proposed Delivery Department Structure

### Director: Delivery Director (exists)
Reports to COO. Owns: Client Delivery, Project Management, QA, Client Success, Documentation.

### Employees (6 specialists — each improves ≥2 departments)

| # | Role | Primary Focus | Improves Departments |
|---|------|---------------|---------------------|
| 1 | **Client Onboarding Specialist** | Onboarding, kickoff, access, plan | Commercial, Delivery, Operations |
| 2 | **Project Manager** | Timeline, deliverables, milestones, risks | Delivery, Commercial, Engineering |
| 3 | **Technical Delivery Lead** | Architecture, implementation, integration | Engineering, Delivery, Commercial |
| 4 | **Delivery Quality Engineer** | QA gates, testing, validation, acceptance | Engineering, Delivery, Commercial |
| 5 | **Client Success Manager** | Health monitoring, value realization, renewal | Commercial, Delivery, Finance |
| 6 | **Expansion & Referral Specialist** | Upsell, cross-sell, referrals, case studies | Commercial, Marketing, Delivery |

---

## 6. Implementation Order

| Phase | Employees | Rationale |
|-------|-----------|-----------|
| **1** | Client Onboarding Specialist, Project Manager | Foundation: start projects right, manage execution |
| **2** | Technical Delivery Lead, Delivery Quality Engineer | Execution quality: build right, validate right |
| **3** | Client Success Manager, Expansion & Referral Specialist | Retention & growth: retain, expand, advocate |

---

## 7. Shared Documentation References (No Duplication)

All Delivery employees reference these 04_Knowledge paths:

| Doc | Used By |
|-----|---------|
| `Playbooks/Sales/Sales_Call_Playbook.md` | All (context from Commercial) |
| `Offers/Pricing_Packages.md` | All (scope, tier boundaries) |
| `Company/Target_Market.md` | All (ICP context) |
| `Playbooks/Sales/Objection_Handling.md` | Success, Expansion |
| `Company/Value_Proposition.md` | All (promise alignment) |
| `Operations/SOP_Documentation_Librarian` | All (SOPs for delivery) |
| `Operations/Quality_Reliability_Engineer` | QA, Tech Lead (quality gates) |
| `Operations/Automation_Systems_Coordinator` | Tech Lead (automation delivery) |
| `Finance_Director.md` | PM, Success (invoicing, forecasting) |

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
    "project_management": ["Linear", "Notion"],
    "monitoring": ["Datadog", "Grafana"],
    "documentation": ["Notion", "GitBook"],
    "testing": ["Playwright", "pytest"],        # NEW
    "code_review": ["GitHub", "GitLab"],        # NEW
}
```

---

## 9. Next Steps

1. **Create comparison report** (this document) → commit
2. **Build 6 Delivery employees** using EMPLOYEE_TEMPLATE
3. **Add capabilities** to runtime/capabilities.py
4. **Verify** org discovery, capability routing, executive loop
5. **Commit & push** as single milestone