# CraftworkflowOS Runtime Configuration - Phase 7

## Provider Status (Production Environment)

| Provider | Status | Capability | Notes |
|----------|--------|------------|-------|
| **HubSpot** | ❌ UNAVAILABLE | crm | Legacy FyreStrokeDigital account - DO NOT USE |
| **Notion** | ✅ ACTIVE | crm, document | Primary CRM & operational workspace |
| **Airtable** | ✅ ACTIVE | crm | Fallback CRM |
| **Pipedrive** | ⚠️ STANDBY | crm | Available if configured |
| **GitHub** | ✅ ACTIVE | storage, automation | Source of truth |
| **Gmail** | ✅ ACTIVE | email | Communication |
| **Google Calendar** | ✅ ACTIVE | calendar | Scheduling |
| **Composio** | ✅ ACTIVE | automation | Tool abstraction layer |
| **NVIDIA NIM** | ✅ ACTIVE | writing, analysis, coding | reasoning, cost-free |
| **Groq** | ✅ ACTIVE | writing, analysis, coding | Low latency (800ms), API key available |
| **OpenRouter** | ✅ ACTIVE | writing, analysis, coding | Cost-optimized, API key available |
| **Perplexity** | ✅ ACTIVE | research, search | Deep research |
| **Browser** | ✅ ACTIVE | search, research | Quick search (Serper) |
| **GPT-4o** | ✅ ACTIVE | writing, analysis, coding | High quality |
| **Claude 3.5 Sonnet** | ✅ ACTIVE | writing, analysis, coding | Complex reasoning |
| **Figma** | ✅ ACTIVE | design | UI/UX design |
| **Premiere** | ✅ ACTIVE | video_editing | Professional video |
| **HeyGen** | ✅ ACTIVE | video_editing | Avatar videos |
| **VEED** | ✅ ACTIVE | video_editing | Quick social video |
| **Make** | ✅ ACTIVE | automation | Workflow automation |
| **n8n** | ⚠️ STANDBY | automation | Available if configured |
| **Zapier** | ⚠️ STANDBY | automation | Available if configured |
| **Google Docs** | ✅ ACTIVE | document | Collaborative docs |
| **Google Drive** | ✅ ACTIVE | storage | File storage |
| **Dropbox** | ⚠️ STANDBY | storage | Available if configured |
| **Cloudinary** | ⚠️ STANDBY | storage | Available if configured |
| **S3** | ⚠️ STANDBY | storage | Available if configured |
| **Playwright** | ✅ ACTIVE | testing | E2E testing |
| **pytest** | ✅ ACTIVE | testing | Unit testing |
| **Vitest** | ✅ ACTIVE | testing | Frontend testing |

---

## CRM Strategy

**Primary**: Notion (capability: `crm`)
**Fallback**: Airtable (capability: `crm`)
**Future**: HubSpot (when dedicated workspace connected)

**Routing Rule**: `CRM.primary` → Notion, `CRM.fallback` → Airtable

Employees **must** request the `crm` capability — never HubSpot directly.
The runtime router selects the provider based on availability and health.

---

## Capability Routing (Updated)

| Capability | Primary Provider | Fallback(s) | Cost-Optimized | Low-Latency |
|------------|-----------------|-------------|----------------|-------------|
| research | Perplexity | Browser, Exa | - | Browser |
| writing | GPT-4o | Claude, Groq | OpenRouter | Groq |
| analysis | GPT-4o | Claude, Groq | OpenRouter | NVIDIA NIM |
| coding | Groq | Claude, GPT-4o | OpenRouter | Groq |
| design | Figma | - | - | - |
| video_editing | Premiere | HeyGen, VEED | VEED | VEED |
| automation | Make | n8n, Zapier | - | - |
| crm | **Notion** | Airtable | - | - |
| email | Gmail | SendGrid, Mailgun | - | - |
| search | Browser | Perplexity, Exa | Browser | Browser |
| calendar | Google Calendar | Calendly | - | - |
| document | Google Docs | Notion, Pandoc | - | - |
| storage | Google Drive | Dropbox, Cloudinary, S3 | - | - |
| testing | Playwright | pytest, Vitest | - | - |

---

## Notion Database Schemas

### 1. Leads
**Owner**: Commercial / Lead Intelligence Specialist

