from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from memory.compile import compile_wiki, extract_entities
from memory.ingest import infer_tags, ingest_text, ingest_url, split_sections
from memory.retrieve import search, tokenize
from memory.store import MemoryStore, Note, make_note_id, parse_frontmatter, parse_tags, slugify


STAMP = datetime(2026, 3, 15, 12, 0, 0)


def test_slugify_and_deterministic_note_ids() -> None:
    assert slugify("Hello World!") == "hello-world"
    assert slugify("???") == "note"
    first = make_note_id("sources/loop.md", "How agents remember", STAMP)
    again = make_note_id("sources/loop.md", "How agents remember", STAMP)
    later = make_note_id("sources/loop.md", "How agents remember", datetime(2026, 4, 1))
    other = make_note_id("sources/other.md", "How agents remember", STAMP)
    assert first == again
    assert first.startswith("20260315-")
    assert first.split("-")[1] == later.split("-")[1]
    assert first != other


def test_parse_frontmatter_and_tags() -> None:
    fields, body = parse_frontmatter(
        "---\nid: abc\ntags: [memory, agents]\n---\nBody text\n"
    )
    assert fields["id"] == "abc"
    assert parse_tags(fields["tags"]) == ("memory", "agents")
    assert body.strip() == "Body text"
    assert parse_frontmatter("plain note") == ({}, "plain note")
    assert parse_tags("alpha, beta") == ("alpha", "beta")
    assert parse_tags("") == ()


def test_store_add_get_overwrite_and_missing(tmp_path: Path) -> None:
    store = MemoryStore(tmp_path)
    note = store.add_note(
        title="Working memory is short",
        source="sources/memory-layers.md",
        text="Long-term memory needs files.",
        tags=["Memory", " memory ", "Agents"],
        when=STAMP,
    )
    loaded = store.get(note.id)
    assert loaded is not None
    assert loaded.title == "Working memory is short"
    assert loaded.tags == ("agents", "memory")
    assert loaded.source == "sources/memory-layers.md"
    again = store.add_note(
        title="Working memory is short",
        source="sources/memory-layers.md",
        text="Updated body.",
        tags=["memory"],
        when=STAMP,
    )
    assert again.id == note.id
    assert store.get(note.id) is not None
    assert store.get(note.id).text == "Updated body."  # type: ignore[union-attr]
    assert store.get("missing-id") is None
    assert len(store.all_notes()) == 1


def test_tokenize_drops_stopwords_and_single_chars() -> None:
    tokens = tokenize("The agent remembers a plan on a map")
    assert "the" not in tokens
    assert "a" not in tokens
    assert "agent" in tokens
    assert "remembers" in tokens


def test_search_ranks_lexical_overlap_and_handles_empty() -> None:
    corpus = [
        Note(
            id="20260315-aaaa-bm25",
            source="sources/retrieval-notes.md",
            title="BM25 retrieval first",
            date="2026-03-15T12:00:00",
            tags=("retrieval",),
            text="Lexical ranking over notes with provenance.",
        ),
        Note(
            id="20260315-bbbb-tools",
            source="sources/tool-use.md",
            title="Tool results belong in memory",
            date="2026-03-15T12:00:00",
            tags=("tools",),
            text="Idempotent actions and tool logs.",
        ),
    ]
    hits = search(corpus, "how does bm25 retrieval rank notes", top_k=2)
    assert hits
    assert hits[0].note_id == "20260315-aaaa-bm25"
    assert hits[0].source == "sources/retrieval-notes.md"
    assert hits[0].score > 0
    assert search(corpus, "the and or", top_k=5) == []
    assert search([], "memory", top_k=5) == []


def test_split_sections_and_infer_tags() -> None:
    sections = split_sections(
        "Preamble stays unnamed.\n\n# First heading\nAlpha body.\n\n## Second\nBeta body.\n"
    )
    assert sections[0] == ("", "Preamble stays unnamed.")
    assert sections[1][0] == "First heading"
    assert "Alpha" in sections[1][1]
    assert infer_tags("random fluff about weather") == ["inbox"]
    assert "retrieval" in infer_tags("Why BM25 beats vibes")


def test_ingest_text_one_note_per_heading(tmp_path: Path) -> None:
    store = MemoryStore(tmp_path)
    notes = ingest_text(
        store,
        "# Provenance beats vibes\nCite the source.\n\n# Query hygiene\nDrop stopwords.\n",
        source="sources/memory-layers.md",
        when=STAMP,
    )
    assert [note.title for note in notes] == ["Provenance beats vibes", "Query hygiene"]
    assert all(note.source == "sources/memory-layers.md" for note in notes)


def test_ingest_url_rejects_remote_and_accepts_file(tmp_path: Path) -> None:
    store = MemoryStore(tmp_path)
    with pytest.raises(ValueError, match="offline"):
        ingest_url(store, "https://example.invalid/notes.md")
    with pytest.raises(ValueError, match="unsupported URL scheme"):
        ingest_url(store, "ftp://example.invalid/notes.md")

    source = tmp_path / "seed.md"
    source.write_text("# Local seed\nA file:// ingest stays offline.\n", encoding="utf-8")
    notes = ingest_url(store, source.as_uri(), root=tmp_path)
    assert len(notes) == 1
    assert notes[0].title == "Local seed"


def test_compile_wiki_writes_tag_entity_and_index(tmp_path: Path) -> None:
    store = MemoryStore(tmp_path / "notes")
    store.add_note(
        title="Agents remember files",
        source="sources/agent-loop.md",
        text="See [[Agent Memory]] and keep provenance.",
        tags=["memory", "agents"],
        when=STAMP,
    )
    wiki = tmp_path / "wiki"
    written = compile_wiki(store.all_notes(), wiki)
    names = {path.name for path in written}
    assert "index.md" in names
    assert "memory.md" in names
    assert "agents.md" in names
    assert "ent-agent-memory.md" in names
    index = (wiki / "index.md").read_text(encoding="utf-8")
    assert "notes: **1**" in index
    assert extract_entities("See [[Agent Memory]] and [[Wiki]]") == ["Agent Memory", "Wiki"]
