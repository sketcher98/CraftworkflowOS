# Finance Department Comparison Report

**Prepared by:** Chief Systems Architect
**Date:** 2026-07-19
**Sources:**
- SOURCE A: 04_Knowledge (CraftworkflowOS primary)
- SOURCE B: agency-agents (reference only)
- SOURCE C: Current 03_Departments (existing structure)

---

## Executive Summary

Finance currently has **zero employees**. The Finance Director exists with mission "Protect profitability and allocate capital wisely" owning Cash Flow, Budgeting, Pricing, Forecasting, Profitability — but no operational team.

**Critical Gap:** Every closed deal flows from Commercial → Delivery → Finance for invoicing, but **no one receives it**. The client lifecycle ends at Delivery with no Finance handoff.

---

## 1. Financial Touchpoint Mapping (Current State)

### Commercial → Finance Touchpoints

| Touchpoint | Commercial Owner | Artifact Produced | Finance Need |
|------------|-----------------|-------------------|--------------|
| Proposal Pricing | Proposal Specialist | `proposal_{id}.md` (tier, amount) | Validate pricing, margin check |
| Deal Structure | Deal Strategist | `deal_structure_{id}.md` (price, terms, margin) | Approve structure, revenue recognition |
| Pipeline Forecast | Pipeline Specialist | `forecast_{period}.json` (weighted, commit) | Cash flow forecasting, revenue planning |
| Contract Terms | Account Strategist | `procurement_strategy_{id}.md` (payment terms) | Billing schedule, collections planning |

### Delivery → Finance Touchpoints

| Touchpoint | Delivery Owner | Artifact Produced | Finance Need |
|------------|----------------|-------------------|--------------|
| Project Milestones | Project Manager | `project_plan_{id}.md` (milestones, dates) | Invoice trigger scheduling |
| Delivery Completion | Project Manager | `project_closure_{id}.md` | Final invoice, revenue recognition |
| Expansion Signals | Client Success Manager | `expansion_signal_{id}.json` | Upsell revenue forecasting |
| Renewal Packages | Client Success Manager | `renewal_package_{id}.md` | Recurring revenue, contract renewal |
| Referral Conversions | Expansion Specialist | `referral_reward_{id}.json` | Referral payout, tracking |

### Operations → Finance Touchpoints

| Touchpoint | Operations Owner | Artifact Produced | Finance Need |
|------------|-----------------|-------------------|--------------|
| Tool Contracts | Automation Internal Tools PM | `tool_contract_{name}.md` (vendor, cost, renewal) | Vendor spend, budget tracking |
| Planning Budgets | Planning Rhythm Coordinator | `quarterly_plan_{quarter}.md` | Budget allocation, variance analysis |

---

## 2. Missing Financial Capabilities

| Capability | Currently Handled By | Should Be Owned By Finance |
|------------|---------------------|---------------------------|
| Proposal pricing validation | Proposal Specialist (self-check) | Pricing & Profitability Analyst |
| Margin analysis | Deal Strategist (ad-hoc) | Pricing & Profitability Analyst |
| Invoice generation | Manual/Ad-hoc | Billing & Invoicing Specialist |
| Payment tracking | None | Billing & Invoicing Specialist |
| Cash flow forecasting | None | Cash Flow & Forecasting Analyst |
| Revenue recognition | None | Financial Controller |
| Budget vs actuals | None | Financial Controller |
| Executive dashboards | None | Executive Finance Analyst |
| Collections | None | Billing & Invoicing Specialist |
| Package profitability | None | Pricing & Profitability Analyst |
| Expansion revenue tracking | Expansion Specialist (pipeline only) | Revenue Operations Specialist |

---

## 3. Proposed Finance Department Structure

### Director: Finance Director (exists)
Reports to: Hermes COO
Owns: Cash Flow, Budgeting, Pricing, Forecasting, Profitability

### 6 Specialist Employees

| # | Role | Primary Focus | Key Handoffs |
|---|------|---------------|--------------|
| 1 | **Revenue Operations Specialist** | End-to-end revenue lifecycle, deal-to-cash | Commercial (Pipeline), Delivery (Closure), All Finance |
| 2 | **Pricing & Profitability Analyst** | Package margins, pricing optimization, discount governance | Commercial (Proposal, Deal), Finance (Revenue Ops) |
| 3 | **Billing & Invoicing Specialist** | Invoice generation, payment tracking, collections | Delivery (Milestones), Commercial (Contracts), Finance (Cash Flow) |
| 4 | **Cash Flow & Forecasting Analyst** | 13-week cash flow, revenue forecasting, runway | Commercial (Pipeline), Finance (All), COO |
| 5 | **Financial Controller** | Revenue recognition, GAAP compliance, month-end close | All Finance, COO, External (auditors) |
| 6 | **Executive Finance Analyst** | Executive dashboards, board decks, strategic analysis | All Finance, CEO/COO, Board |