| Property | Type | Required | Options / Notes |
|----------|------|----------|-----------------|
| Lead ID | Title | ✅ | Auto: LD-{timestamp} |
| Name | Rich Text | ✅ | Full name |
| Email | Email | ✅ | |
| Phone | Phone | | |
| Company | Relation | | → Companies |
| Source | Select | ✅ | Inbound, Outbound, Referral, Event, Organic |
| Status | Select | ✅ | New, Qualified, Contacted, Disqualified, Converted |
| Score | Number | | 0-100 |
| ICP Tier | Select | | Tier 1, Tier 2, Tier 3 |
| Assigned To | Person | | Commercial team |
| Created Date | Created Time | ✅ | |
| Last Contact | Date | | |
| Next Action | Rich Text | | |
| Notes | Rich Text | | |
| HubSpot ID | Rich Text | | Migration field |

**Views**: 
- All Leads (table)
- By Status (board/kanban)
- By Assignee (table)
- High Score (>70) (table)
- This Week (calendar by Created Date)

**Templates**:
- New Outbound Lead
- Inbound Inquiry
- Referral Lead

**Automations**:
- On Status → "Qualified": Create Opportunity, notify assigned
- On Score > 70 & Status = "New": Auto-assign to Prospecting Specialist
- Daily: Stale leads (>7 days no contact) → escalate to Pipeline Manager

---

### 2. Companies
**Owner**: Commercial / Account Strategist

| Property | Type | Required | Options / Notes |
|----------|------|----------|-----------------|
| Company ID | Title | ✅ | Auto: CO-{timestamp} |
| Name | Rich Text | ✅ | |
| Domain | URL | | |
| Industry | Select | | Agency, Consultancy, SaaS, E-commerce, Other |
| Size | Select | | 1-10, 11-50, 51-200, 201-500, 500+ |
| Location | Rich Text | | City, Country |
| Annual Revenue | Number | | USD |
| Website | URL | | |
| LinkedIn | URL | | |
| Status | Select | ✅ | Prospect, Lead, Customer, Churned |
| Owner | Person | | |
| Created Date | Created Time | ✅ | |
| Last Updated | Last Edited Time | ✅ | |
| HubSpot ID | Rich Text | | Migration field |
| Notes | Rich Text | | |

**Views**: By Status, By Industry, By Owner, By Size, Active Customers

**Templates**: New Prospect Company, New Customer Company

**Automations**:
- On Status → "Customer": Create Client record, notify Delivery Director
- On new Company: Auto-create primary Contact if email found

---

### 3. Contacts
**Owner**: Commercial / Sales Engineer

| Property | Type | Required | Options / Notes |
|----------|------|----------|-----------------|
| Contact ID | Title | ✅ | Auto: CT-{timestamp} |
| First Name | Rich Text | ✅ | |
| Last Name | Rich Text | ✅ | |
| Email | Email | ✅ | |
| Phone | Phone | | |
| Title | Rich Text | | |
| Company | Relation | ✅ | → Companies |
| Lead | Relation | | → Leads |
| Status | Select | ✅ | Active, Inactive, Do Not Contact |
| Owner | Person | | |
| Created Date | Created Time | ✅ | |
| Last Contact | Date | | |
| HubSpot ID | Rich Text | | Migration field |
| Notes | Rich Text | | |

**Views**: By Company, By Status, By Owner, Active Only

**Templates**: New Contact, Decision Maker, Champion

---

### 4. Opportunities
**Owner**: Commercial / Pipeline Manager / Deal Strategist

| Property | Type | Required | Options / Notes |
|----------|------|----------|-----------------|
| Opportunity ID | Title | ✅ | Auto: OP-{timestamp} |
| Name | Rich Text | ✅ | e.g., "Acme Corp - Goldilocks" |
| Company | Relation | ✅ | → Companies |
| Contact | Relation | | → Contacts |
| Lead | Relation | | → Leads |
| Stage | Select | ✅ | Discovery, Qualification, Proposal, Negotiation, Closed Won, Closed Lost |
| Amount | Number | | USD |
| Probability | Number | | 0-100% |
| Expected Close | Date | | |
| Actual Close | Date | | |
| Product | Select | | Jumpstart, Goldilocks, Visionary, Custom |
| Owner | Person | ✅ | |
| Created Date | Created Time | ✅ | |
| Last Updated | Last Edited Time | ✅ | |
| HubSpot Deal ID | Rich Text | | Migration field |
| Notes | Rich Text | | |

