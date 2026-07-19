# Notion Workspace Migration Plan

**Generated:** After running `scripts/discover_notion_workspace.py`
**Workspace:** Craftedworkflows.Inc (parent page)

---

## Executive Summary

| Metric | Count |
|--------|-------|
| Existing Databases | TBD |
| Existing Pages | TBD |
| Required Runtime Databases | 12 |
| Databases to Reuse | TBD |
| Databases to Extend | TBD |
| Databases to Create | TBD |

---

## Existing Database Inventory

*Run `scripts/discover_notion_workspace.py` to populate this section*

### Database 1: [Name]
- **Notion ID:** 
- **URL:** 
- **Properties:** 
- **Current Use:** 

### Database 2: [Name]
- **Notion ID:** 
- **URL:** 
- **Properties:** 
- **Current Use:** 

---

## Runtime Schema Requirements (12 Databases)

| # | Runtime Database | Purpose | Owning Department | Owning Employee |
|---|------------------|---------|-------------------|-----------------|
| 1 | Leads | Lead pipeline | Commercial | Lead Intelligence Specialist |
| 2 | Companies | Company records | Commercial | Account Strategist |
| 3 | Contacts | Contact records | Commercial | Sales Engineer |
| 4 | Opportunities | Deal pipeline | Commercial | Pipeline Manager |
| 5 | Sales Calls | Call logs | Commercial | Discovery Specialist |
| 6 | Proposals | Proposal tracking | Commercial | Proposal Specialist |
| 7 | Clients | Client records | Delivery | Client Success Manager |
| 8 | Projects | Project delivery | Delivery | Project Manager |
| 9 | Tasks | Task management | All | All |
| 10 | Knowledge Base | Docs/SOPs/Playbooks | Operations | SOP Documentation Librarian |
| 11 | SOPs | Standard procedures | Operations | SOP Documentation Librarian |
| 12 | Executive Dashboard | Exec reporting | Finance | Executive Finance Analyst |

---

## Migration Decision Matrix

| Existing Database | Runtime Equivalent | Action | Property Additions | Relation Additions | Views Needed | Risk |
|-------------------|-------------------|--------|-------------------|-------------------|--------------|------|
| [e.g., "Leads DB"] | Leads | Reuse/Extend/Replace | [list] | [list] | [list] | Low/Med/High |

---

## Detailed Per-Database Analysis

### 1. Leads
**Runtime Schema:** `runtime/notion_crm_schemas.py` → `LEADS_SCHEMA`

| Property | Required | Current | Action |
|----------|----------|---------|--------|
| Lead ID (Title) | ✅ | | |
| Name | ✅ | | |
| Email | ✅ | | |
| Phone | | | |
| Company (Relation → Companies) | ✅ | | |
| Source (Select) | ✅ | | |
| Status (Select) | ✅ | | |
| Score (Number) | ✅ | | |
| ICP Tier (Select) | ✅ | | |
| Assigned To (Person) | | | |
| Created Date | ✅ | | |
| Last Contact (Date) | | | |
| Next Action (Rich Text) | | | |
| Notes (Rich Text) | | | |
| HubSpot ID (Rich Text) | ✅ | | |

**Views Required:**
- All Leads (Table)
- By Status (Kanban)
- By Assignee (Table)
- High Score >70 (Table)
- This Week (Calendar)

**Action:** [Reuse / Extend / Replace / Create]
**Risk:** [Low / Medium / High]

---

### 2. Companies
**Runtime Schema:** `COMPANIES_SCHEMA`

| Property | Required | Current | Action |
|----------|----------|---------|--------|
| Company ID (Title) | ✅ | | |
| Name | ✅ | | |
| Domain (URL) | | | |
| Industry (Select) | ✅ | | |
| Size (Select) | ✅ | | |
| Location (Rich Text) | | | |
| Annual Revenue (Number) | | | |
| Website (URL) | | | |
| LinkedIn (URL) | | | |
| Status (Select) | ✅ | | |
| Owner (Person) | | | |
| Created Date | ✅ | | |
| Last Updated | ✅ | | |
| HubSpot ID (Rich Text) | ✅ | | |
| Notes (Rich Text) | | | |

