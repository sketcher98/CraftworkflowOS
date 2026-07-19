# Creative Department Comparison Report

**Prepared by:** Chief Systems Architect
**Date:** 2026-07-19
**Sources:**
- SOURCE A: 04_Knowledge (CraftworkflowOS primary)
- SOURCE B: agency-agents (reference only)
- SOURCE C: Current 03_Departments (existing structure)

---

## Executive Summary

Creative currently has **zero employees**. The Creative Director exists with mission "Create world-class visual communication" owning Design, Branding, UI/UX, Video, Motion Graphics — but no operational team.

**Critical Gap:** Creative supports every department but has no one to execute. Marketing produces messaging that needs visual translation. Commercial needs proposal assets, sales enablement, technical diagrams. Delivery needs onboarding visuals, QBR decks, case studies.

---

## 1. Creative Consumption Map (Artifacts from Other Departments)

### From Marketing (Messaging Source — Creative Translates to Visual)

| Marketing Role | Artifact | Creative Translates To |
|----------------|----------|------------------------|
| Founder Brand Architect | `founder_voice_profile.md`, LinkedIn/Twitter posts | Visual brand system, post templates, profile graphics |
| Content Strategist | `company_content_calendar`, blog articles, newsletter | Blog headers, newsletter templates, social cards |
| Lead Magnet Designer | `lead_magnet_{name}.md`, landing pages, delivery sequences | PDF design, landing page UI, email templates |
| Authority PR Builder | `founder_media_kit.md`, media pitches, speaking proposals | Media kit design, speaker deck, one-pagers |
| Sales Enablement Content | `proposal_asset`, `objection_armor`, `battlecard`, `proof_asset` | Designed proposals, objection cards, battlecards, proof PDFs |

### From Commercial (Deal Assets)

| Commercial Role | Artifact | Creative Translates To |
|----------------|----------|------------------------|
| Proposal Specialist | `proposal_{id}.md` (tier, scope, pricing) | Professional proposal design, pricing tables |
| Sales Engineer | `solution_architecture`, `poc_scope`, `technical_risk` | Architecture diagrams, technical one-pagers |
| Account Strategist | `account_plan`, `stakeholder_map`, `champion_kit` | Account maps, stakeholder visualizations |
| Deal Strategist | `deal_structure`, `pricing_rationale`, `terms_summary` | Deal structure visualizations |

### From Delivery (Client Assets)

| Delivery Role | Artifact | Creative Translates To |
|----------------|----------|------------------------|
| Client Onboarding | `onboarding_plan`, `kickoff_notes`, `access_provisioning` | Welcome decks, onboarding portals, checklists |
| Client Success Manager | `health_report`, `success_plan`, `qbr_deck`, `renewal_package` | QBR decks, health dashboards, renewal presentations |
| Expansion Specialist | `expansion_proposal`, `case_study`, `referral_reward` | Case study PDFs, expansion proposals, referral cards |
| Quality Engineer | `test_plan`, `quality_gate_report`, `uat_signoff` | Test reports, quality dashboards |

---

## 2. Missing Creative Capabilities

| Capability | Currently | Should Be Owned By Creative |
|------------|-----------|----------------------------|
| Brand identity system | Marketing (text only) | Brand Designer |
| UI/UX for dashboards/tools | Engineering (ad-hoc) | UI/UX Designer |
| Website/landing pages | Marketing (copy only) | Web Experience Designer |
| Motion/video for social/sales | None | Motion & Video Designer |
| Social/content visual assets | Marketing (text only) | Visual Content Designer |
| Proposal/sales asset design | Commercial (text only) | Visual Content Designer |
| Client deliverable design | Delivery (text only) | Visual Content Designer |
| Case study production | Expansion (text only) | Visual Content Designer |

---

## 3. Proposed Creative Department Structure

### Director: Creative Director (exists)
Reports to: Hermes COO
Owns: Design, Branding, UI/UX, Video, Motion Graphics

### 5 Specialist Employees

| # | Role | Primary Focus | Supports Departments |
|---|------|---------------|---------------------|
| 1 | **Brand Designer** | Visual identity, brand system, guidelines, templates | Marketing, All (brand consistency) |
| 2 | **UI/UX Designer** | Product interfaces, dashboards, internal tools, client portals | Engineering, Delivery, Operations |
| 3 | **Web Experience Designer** | Website, landing pages, conversion optimization, funnels | Marketing, Commercial |
| 4 | **Motion & Video Designer** | Founder videos, social motion, demo videos, case study videos | Marketing, Sales Enablement, Delivery |
| 5 | **Visual Content Designer** | Social assets, sales collateral, proposals, case studies, onboarding | Marketing, Commercial, Delivery |

---

## 4. Handoff Contracts (Creative ↔ Other Departments)

### Creative → Marketing
- `brand_system_{version}.json` — Tokens, components, usage rules
- `social_template_pack_{quarter}.figma` — Post templates, story templates
- `video_assets_{campaign}.mp4` — Founder clips, motion graphics
- `lead_magnet_design_{magnet}.figma` — PDF, landing page, email designs

### Creative → Commercial
- `proposal_template_{tier}.figma` — Professional proposal designs
- `battlecard_design_{competitor}.figma` — Competitive battlecards
- `technical_diagram_{project}.drawio` — Architecture diagrams
- `pricing_table_design.figma` — Pricing visualizations

### Creative → Delivery
- `onboarding_deck_template.figma` — Welcome deck, kickoff slides
- `qbr_deck_template.figma` — QBR structure, health visualizations
- `case_study_template.figma` — Case study layout, data viz
- `health_dashboard_ui.figma` — Client health dashboard design

### Marketing → Creative (Messaging Input)
- `founder_voice_profile.md` → Brand voice for visual tone
- `content_calendar_{month}.json` → Production schedule
- `campaign_brief_{id}.md` → Messaging, audience, goals
- `media_kit_copy.md` → Copy for media kit design

### Commercial → Creative (Deal Context)
- `proposal_{id}.md` → Content for proposal design
- `solution_architecture_{id}.md` → Content for diagrams
- `deal_structure_{id}.md` → Content for deal viz
- `battlecard_copy_{competitor}.md` → Copy for battlecard design

### Delivery → Creative (Client Context)
- `onboarding_plan_{id}.md` → Content for welcome deck
- `qbr_deck_{id}.pdf` → Content for QBR design
- `case_study_{id}.md` → Content for case study design
- `health_report_{id}.md` → Data for dashboard design

---

## 5. Required Capabilities (Provider-Agnostic)

```python
CREATIVE_CAPABILITIES = {
    "design": ["Figma", "Future: Penpot", "Future: Sketch"],
    "motion_design": ["After Effects", "Future: Rive", "Future: Lottie"],
    "video_editing": ["Premiere", "Future: DaVinci", "Future: CapCut"],
    "prototyping": ["Figma", "Future: Framer"],
    "illustration": ["Figma", "Future: Illustrator"],
    "design_system": ["Figma", "Future: Storybook"],
}
```

No vendor hardcoding — capabilities route through provider registry.

---

## 6. Implementation Priority

| Phase | Employees | Rationale |
|-------|-----------|-----------|
| 1 | Brand Designer, Visual Content Designer | Foundation: brand system + immediate asset needs |
| 2 | UI/UX Designer, Web Experience Designer | Product: dashboards, portals, website |
| 3 | Motion & Video Designer | Scale: video for social, sales, case studies |