**Views**:
- Pipeline (board by Stage)
- By Owner
- Forecast (Probability × Amount)
- This Quarter Close
- Won / Lost Analysis

**Templates**: New Opportunity, Renewal, Upsell

**Automations**:
- On Stage → "Proposal": Trigger Proposal Specialist
- On Stage → "Closed Won": Create Client, Project, notify Finance (Revenue Ops), Delivery
- On Stage → "Closed Lost": Log reason, notify Pipeline Manager
- Daily: Stale opportunities (>14 days no activity) → alert Owner

---

### 5. Sales Calls
**Owner**: Commercial / Discovery Specialist / Proposal Specialist

| Property | Type | Required | Options / Notes |
|----------|------|----------|-----------------|
| Call ID | Title | ✅ | Auto: SC-{timestamp} |
| Date | Date | ✅ | |
| Time | Rich Text | | HH:MM |
| Duration | Number | | Minutes |
| Type | Select | ✅ | Discovery, Demo, Proposal Review, Negotiation, Follow-up, QBR |
| Lead | Relation | | → Leads |
| Contact | Relation | | → Contacts |
| Company | Relation | | → Companies |
| Opportunity | Relation | | → Opportunities |
| Outcome | Select | ✅ | Scheduled, Completed, No Show, Cancelled, Rescheduled |
| Recording URL | URL | | |
| Transcript | Rich Text | | |
| Key Insights | Rich Text | | |
| Action Items | Rich Text | | |
| Next Steps | Rich Text | | |
| Owner | Person | ✅ | |
| HubSpot Activity ID | Rich Text | | Migration field |

**Views**: By Date (calendar), By Type, By Owner, By Outcome, This Week

**Templates**: Discovery Call, Demo Call, Proposal Review, QBR

**Automations**:
- On Outcome → "Completed": Update Opportunity Last Contact, create Tasks from Action Items
- On Type = "Discovery": Link to Lead Qualification playbook

---

### 6. Proposals
**Owner**: Commercial / Proposal Specialist

| Property | Type | Required | Options / Notes |
|----------|------|----------|-----------------|
| Proposal ID | Title | ✅ | Auto: PR-{timestamp} |
| Title | Rich Text | ✅ | |
| Opportunity | Relation | ✅ | → Opportunities |
| Company | Relation | ✅ | → Companies |
| Contact | Relation | | → Contacts |
| Stage | Select | ✅ | Draft, Sent, Viewed, Negotiating, Accepted, Rejected, Expired |
| Tier | Select | | Jumpstart, Goldilocks, Visionary, Custom |
| Amount | Number | | USD |
| Sent Date | Date | | |
| Viewed Date | Date | | |
| Response Date | Date | | |
| Expiry Date | Date | | |
| Document URL | URL | | Notion page / Google Doc |
| Owner | Person | ✅ | |
| HubSpot Deal ID | Rich Text | | Migration field |
| Notes | Rich Text | | |

**Views**: By Stage, By Owner, Pending Response, This Month

**Templates**: Jumpstart Proposal, Goldilocks Proposal, Visionary Proposal, Custom Proposal

**Automations**:
- On Stage → "Sent": Set Sent Date, notify Prospecting for follow-up
- On Stage → "Viewed": Set Viewed Date, alert Owner
- On Stage → "Accepted": Trigger Opportunity → "Closed Won"
- On Stage → "Rejected": Trigger Opportunity → "Closed Lost"
- Expiry Date passed & Stage ≠ Accepted/Rejected → "Expired", alert Owner

---

### 7. Clients
**Owner**: Delivery / Client Success Manager

| Property | Type | Required | Options / Notes |
|----------|------|----------|-----------------|
| Client ID | Title | ✅ | Auto: CL-{timestamp} |
| Name | Rich Text | ✅ | |
| Company | Relation | ✅ | → Companies |
| Primary Contact | Relation | ✅ | → Contacts |
| Status | Select | ✅ | Onboarding, Active, At Risk, Churned, Alumni |
| Tier | Select | | Jumpstart, Goldilocks, Visionary, Custom |
| Monthly Value | Number | | USD |
| Contract Start | Date | | |
| Contract End | Date | | |
| Renewal Date | Date | | |
| Health Score | Number | | 0-100 |
| CSM | Person | | Client Success Manager |
| HubSpot Company ID | Rich Text | | Migration field |
| Notes | Rich Text | | |

