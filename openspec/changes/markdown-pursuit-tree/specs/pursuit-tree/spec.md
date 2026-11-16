# Pursuit Tree — Specification

## ADDED Requirements

### Requirement: Durable ticket identity
The system SHALL store every ticket in its own Obsidian-compatible Markdown document with a unique immutable three-character Crockford Base32 ID and short descriptive title.

Each title SHALL name one outcome in concise title case. Independently reviewable outcomes SHALL use separate tickets.

#### Scenario: Create or rename
- **WHEN** an agent creates a ticket
- **THEN** it allocates an unused ID and creates its file
- **AND** a later rename preserves the ID and repairs references.

### Requirement: Single-parent filesystem tree
Every non-root ticket SHALL have exactly one parent and MAY have unlimited children and depth. Child files SHALL reside in the parent's ID-only sibling folder. Parent and ordered child fields SHALL use reciprocal Obsidian wikilinks.

#### Scenario: Reparent a subtree
- **WHEN** a ticket moves to another parent
- **THEN** its descendants, files, metadata, and affected diagrams are reconciled without changing IDs.

### Requirement: Nonhierarchical references
Tickets MAY reference other tickets as `related` wikilinks. The system SHALL exclude these references from parent relationships and diagram edges.

#### Scenario: Related pursuit
- **WHEN** a ticket links to another as related
- **THEN** the single-parent tree and diagram structure remain unchanged.

### Requirement: Visual navigation
Every ticket SHALL appear in a Mermaid diagram, ordinarily exactly once. A transition ticket SHALL appear exactly twice: at the right edge of its preceding diagram and as leftmost root of its continuation diagram in its own document. Every diagram ticket node SHALL link directly to its own document. No child tables SHALL be required.

#### Scenario: Follow a diagram handoff
- **WHEN** a user views a diagram with a boundary ticket
- **THEN** the boundary ticket has a double-sided outline
- **AND** selecting the ticket opens its document with the continuation diagram immediately after frontmatter.

### Requirement: Bounded horizontal depth
Diagrams SHALL use left-to-right layout, normally 3–5 generations, with five as default maximum unless an explicit space-based exception is justified. There SHALL be no sibling or total-tree depth limit.

#### Scenario: Many children
- **WHEN** a node has numerous children
- **THEN** all may be shown in the generation without an arbitrary sibling cap.

### Requirement: Accessible status presentation
Nodes SHALL show the ticket title above a separate line with the stable ID and written status. The ID SHALL use monospace when supported. The status dot palette SHALL be gray Open, yellow Defining, green Working, blue Done, red Blocked, and purple Paused.

#### Scenario: Color unavailable
- **WHEN** a user cannot distinguish colors
- **THEN** statuses remain understandable from labels.

### Requirement: Optional scheduling and prioritization
Tickets MAY omit `due`, `urgency`, and `importance`. When present, due SHALL be an ISO date and urgency/importance SHALL each be an integer from 1 through 4.

#### Scenario: No priority
- **WHEN** no importance score is provided
- **THEN** the ticket remains valid and no default score is fabricated.

### Requirement: Single-executor actionable leaves
A ready executable leaf SHALL have exactly one executor (`human` or `agent`), sufficient context, and verifiable acceptance criteria. Fully decomposed parents MAY be `unassigned`.

#### Scenario: Mixed human and agent work
- **WHEN** independent human and agent actions coexist
- **THEN** the agent proposes sibling or dependent child tickets separating the executors.

### Requirement: Completion consistency
A ticket SHALL be `done` only when its own criteria and all children are complete. Adding or reopening unfinished children SHALL reopen completed parents and affected ancestors. Post-completion discoveries MAY instead be captured in a new sibling ticket when they represent a distinct outcome.

#### Scenario: Add child to done ticket
- **WHEN** a new unfinished child is added to a done ticket
- **THEN** the ticket and any affected completed ancestors reopen.

#### Scenario: Distinct follow-up work
- **WHEN** new work is a distinct outcome after a sibling's completion
- **THEN** a new sibling MAY be created without reopening the completed ticket.

### Requirement: Human Notes inbox
Every ticket SHALL include a Notes section with native numbered-list input, initialized with `1.` followed by one ASCII space. Agents SHALL NOT add their own working notes there; agents SHALL write substantive content to flexible main-matter sections.

#### Scenario: Dictate feedback
- **WHEN** a human opens any ticket
- **THEN** an empty numbered Notes item is available for input.

### Requirement: Traceable notes processing
When agents process Notes, they SHALL record interpretation and resulting edits in the ticket's Change Log and clear only successfully processed notes. Unresolved notes SHALL remain. When no notes remain, agents SHALL leave `1.` followed by one ASCII space.

#### Scenario: Ambiguous note
- **WHEN** an agent cannot confidently interpret a note
- **THEN** it retains that note and requests clarification instead of discarding it.

### Requirement: Referenceable list items
All unordered-list items SHALL use native Markdown bullets plus unique letter labels across each ticket, extending beyond `z` as `aa`, `ab`, etc. Existing labels SHOULD remain stable across edits. Notes SHALL instead use native numbered lists; ordered procedural lists SHALL use numbers.

#### Scenario: Insert criterion
- **WHEN** a new acceptance criterion is inserted
- **THEN** it receives an unused letter label without unnecessarily changing established references.

### Requirement: Agent continuity and structural maintenance
An agent SHALL be able to reconstruct a ticket's state and resume without chat history. Agents SHALL maintain files, relationships and diagrams when performing structural edits.

#### Scenario: Fresh session
- **WHEN** a new agent enters a ticket
- **THEN** it can determine its objective, constraints, status, outstanding feedback and remaining work from durable artifacts.

### Requirement: Reviewable agent work
Agents SHALL create or identify a ticket when taking on substantial work and record the approach, what was verified, and remaining limits in the ticket before linking to the result. An independently reviewable outcome that supports a larger decision or execution task SHALL be represented by a child ticket. The parent and child SHALL have their own acceptance criteria.

#### Scenario: Research informs a later decision
- **WHEN** an agent compares desk mats before the user chooses one
- **THEN** the tree shows the research as an agent ticket with the checks performed and a link to the comparison findings
- **AND** the selection ticket stays open until its own acceptance criteria are met.

### Requirement: Obsidian compatibility and validation
Canonical files SHALL use Obsidian-compatible Markdown, YAML, wikilinks, lists, checkboxes and Mermaid without custom plugins. Validation SHALL identify malformed IDs, duplicate IDs, broken links, cycles, inconsistent parents/children, invalid status or priority, incorrect completion states, misplaced files, and diagram violations.

#### Scenario: Open on iPad
- **WHEN** a user opens a ticket in Obsidian on iPad
- **THEN** they can inspect content and diagrams, follow ticket links and add numbered Notes.
