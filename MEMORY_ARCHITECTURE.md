# CraftworkflowOS Memory Architecture
Version: 1.0
Date: 2026-07-19

---

## 1. Overview

This document defines the persistent memory architecture for Hermes COO. The memory system enables Hermes to maintain continuity across sessions, learn from experience, and make better decisions over time.

**Design Principles:**
- **Separation of concerns**: Each memory layer has a single responsibility
- **No duplication**: Memory never duplicates information already in documentation (00-09 folders)
- **Version controlled where appropriate**: Structured memory lives in Git; secrets and raw logs do not
- **Hierarchical trust**: Documentation > Memory > General knowledge
- **Incremental adoption**: System works with just checkpoints; layers add capability

---

## 2. Memory Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    DOCUMENTATION (Source of Truth)          │
│  00_Systems, 01_CEO, 02_COO, 03_Departments, 04_Knowledge,  │
│  05_Operations, 06_Clients, 07_Projects, 08_Command_Center, │
│  09_Archive, Project_Management                             │
└─────────────────────────────────────────────────────────────┘
                              ↑
                              │ Higher authority
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      MEMORY LAYERS                           │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  IDENTITY    │  WORKING     │  LONG-TERM   │  REFLECTIONS   │
│  (static)    │  (session)   │  (persistent)│  (learning)    │
├──────────────┼──────────────┼──────────────┼────────────────┤
│  SKILLS      │  DECISIONS   │  PREFERENCES │  CHECKPOINTS   │
│  (reusable)  │  (record)    │  (learned)   │  (session)     │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

### Layer 1: Identity Memory (Static, Git-tracked)
**Purpose**: Who Hermes is - never changes without explicit update
**Location**: `memory/identity/`
**Contents**:
- `role.md` - COO role definition (from 02_COO/identity.md)
- `mission.md` - Personal mission statement
- `principles.md` - Operating principles (from 01_CEO/decision_principles.md)
- `authority.md` - What Hermes can/cannot decide
**Persistence**: Git-tracked, loaded once at boot
**Updates**: Only when CEO explicitly updates role

### Layer 2: Working Memory (Session-scoped, Not Git)
**Purpose**: Active context for current session
**Location**: `memory/working/` (runtime only, not committed)
**Contents**:
- `current_objective.md` - What Hermes is focused on now
- `active_projects.md` - Projects currently engaged
- `current_client.md` - Client being worked with
- `session_notes.md` - Scratchpad for current session
- `inbox_snapshot.md` - Inbox state at session start
**Persistence**: Saved to checkpoint, restored on resume
**Lifecycle**: Cleared on explicit reboot; checkpointed otherwise

### Layer 3: Long-Term Memory (Persistent, Git-tracked)
**Purpose**: Accumulated knowledge that survives sessions
**Location**: `memory/longterm/`
**Contents**:
- `clients/` - Client profiles, history, preferences
  - `{client_name}/profile.md` - Company info, contacts, pain points
  - `{client_name}/history.md` - Engagement timeline
  - `{client_name}/preferences.md` - Communication style, tools
- `patterns/` - Recognized business patterns
  - `successful_approaches.md` - What worked for which client types
  - `failed_approaches.md` - What didn't work and why
  - `industry_insights.md` - Sector-specific learnings
- `relationships/` - Network map
  - `contacts.md` - Key people, roles, connections
  - `referrals.md` - Referral sources and outcomes
- `market_intelligence/` - Competitive landscape
  - `competitors.md` - Who else plays in our space
  - `pricing_benchmarks.md` - Market rates observed
**Persistence**: Git-tracked, updated after significant engagements

### Layer 4: Episodic Memory (Persistent, Git-tracked)
**Purpose**: Specific events and experiences with timestamps
**Location**: `memory/episodic/`
**Structure**: Chronological, one file per significant episode
**Contents**:
- `YYYY-MM-DD-{slug}.md` - Episode records
  - Context: What was happening
  - Action: What Hermes did
  - Outcome: What happened
  - Learning: What to do differently next time
- Examples:
  - `2026-07-15-first-client-onboarded.md`
  - `2026-07-18-outreach-campaign-launched.md`
  - `2026-07-20-pricing-model-adjusted.md`
**Persistence**: Git-tracked, append-only (immutable history)

### Layer 5: Skills Memory (Persistent, Git-tracked)
**Purpose**: Reusable procedures and playbooks
**Location**: `memory/skills/`
**Contents**:
- `outreach/` - Proven outreach sequences
  - `founder-mirror.md` - Flow 1 execution guide
  - `risk-audit.md` - Flow 5 execution guide
  - `permission-based.md` - Flow 2 execution guide
- `discovery/` - Discovery call frameworks
  - `pre-call-research.md`
  - `question-framework.md`
  - `pain-diagnosis.md`
- `proposal/` - Proposal templates
  - `structure.md`
  - `pricing-models.md`
  - `roi-calculator.md`