**Views**: By Status, By Tier, By CSM, Renewals Due (next 90 days), Health < 70

**Templates**: New Client Onboarding, Renewal Review, QBR Prep

**Automations**:
- On Status → "Active": Create initial Project, notify Delivery Director
- On Health Score < 60: Alert CSM, create "At Risk" task
- 90 days before Renewal: Create Renewal Opportunity, notify Account Strategist
- Monthly: Health Score review for all Active clients

---

### 8. Projects
**Owner**: Delivery / Project Manager

| Property | Type | Required | Options / Notes |
|----------|------|----------|-----------------|
| Project ID | Title | ✅ | Auto: PJ-{timestamp} |
| Name | Rich Text | ✅ | |
| Client | Relation | ✅ | → Clients |
| Type | Select | | Implementation, Optimization, Migration, Support, Custom |
| Status | Select | ✅ | Planning, Active, On Hold, Completed, Cancelled |
| Progress | Number | | 0-100% |
| Start Date | Date | | |
| Target End | Date | | |
| Actual End | Date | | |
| Budget | Number | | USD |
| Spent | Number | | USD |
| PM | Person | ✅ | Project Manager |
| Team | Person (multi) | | Delivery team |
| HubSpot Project ID | Rich Text | | Migration field |
| Notes | Rich Text | | |

**Views**: By Status, By PM, By Client, Timeline (Gantt), Budget vs Spent

**Templates**: Implementation Project, Optimization Sprint, Migration Project, Support Retainer

**Automations**:
- On Status → "Active": Create default Task templates, notify team
- On Progress = 100% & Status ≠ "Completed" → auto-set "Completed"
- Weekly: Budget > 80% spent → alert PM and Finance

---

### 9. Tasks
**Owner**: All Departments (each owns their tasks)

| Property | Type | Required | Options / Notes |
|----------|------|----------|-----------------|
| Task ID | Title | ✅ | Auto: TK-{timestamp} |
| Title | Rich Text | ✅ | |
| Description | Rich Text | | |
| Project | Relation | | → Projects |
| Client | Relation | | → Clients |
| Assignee | Person | ✅ | |
| Status | Select | ✅ | Backlog, Ready, In Progress, Review, Done, Blocked |
| Priority | Select | ✅ | Low, Medium, High, Critical |
| Due Date | Date | | |
| Estimated Hours | Number | | |
| Actual Hours | Number | | |
| Sprint | Rich Text | | Sprint name/number |
| Tags | Multi-select | | |
| Created Date | Created Time | ✅ | |
| Completed Date | Date | | |
| HubSpot Task ID | Rich Text | | Migration field |

**Views**: By Assignee (board), By Status (kanban), By Project, By Sprint, My Tasks, Overdue, This Week

**Templates**: Standard Task, Bug, Feature, Review, Meeting Prep

**Automations**:
- On Status → "Done": Set Completed Date, update Project Progress
- On Status → "Blocked": Notify Assignee + PM
- Daily: Overdue tasks → daily digest to Assignee
- On Task created with Project: Auto-link to Project's Sprint if Sprint field matches

---

### 10. Knowledge Base
**Owner**: Operations / SOP Documentation Librarian

| Property | Type | Required | Options / Notes |
|----------|------|----------|-----------------|
| KB ID | Title | ✅ | Auto: KB-{timestamp} |
| Title | Rich Text | ✅ | |
| Category | Select | ✅ | Company, Playbooks, SOPs, Offers, Research, Frameworks, Templates, Competitive Intel, Market Intel, Case Studies, Prompts |
| Subcategory | Select | | Per Category (e.g., Playbooks: Outreach, Marketing, Sales) |
| Status | Select | ✅ | Draft, Review, Published, Archived |
| Version | Number | | |
| Owner | Person | | |
| Reviewer | Person | | |
| Approved By | Person | | |
| Approved Date | Date | | |
| Review Date | Date | | Next review due |
| Document URL | URL | | Notion page / Google Doc |
| Tags | Multi-select | | |
| Applies To | Multi-select | | Leads, Companies, Contacts, Opportunities, Clients, Projects |
| HubSpot ID | Rich Text | | Migration field |

