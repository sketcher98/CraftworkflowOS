# Organization Architecture Comparison Report

**Prepared by:** Chief Organization Architect
**Date:** 2026-07-19
**Sources:** 04_Knowledge (SOURCE A - Primary) + agency-agents (SOURCE B - Reference)

---

## Executive Summary

This report compares CraftworkflowOS's current organization (SOURCE A) against the agency-agents repository (SOURCE B) to identify strengths, gaps, and a roadmap for building a complete, production-ready CraftedWorkflows organization.

**Key Finding:** SOURCE A has strong executive architecture (Director standards, hierarchy, capability routing, memory system) but only Commercial department is partially populated. SOURCE B has 20+ divisions with 100+ deeply detailed specialist agents but lacks the executive orchestration layer. The winning combination is SOURCE A's orchestration + SOURCE B's specialist depth, adapted to CraftedWorkflows' specific business model.

---

## 1. Strengths of CraftworkflowOS (SOURCE A)

| Area | Strength |
|------|----------|
| **Executive Hierarchy** | Clear CEO → COO → Director → Employee chain with enforced delegation rules |
| **Director Standards** | Uniform operating model: inputs, responsibilities, outputs, success criteria |
| **Capability Routing** | Provider registry with browser/GPT/Perplexity, capability-based delegation |
| **Memory Architecture** | 9-layer persistent memory (identity, working, long-term, episodic, skills, reflections, decisions, preferences, checkpoints) |
| **Refresh Policy** | Tiered cache (Hot/Warm/Cold) with file change detection |
| **Boot Sequence** | 13-phase boot with memory integration at Phases 10-13 |
| **Git Hygiene** | Version-controlled docs, working memory excluded |
| **Commercial Department** | 6 employees defined with Profile.md structure (Lead Intelligence, Prospecting, Outreach, Discovery, Proposal, Pipeline) |
| **Playbook Integration** | Departments reference Playbook.md |
| **Knowledge Base** | Structured 04_Knowledge with Company, Playbooks, Offers, Research |

---

## 2. Strengths of agency-agents (SOURCE B)

| Division | Notable Agents (Depth) |
|----------|------------------------|
| **Sales** | 9 agents: Outbound Strategist (signal-based selling, ICP tiering, multi-channel sequences), Discovery Coach (SPIN/Gap/Sandler, AECR objection handling), Deal Strategist, Proposal Strategist, Pipeline Analyst, Account Strategist, Sales Engineer, Coach, Lead Gen Strategist |
| **Marketing** | 30+ agents: SEO Specialist, Email Strategist, LinkedIn Content Creator, Twitter Engager, Podcast Strategist, Short Video Coach, PR Manager, Reddit Builder, TikTok/Reels/Douyin/Kuaishou/Xiaohongshu specialists, Global Podcast Strategist, Cross-border Ecommerce |
| **Engineering** | 60+ agents: Software Architect (DDD, ADRs, architecture patterns), AI Engineer, Backend Architect, DevOps Automator, RAG Pipeline Engineer, Multi-Agent Systems Architect, Prompt Engineer, Incident Response Commander, FinOps Engineer, Code Reviewer, Senior Developer, API Platform Engineer |
| **Finance** | 5 agents: Bookkeeper/Controller, Financial Analyst, FP&A Analyst, Investment Researcher, Tax Strategist |
| **Project Management** | Dedicated division with specialist agents |
| **Paid Media** | Separate division for performance marketing |
| **Product** | Product-focused agents |
| **Design** | Design specialists |
| **Support** | Customer support agents |
| **Testing** | QA/testing specialists |
| **Security** | Security-focused agents |

**SOURCE B Agent Quality:**
- Each agent has: Identity, Core Mission, Frameworks/Methodologies, Rules, Communication Style, Metrics/KPIs, Templates
- Deep domain expertise (e.g., Outbound Strategist has 4-tier signal system, tiered account model, 8-12 touch sequences, email anatomy)
- Practical, battle-tested methodologies

---

## 3. Missing Capabilities (Gap Analysis)

