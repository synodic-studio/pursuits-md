# Markdown Pursuit Tree — Design

## Unified model and IDs

All nodes are tickets; no separate handoff type. Every ticket has one Markdown document, short descriptive title, stable ID, status, parent (except root), and ordered children. No limit on tree depth or siblings. IDs are three random uppercase, case-insensitive Crockford Base32 characters from `0123456789ABCDEFGHJKMNPQRSTVWXYZ` (32,768 possibilities). Check existing **and archived** IDs; never reuse. Validate duplicates on merges. An optional index can be reconstructed by scanning files. ID is a shorthand handle; title is the human-readable name.

## Paths and references

Prefer vault links for working notes and artifacts. Keep outside URLs as sources or for actions that must happen on an external service. Confirm whether linked attachments sync to the devices where they are needed.

Files use `<ID> - <Short title>.md`; the sibling folder containing immediate child documents is named `<ID>/` only. Move descendants with their parent; rename filenames but not ID folders. Parent and children are reciprocal Obsidian `[[wikilinks]]`, updated on moves/renames. Use paths relative to the vault root. No body tables of children. Optional `related` wikilinks allow nonhierarchical connections and do not create diagram edges or additional parents.

```text
pursuits/
  README.md
  7KM - Independent Software.md
  7KM/
    2HF - Component Library.md
    2HF/
      9PV - Define API.md
      4RT - Documentation.md
```

## Metadata

```yaml
---
id: "2HF"
status: open
executor: unassigned
parent: "[[pursuits/7KM - Independent Software]]"
children:
  - "[[pursuits/7KM/2HF/9PV - Define API]]"
  - "[[pursuits/7KM/2HF/4RT - Documentation]]"
related: []
due: 2026-12-15
urgency: 3
importance: 4
---
```

Required: `id`, `status`, `executor`, `parent` (null for roots), `children` (empty for leaves). `related`, `due`, `urgency`, `importance` optional; omit if unknown. Dates are ISO `YYYY-MM-DD`; urgency and importance are **integers 1–4 only**. Agents may propose but must not silently override human priorities.

Statuses: `open` (gray), `defining` (yellow), `working` (green), `done` (blue). `blocked` and `paused` are permitted with explicit text labels; their visual styles may be refined. Every diagram node shows readable status text, not color alone. Test contrast in light/dark Obsidian themes.

## Executor, granularity and completion

Executors: `human`, `agent`, `unassigned`. A ready actionable leaf has exactly one executor, one coherent independently verifiable outcome, sufficient context, and acceptance criteria; no rigid duration, word-count or complexity threshold. Mixed human/agent work should generally be split into siblings or dependent generations. Fully decomposed parents may be unassigned. A ticket is `done` only when its own acceptance criteria and all children's completion conditions are met. Adding an unfinished child to a done ticket reopens it and affected completed ancestors; reopening a child similarly propagates. New work discovered after completion may instead be a **sibling** when it is a distinct outcome; the original ticket remains done. Both choices are valid, based on whether original completion requirements have expanded.

Use concise title case for all tickets, including branch titles. Use a noun phrase when it clearly names the outcome, such as “Desk Setup”. When a draft title needs “and” to join different outcomes, split them into siblings or name the one result that the work supports.

## Document layout

YAML frontmatter comes first. **If present, the Mermaid diagram immediately follows frontmatter**, before title and prose. The flexible main body contains at minimum Description/Context, Acceptance Criteria, and Notes; agents may add headings for research, constraints, decisions, dependencies, progress, etc. Agents write content to the main body, **never Notes**.

```markdown
---
id: "2HF"
status: open
executor: unassigned
parent: "[[pursuits/7KM - Independent Software]]"
children: []
---

# Component Library

## Description

Brief intent and essential context.

## Acceptance Criteria

- [ ] a. First observable outcome.
- [ ] b. Second observable outcome.

## Notes

1. 

## Change Log
```

All unordered-list items, including checkboxes, use native Markdown bullets **plus unique letter labels across the entire ticket** (`a`…`z`, then `aa`, `ab`…). Labels need not be sequential after edits; preserve established references instead of renumbering. Ordered procedural lists use native numbered lists. **Notes is an exception:** use native numbered entries, automatically managed by Obsidian, with one empty numbered entry after processing. Agents should not edit human notes except as part of explicit processing. Section-scoped references may be used for clarity.

## Human Notes inbox and Change Log