**Views**: By Category, By Status, By Owner, Needs Review (Review Date passed), Published Only

**Templates**: New SOP, New Playbook, New Framework, Research Note, Competitive Intel

**Automations**:
- On Status → "Published": Notify relevant department leads
- On Review Date passed: Alert Owner + Reviewer
- Quarterly: Audit all Published docs for freshness

---

### 11. SOPs
**Owner**: Operations / SOP Documentation Librarian (specialized from Knowledge Base)

| Property | Type | Required | Options / Notes |
|----------|------|----------|-----------------|
| SOP ID | Title | ✅ | Auto: SOP-{timestamp} |
| Title | Rich Text | ✅ | |
| Category | Select | ✅ | Sales, Marketing, Delivery, Operations, Finance, HR, Technical |
| Status | Select | ✅ | Draft, Review, Approved, Published, Archived |
| Version | Number | ✅ | |
| Owner | Person | ✅ | |
| Reviewer | Person | | |
| Approved By | Person | | |
| Approved Date | Date | | |
| Review Date | Date | | Next review due |
| Document URL | URL | | Notion page |
| Tags | Multi-select | | |
| Applies To | Multi-select | | Leads, Companies, Contacts, Opportunities, Clients, Projects |
| HubSpot ID | Rich Text | | Migration field |

**Views**: By Category, By Status, By Owner, Needs Review, Published by Category

**Templates**: Standard SOP, Emergency Procedure, Onboarding SOP, Compliance SOP

**Automations**:
- On Status → "Approved": Auto-increment Version, set Approved Date
- On Review Date passed: Alert Owner + Reviewer
- Monthly: Check for SOPs with no review in 90 days

---

### 12. Executive Dashboard
**Owner**: Executive Team / COO

| Property | Type | Required | Options / Notes |
|----------|------|----------|-----------------|
| Dashboard ID | Title | ✅ | Auto: EXEC-{timestamp} |
| Period | Select | ✅ | Daily, Weekly, Monthly, Quarterly |
| Period Start | Date | ✅ | |
| Period End | Date | ✅ | |
| Revenue | Number | | USD |
| Pipeline Value | Number | | USD |
| Deals Closed | Number | | |
| Deals Lost | Number | | |
| New Leads | Number | | |
| Qualified Leads | Number | | |
| Active Clients | Number | | |
| Churned Clients | Number | | |
| Avg Health Score | Number | | 0-100 |
| Projects On Track | Number | | |
| Projects At Risk | Number | | |
| Cash Flow | Number | | USD |
| Runway | Number | | Months |
| Notes | Rich Text | | Key insights, decisions |
| Prepared By | Person | ✅ | |
| Created Date | Created Time | ✅ | |

**Views**: Current Period, Historical (table by Period), Trend Charts

**Templates**: Daily Standup Dashboard, Weekly Executive Summary, Monthly Board Pack, Quarterly Review

**Automations**:
- Daily 6 AM: Generate Daily Dashboard from live data
- Weekly Monday 8 AM: Generate Weekly Dashboard
- Monthly 1st 9 AM: Generate Monthly Dashboard
- Quarterly: Generate Quarterly Dashboard + trigger Board Pack creation

---

## Workflow Definitions

### WF-01: Lead Discovery → Qualification
**Trigger**: Scheduled (daily 8 AM) or Manual
**Owner**: Commercial / Lead Intelligence Specialist

| Step | Input | Tool Call | Output | Event |
|------|-------|-----------|--------|-------|
| 1. Discover | ICP criteria | `crm` search (Notion) + `research` (Perplexity) | Raw leads | `lead.discovered` |
| 2. Enrich | Raw leads | `research` (Perplexity) + `search` (Browser) | Enriched leads | `lead.enriched` |
| 3. Score | Enriched leads | `analysis` (GPT-4o) | Scored leads | `lead.scored` |
| 4. Create | Scored leads ≥ threshold | `crm` create (Notion Leads DB) | Lead records | `lead.created` |
| 5. Assign | New leads | `crm` update (Notion) | Assigned leads | `lead.assigned` |

