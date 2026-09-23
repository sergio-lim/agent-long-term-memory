"""Ingest local sources into provenance-stamped notes."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
from urllib.parse import unquote, urlparse

from memory.store import MemoryStore, Note, slugify

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)

# Cheap keyword → tag map so ingested demo sources land in the wiki.
TAG_HINTS: tuple[tuple[str, str], ...] = (
    ("agent", "agents"),
    ("memory", "memory"),
    ("remember", "memory"),
    ("provenance", "provenance"),
    ("bm25", "retrieval"),
    ("retriev", "retrieval"),
    ("search", "retrieval"),
    ("tool", "tools"),
    ("action", "tools"),
    ("decision", "decisions"),
    ("adr", "decisions"),
    ("prompt", "prompts"),
    ("test", "testing"),
    ("eval", "testing"),
    ("wiki", "wiki"),
    ("backlink", "wiki"),
    ("ingest", "ingest"),
)


def split_sections(text: str) -> list[tuple[str, str]]:
    """Split markdown into ``(heading, body)`` pairs.

    Text before the first heading is returned with an empty title so the
    caller can name it from the source path.
    """
    matches = list(HEADING_RE.finditer(text))
    if not matches:
        body = text.strip()
        return [("", body)] if body else []

    sections: list[tuple[str, str]] = []
    preamble = text[: matches[0].start()].strip()
    if preamble:
        sections.append(("", preamble))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        title = match.group(2).strip()
        if title and body:
            sections.append((title, body))
    return sections


def infer_tags(*parts: str) -> list[str]:
    """Tag a section from its title, body, and source path."""
    blob = " ".join(parts).lower()
    tags = {name for needle, name in TAG_HINTS if needle in blob}
    return sorted(tags) or ["inbox"]


def _default_title(source: str) -> str:
    stem = Path(source).stem
    return stem.replace("-", " ").replace("_", " ").title() or "Untitled"


def _relative_source(path: Path, root: Path | None) -> str:
    if root is None:
        return str(path)
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def ingest_text(
    store: MemoryStore,
    text: str,
    source: str,
    title: str | None = None,
    tags: list[str] | None = None,
    when: datetime | None = None,
) -> list[Note]:
    """Turn raw text into one note per heading section."""
    fallback = title or _default_title(source)
    notes: list[Note] = []
    for heading, body in split_sections(text):
        section_title = heading or fallback
        hint = Path(source).stem
        section_tags = tags if tags is not None else infer_tags(section_title, body, hint)
        notes.append(
            store.add_note(
                title=section_title,
                source=source,
                text=body,
                tags=section_tags,
                when=when,
            )
        )
    return notes


def ingest_file(
    store: MemoryStore,
    path: Path | str,
    root: Path | None = None,
    when: datetime | None = None,
) -> list[Note]:
    """Read a local markdown file and ingest each heading as a note."""
    path = Path(path)
    source = _relative_source(path, root)
    stamp = when or datetime.fromtimestamp(path.stat().st_mtime)
    return ingest_text(
        store,
        path.read_text(encoding="utf-8"),
        source=source,
        title=_default_title(source),
        when=stamp,
    )


def ingest_url(store: MemoryStore, url: str, root: Path | None = None) -> list[Note]:
    """Ingest a local ``file://`` URL or filesystem path. Offline only."""
    parsed = urlparse(url)
    if parsed.scheme in {"http", "https"}:
        raise ValueError("ingest_url is offline: use a local path or file:// URL")
    if parsed.scheme == "file":
        path = unquote(parsed.path)
    elif parsed.scheme == "":
        path = url
    else:
        raise ValueError(f"unsupported URL scheme: {parsed.scheme}")
    return ingest_file(store, path, root=root)


def ingest_all(
    store: MemoryStore,
    sources_dir: Path | str,
    root: Path | None = None,
) -> list[Note]:
    """Ingest every ``*.md`` file in ``sources_dir``."""
    directory = Path(sources_dir)
    notes: list[Note] = []
    for path in sorted(directory.glob("*.md")):
        notes.extend(ingest_file(store, path, root=root))
    return notes


# Re-export for callers that want a stable slug helper next to ingest.
__all__ = [
    "infer_tags",
    "ingest_all",
    "ingest_file",
    "ingest_text",
    "ingest_url",
    "slugify",
    "split_sections",
]