- `onboarding/` - Client onboarding checklists
- `internal/` - Internal operations
  - `daily-briefing.md`
  - `weekly-review.md`
  - `project-kickoff.md`
**Persistence**: Git-tracked, versioned, evolves with experience

### Layer 6: Reflections Memory (Persistent, Git-tracked)
**Purpose**: Post-action learning and pattern extraction
**Location**: `memory/reflections/`
**Contents**:
- `daily/` - End-of-day reflections
  - `YYYY-MM-DD.md` - What worked, what didn't, adjustments
- `weekly/` - Weekly synthesis
  - `YYYY-WW.md` - Patterns, metrics, strategic adjustments
- `project/` - Project retrospectives
  - `{project_name}-retro.md` - What to repeat/avoid
- `strategic/` - Strategic pivots
  - `YYYY-MM-DD-{topic}.md` - Major direction changes with rationale
**Persistence**: Git-tracked, append-only

### Layer 7: Decisions Memory (Persistent, Git-tracked)
**Purpose**: Record of significant decisions with rationale
**Location**: `memory/decisions/`
**Contents**:
- `YYYY-MM-DD-{topic}.md` - Decision records
  - Decision: What was decided
  - Context: Why it was needed
  - Options: What was considered
  - Rationale: Why this option
  - Reversibility: How to undo if wrong
  - Review date: When to revisit
- Index: `index.md` - Chronological list with status
**Persistence**: Git-tracked, immutable once recorded

### Layer 8: Preferences Memory (Persistent, Git-tracked)
**Purpose**: Learned preferences and defaults
**Location**: `memory/preferences/`
**Contents**:
- `communication.md` - Tone, length, channel preferences
- `scheduling.md` - Optimal times for outreach, meetings
- `tooling.md` - Preferred tools, integrations, shortcuts
- `workflow.md` - Default processes, templates, sequences
- `client_defaults.md` - Default assumptions for new clients
**Persistence**: Git-tracked, updated when patterns stabilize

### Layer 9: Checkpoints (Session persistence, Not Git)
**Purpose**: Fast session resume
**Location**: `runtime/cache/` (already exists)
**Contents**: Runtime state serialization (OperatingContext.to_dict())
**Persistence**: Local file only, overwritten each session
**Excludes**: Working memory scratchpad, sensitive data

---

## 3. Boot Sequence Integration

### Updated Boot Sequence (Phase 10)

```markdown
# Phase 10 — Load Memory
Load:
memory/identity/           # Static identity (once)
memory/working/            # Restore from checkpoint or fresh
memory/longterm/clients/   # Client context if active project
memory/skills/             # Available skills index
memory/preferences/        # Loaded defaults

# Phase 11 — Restore Working Memory
If checkpoint exists AND valid:
  Restore working memory from checkpoint
  Verify critical docs unchanged
Else:
  Initialize fresh working memory

# Phase 12 — Activate Skills
Load relevant skills based on:
  - Current objective
  - Active client
  - Current department
```

### Memory Loading Priority

| Priority | Layer | When |
|----------|-------|------|
| 1 | Identity | Always (once) |
| 2 | Working | Always (session) |
| 3 | Skills | On demand (by objective) |
| 4 | Long-term (clients) | When client active |
| 5 | Preferences | Always (defaults) |
| 6 | Checkpoints | On resume |
| 7 | Reflections/Decisions | On demand (learning) |

---

## 4. File Structure

```
CraftworkflowOS/
├── memory/                    # NEW - Persistent memory (Git-tracked)
│   ├── identity/
│   │   ├── role.md
│   │   ├── mission.md
│   │   ├── principles.md
│   │   └── authority.md
│   ├── working/               # NOT in Git (runtime only)
│   │   ├── current_objective.md
│   │   ├── active_projects.md
│   │   ├── current_client.md
│   │   ├── session_notes.md
│   │   └── inbox_snapshot.md
│   ├── longterm/
│   │   ├── clients/
│   │   ├── patterns/
│   │   ├── relationships/
│   │   └── market_intelligence/
│   ├── episodic/
│   │   └── 2026-07-15-example.md
│   ├── skills/
│   │   ├── outreach/
│   │   ├── discovery/
│   │   ├── proposal/
│   │   ├── onboarding/
│   │   └── internal/
│   ├── reflections/
│   │   ├── daily/
│   │   ├── weekly/
│   │   ├── project/
│   │   └── strategic/
│   ├── decisions/
│   │   └── index.md
│   └── preferences/
│       ├── communication.md
│       ├── scheduling.md
│       ├── tooling.md
│       ├── workflow.md
│       └── client_defaults.md
├── runtime/
│   ├── cache/
│   │   └── runtime_cache.json      # Checkpoints (NOT in Git)
│   └── memory/
│       ├── manager.py              # Memory management
│       ├── identity.py             # Identity layer
│       ├── working.py              # Working memory
│       ├── longterm.py             # Long-term memory
│       ├── episodic.py             # Episodic memory
│       ├── skills.py               # Skills registry
│       ├── reflections.py          # Reflections
│       ├── decisions.py            # Decisions log
│       ├── preferences.py          # Preferences
│       └── checkpoints.py          # Checkpoint integration
└── .gitignore
    # memory/working/
    # runtime/cache/
```