**Artifacts**: Lead Intelligence Report, Scored Lead List
**Retry**: 3x with exponential backoff on API failures
**Failure**: Alert Lead Intelligence Specialist, log to dead letter queue

---

### WF-02: Outbound Outreach
**Trigger**: New qualified leads available (event: `lead.assigned`)
**Owner**: Commercial / Prospecting Specialist

| Step | Input | Tool Call | Output | Event |
|------|-------|-----------|--------|-------|
| 1. Select | Assigned leads | `crm` query (Notion) | Lead batch | - |
| 2. Message | Lead + Playbook | `writing` (GPT-4o) | DM messages | `message.generated` |
| 3. Send | Messages | `email` (Gmail) / LinkedIn (manual) | Sent confirmations | `message.sent` |
| 4. Track | Sent messages | `crm` update (Notion) | Updated leads | `outreach.tracked` |

**Artifacts**: Outreach Messages, Send Confirmations
**Retry**: 2x on send failure
**Failure**: Log failure, re-queue for next batch

---

### WF-03: Discovery Call → Qualification
**Trigger**: Lead responds / Meeting scheduled (event: `meeting.scheduled`)
**Owner**: Commercial / Discovery Specialist

| Step | Input | Tool Call | Output | Event |
|------|-------|-----------|--------|-------|
| 1. Prep | Lead + Company | `crm` query (Notion) + `research` (Perplexity) | Pre-call brief | `call.prepped` |
| 2. Conduct | Pre-call brief | Human (Zoom/Meet) | Call notes, recording | `call.completed` |
| 3. Log | Call notes | `crm` create (Notion Sales Calls) | Call record | `call.logged` |
| 4. Qualify | Call insights | `analysis` (Claude) | Qualification score | `lead.qualified` |
| 5. Decision | Score + criteria | Human decision | Qualified / Disqualified | `qualification.decided` |
| 6. Create Opp | If Qualified | `crm` create (Notion Opportunities) | Opportunity | `opportunity.created` |

**Artifacts**: Pre-call Brief, Call Recording, Qualification Analysis
**Retry**: N/A (human step)
**Failure**: Escalate to Pipeline Manager

---

### WF-04: Proposal Generation
**Trigger**: Opportunity Stage → "Proposal" (event: `opportunity.stage_changed`)
**Owner**: Commercial / Proposal Specialist

| Step | Input | Tool Call | Output | Event |
|------|-------|-----------|--------|-------|
| 1. Gather | Opportunity + Client | `crm` query (Notion) | Context bundle | - |
| 2. Draft | Context + Pricing | `writing` (GPT-4o) | Proposal draft | `proposal.drafted` |
| 3. Review | Draft | Human (Proposal Specialist) | Approved proposal | `proposal.approved` |
| 4. Create | Approved | `document` (Notion/Google Docs) | Proposal doc | `proposal.created` |
| 5. Send | Proposal doc | `email` (Gmail) + `crm` update (Notion) | Sent confirmation | `proposal.sent` |

**Artifacts**: Proposal Draft, Final Proposal Document
**Retry**: 2x on document creation
**Failure**: Alert Proposal Specialist, fallback to manual

---

### WF-05: Deal Close → Client Onboarding
**Trigger**: Opportunity Stage → "Closed Won" (event: `deal.closed_won`)
**Owner**: Delivery / Client Onboarding Specialist / Finance

| Step | Input | Tool Call | Output | Event |
|------|-------|-----------|--------|-------|
| 1. Create Client | Opportunity | `crm` create (Notion Clients) | Client record | `client.created` |
| 2. Create Project | Client + Scope | `crm` create (Notion Projects) | Project record | `project.created` |
| 3. Create Tasks | Project template | `crm` create (Notion Tasks) | Task list | `tasks.created` |
| 4. Invoice | Client + Amount | `crm` create (Notion) + Finance system | Invoice | `invoice.created` |
| 5. Welcome | Client + Project | `email` (Gmail) + Calendar | Welcome packet | `onboarding.started` |
| 6. Notify | All stakeholders | `email` (Gmail) + Slack | Notifications | `team.notified` |

**Artifacts**: Client Record, Project Plan, Task List, Invoice, Welcome Packet
**Retry**: 3x on all API calls
**Failure**: Rollback created records, alert COO, manual intervention

---