**Views Required:**
- All Companies (Table)
- By Status (Kanban)
- By Industry (Table)
- By Owner (Table)
- Active Customers (Table)

**Action:** [Reuse / Extend / Replace / Create]
**Risk:** [Low / Medium / High]

---

### 3. Contacts
**Runtime Schema:** `CONTACTS_SCHEMA`

| Property | Required | Current | Action |
|----------|----------|---------|--------|
| Contact ID (Title) | ✅ | | |
| First Name | ✅ | | |
| Last Name | ✅ | | |
| Email | ✅ | | |
| Phone | | | |
| Title (Rich Text) | | | |
| Company (Relation → Companies) | ✅ | | |
| Lead (Relation → Leads) | | | |
| Status (Select) | ✅ | | |
| Owner (Person) | | | |
| Created Date | ✅ | | |
| Last Contact (Date) | | | |
| HubSpot ID (Rich Text) | ✅ | | |
| Notes (Rich Text) | | | |

**Action:** [Reuse / Extend / Replace / Create]
**Risk:** [Low / Medium / High]

---

### 4. Opportunities
**Runtime Schema:** `OPPORTUNITIES_SCHEMA`

| Property | Required | Current | Action |
|----------|----------|---------|--------|
| Opportunity ID (Title) | ✅ | | |
| Name | ✅ | | |
| Company (Relation → Companies) | ✅ | | |
| Contact (Relation → Contacts) | | | |
| Lead (Relation → Leads) | | | |
| Stage (Select) | ✅ | | |
| Amount (Number) | | | |
| Probability (Number) | | | |
| Expected Close (Date) | | | |
| Actual Close (Date) | | | |
| Product (Select) | | | |
| Owner (Person) | ✅ | | |
| Created Date | ✅ | | |
| Last Updated | ✅ | | |
| HubSpot Deal ID (Rich Text) | ✅ | | |
| Notes (Rich Text) | | | |

**Views Required:**
- Pipeline (Kanban by Stage)
- By Owner (Table)
- Forecast (Probability × Amount)
- This Quarter Close (Calendar)
- Won/Lost Analysis (Table)

**Action:** [Reuse / Extend / Replace / Create]
**Risk:** [Low / Medium / High]

---

### 5. Sales Calls
**Runtime Schema:** `SALES_CALLS_SCHEMA`

| Property | Required | Current | Action |
|----------|----------|---------|--------|
| Call ID (Title) | ✅ | | |
| Date | ✅ | | |
| Time | | | |
| Duration (Number) | | | |
| Type (Select) | ✅ | | |
| Lead (Relation → Leads) | | | |
| Contact (Relation → Contacts) | | | |
| Company (Relation → Companies) | | | |
| Opportunity (Relation → Opportunities) | | | |
| Outcome (Select) | ✅ | | |
| Recording URL | | | |
| Transcript (Rich Text) | | | |
| Key Insights (Rich Text) | | | |
| Action Items (Rich Text) | | | |
| Next Steps (Rich Text) | | | |
| Owner (Person) | ✅ | | |
| HubSpot Activity ID (Rich Text) | ✅ | | |

**Action:** [Reuse / Extend / Replace / Create]
**Risk:** [Low / Medium / High]

---

### 6. Proposals
**Runtime Schema:** `PROPOSALS_SCHEMA`

| Property | Required | Current | Action |
|----------|----------|---------|--------|
| Proposal ID (Title) | ✅ | | |
| Title | ✅ | | |
| Opportunity (Relation → Opportunities) | ✅ | | |
| Company (Relation → Companies) | ✅ | | |
| Contact (Relation → Contacts) | | | |
| Stage (Select) | ✅ | | |
| Tier (Select) | | | |
| Amount (Number) | | | |
| Sent Date | | | |
| Viewed Date | | | |
| Response Date | | | |
| Expiry Date | | | |
| Document URL | | | |
| Owner (Person) | ✅ | | |
| HubSpot Deal ID (Rich Text) | ✅ | | |
| Notes (Rich Text) | | | |