Notes are human-only capture for typing/dictation. Agents detect unprocessed numbered notes (trigger mechanism deferred), interpret and apply clear feedback to main matter or tickets, and record each processed note's original number, interpretation and resulting changes in a `Change Log` section directly beneath Notes. When initializing a ticket or clearing the last processed note, leave `1.` followed by exactly one space. The trailing space is intentional so the user can start typing immediately. Keep ambiguous/unresolved notes intact and ask for clarification. Git history may supplement the in-ticket log. Preserve the original meaning; never silently discard notes.

## Diagrams

Use Obsidian-compatible Mermaid `flowchart LR`, with ticket nodes linking **directly to their own Markdown documents**. Display normally 3–5 horizontal generations; five is the default hard maximum unless available horizontal space justifies an explicit exception. Unlimited siblings and total tree depth. Every ticket appears in one diagram, except a diagram-transition ticket appearing **exactly twice**: rightmost at the preceding diagram boundary and leftmost as root in the continuation diagram contained in its own document. Same ordinary ticket, ID, title, and file in both places. No synthetic connector nodes or child tables. Choose breakpoints at useful, preferably natural conceptual divisions. The pursuits directory’s `README.md` holds the overview diagram. The graph helper identifies generated blocks by the `<!-- pursuits-md:graph -->` marker directly above their opening fence. Every ticket with children does **not** need a diagram. Metadata and filesystem are canonical; diagrams are derived navigational representations, initially maintainable by agents. Canvas is a possible later alternative, not part of v0.1.

Put the ticket title above its monospace ID, status dot, and status text. The ID and status share one line, for example `9PV 🔵 Done`. Long titles may wrap. Use gray for Open, yellow for Defining, green for Working, blue for Done, red for Blocked, and purple for Paused. Keep the status text readable on either theme.

In the preceding diagram, use Mermaid’s double-sided box (`TABC[["Title"]]`) for a ticket that opens a continuation diagram. Use the regular box for the root shown in its own diagram. Check that every rendered parent-to-child arrow advances to the right. Siblings can share a column.

Keep `flowchart LR` and put all the nodes and edges inside an unlabelled `subgraph horizontal[" "]` with `direction LR`. Hide the group border and fill with `style horizontal fill:none,stroke:none,stroke-width:0px;`. This preserves the left-to-right layout when Pele auto-adjusts for narrow screens. [Pele narrow-screen behavior](https://github.com/obsidianmd/pele/blob/main/website/src/content/docs/api.md#narrow-screens)

Use `<br/>` for the line break and `<code>` for the ID. Add a separate Mermaid `click` directive for each node, with `obsidian://open?file=` followed by the percent-encoded vault-relative ticket path. The link opens the note in the active vault. This format uses Obsidian’s URI click support from 1.15.1. [Obsidian 1.15.1 release notes](https://obsidian.md/changelog/2026-11-03-desktop-v1.15.1/)

## Agent operations and continuity

Refine objectives and acceptance criteria, maintain files and diagrams, research and cite findings, review gaps, and execute authorized work. Agents perform structural edits while humans navigate, annotate, and review. Fresh sessions must be able to reconstruct the objective, current state, relationships, unresolved feedback, and remaining work from durable artifacts. Escalate consequential ambiguity and respect approval boundaries.

Create or identify a ticket when taking on substantial agent work. Give a separately reviewable outcome its own child ticket when it supports a larger decision or execution task. On the work ticket, record the approach, important sources or checks, what was verified, and what remains open. Present that record before linking to the result or supporting note so the user can review the work from the tree. A short record in the existing ticket is enough for small checks that serve the same outcome. Use headings and detail appropriate to the work.

## Git and review

Git is optional infrastructure for history, recovery, reviewing substantial agent diffs/PRs, and reconciling concurrent edits. Not required for ordinary human note entry. Avoid silent overwrites and report conflicts.

## Archiving (deferred)

Evaluate in-place archive status vs archive directory/subtree vs dedicated top-level branch. Preserve IDs, historical context, and relationship integrity; never silently delete or recycle IDs.

## Validation and compatibility

Validate ID format/uniqueness, wikilinks, parent-child reciprocity, folder placement, cycles, statuses/executors, numeric priority bounds, completion invariants, diagram coverage/handoff placement/depth, and conflicting changes. All canonical Markdown, YAML, wikilinks, lists, checkboxes and Mermaid must render/work in Obsidian desktop and iPad without custom plugins.