### WF-06: Project Delivery → QA → Completion
**Trigger**: Project Status → "Active" (event: `project.started`)
**Owner**: Delivery / Project Manager / QA Engineer

| Step | Input | Tool Call | Output | Event |
|------|-------|-----------|--------|-------|
| 1. Plan | Project scope | Human + `crm` query | Delivery plan | `delivery.planned` |
| 2. Execute | Plan + Tasks | Human + `automation` (Make) | Deliverables | `deliverable.created` |
| 3. QA | Deliverables | `testing` (Playwright) + Human | QA report | `qa.completed` |
| 4. Review | QA report | Human (PM + Client) | Approval / Changes | `delivery.reviewed` |
| 5. Complete | Approval | `crm` update (Notion) | Completed project | `project.completed` |

**Artifacts**: Delivery Plan, Deliverables, QA Report, Client Approval
**Retry**: Per-task retry policies
**Failure**: Escalate to Delivery Director

---

### WF-07: Client Health Monitoring
**Trigger**: Scheduled (weekly Monday) or Event (health score change)
**Owner**: Delivery / Client Success Manager

| Step | Input | Tool Call | Output | Event |
|------|-------|-----------|--------|-------|
| 1. Collect | All active clients | `crm` query (Notion) | Client list | - |
| 2. Score | Client data + Usage | `analysis` (GPT-4o) | Health scores | `health.scored` |
| 3. Update | Scores | `crm` update (Notion Clients) | Updated records | `health.updated` |
| 4. Alert | Scores < 70 | `email` (Gmail) + `crm` create (Tasks) | At-risk alerts | `health.alert` |
| 5. QBR Prep | Quarterly clients | `crm` query + `document` | QBR deck | `qbr.prepared` |

**Artifacts**: Health Scores, At-Risk Alerts, QBR Decks
**Retry**: 2x
**Failure**: Log, continue with remaining clients

---

### WF-08: Expansion & Referral Detection
**Trigger**: Health score > 85 + Usage growth, or Event (client mentions need)
**Owner**: Delivery / Expansion & Referral Specialist

| Step | Input | Tool Call | Output | Event |
|------|-------|-----------|--------|-------|
| 1. Detect | Health + Usage + Signals | `analysis` (Claude) | Expansion signals | `expansion.detected` |
| 2. Qualify | Signals + Context | Human (Expansion Specialist) | Qualified opportunity | `expansion.qualified` |
| 3. Create Opp | Qualified | `crm` create (Notion Opportunities) | Opportunity | `opportunity.created` |
| 4. Referral Ask | Happy client (NPS > 9) | Human + `writing` (GPT-4o) | Referral request | `referral.requested` |

**Artifacts**: Expansion Signals, Qualified Opportunities, Referral Requests
**Retry**: N/A (human decisions)
**Failure**: Log, continue monitoring

---

### WF-09: Executive Dashboard Generation
**Trigger**: Scheduled (Daily 6 AM, Weekly Mon 8 AM, Monthly 1st 9 AM, Quarterly)
**Owner**: Finance / Executive Finance Analyst

| Step | Input | Tool Call | Output | Event |
|------|-------|-----------|--------|-------|
| 1. Query | Period | `crm` query (Notion) + Finance data | Raw metrics | - |
| 2. Compute | Raw metrics | `analysis` (GPT-4o) | Computed KPIs | `metrics.computed` |
| 3. Render | KPIs + Template | `document` (Notion) | Dashboard page | `dashboard.created` |
| 4. Distribute | Dashboard | `email` (Gmail) | Sent to execs | `dashboard.distributed` |

**Artifacts**: Executive Dashboard (Notion page), Email Summary
**Retry**: 3x
**Failure**: Alert Finance Director, fallback to manual

---

### WF-10: Knowledge Base Maintenance
**Trigger**: Scheduled (Monthly) or Event (SOP review due, new playbook)
**Owner**: Operations / SOP Documentation Librarian

| Step | Input | Tool Call | Output | Event |
|------|-------|-----------|--------|-------|
| 1. Audit | All KB items | `crm` query (Notion Knowledge Base) | Audit report | `kb.audited` |
| 2. Identify | Expired reviews, gaps | `analysis` (GPT-4o) | Action items | `kb.gaps_found` |
| 3. Assign | Action items | `crm` create (Notion Tasks) | Assigned tasks | `kb.tasks_created` |
| 4. Publish | Approved items | `crm` update (Notion) | Published docs | `kb.published` |