### Departments with NO employees in SOURCE A:
| Department | Required Specialists | Source B Coverage |
|------------|---------------------|-------------------|
| **Marketing** | 0 employees | 30+ agents available |
| **Operations** | 0 employees | Project Management division available |
| **Finance** | 0 employees | 5 agents available |
| **Delivery** | 0 employees | Support + specialized agents available |
| **Creative** | 0 employees | Design division available |
| **Engineering** | Directory exists but empty | 60+ agents available |
| **Intelligence** | Future only | Academic + specialized agents |

### Commercial Department Gaps (SOURCE A has 6, could use more):
| Current | Could Add from SOURCE B |
|---------|------------------------|
| Lead Intelligence Specialist | Sales Engineer, Account Strategist |
| Prospecting Specialist | Deal Strategist |
| Outreach Specialist | Sales Coach |
| Discovery Specialist | Pipeline Analyst (exists) |
| Proposal Specialist | Proposal Strategist (exists) |
| Pipeline Specialist | Sales Account Strategist |

### Cross-Cutting Capabilities Missing:
| Capability | Need |
|------------|------|
| **Competitive Intelligence** | No dedicated employee |
| **Market Research** | No dedicated employee |
| **Customer Success** | No dedicated employee |
| **Technical Implementation** | No engineering employees |
| **Content Production** | No marketing employees |
| **Paid Acquisition** | No paid media employees |
| **Financial Modeling** | No finance employees |
| **Legal/Compliance** | No security/legal employees |

---

## 4. Proposed Improvements

### A. Commercial Department (Enhance Existing)

| Employee | SOURCE A Profile | SOURCE B Enhancement | Action |
|----------|------------------|----------------------|--------|
| **Lead Intelligence Specialist** | Basic profile | Signal-based ICP, tiered account model, 4-tier signal system | Rewrite Profile.md referencing 04_Knowledge/Playbooks/Outreach/ |
| **Prospecting Specialist** | Basic profile | Multi-channel sequence design, channel selection by persona | Enhance with sequence architecture |
| **Outreach Specialist** | Basic profile | Cold email anatomy, reply rate benchmarks, follow-up discipline | Add signal-based frameworks |
| **Discovery Specialist** | Basic profile | SPIN + Gap Selling + Sandler, AECR objection handling, 30-min call structure | Full methodology integration |
| **Proposal Specialist** | Basic profile | Proposal architecture, pricing psychology, guarantee design | Add offer stack templates |
| **Pipeline Specialist** | Basic profile | Pipeline health metrics, stage conversion, forecasting | Add forecasting methodology |

**New Commercial Employees to Create:**
- **Sales Engineer** — Technical discovery, solution architecture, proof-of-concept design (from agency-agents)
- **Account Strategist** — Multi-threaded enterprise deals, champion development (from agency-agents)
- **Deal Strategist** — Complex deal architecture, negotiation, legal/commercial terms (from agency-agents)

### B. Marketing Department (Build from Scratch)

| Employee | Source B Inspiration | CraftedWorkflows Adaptation |
|----------|---------------------|----------------------------|
| **Content Strategist** | marketing-content-creator, marketing-linkedin-content-creator | Use 04_Knowledge/Playbooks/Marketing/Content_Pillars.md (4 pillars) |
| **SEO Specialist** | marketing-seo-specialist | Focus on agency/consultant keywords |
| **Email Strategist** | marketing-email-strategist | Nurture sequences for Automation Escape Audit funnel |
| **Short Video Coach** | marketing-short-video-editing-coach | Goat Farmer parables for TikTok/Reels/Shorts |
| **Podcast Strategist** | marketing-podcast-strategist | Guest appearances, own show for authority |
| **PR/Communications Manager** | marketing-pr-communications-manager | Thought leadership placement |
| **LinkedIn Content Creator** | marketing-linkedin-content-creator | Founder brand, belief content |
| **Twitter Engager** | marketing-twitter-engager | DM flow execution, reply mining |

### C. Operations Department (Build from Scratch)

| Employee | Source B Inspiration | CraftedWorkflows Adaptation |
|----------|---------------------|----------------------------|
| **SOP Architect** | project-management division | Document all processes in 04_Knowledge/SOPs/ |
| **Systems Automator** | engineering-devops-automator | Internal tooling, Make.com/Zapier/n8n workflows |
| **Documentation Engineer** | engineering-technical-writer | Maintain runtime docs, API docs, runbooks |
| **Internal Ops Specialist** | project-management | Meeting rhythms, OKRs, retrospectives |
| **Knowledge Manager** | academic division | Curate 04_Knowledge, manage ingestion pipeline |

