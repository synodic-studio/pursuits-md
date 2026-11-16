# Pursuits MD 0.1.1

A Markdown ticket tree with reciprocal wikilinks and generated Mermaid diagrams. Each ticket holds its goal, acceptance criteria, status, and notes. A parent file sits beside the ID-named folder that holds its children.

The [v0.1 trial notes](docs/v0.1-trial.md) explain the ticket, review, and navigation conventions documented in v0.1.1.

## Try the example

Open the [example overview](examples/demo-vault/pursuits/README.md) on GitHub and click a ticket in the chart. A double-sided box identifies a ticket with a continuation. The Markdown links below each diagram also open the tickets.

To verify the published example from a checkout, run the helper with [uv](https://docs.astral.sh/uv/). It uses Python 3.11 or newer and PyYAML.

```sh
uv run tools/pursuit_graph.py check --vault examples/demo-vault \
  --github-base /synodic-studio/pursuits-md/blob/HEAD/examples/demo-vault
```

To try the same tree locally in Obsidian, run `uv run tools/pursuit_graph.py render --vault examples/demo-vault` and open that folder as a vault. The helper generates vault-local diagram destinations by default.

## Use your own vault

1. Put an overview `README.md` and your tickets under `pursuits/`. Set `--pursuits-dir` for a different vault-relative folder. Set `--vault` when running outside the vault.
2. Use the [example ticket](examples/demo-vault/pursuits/DSK%20-%20Desk%20Setup.md) as a template. Quote IDs in YAML so numeric IDs stay text. Put each child in its parent's ID folder. Write both sides of each relationship as slash-separated wikilinks relative to the vault, with no `.md` suffix.
3. Put the following block in the overview. The helper manages Mermaid blocks immediately preceded by this marker.

   ~~~markdown
   <!-- pursuits-md:graph -->
   ```mermaid
   flowchart LR
   ```
   ~~~

4. Run `render` to update the diagrams and ticket links. Run `check` to validate the tree and catch stale diagrams or links. Use `render --continuation ID` to start a new continuation on a ticket with children. Subsequent runs recognize its marked block.

When publishing to GitHub, pass `--github-base /OWNER/REPO/blob/REF/PATH/TO/VAULT` to both commands. The built-in GitHub diagram viewer resolves clicks from the site root. The published example uses `HEAD` to follow this repository's default branch. Use a specific branch or tag for a publication tied to that ref.

The helper checks filenames, IDs, parent and child links, folder placement, cycles, status, executor, and completion consistency. It updates diagrams. Edit ticket content, properties, and file placement directly in your vault.

See the [proposal](openspec/changes/markdown-pursuit-tree/proposal.md), [design](openspec/changes/markdown-pursuit-tree/design.md), [requirements](openspec/changes/markdown-pursuit-tree/specs/pursuit-tree/spec.md), and [implementation tasks](openspec/changes/markdown-pursuit-tree/tasks.md) for the broader design.