**Artifacts**: Audit Report, Action Items, Published Documents
**Retry**: 2x
**Failure**: Alert Operations Director

---

## Environment Variables Required

```bash
# Notion (Primary CRM)
NOTION_API_KEY=secret_xxx
NOTION_LEADS_DB_ID=xxx
NOTION_COMPANIES_DB_ID=xxx
NOTION_CONTACTS_DB_ID=xxx
NOTION_OPPORTUNITIES_DB_ID=xxx
NOTION_SALES_CALLS_DB_ID=xxx
NOTION_PROPOSALS_DB_ID=xxx
NOTION_CLIENTS_DB_ID=xxx
NOTION_PROJECTS_DB_ID=xxx
NOTION_TASKS_DB_ID=xxx
NOTION_KNOWLEDGE_BASE_DB_ID=xxx
NOTION_SOPS_DB_ID=xxx
NOTION_EXECUTIVE_DASHBOARD_DB_ID=xxx
NOTION_PARENT_PAGE_ID=xxx  # For initial database creation

# Composio (Tool Abstraction)
COMPOSIO_API_KEY=xxx

# Gmail
GOOGLE_OAUTH_TOKEN=xxx

# Google Calendar
GOOGLE_CALENDAR_TOKEN=xxx

# GitHub (Source of Truth)
GITHUB_TOKEN=xxx

# Perplexity (Research)
PERPLEXITY_API_KEY=xxx

# OpenAI (GPT-4o)
OPENAI_API_KEY=xxx

# Anthropic (Claude)
ANTHROPIC_API_KEY=xxx

# Groq (Low Latency)
GROQ_API_KEY=xxx

# OpenRouter (Cost Optimized)
OPENROUTER_API_KEY=xxx

# NVIDIA NIM (Reasoning)
NVIDIA_API_KEY=xxx

# Figma (Design)
FIGMA_TOKEN=xxx

# Browser Search (Serper)
SERPER_API_KEY=xxx

# DO NOT SET - HubSpot Unavailable
# HUBSPOT_API_KEY=
# HUBSPOT_CLIENT_ID=
# HUBSPOT_CLIENT_SECRET=
```

---

## Migration Path: Notion → HubSpot

When CraftedWorkflows HubSpot workspace is ready:

1. **Export** all 12 Notion databases to CSV (preserving HubSpot ID fields)
2. **Map** Notion properties → HubSpot properties (1:1 where possible)
3. **Import** to HubSpot via API or Import tool
4. **Enable** Composio HubSpot integration
5. **Switch** CRM routing: `CRM.primary` → HubSpot, `CRM.fallback` → Notion
6. **Verify** data integrity (record counts, relationships, custom fields)
7. **Decommission** Notion as primary CRM (retain as operational workspace)
8. **Update** all workflows to use new routing (router change only)

---

## Implementation Roadmap (Updated)

### P0 - Critical (Week 1-2) ✅ COMPLETED
- [x] Runtime contracts, capability routing, provider routing, event system
- [x] Provider router with 30+ providers
- [x] Technical debt resolution
- [x] HubSpot disabled, Notion as CRM

### P1 - Core Integrations (Week 2-4) 🔄 IN PROGRESS
- [x] Notion CRM schemas (12 databases)
- [x] Notion CRM client (CRUD operations)
- [ ] Composio Notion integration (auth, connection)
- [ ] Composio Gmail integration
- [ ] Composio Google Calendar integration
- [ ] Composio GitHub integration
- [ ] Database creation script (Notion API)

### P2 - Workflow Automation (Week 4-6)
- [ ] Workflow engine implementation
- [ ] WF-01 Lead Discovery implementation
- [ ] WF-02 Outbound Outreach implementation
- [ ] WF-03 Discovery Call implementation
- [ ] WF-04 Proposal Generation implementation
- [ ] WF-05 Deal Close → Onboarding implementation
- [ ] Make/n8n scenario templates for each workflow

### P3 - Observability & Self-Improvement (Week 6-8)
- [ ] Executive Dashboard generation
- [ ] Health monitoring automation
- [ ] Reflection loops
- [ ] Continuous improvement pipeline

---

## Test Results

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