### D. Finance Department (Build from Scratch)

| Employee | Source B Inspiration | CraftedWorkflows Adaptation |
|----------|---------------------|----------------------------|
| **FP&A Analyst** | finance-fpa-analyst | Revenue forecasting, unit economics, cohort analysis |
| **Bookkeeper/Controller** | finance-bookkeeper-controller | AP/AR, reconciliation, monthly close |
| **Pricing Strategist** | finance-financial-analyst + sales-proposal-strategist | Tier pricing, discount authority, margin optimization |
| **Cash Flow Manager** | finance-fpa-analyst | Runway, collections, vendor payments |
| **Tax Strategist** | finance-tax-strategist | R&D credits, entity structure, compliance |

### E. Delivery Department (Build from Scratch)

| Employee | Source B Inspiration | CraftedWorkflows Adaptation |
|----------|---------------------|----------------------------|
| **Client Onboarding Specialist** | support division | 30-day sprint execution, kickoff, milestone tracking |
| **Project Manager** | project-management division | Delivery timeline, resource allocation, status reporting |
| **QA Specialist** | testing division | Automation testing, delivery checklists |
| **Client Success Manager** | support division | Renewal, expansion, NPS, reference generation |
| **Technical Delivery Lead** | engineering-sre + engineering-devops-automator | Infrastructure handoff, monitoring, runbooks |

### F. Creative Department (Build from Scratch)

| Employee | Source B Inspiration | CraftedWorkflows Adaptation |
|----------|---------------------|----------------------------|
| **Brand Designer** | design division | Visual identity, Goat Farmer aesthetics |
| **UI/UX Designer** | design division | Client portal, dashboards, audit reports |
| **Video Editor** | marketing-short-video-editing-coach | Social clips, case study videos, Loom-style content |
| **Presentation Designer** | design division | Proposals, pitch decks, audit deliverables |
| **Motion Graphics** | marketing-short-video-editing-coach | Animated explainers, social proof assets |

### G. Engineering Department (Build from Scratch)

| Employee | Source B Inspiration | CraftedWorkflows Adaptation |
|----------|---------------------|----------------------------|
| **Software Architect** | engineering-software-architect | Extend runtime architecture, ADRs, domain modeling |
| **AI/ML Engineer** | engineering-ai-engineer + engineering-rag-pipeline-engineer | Provider integrations, prompt engineering, RAG |
| **Backend Engineer** | engineering-backend-architect | API, database, auth, queueing |
| **DevOps/Platform Engineer** | engineering-devops-automator + engineering-sre | CI/CD, infra, monitoring, secrets |
| **Automation Engineer** | engineering-devops-automator | n8n/Make.com/Zapier builds for clients |
| **Prompt Engineer** | engineering-prompt-engineer | System prompts, few-shot libraries, eval harnesses |
| **Full Stack Engineer** | engineering-senior-developer | Client portals, internal tools, integrations |

---

## 5. Implementation Order

### Phase 1: Commercial Completion (Week 1)
**Priority:** Revenue-critical
- [ ] Enhance 6 existing Commercial employees with SOURCE B methodologies
- [ ] Add 3 new Commercial employees (Sales Engineer, Account Strategist, Deal Strategist)
- [ ] Link all to 04_Knowledge playbooks (Outreach, Sales, Offers)
- [ ] Verify capability routing works for each

### Phase 2: Marketing Department (Week 2)
**Priority:** Pipeline generation
- [ ] Create 8 Marketing employees
- [ ] Each references 04_Knowledge/Playbooks/Marketing/
- [ ] Content Strategist owns Content_Pillars.md
- [ ] SEO/Email/Video specialists for funnel support
- [ ] LinkedIn/Twitter specialists for DM flow execution

### Phase 3: Operations Department (Week 3)
**Priority:** Operational excellence
- [ ] Create 5 Operations employees
- [ ] SOP Architect owns 04_Knowledge/SOPs/
- [ ] Systems Automator builds internal automations
- [ ] Knowledge Manager owns Inbox processing pipeline