**Action:** [Reuse / Extend / Replace / Create]
**Risk:** [Low / Medium / High]

---

### 7. Clients
**Runtime Schema:** `CLIENTS_SCHEMA`

| Property | Required | Current | Action |
|----------|----------|---------|--------|
| Client ID (Title) | ✅ | | |
| Name | ✅ | | |
| Company (Relation → Companies) | ✅ | | |
| Primary Contact (Relation → Contacts) | ✅ | | |
| Status (Select) | ✅ | | |
| Tier (Select) | | | |
| Monthly Value (Number) | | | |
| Contract Start | | | |
| Contract End | | | |
| Renewal Date | | | |
| Health Score (Number) | | | |
| CSM (Person) | | | |
| HubSpot Company ID (Rich Text) | ✅ | | |
| Notes (Rich Text) | | | |

**Views Required:**
- By Status (Kanban)
- By Tier (Table)
- By CSM (Table)
- Renewals Due (Calendar)
- Health < 70 (Table)

**Action:** [Reuse / Extend / Replace / Create]
**Risk:** [Low / Medium / High]

---

### 8. Projects
**Runtime Schema:** `PROJECTS_SCHEMA`

| Property | Required | Current | Action |
|----------|----------|---------|--------|
| Project ID (Title) | ✅ | | |
| Name | ✅ | | |
| Client (Relation → Clients) | ✅ | | |
| Type (Select) | | | |
| Status (Select) | ✅ | | |
| Progress (Number) | | | |
| Start Date | | | |
| Target End | | | |
| Actual End | | | |
| Budget (Number) | | | |
| Spent (Number) | | | |
| PM (Person) | ✅ | | |
| Team (Person multi) | | | |
| HubSpot Project ID (Rich Text) | ✅ | | |
| Notes (Rich Text) | | | |

**Action:** [Reuse / Extend / Replace / Create]
**Risk:** [Low / Medium / High]

---

### 9. Tasks
**Runtime Schema:** `TASKS_SCHEMA`

| Property | Required | Current | Action |
|----------|----------|---------|--------|
| Task ID (Title) | ✅ | | |
| Title | ✅ | | |
| Description (Rich Text) | | | |
| Project (Relation → Projects) | | | |
| Client (Relation → Clients) | | | |
| Assignee (Person) | ✅ | | |
| Status (Select) | ✅ | | |
| Priority (Select) | ✅ | | |
| Due Date | | | |
| Estimated Hours | | | |
| Actual Hours | | | |
| Sprint (Rich Text) | | | |
| Tags (Multi-select) | | | |
| Created Date | ✅ | | |
| Completed Date | | | |
| HubSpot Task ID (Rich Text) | ✅ | | |

**Action:** [Reuse / Extend / Replace / Create]
**Risk:** [Low / Medium / High]

---

### 10. Knowledge Base
**Runtime Schema:** `KNOWLEDGE_BASE_SCHEMA`

| Property | Required | Current | Action |
|----------|----------|---------|--------|
| KB ID (Title) | ✅ | | |
| Title | ✅ | | |
| Category (Select) | ✅ | | |
| Subcategory (Select) | | | |
| Status (Select) | ✅ | | |
| Version (Number) | | | |
| Owner (Person) | | | |
| Reviewer (Person) | | | |
| Approved By (Person) | | | |
| Approved Date | | | |
| Review Date | | | |
| Document URL | | | |
| Tags (Multi-select) | | | |
| Applies To (Multi-select) | | | |
| HubSpot ID (Rich Text) | ✅ | | |

**Action:** [Reuse / Extend / Replace / Create]
**Risk:** [Low / Medium / High]

---

### 11. SOPs
**Runtime Schema:** `SOPS_SCHEMA`