---

## 5. Git Tracking Rules

### ✅ COMMITTED (Version Controlled)
| Path | Reason |
|------|--------|
| `memory/identity/` | Defines Hermes, changes require approval |
| `memory/longterm/` | Accumulated business knowledge |
| `memory/episodic/` | Immutable history of experiences |
| `memory/skills/` | Reusable procedures, team-shared |
| `memory/reflections/` | Learning record, audit trail |
| `memory/decisions/` | Decision audit trail |
| `memory/preferences/` | Learned defaults, team-shared |

### ❌ NOT COMMITTED (Gitignored)
| Path | Reason |
|------|--------|
| `memory/working/` | Session-scoped, contains scratchpad |
| `runtime/cache/` | Checkpoints, auto-generated, session-specific |
| Any file with API keys, secrets, tokens | Security |

### .gitignore Additions
```gitignore
# Memory - working (session only)
memory/working/

# Runtime cache - checkpoints
runtime/cache/
```

---

## 6. Memory Manager API

```python
class MemoryManager:
    """Central memory management for Hermes."""
    
    def __init__(self, workspace_root: Path):
        self.root = workspace_root
        self.memory_root = workspace_root / "memory"
    
    # Identity
    def load_identity(self) -> IdentityMemory
    def save_identity(self, identity: IdentityMemory)
    
    # Working Memory
    def load_working(self, checkpoint: dict = None) -> WorkingMemory
    def save_working(self, working: WorkingMemory)
    
    # Long-term
    def get_client(self, name: str) -> ClientProfile
    def save_client(self, client: ClientProfile)
    def list_clients() -> List[str]
    def add_pattern(self, pattern: Pattern)
    
    # Episodic
    def record_episode(self, episode: Episode)
    def get_episodes(self, since: datetime = None) -> List[Episode]
    
    # Skills
    def load_skill(self, name: str) -> Skill
    def list_skills(category: str = None) -> List[str]
    def save_skill(self, skill: Skill)
    
    # Reflections
    def add_reflection(self, reflection: Reflection)
    def get_recent_reflections(self, days: int = 7) -> List[Reflection]
    
    # Decisions
    def record_decision(self, decision: Decision)
    def get_decisions(self, topic: str = None) -> List[Decision]
    
    # Preferences
    def load_preferences(self) -> Preferences
    def update_preference(self, key: str, value: Any)
    
    # Checkpoints
    def save_checkpoint(self, runtime_state: dict)
    def load_checkpoint() -> dict
```

---

## 7. Integration Points

### With Existing Systems
| System | Integration |
|--------|-------------|
| `runtime/checkpoint.py` | Extended to save/load working memory |
| `runtime/loader.py` | Loads memory during boot |
| `runtime/executive.py` | Uses memory for context |
| `runtime/commercial_briefing.py` | Records episodes, updates clients |
| `runtime/workspace_api.py` | Exposes memory via CLI |

### With Documentation
- Memory **never** duplicates 00-09 folder content
- Memory **references** docs by path (e.g., "see 01_CEO/company.md")
- Memory **extends** docs with experience (e.g., "Client X preferred Flow 2")

---

## 8. Implementation Plan

### Phase 1: Foundation (Day 1)
1. Create memory directory structure
2. Add `.gitignore` entries
3. Create base memory manager class
4. Implement identity layer (copy from 02_COO/identity.md)

### Phase 2: Working Memory & Checkpoints (Day 1-2)
1. Working memory data structures
2. Extend checkpoint system to include working memory
3. Integrate with boot sequence (Phase 10-12)

### Phase 3: Long-term & Episodic (Day 2)
1. Client profiles and history
2. Episode recording
3. Pattern extraction

### Phase 4: Skills & Reflections (Day 2-3)
1. Skills registry from existing playbooks
2. Reflection system (daily/weekly)
3. Decision logging

### Phase 5: Preferences & Integration (Day 3)
1. Preferences system
2. Wire into executive loop
3. Update commercial briefing to use memory

### Phase 6: Documentation & Testing (Day 3)
1. Document architecture
2. Test full memory cycle
3. Commit and push

---

## 9. Success Criteria

- [ ] Hermes survives reboot with full context
- [ ] Client history accumulates across sessions
- [ ] Skills are discoverable and reusable
- [ ] Decisions are auditable
- [ ] Reflections improve future performance
- [ ] No documentation duplication
- [ ] Git history shows memory evolution
- [ ] Checkpoints enable <5 second resume