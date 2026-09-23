#!/usr/bin/env python3
"""CLI for a long-term memory store with provenance.

    python3 brain.py --demo
    python3 brain.py --ingest-all
    python3 brain.py --query "how do agents remember things"
    python3 brain.py --compile
    python3 brain.py --stats
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from memory.compile import compile_wiki
from memory.ingest import ingest_all
from memory.retrieve import search
from memory.store import MemoryStore

ROOT = Path(__file__).resolve().parent
NOTES_DIR = ROOT / "notes"
SOURCES_DIR = ROOT / "sources"
WIKI_DIR = ROOT / "wiki"


def _store() -> MemoryStore:
    return MemoryStore(NOTES_DIR)


def cmd_stats(store: MemoryStore) -> int:
    notes = store.all_notes()
    tags = {tag for note in notes for tag in note.tags}
    sources = {note.source for note in notes}
    print("agent-long-term-memory")
    print("======================")
    print(f"notes    {len(notes)}")
    print(f"tags     {len(tags)}")
    print(f"sources  {len(sources)}")
    if tags:
        print("tag set:", ", ".join(sorted(tags)))
    return 0


def cmd_query(store: MemoryStore, query: str, top_k: int = 5) -> int:
    notes = store.all_notes()
    hits = search(notes, query, top_k=top_k)
    print(f'query: "{query}"')
    print(f"corpus: {len(notes)} notes")
    print()
    if not hits:
        print("no hits")
        return 0
    for index, hit in enumerate(hits, start=1):
        print(f"{index}. {hit.score:6.3f}  {hit.title}")
        print(f"      source: {hit.source}")
        if hit.tags:
            print(f"      tags:   {', '.join(hit.tags)}")
    return 0


def cmd_ingest_all(store: MemoryStore) -> int:
    created = ingest_all(store, SOURCES_DIR, root=ROOT)
    print(f"ingested {len(created)} notes from {SOURCES_DIR.relative_to(ROOT)}/")
    for note in created:
        print(f"  + {note.id}  ← {note.source}")
    return 0


def cmd_compile(store: MemoryStore) -> int:
    paths = compile_wiki(store.all_notes(), WIKI_DIR)
    print(f"compiled {len(paths)} wiki pages → {WIKI_DIR.relative_to(ROOT)}/")
    for path in sorted(paths, key=lambda item: item.name):
        print(f"  - {path.name}")
    return 0


def cmd_demo(store: MemoryStore) -> int:
    notes = store.all_notes()
    tags = {tag for note in notes for tag in note.tags}
    sources = {note.source for note in notes}
    query = "how do agents remember things"
    hits = search(notes, query, top_k=5)
    pages = compile_wiki(notes, WIKI_DIR)

    width = 58
    bar = "─" * width
    print(f"┌{bar}┐")
    print(f"│{'agent-long-term-memory':^{width}}│")
    print(f"│{'offline · no keys · provenance-first':^{width}}│")
    print(f"└{bar}┘")
    print()
    print(f"  notes    {len(notes)}")
    print(f"  tags     {len(tags)}")
    print(f"  sources  {len(sources)}")
    print()
    print(f'  query: "{query}"')
    print()
    for index, hit in enumerate(hits, start=1):
        print(f"  {index}. {hit.score:6.3f}  {hit.title}")
        print(f"        ← {hit.source}")
    print()
    print(f"  compiled wiki/  ({len(pages)} pages)")
    print("  sources → ingest → notes(frontmatter) → BM25 / wiki")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="brain.py",
        description="Long-term memory with provenance. No API keys, no pip.",
    )
    parser.add_argument(
        "--ingest-all",
        action="store_true",
        help="ingest every markdown file in sources/ into notes/",
    )
    parser.add_argument(
        "--query",
        metavar="TEXT",
        help="BM25 search over title + tags + text (top 5)",
    )
    parser.add_argument(
        "--compile",
        action="store_true",
        dest="do_compile",
        help="write wiki/<tag>.md pages and wiki/index.md",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="print note / tag / source counts",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="run stats + query + compile and print a short tour",
    )
    args = parser.parse_args(argv)
    if not any((args.ingest_all, args.query, args.do_compile, args.stats, args.demo)):
        parser.print_help()
        return 0

    store = _store()
    status = 0
    if args.ingest_all:
        status = cmd_ingest_all(store) or status
    if args.stats:
        status = cmd_stats(store) or status
    if args.query:
        status = cmd_query(store, args.query) or status
    if args.do_compile:
        status = cmd_compile(store) or status
    if args.demo:
        status = cmd_demo(store) or status
    return status


if __name__ == "__main__":
    sys.exit(main())