### Phase 4: Finance Department (Week 4)
**Priority:** Business health
- [ ] Create 5 Finance employees
- [ ] FP&A owns forecasting, unit economics
- [ ] Pricing Strategist owns tier logic
- [ ] Controller owns monthly close

### Phase 5: Delivery Department (Week 5)
**Priority:** Client success
- [ ] Create 5 Delivery employees
- [ ] Onboarding Specialist owns 30-day sprint
- [ ] PM owns delivery timeline
- [ ] CSM owns renewal/expansion

### Phase 6: Creative Department (Week 6)
**Priority:** Brand & deliverables
- [ ] Create 5 Creative employees
- [ ] Brand Designer owns Goat Farmer visual language
- [ ] Video Editor for social proof content
- [ ] Presentation Designer for proposals/audits

### Phase 7: Engineering Department (Week 7)
**Priority:** Platform scaling
- [ ] Create 7 Engineering employees
- [ ] Architect extends runtime (not replace)
- [ ] AI Engineer owns provider integrations
- [ ] Automation Engineer builds client deliverables

### Phase 8: Cross-Department Integration (Week 8)
- [ ] Director delegation testing
- [ ] End-to-end workflow: CEO goal → Commercial briefing → Marketing content → Operations SOPs → Delivery kickoff → Finance forecast
- [ ] Memory integration verification
- [ ] Checkpoint/restore testing

---

## 6. Architecture Principles (Non-Negotiable)

| Principle | Enforcement |
|-----------|-------------|
| **Documentation > Memory** | Employees reference 04_Knowledge via relative links; memory only stores learned patterns/decisions |
| **Capability Routing** | Employees declare capabilities; router selects provider (Browser/GPT/Perplexity) |
| **Director Delegation** | Directors never do specialist work; they delegate, review, report |
| **Executive Hierarchy** | CEO → COO → Director → Employee (no bypassing) |
| **Git Hygiene** | Working memory, checkpoints, cache excluded; docs versioned |
| **Refresh Policy** | Hot (1hr), Warm (15min), Cold (manual) — file change detection |
| **Boot Sequence** | Memory loads at Phases 10-13; runtime context hydrated |
| **Playbook-Driven** | Every employee has Playbook.md reference; executes plays, not improvises |

---

## 7. Next Steps

1. **Approve this comparison report**
2. **Begin Phase 1: Commercial Completion** — enhance existing 6, add 3 new
3. **Establish employee template** — standard Profile.md structure with all required fields
4. **Create first enhanced Commercial employee** as pattern for all others
5. **Verify runtime integration** — capability routing, delegation, memory writes

---

## Appendix: Standard Employee Profile Template

```markdown
# [Employee Name]

## Role
[Title]

## Department
[Department]

## Reports To
[Director Name]

## Responsibilities
- [ ] Primary responsibility 1
- [ ] Primary responsibility 2
- [ ] Primary responsibility 3

## Inputs
- From 04_Knowledge: [specific files]
- From memory: [client intelligence, preferences, decisions]
- From runtime: [context, checkpoints, working memory]

## Outputs
- [Artifact 1] → stored at [path]
- [Artifact 2] → stored at [path]
- Memory writes: [what gets written to which layer]

## KPIs
- Metric 1: Target
- Metric 2: Target
- Metric 3: Target

## Tools / Capabilities
- capability: [research|writing|analysis|etc.]
- provider: [browser|gpt|perplexity|auto]

## Authority
- Can decide: [scope]
- Must escalate: [scope]
- Can delegate to: [none - specialists don't delegate]

## Escalation Path
- First: [Director Name]
- Second: [COO]
- Final: [CEO]

## Memory Usage
- Reads: [which layers, what keys]
- Writes: [which layers, what keys, triggers]

## Playbooks
- Primary: [04_Knowledge/Playbooks/...]
- Secondary: [04_Knowledge/Playbooks/...]
- Reference: [04_Knowledge/Company/...]

## Capabilities Declaration
```yaml
capabilities:
  - name: "capability_name"
    description: "what this capability does"
    provider_preference: "auto|browser|gpt|perplexity"
    required_context: ["key1", "key2"]
```

---