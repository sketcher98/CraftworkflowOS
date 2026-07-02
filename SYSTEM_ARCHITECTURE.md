# CraftworkflowOS - System Architecture

Version: 1.0

## Purpose

CraftworkflowOS is an operating system for running CraftedWorkflows.

The system separates:

- Company Knowledge
- Runtime Execution
- Long-Term Memory
- AI Employees
- External Integrations

Each layer has a single responsibility.

---

# Layer 1 — Documentation

Purpose:

Defines the company's authoritative knowledge.

Examples:

- company.md
- identity.md
- decision_principles.md
- company_state.md
- SOPs

This layer is the source of truth.

---

# Layer 2 — Runtime

Purpose:

Manages the active operating session.

Responsibilities:

- Session initialization
- Context loading
- Runtime context
- Refresh management
- Reflection
- Cache management

The Runtime never invents company knowledge.

It only loads and manages it efficiently.

---

# Layer 3 — Memory

Purpose:

Stores historical experience.

Examples:

- Graph Memory
- Episodic Memory
- Semantic Memory

Memory provides context but never overrides documentation.

---

# Layer 4 — AI Employees

Examples:

- Hermes (COO)
- Claude
- GPT
- Future agents

AI employees execute work using the Runtime.

They never access documentation directly.

---

# Layer 5 — External Systems

Examples:

- GitHub
- Make
- Gmail
- Calendar
- OpenRouter
- Groq
- OpenAI

These systems extend the operating system.

---

# Information Flow

Documentation

↓

Runtime

↓

AI Employee

↓

Reflection

↓

Memory

↓

Next Task

Documentation always has the highest authority.


# Runtime Checkpoint

## Purpose

The Runtime Checkpoint allows Hermes to resume work quickly after a restart, computer shutdown, or power outage.

Instead of reloading the entire CraftworkflowOS workspace, Hermes should restore the most recent Runtime Checkpoint whenever possible.

This reduces startup time and minimizes unnecessary context loading.

---

## What is stored

The Runtime Checkpoint may contain:

- Session information
- Loaded company context
- Current company state
- Current objective
- Current project
- Current client
- Runtime cache
- Last refresh time

Long-term memory is NOT stored in the Runtime Checkpoint.

---

## Restore Policy

When Hermes starts:

1. Check whether a Runtime Checkpoint exists.
2. If the checkpoint is valid, restore it.
3. Verify that important company documents have not changed.
4. Refresh only the documents that have changed.
5. Continue working.

---

## Invalidation

A Runtime Checkpoint becomes invalid when:

- The CEO requests a fresh boot.
- Critical company files change.
- The checkpoint becomes corrupted.

Otherwise, Hermes should prefer restoring the checkpoint instead of rebuilding the session from scratch.

---

# Engineering Principles

CraftworkflowOS is built incrementally.

Every new feature must satisfy all three conditions:

1. It compiles.
2. It runs.
3. It provides a real business capability.

Avoid placeholder architecture.

Avoid speculative engineering.

Build only what the COO needs today.

Future capabilities should be documented, not implemented, until they become necessary.