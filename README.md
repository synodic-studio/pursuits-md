# Pursuits MD 0.1.1

A Markdown ticket tree with reciprocal links and generated Obsidian diagrams. Each ticket holds its goal, acceptance criteria, status, and notes. A parent file sits beside the ID-named folder that holds its children.

The [v0.1 trial notes](docs/v0.1-trial.md) explain the ticket, review, and navigation conventions documented in v0.1.1.

## Try the example

From this directory, run the helper with [uv](https://docs.astral.sh/uv/). It uses Python 3.11 or newer and PyYAML.

```sh
uv run tools/pursuit_graph.py --vault examples/demo-vault check
uv run tools/pursuit_graph.py --vault examples/demo-vault render
```

Open `examples/demo-vault` as a vault in Obsidian and start with the [example overview](examples/demo-vault/pursuits/README.md). The double-sided node opens the ticket containing the continuation diagram. Diagram links use Obsidian URI support from 1.15.1. Use the overview's Markdown links in other readers.

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

4. Run `render` to update the diagrams and `check` to validate the tree and catch stale diagrams. Use `render --continuation ID` to start a new continuation on a ticket with children. Subsequent runs recognize its marked block.

The helper checks filenames, IDs, parent and child links, folder placement, cycles, status, executor, and completion consistency. It updates diagrams. Edit ticket content, properties, and file placement directly in your vault.

See the [proposal](openspec/changes/markdown-pursuit-tree/proposal.md), [design](openspec/changes/markdown-pursuit-tree/design.md), [requirements](openspec/changes/markdown-pursuit-tree/specs/pursuit-tree/spec.md), and [implementation tasks](openspec/changes/markdown-pursuit-tree/tasks.md) for the broader design.
