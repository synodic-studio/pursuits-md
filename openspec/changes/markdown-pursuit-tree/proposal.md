# Markdown Pursuit Tree — Proposal

**Version:** 0.1

**Status:** Approved baseline

## Why

AI conversations quickly branch into multiple ideas, goals, questions, and work items. As threads multiply, humans and agents lose track of their context, progress, and unresolved work. This system externalizes those branches into a persistent, visually navigable tree so a person can contribute to any part at any time and agents can resume work without depending on chat history.

## What changes

- One Obsidian-compatible Markdown document per ticket, from exploratory pursuit to executable task.
- Strict single-parent tree with unlimited children and depth; stable three-character Crockford Base32 references.
- Short descriptive filenames, ID-only child folders, reciprocal wikilink relationships, and navigable left-to-right Mermaid diagrams.
- Agent-driven refinement, research, decomposition, reorganization, and execution, with direct human notes and traceable processing.
- Decomposition toward one human or agent executor per actionable leaf, while fully decomposed parents may remain unassigned.

## Goals and success criteria

- Users navigate and inspect the entire tree visually in Obsidian, including iPad, and add feedback directly to any ticket.
- Each ticket is independently addressable; agents can create, move, refine, and resume tickets with durable context and no reliance on prior conversations.
- Ready leaves have one coherent outcome, one executor, and verifiable acceptance criteria.
- Agents preserve valid relationships, diagram handoffs, notes provenance, and completion consistency.
- Canonical data remains ordinary Markdown/YAML/Mermaid without custom plugins or a proprietary service.

## Out of scope

Dedicated web/native app, Obsidian plugin, hosting/sync, Jira, mandatory Beads integration, autonomous scheduling/orchestration, and multi-user permissions. Git may be used for review and history but is not mandatory for routine edits.

## Open implementation questions

Notes-processing trigger and review UX; archiving mechanism; density/readability of Mermaid layouts; optional Canvas fallback; practical ticket-size heuristics; whether a separate Git review workflow adds value.
