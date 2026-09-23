"""Markdown note store with a tiny YAML-like frontmatter parser."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from pathlib import Path
import re
from typing import Iterable

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.DOTALL)
SLUG_RE = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True)
class Note:
    """One durable memory: body plus provenance in frontmatter."""

    id: str
    source: str
    title: str
    date: str
    tags: tuple[str, ...]
    text: str
    path: Path | None = None

    def searchable(self) -> str:
        """Title and tags repeated so BM25 prefers them over body text."""
        tags = " ".join(self.tags)
        return f"{self.title} {self.title} {tags} {tags} {self.text}"


def slugify(title: str, limit: int = 40) -> str:
    """Turn a title into a filesystem-safe slug."""
    slug = SLUG_RE.sub("-", title.lower()).strip("-")
    return slug[:limit] or "note"


def make_note_id(source: str, title: str, when: datetime | None = None) -> str:
    """Deterministic id from sha256(source + title), shaped like YYYYMMDD-hash-slug."""
    digest = sha256(f"{source}\n{title}".encode("utf-8")).hexdigest()
    stamp = (when or datetime.now()).strftime("%Y%m%d")
    return f"{stamp}-{digest[:4]}-{slugify(title)}"


def parse_tags(value: str) -> tuple[str, ...]:
    """Parse ``[a, b]`` or ``a, b`` into a tuple of tags."""
    raw = value.strip()
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1]
    parts = [part.strip().strip("'\"") for part in raw.split(",")]
    return tuple(tag for tag in parts if tag)


def parse_frontmatter(raw: str) -> tuple[dict[str, str], str]:
    """Split a markdown file into a key/value map and the body."""
    match = FRONTMATTER_RE.match(raw)
    if not match:
        return {}, raw
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields, match.group(2)


def render_note(note: Note) -> str:
    """Serialize a note to markdown with frontmatter."""
    tags = ", ".join(note.tags)
    return (
        "---\n"
        f"id: {note.id}\n"
        f"source: {note.source}\n"
        f"title: {note.title}\n"
        f"date: {note.date}\n"
        f"tags: [{tags}]\n"
        "---\n"
        f"{note.text.rstrip()}\n"
    )


class MemoryStore:
    """Create, read, and list markdown notes under ``root``."""

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def add_note(
        self,
        title: str,
        source: str,
        text: str,
        tags: Iterable[str] | None = None,
        when: datetime | None = None,
    ) -> Note:
        """Write a note. Same (source, title) overwrites the same id."""
        when = when or datetime.now()
        note_id = make_note_id(source, title, when)
        cleaned = tuple(
            sorted({tag.strip().lower() for tag in (tags or ()) if tag.strip()})
        )
        note = Note(
            id=note_id,
            source=source,
            title=title.strip(),
            date=when.strftime("%Y-%m-%dT%H:%M:%S"),
            tags=cleaned,
            text=text.strip(),
            path=self.root / f"{note_id}.md",
        )
        assert note.path is not None
        note.path.write_text(render_note(note), encoding="utf-8")
        return note

    def parse_note(self, path: Path | str) -> Note:
        """Load one markdown file into a ``Note``."""
        path = Path(path)
        fields, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        tags = parse_tags(fields.get("tags", ""))
        return Note(
            id=fields.get("id") or path.stem,
            source=fields.get("source", str(path)),
            title=fields.get("title", path.stem),
            date=fields.get("date", ""),
            tags=tags,
            text=body.strip(),
            path=path,
        )

    def all_notes(self) -> list[Note]:
        """Return every ``*.md`` note, sorted by id."""
        notes = [self.parse_note(path) for path in self.root.glob("*.md")]
        notes.sort(key=lambda note: note.id)
        return notes

    def get(self, note_id: str) -> Note | None:
        """Fetch a note by id, or ``None`` if it is missing."""
        direct = self.root / f"{note_id}.md"
        if direct.is_file():
            return self.parse_note(direct)
        for note in self.all_notes():
            if note.id == note_id:
                return note
        return None
