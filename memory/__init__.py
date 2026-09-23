"""Long-term memory with provenance: notes, ingest, BM25, compiled wiki."""

from __future__ import annotations

from memory.compile import compile_wiki
from memory.ingest import ingest_all, ingest_file, ingest_text, ingest_url
from memory.retrieve import SearchHit, build_index, search, tokenize
from memory.store import MemoryStore, Note

__all__ = [
    "MemoryStore",
    "Note",
    "SearchHit",
    "build_index",
    "compile_wiki",
    "ingest_all",
    "ingest_file",
    "ingest_text",
    "ingest_url",
    "search",
    "tokenize",
]
__version__ = "1.0.0"
