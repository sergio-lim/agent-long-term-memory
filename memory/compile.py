"""Compile notes into a wiki: one page per tag/entity, plus an index."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re

from memory.store import Note, slugify

WIKILINK_RE = re.compile(r"\[\[([^\[\]]+)\]\]")


def extract_entities(text: str) -> list[str]:
    """Return ``[[WikiLink]]`` targets from a note body."""
    return [match.strip() for match in WIKILINK_RE.findall(text) if match.strip()]


def _backlink_line(note: Note) -> str:
    note_ref = f"../notes/{note.id}.md" if note.path else note.id
    return (
        f"- **[{note.title}]({note_ref})** — source: `{note.source}`"
        f" · `{note.id}`"
    )


def _page_markdown(label: str, kind: str, notes: list[Note]) -> str:
    unique: dict[str, Note] = {note.id: note for note in notes}
    ordered = sorted(unique.values(), key=lambda note: note.title.lower())
    lines = [
        f"# {label}",
        "",
        f"{len(ordered)} notes linked as **{kind}** `{label}`.",
        "",
        "## Notes",
        "",
    ]
    for note in ordered:
        lines.append(_backlink_line(note))
        if note.tags:
            lines.append(f"  - tags: {', '.join(f'`{tag}`' for tag in note.tags)}")
        snippet = note.text.replace("\n", " ").strip()
        if snippet:
            lines.append(f"  - _{snippet[:180]}{'…' if len(snippet) > 180 else ''}_")
        lines.append("")
    lines.extend(
        [
            "## Backlinks",
            "",
            "Every line above is a backlink: the wiki page does not own the fact,",
            "the **source** on the note does.",
            "",
        ]
    )
    return "\n".join(lines)


def _index_markdown(
    notes: list[Note],
    tags: dict[str, list[Note]],
    entities: dict[str, list[Note]],
) -> str:
    sources = sorted({note.source for note in notes})
    lines = [
        "# Wiki index",
        "",
        "Compiled from the markdown store. Each tag and entity page lists the",
        "notes that mention it, and each note still points at its original source.",
        "",
        f"- notes: **{len(notes)}**",
        f"- tags: **{len(tags)}**",
        f"- entities: **{len(entities)}**",
        f"- sources: **{len(sources)}**",
        "",
        "## Tags",
        "",
    ]
    if tags:
        for tag in sorted(tags):
            count = len({note.id for note in tags[tag]})
            lines.append(f"- [{tag}]({slugify(tag)}.md) — {count} notes")
    else:
        lines.append("_No tags yet._")
    lines.extend(["", "## Entities", ""])
    if entities:
        for name in sorted(entities, key=str.lower):
            count = len({note.id for note in entities[name]})
            lines.append(f"- [{name}](ent-{slugify(name)}.md) — {count} notes")
    else:
        lines.append("_No `[[WikiLink]]` entities yet._")
    lines.extend(["", "## All notes", ""])
    for note in sorted(notes, key=lambda item: item.title.lower()):
        href = f"../notes/{note.id}.md" if note.path else note.id
        lines.append(f"- [{note.title}]({href}) ← `{note.source}`")
    lines.append("")
    return "\n".join(lines)


def compile_wiki(notes: list[Note], wiki_dir: Path | str) -> list[Path]:
    """Write ``wiki/<tag>.md``, ``wiki/ent-<entity>.md``, and ``wiki/index.md``."""
    directory = Path(wiki_dir)
    directory.mkdir(parents=True, exist_ok=True)
    for stale in directory.glob("*.md"):
        stale.unlink()

    tags: dict[str, list[Note]] = defaultdict(list)
    entities: dict[str, list[Note]] = defaultdict(list)
    for note in notes:
        for tag in note.tags:
            tags[tag].append(note)
        for entity in extract_entities(note.text):
            entities[entity].append(note)

    written: list[Path] = []
    for tag, group in sorted(tags.items()):
        path = directory / f"{slugify(tag)}.md"
        path.write_text(_page_markdown(tag, "tag", group), encoding="utf-8")
        written.append(path)
    for name, group in sorted(entities.items(), key=lambda item: item[0].lower()):
        path = directory / f"ent-{slugify(name)}.md"
        path.write_text(_page_markdown(name, "entity", group), encoding="utf-8")
        written.append(path)

    index = directory / "index.md"
    index.write_text(_index_markdown(notes, tags, entities), encoding="utf-8")
    written.append(index)
    return written