| Property | Required | Current | Action |
|----------|----------|---------|--------|
| SOP ID (Title) | ✅ | | |
| Title | ✅ | | |
| Category (Select) | ✅ | | |
| Status (Select) | ✅ | | |
| Version (Number) | ✅ | | |
| Owner (Person) | ✅ | | |
| Reviewer (Person) | | | |
| Approved By (Person) | | | |
| Approved Date | | | |
| Review Date | | | |
| Document URL | | | |
| Tags (Multi-select) | | | |
| Applies To (Multi-select) | | | |
| HubSpot ID (Rich Text) | ✅ | | |

**Action:** [Reuse / Extend / Replace / Create]
**Risk:** [Low / Medium / High]

---

### 12. Executive Dashboard
**Runtime Schema:** `EXECUTIVE_DASHBOARD_SCHEMA`

| Property | Required | Current | Action |
|----------|----------|---------|--------|
| Dashboard ID (Title) | ✅ | | |
| Period (Select) | ✅ | | |
| Period Start | ✅ | | |
| Period End | ✅ | | |
| Revenue (Number) | | | |
| Pipeline Value (Number) | | | |
| Deals Closed (Number) | | | |
| Deals Lost (Number) | | | |
| New Leads (Number) | | | |
| Qualified Leads (Number) | | | |
| Active Clients (Number) | | | |
| Churned Clients (Number) | | | |
| Avg Health Score (Number) | | | |
| Projects On Track (Number) | | | |
| Projects At Risk (Number) | | | |
| Cash Flow (Number) | | | |
| Runway (Number) | | | |
| Notes (Rich Text) | | | |
| Prepared By (Person) | ✅ | | |
| Created Date | ✅ | | |

**Action:** [Reuse / Extend / Replace / Create]
**Risk:** [Low / Medium / High]

---

## Relation Mapping

| From Database | To Database | Relation Property | Inverse Property |
|---------------|-------------|-------------------|------------------|
| Leads | Companies | Company | Leads |
| Contacts | Companies | Company | Contacts |
| Contacts | Leads | Lead | Contacts |
| Opportunities | Companies | Company | Opportunities |
| Opportunities | Contacts | Contact | Opportunities |
| Opportunities | Leads | Lead | Opportunities |
| Sales Calls | Leads | Lead | Sales Calls |
| Sales Calls | Contacts | Contact | Sales Calls |
| Sales Calls | Companies | Company | Sales Calls |
| Sales Calls | Opportunities | Opportunity | Sales Calls |
| Proposals | Opportunities | Opportunity | Proposals |
| Proposals | Companies | Company | Proposals |
| Proposals | Contacts | Contact | Proposals |
| Clients | Companies | Company | Clients |
| Clients | Contacts | Primary Contact | Clients |
| Projects | Clients | Client | Projects |
| Tasks | Projects | Project | Tasks |
| Tasks | Clients | Client | Tasks |

---

## Implementation Sequence

1. **Phase 1 (Week 1):** Core CRM — Leads, Companies, Contacts, Opportunities
2. **Phase 2 (Week 2):** Sales Activity — Sales Calls, Proposals
3. **Phase 3 (Week 2):** Delivery — Clients, Projects, Tasks
4. **Phase 4 (Week 3):** Knowledge — Knowledge Base, SOPs, Executive Dashboard

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Existing data loss | Medium | High | Backup before changes; use Extend not Replace |
| Relation breakage | Medium | High | Map all relations before changes |
| Property type conflicts | Low | High | Audit types before extending |
| Permission issues | Low | Medium | Verify integration access |
| View disruption | Medium | Medium | Document existing views first |

---

## Approval Checklist

- [ ] Existing workspace discovered
- [ ] Migration plan reviewed
- [ ] Stakeholder approval obtained
- [ ] Backup created
- [ ] Migration executed
- [ ] Validation complete
- [ ] Rollback plan tested

---

**Next Step:** Run `scripts/discover_notion_workspace.py` with credentials to populate existing database inventory.