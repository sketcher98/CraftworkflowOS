# CraftworkflowOS Runtime Configuration

## Provider Status

| Provider | Status | Notes |
|----------|--------|-------|
| HubSpot | ❌ UNAVAILABLE | Legacy FyreStrokeDigital account - DO NOT USE |
| Notion | ✅ ACTIVE | Primary CRM & Operational Workspace |
| GitHub | ✅ ACTIVE | Source of Truth |
| Gmail | ✅ ACTIVE | Communication |
| Google Calendar | ✅ ACTIVE | Scheduling |
| Composio | ✅ ACTIVE | Tool Abstraction Layer |
| Perplexity | ✅ ACTIVE | Research |
| GPT-4o | ✅ ACTIVE | Writing/Analysis |
| Browser | ✅ ACTIVE | Search |
| Figma | ✅ ACTIVE | Design |

## CRM Configuration

**Primary CRM**: Notion (until CraftedWorkflows HubSpot workspace is connected)

**Fallback Strategy**: All CRM workflows degrade gracefully to Notion databases.
When HubSpot becomes available, migration path exists via Notion → HubSpot sync.

## Notion Database Schemas (CRM Fallback)

### Leads Database
```
Properties:
- Lead ID (Title) - Auto-generated: LD-{timestamp}
- Name (Rich Text)
- Email (Email)
- Phone (Phone Number)
- Company (Relation → Companies)
- Source (Select: Inbound, Outbound, Referral, Event, Organic)
- Status (Select: New, Qualified, Contacted, Disqualified, Converted)
- Score (Number 0-100)
- ICP Tier (Select: Tier 1, Tier 2, Tier 3)
- Assigned To (Person)
- Created Date (Created Time)
- Last Contact (Date)
- Next Action (Rich Text)
- Notes (Rich Text)
- HubSpot ID (Rich Text) - For future migration
```

### Companies Database
```
Properties:
- Company ID (Title) - Auto-generated: CO-{timestamp}
- Name (Rich Text)
- Domain (URL)
- Industry (Select: Agency, Consultancy, SaaS, E-commerce, Other)
- Size (Select: 1-10, 11-50, 51-200, 201-500, 500+)
- Location (Rich Text)
- Annual Revenue (Number)
- Website (URL)
- LinkedIn (URL)
- Status (Select: Prospect, Lead, Customer, Churned)
- Owner (Person)
- Created Date (Created Time)
- Last Updated (Last Edited Time)
- HubSpot ID (Rich Text)
- Notes (Rich Text)
```

### Contacts Database
```
Properties:
- Contact ID (Title) - Auto-generated: CT-{timestamp}
- First Name (Rich Text)
- Last Name (Rich Text)
- Email (Email)
- Phone (Phone Number)
- Title (Rich Text)
- Company (Relation → Companies)
- Lead (Relation → Leads)
- Status (Select: Active, Inactive, Do Not Contact)
- Owner (Person)
- Created Date (Created Time)
- Last Contact (Date)
- HubSpot ID (Rich Text)
- Notes (Rich Text)
```

### Opportunities Database
```
Properties:
- Opportunity ID (Title) - Auto-generated: OP-{timestamp}
- Name (Rich Text)
- Company (Relation → Companies)
- Contact (Relation → Contacts)
- Lead (Relation → Leads)
- Stage (Select: Discovery, Qualification, Proposal, Negotiation, Closed Won, Closed Lost)
- Amount (Number)
- Probability (Number 0-100)
- Expected Close Date (Date)
- Actual Close Date (Date)
- Product (Select: Jumpstart, Goldilocks, Visionary, Custom)
- Owner (Person)
- Created Date (Created Time)
- Last Updated (Last Edited Time)
- HubSpot Deal ID (Rich Text)
- Notes (Rich Text)
```

### Sales Calls Database
```
Properties:
- Call ID (Title) - Auto-generated: SC-{timestamp}
- Date (Date)
- Time (Time)
- Duration (Number - minutes)
- Type (Select: Discovery, Demo, Proposal Review, Negotiation, Follow-up, QBR)
- Lead (Relation → Leads)
- Contact (Relation → Contacts)
- Company (Relation → Companies)
- Opportunity (Relation → Opportunities)
- Outcome (Select: Scheduled, Completed, No Show, Cancelled, Rescheduled)
- Recording URL (URL)
- Transcript (Rich Text)
- Key Insights (Rich Text)
- Action Items (Rich Text)
- Next Steps (Rich Text)
- Owner (Person)
- HubSpot Activity ID (Rich Text)
```

### Proposals Database
```
Properties:
- Proposal ID (Title) - Auto-generated: PR-{timestamp}
- Title (Rich Text)
- Opportunity (Relation → Opportunities)
- Company (Relation → Companies)
- Contact (Relation → Contacts)
- Stage (Select: Draft, Sent, Viewed, Negotiating, Accepted, Rejected, Expired)
- Tier (Select: Jumpstart, Goldilocks, Visionary, Custom)
- Amount (Number)
- Sent Date (Date)
- Viewed Date (Date)
- Response Date (Date)
- Expiry Date (Date)
- Document URL (URL)
- Owner (Person)
- HubSpot Deal ID (Rich Text)
- Notes (Rich Text)
```

