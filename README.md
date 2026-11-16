# Pursuits MD 0.1.1

A Markdown ticket tree with reciprocal wikilinks and generated Mermaid diagrams. Each ticket holds its goal, acceptance criteria, status, and notes. A parent file sits beside the ID-named folder that holds its children.

The [v0.1 trial notes](docs/v0.1-trial.md) explain the ticket, review, and navigation conventions documented in v0.1.1.

## Try the example

Open `examples/demo-vault` as an Obsidian vault and click a ticket in the chart. A double-sided box identifies a ticket with a continuation. When browsing the [same example](examples/demo-vault/pursuits/README.md) on GitHub, use the Markdown links below each chart.

To validate the example from a checkout, run the helper with [uv](https://docs.astral.sh/uv/). It uses Python 3.11 or newer and PyYAML.

```sh
uv run tools/pursuit_graph.py check --vault examples/demo-vault
```

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

The default render generates clickable nodes for Obsidian. For clickable nodes in GitHub, pass the published vault URL to both commands, such as `--github-base https://github.com/OWNER/REPO/blob/REF/PATH/TO/VAULT`. Use the review branch for a PR preview and the release branch or tag for a published release. The Markdown links below the chart stay relative in both modes.

The helper checks filenames, IDs, parent and child links, folder placement, cycles, status, executor, and completion consistency. It updates diagrams. Edit ticket content, properties, and file placement directly in your vault.

See the [proposal](openspec/changes/markdown-pursuit-tree/proposal.md), [design](openspec/changes/markdown-pursuit-tree/design.md), [requirements](openspec/changes/markdown-pursuit-tree/specs/pursuit-tree/spec.md), and [implementation tasks](openspec/changes/markdown-pursuit-tree/tasks.md) for the broader design.
