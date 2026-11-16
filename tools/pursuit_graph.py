#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6,<7"]
# ///
"""Validate the pursuit tree and regenerate its linked Obsidian diagrams."""

import argparse
from dataclasses import dataclass
from html import escape
from pathlib import Path
import re
from tempfile import NamedTemporaryFile
from urllib.parse import quote

import yaml


ID = r"[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{3}"
TICKET_NAME = re.compile(rf"({ID}) - (.+)\.md")
DIAGRAM_MARKER = "<!-- pursuits-md:graph -->"
DIAGRAM = re.compile(
    rf"^{re.escape(DIAGRAM_MARKER)}\n^```mermaid\n.*?^```\n",
    re.MULTILINE | re.DOTALL,
)
NODE = re.compile(rf"^\s+T({ID})\[", re.MULTILINE)
PALETTE = {
    "open": ("⚪", "#818994"),
    "working": ("🟢", "#389364"),
    "done": ("🔵", "#4185ba"),
    "defining": ("🟡", "#bd861e"),
    "blocked": ("🔴", "#bb5555"),
    "paused": ("🟣", "#8b65a3"),
}


@dataclass
class Ticket:
    id: str
    title: str
    path: Path
    text: str
    status: str
    parent: str | None
    children: list[str]

    @property
    def target(self) -> str:
        return self.path.with_suffix("").as_posix()


def read_tickets(vault: Path, pursuit_root: Path) -> dict[str, Ticket]:
    tickets = {}
    for file in sorted(pursuit_root.rglob("*.md")):
        match = TICKET_NAME.fullmatch(file.name)
        if not match:
            if re.match(r"[A-Z0-9]{3} - ", file.name):
                raise ValueError(f"{file}: invalid ticket filename")
            continue
        id, title = match.groups()
        text = file.read_text(encoding="utf-8")
        header = text.split("---\n", 2)
        if len(header) != 3 or header[0]:
            raise ValueError(f"{file}: expected YAML frontmatter")
        meta = yaml.safe_load(header[1])
        if not isinstance(meta, dict) or meta.get("id") != id or id in tickets:
            raise ValueError(f"{file}: invalid or duplicate ticket ID {id}")
        if not isinstance(meta.get("status"), str) or meta["status"] not in PALETTE:
            raise ValueError(f"{file}: invalid status")
        if meta.get("executor") not in (
            "agent", "human", "unassigned"
        ):
            raise ValueError(f"{file}: invalid executor")
        if not isinstance(meta.get("children"), list) or "parent" not in meta:
            raise ValueError(f"{file}: expected parent and children fields")
        if meta["parent"] is not None and not isinstance(meta["parent"], str):
            raise ValueError(f"{file}: expected a parent wikilink or null")
        if f"\n# {title}\n" not in text:
            raise ValueError(f"{file}: title differs from the filename")
        tickets[id] = Ticket(
            id, title, file.relative_to(vault), text, meta["status"], meta["parent"], meta["children"]
        )
    if not tickets:
        raise ValueError(f"No tickets found in {pursuit_root}")
    return tickets


def validate_tree(tickets: dict[str, Ticket]) -> dict[str, Ticket]:
    links = {f"[[{ticket.target}]]": ticket for ticket in tickets.values()}
    for ticket in tickets.values():
        own_link = f"[[{ticket.target}]]"
        if any(not isinstance(link, str) for link in ticket.children):
            raise ValueError(f"{ticket.path}: children must be wikilinks")
        if len(set(ticket.children)) != len(ticket.children):
            raise ValueError(f"{ticket.path}: duplicate child")
        for child_link in ticket.children:
            child = links.get(child_link)
            if child is None or child.parent != own_link:
                raise ValueError(f"{ticket.path}: invalid child {child_link}")
            if child.path.parent != ticket.path.parent / ticket.id:
                raise ValueError(f"{child.path}: expected to be in {ticket.id}/")
            if ticket.status == "done" and child.status != "done":
                raise ValueError(f"{ticket.path}: completed ticket has open child {child.id}")
        if ticket.parent is not None:
            parent = links.get(ticket.parent)
            if parent is None or own_link not in parent.children:
                raise ValueError(f"{ticket.path}: parent link has no matching child")
        if ticket.status == "done" and re.search(r"^- \[ \]", ticket.text, re.MULTILINE):
            raise ValueError(f"{ticket.path}: completed ticket has an unchecked criterion")
    for ticket in tickets.values():
        seen = {ticket.id}
        parent_link = ticket.parent
        while parent_link is not None:
            parent = links[parent_link]
            if parent.id in seen:
                raise ValueError(f"{ticket.path}: parent cycle")
            seen.add(parent.id)
            parent_link = parent.parent
    return links