### Clients Database
```
Properties:
- Client ID (Title) - Auto-generated: CL-{timestamp}
- Name (Rich Text)
- Company (Relation → Companies)
- Primary Contact (Relation → Contacts)
- Status (Select: Onboarding, Active, At Risk, Churned, Alumni)
- Tier (Select: Jumpstart, Goldilocks, Visionary, Custom)
- Monthly Value (Number)
- Contract Start (Date)
- Contract End (Date)
- Renewal Date (Date)
- Health Score (Number 0-100)
- CSM (Person)
- HubSpot Company ID (Rich Text)
- Notes (Rich Text)
```

### Projects Database
```
Properties:
- Project ID (Title) - Auto-generated: PJ-{timestamp}
- Name (Rich Text)
- Client (Relation → Clients)
- Type (Select: Implementation, Optimization, Migration, Support, Custom)
- Status (Select: Planning, Active, On Hold, Completed, Cancelled)
- Progress (Number 0-100)
- Start Date (Date)
- Target End Date (Date)
- Actual End Date (Date)
- Budget (Number)
- Spent (Number)
- PM (Person)
- Team (Multi-select → People)
- HubSpot Project ID (Rich Text)
- Notes (Rich Text)
```

### Tasks Database
```
Properties:
- Task ID (Title) - Auto-generated: TK-{timestamp}
- Title (Rich Text)
- Description (Rich Text)
- Project (Relation → Projects)
- Client (Relation → Clients)
- Assignee (Person)
- Status (Select: Backlog, Ready, In Progress, Review, Done, Blocked)
- Priority (Select: Low, Medium, High, Critical)
- Due Date (Date)
- Estimated Hours (Number)
- Actual Hours (Number)
- Sprint (Rich Text)
- Tags (Multi-select)
- Created Date (Created Time)
- Completed Date (Date)
- HubSpot Task ID (Rich Text)
```

### SOPs Database
```
Properties:
- SOP ID (Title) - Auto-generated: SOP-{timestamp}
- Title (Rich Text)
- Category (Select: Sales, Marketing, Delivery, Operations, Finance, HR, Technical)
- Status (Select: Draft, Review, Approved, Published, Archived)
- Version (Number)
- Owner (Person)
- Reviewer (Person)
- Approved By (Person)
- Approved Date (Date)
- Review Date (Date)
- Document URL (URL)
- Tags (Multi-select)
- Applies To (Multi-select: Leads, Companies, Contacts, Opportunities, Clients, Projects)
- HubSpot ID (Rich Text)
```

## Workflow Degradation Rules

### Lead Management
- **With HubSpot**: Leads created in HubSpot → Synced to Notion
- **Without HubSpot**: Leads created directly in Notion Leads DB → Manual enrichment

### Contact Management
- **With HubSpot**: Contacts synced bidirectionally
- **Without HubSpot**: Contacts created in Notion Contacts DB → Linked to Companies/Leads

### Opportunity Tracking
- **With HubSpot**: Deals in HubSpot → Synced to Notion Opportunities
- **Without HubSpot**: Opportunities managed in Notion → Manual pipeline tracking

### Proposal Generation
- **With HubSpot**: Proposals generated from HubSpot deals
- **Without HubSpot**: Proposals created in Notion → Linked to Opportunities

### Client Onboarding
- **With HubSpot**: Triggered by Closed Won deal
- **Without HubSpot**: Triggered manually from Notion Opportunity (Stage = Closed Won)

### Activity Logging
- **With HubSpot**: Activities logged in HubSpot → Synced
- **Without HubSpot**: Activities logged in Notion Sales Calls/Tasks → Manual CRM entry

## Migration Path to HubSpot

When CraftedWorkflows HubSpot workspace is connected:

1. **Export Notion databases** to CSV
2. **Map fields** using HubSpot ID properties (stored in each record)
3. **Import to HubSpot** via API or import tool
4. **Enable bidirectional sync** via Composio HubSpot integration
5. **Verify data integrity** before decommissioning Notion as primary CRM
6. **Retain Notion** as operational workspace (project management, SOPs, docs)

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
NOTION_SOPS_DB_ID=xxx

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

# OpenAI (Writing)
OPENAI_API_KEY=xxx

# Anthropic (Analysis)
ANTHROPIC_API_KEY=xxx

# Groq (Fast Inference)
GROQ_API_KEY=xxx

# DO NOT SET - HubSpot Unavailable
# HUBSPOT_API_KEY=
# HUBSPOT_CLIENT_ID=
# HUBSPOT_CLIENT_SECRET=
```

## Capability Routing Updates

```python
# CRM capability routes to Notion (not HubSpot)
CRM_PROVIDER = "Notion"  # Not "HubSpot"

# Capability routing for CRM operations
CAPABILITY_ROUTES = {
    "crm_create_contact": "Notion",
    "crm_update_contact": "Notion", 
    "crm_search_contacts": "Notion",
    "crm_create_company": "Notion",
    "crm_create_deal": "Notion",
    "crm_update_deal": "Notion",
    "crm_log_activity": "Notion",
}
```

## Composio Integration Priority

1. **Notion** - Primary CRM operations
2. **Gmail** - Communication
3. **Google Calendar** - Scheduling
4. **GitHub** - Source of truth
5. **Composio HubSpot** - Disabled until new workspace