---

## 4. Client Lifecycle Financial Flow

```
LEAD → QUALIFICATION → DISCOVERY → PROPOSAL → CLOSED WON
  ↓         ↓             ↓           ↓           ↓
Marketing  Commercial   Commercial  Commercial  Commercial
           (LI, Pros)   (Disc)      (Prop)      (Pipe)
                                              ↓
                                    FINANCE: Revenue Ops validates
                                    Pricing Analyst approves margin
                                              ↓
ONBOARDING → DELIVERY → QA → SUCCESS → EXPANSION
    ↓          ↓         ↓       ↓          ↓
Delivery   Delivery  Delivery Delivery   Delivery
(Onboard)  (PM)      (QA)     (CS)       (Exp)
                                              ↓
                                    FINANCE: Billing triggers on milestones
                                    Cash Flow forecasts revenue
                                              ↓
INVOICE → PAYMENT → REPORTING → EXECUTIVE DASHBOARD
  ↓         ↓          ↓            ↓
Finance  Finance    Finance      Finance
(Billing) (Billing) (Controller) (Exec Analyst)
```

---

## 5. Required Capabilities (Provider-Agnostic)

```python
FINANCE_CAPABILITIES = {
    "financial_analysis": ["GPT-4o", "Future: Python-Pandas"],
    "financial_writing": ["GPT-4o"],
    "spreadsheet_modeling": ["GPT-4o", "Future: Python"],
    "data_query": ["Browser", "Future: SQL"],
    "document_generation": ["GPT-4o"],
    "forecasting": ["GPT-4o", "Future: Prophet/ARIMA"],
}
```

No vendor hardcoding — capabilities route through provider registry.

---

## 6. Future Integrations (Capability-Based)

| Integration | Capability Needed | Purpose |
|-------------|------------------|---------|
| HubSpot | `crm` | Deal sync, contact enrichment |
| Gmail | `email` | Invoice delivery, payment reminders |
| Notion | `documentation` | Financial wiki, budget docs |
| Make/n8n | `automation` | Workflow automation (invoice → accounting) |
| Accounting Software (Xero/QuickBooks) | `accounting` | GL sync, reconciliation, tax |

---

## 7. Implementation Priority

| Phase | Employees | Rationale |
|-------|-----------|-----------|
| 1 | Revenue Operations Specialist, Billing & Invoicing Specialist | Close deal-to-cash loop immediately |
| 2 | Pricing & Profitability Analyst, Cash Flow & Forecasting Analyst | Protect margins, forecast cash |
| 3 | Financial Controller, Executive Finance Analyst | Compliance, executive visibility |

---

## 8. Artifact Contracts (Finance ↔ Other Departments)

### Finance → Commercial
- `pricing_approval_{deal_id}.json` — Approved price, margin, terms
- `discount_authorization_{deal_id}.json` — Discount limits, approval chain
- `margin_report_{month}.md` — Package profitability by tier

### Finance → Delivery
- `invoice_schedule_{client_id}.json` — Milestone dates, amounts, terms
- `collection_status_{client_id}.json` — Payment status, aging
- `expansion_revenue_target_{quarter}.json` — Targets for CS/Expansion

### Finance → Operations
- `budget_allocation_{quarter}.json` — Dept budgets, variance thresholds
- `vendor_spend_report_{month}.md` — Tool/vendor costs, renewals

### Commercial → Finance
- `proposal_{id}.md` — Tier, amount, terms (trigger: pricing approval)
- `deal_structure_{id}.md` — Structure, margin, rev rec schedule
- `contract_terms_{id}.json` — Payment terms, milestones, penalties

### Delivery → Finance
- `milestone_complete_{client_id}.json` — Trigger: invoice generation
- `project_closure_{id}.md` — Trigger: final invoice, rev rec
- `renewal_package_{id}.md` — Trigger: recurring invoice schedule

### Operations → Finance
- `tool_contract_{name}.md` — Vendor cost, renewal date
- `quarterly_plan_{quarter}.md` — Budget requests, headcount