def build_diagram(
    start: list[Ticket], links: dict[str, Ticket], continuations: set[str],
    owner: str | None, max_columns: int
) -> str:
    nodes, edges = [], []

    def visit(ticket: Ticket, depth: int) -> None:
        if depth > max_columns:
            raise ValueError(f"{ticket.path}: diagram exceeds {max_columns} columns. Choose a continuation.")
        nodes.append(ticket)
        if ticket.id in continuations and ticket.id != owner:
            return
        for link in ticket.children:
            child = links[link]
            edges.append((ticket.id, child.id))
            visit(child, depth + 1)

    for ticket in start:
        visit(ticket, 1)
    lines = [
        DIAGRAM_MARKER, "```mermaid", "flowchart LR", '    subgraph horizontal[" "]', "        direction LR"
    ]
    for ticket in nodes:
        title = escape(ticket.title, quote=False).replace('"', "#quot;")
        dot, _ = PALETTE[ticket.status]
        label = f'"{title}<br/><code>{ticket.id}</code> {dot} {ticket.status.title()}"'
        if ticket.id in continuations and ticket.id != owner:
            label = f"[{label}]"
        lines.append(f"        T{ticket.id}[{label}]")
    lines.extend(f"        T{parent} --> T{child}" for parent, child in edges)
    lines.extend(["    end", "    style horizontal fill:none,stroke:none,stroke-width:0px;"])
    for ticket in nodes:
        uri = quote(ticket.target, safe="")
        lines.append(f'    click T{ticket.id} "obsidian://open?file={uri}"')
    for status, (_, color) in PALETTE.items():
        members = [f"T{ticket.id}" for ticket in nodes if ticket.status == status]
        if members:
            lines.append(f"    classDef {status}Ticket stroke:{color},stroke-width:2px;")
            lines.append(f"    class {','.join(members)} {status}Ticket;")
    return "\n".join([*lines, "```", ""])


def render_plan(
    vault: Path, overview: Path, tickets: dict[str, Ticket], continuations: set[str], max_columns: int
) -> dict[Path, tuple[str, str]]:
    links = validate_tree(tickets)
    old_overview = overview.read_text(encoding="utf-8")
    old_diagram = DIAGRAM.search(old_overview)
    if old_diagram is None:
        raise ValueError(f"{overview}: missing Mermaid block marked with {DIAGRAM_MARKER}")
    order = dict.fromkeys(NODE.findall(old_diagram[0]))
    order.update(dict.fromkeys(tickets))
    roots = [tickets[id] for id in order if id in tickets and tickets[id].parent is None]
    planned = {
        overview: (old_overview, DIAGRAM.sub(
            lambda _: build_diagram(roots, links, continuations, None, max_columns), old_overview, count=1
        )),
    }
    for id in sorted(continuations):
        ticket = tickets.get(id)
        if ticket is None or not ticket.children:
            raise ValueError(f"Continuation {id} must have a ticket with children")
        block = build_diagram([ticket], links, continuations, id, max_columns)
        open_fence, header, body = ticket.text.split("---\n", 2)
        body = DIAGRAM.sub("", body, count=1)
        updated = f"{open_fence}---\n{header}---\n\n{block}\n{body.lstrip(chr(10))}"
        planned[vault / ticket.path] = ticket.text, updated
    return {path: pair for path, pair in planned.items() if pair[0] != pair[1]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "render"))
    parser.add_argument("--vault", type=Path, default=Path.cwd(), help="vault root (default: current directory)")
    parser.add_argument("--pursuits-dir", type=Path, default=Path("pursuits"),
                        help="pursuits directory relative to the vault (default: pursuits)")
    parser.add_argument("--continuation", action="append", default=[], metavar="ID",
                        help="start a continuation diagram at a ticket")
    parser.add_argument("--max-columns", type=int, default=5,
                        help="maximum diagram columns for the current tree (default 5)")
    args = parser.parse_args()
    if args.max_columns < 1:
        parser.error("--max-columns must be positive")
    if args.pursuits_dir.is_absolute() or ".." in args.pursuits_dir.parts:
        parser.error("--pursuits-dir must be a relative path within the vault")
    vault = args.vault.resolve()
    pursuit_root = (vault / args.pursuits_dir).resolve()
    if not pursuit_root.is_relative_to(vault):
        parser.error("--pursuits-dir must stay within the vault")
    try:
        tickets = read_tickets(vault, pursuit_root)
        continuations = {id for id, ticket in tickets.items() if DIAGRAM.search(ticket.text)}
        updates = render_plan(
            vault, pursuit_root / "README.md", tickets,
            continuations | set(args.continuation), args.max_columns,
        )
        if args.command == "check" and updates:
            raise ValueError("Outdated diagrams\n" + "\n".join(str(path) for path in updates))
        if updates:
            for ticket in tickets.values():
                if (vault / ticket.path).read_text(encoding="utf-8") != ticket.text:
                    raise ValueError(f"{ticket.path}: changed during generation")
        for file, (before, after) in updates.items():
            with NamedTemporaryFile(mode="w", encoding="utf-8", dir=file.parent, prefix=".pursuits-", delete=False) as out:
                out.write(after)
            temp = Path(out.name)
            try:
                if file.read_text(encoding="utf-8") != before:
                    raise ValueError(f"{file}: changed during generation")
                temp.chmod(file.stat().st_mode & 0o777)
                temp.replace(file)
            finally:
                temp.unlink(missing_ok=True)
        print(f"{len(tickets)} tickets. {len(updates)} diagrams updated.")
    except (OSError, ValueError, yaml.YAMLError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
