# Refresh Policy

## Purpose

The Refresh Policy defines when an AI employee should refresh information during an active session.

Its purpose is to minimize unnecessary file reads while ensuring decisions are based on current information.

The operating principle is:

> Never reload what is already understood. Refresh only what may have changed.

---

# Refresh Triggers

A refresh should occur when one or more of the following conditions are true:

- A new session begins.
- The CEO explicitly requests a refresh.
- A monitored file has changed.
- A task requires information that is not currently available.
- A decision depends on verifying the latest company state.

---

# Static Context

Static context rarely changes during a session.

Examples include:

- Company Mission
- Vision
- Identity
- Decision Principles
- README

Static context should be loaded once during session initialization.

It should only be refreshed if the underlying documentation changes.

---

# Dynamic Context

Dynamic context changes frequently.

Examples include:

- Company State
- Inbox
- Alerts
- Active Projects
- Active Clients
- Daily Briefs

Dynamic context should be refreshed whenever the current task depends on it.

---

# Reference Context

Reference context contains historical or supporting information.

Examples include:

- SOPs
- Meeting Notes
- Archived Projects
- Historical Logs
- Knowledge Base

Reference context should only be loaded when directly relevant to the current task.

---

# Memory

Long-term memory provides additional context.

Memory must never override documented company knowledge.

Memory should only be queried when:

- historical context is helpful
- relationships matter
- previous experiences may improve a recommendation

---

# Priority Order

When multiple sources are available:

1. Company Documentation
2. Current Company State
3. Historical Records
4. Long-Term Memory
5. General Model Knowledge

Higher-priority sources always override lower-priority sources.

---

# Objective

Maintain an accurate understanding of the business while minimizing unnecessary context loading and token usage.