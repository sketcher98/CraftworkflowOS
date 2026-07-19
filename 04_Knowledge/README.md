# 04_Knowledge — Knowledge Base

The structured, searchable knowledge base for CraftedWorkflows.

---

## Purpose

This directory contains all codified, reusable knowledge for CraftedWorkflows. Unlike the inbox (raw capture) or memory (learned patterns), this is the **curated, version-controlled source of truth**.

**Knowledge here should be:**
- Curated (not raw)
- Version-controlled (git history = audit trail)
- Cross-referenced (linked, not duplicated)
- Actionable (every doc should inform a decision)

---

## Directory Structure

```
04_Knowledge/
├── Company/                    # Company identity & strategy
│   ├── Core_Philosophy.md
│   ├── Origin_Story.md
│   ├── Value_Proposition.md
│   └── Target_Market.md
│
├── Playbooks/                  # Operational playbooks (how we work)
│   ├── README.md
│   ├── Outreach/
│   │   └── DM_Flows.md
│   ├── Sales/
│   │   ├── README.md
│   │   ├── Sales_Call_Playbook.md
│   │   ├── Pre_Call_Sequence.md
│   │   ├── Objection_Handling.md
│   │   └── Roleplay_Scenarios.md
│   ├── Marketing/
│   │   └── Content_Pillars.md
│   ├── Sales/
│   │   ├── Pre_Call_Sequence.md
│   │   └── Objection_Handling.md
│   └── Finance/
│       └── Pricing_Packages.md
│
├── SOPs/                       # Standard Operating Procedures
│   └── (to be created)
│
├── Frameworks/                 # Strategic frameworks & mental models
│   └── (to be created)
│
├── Templates/                  # Reusable templates
│   └── (to be created)
│
├── Offers/                     # Offer structures & pricing
│   └── Pricing_Packages.md
│
├── Research/                   # Market & competitive research
│   ├── README.md
│   ├── Market_Intelligence/
│   ├── Competitive_Intelligence/
│   ├── Customer_Research/
│   └── Technical_Research/
│
├── Case_Studies/               # Client success stories
│   └── (to be created)
│
├── Prompts/                    # Reusable AI prompts
│   └── (to be created)
│
├── Competitive_Intelligence/   # Competitor analysis
│   └── (to be created)
│
├── Market_Intelligence/        # Market trends & sizing
│   └── (to be created)
│
├── Assets/                     # Static assets (logos, images)
│   └── (to be created)
│
└── README.md                   # This file

---

## Inbox (Raw Capture)

**Location:** `04_Knowledge/Inbox/`

Raw, unprocessed knowledge capture. **Do not edit inbox files.**

Processing workflow:
1. Read inbox file completely
2. Extract structured knowledge
3. Create/update files in appropriate directories above
4. Cross-reference with existing docs
5. Leave inbox file untouched (audit trail)

**Current Inbox Files:**
- `craftedworkflows_master.md` — Company manifesto, philosophy, offers, funnels
- `outbound_playbook.md` — 5 DM flows, daily targeting playbook, lead sourcing
- `sales_call_playbook.md` — Complete call script, 8 roleplays, objection handling

---

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Directory | PascalCase | `Playbooks`, `Company` |
| Markdown file | PascalCase_with_Underscores | `Sales_Call_Playbook.md` |
| Subdirectory | PascalCase | `Sales/`, `Outreach/` |
| Cross-reference | Relative markdown link | `[DM Flows](../Outreach/DM_Flows.md)` |

---

## Cross-Reference Standards

1. **Link, don't duplicate** — Use `[Link Text](../Path/File.md)`
2. **Index files** — Each directory has `README.md` with index
3. **Update indexes** — When adding files, update parent README

---

## Ingestion Process (For Future Documents)

When adding new knowledge:

1. **Check** — Does a suitable document already exist?
2. **Place** — Put in correct directory per structure above
3. **Name** — Follow naming conventions
4. **Link** — Add to parent README.md index
4. **Cross-ref** — Add relevant cross-references
5. **Commit** — Version control everything

**Never:**
- Duplicate content across files
- Put raw/unprocessed content in knowledge directories
- Create files without updating parent index

---

## Architecture Principles

1. **Single Source of Truth** — Each concept lives in one place
2. **No Duplication** — Reference, don't copy
3. **Actionable** — Every doc should inform a decision
5. **Version Controlled** — Git history = audit trail
6. **Human + AI Readable** — Clear structure, consistent formatting

---

## Maintenance

- **Monthly:** Review for drift, broken links, outdated info
- **Quarterly:** Audit structure, consolidate duplicates
- **Annually:** Major restructure if needed

---

## Related

- [Playbooks](../Playbooks/README.md)
- [Company](../Company/README.md)
- [Offers](../Offers/README.md)
- [Research](../Research/README.md)