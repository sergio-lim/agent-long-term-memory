"""Offline BM25 retrieval over notes. Pure Python, no embeddings, no keys."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
import math
import re

from memory.store import Note

# k1 saturates term frequency; b down-weights long documents.
K1 = 1.5
B = 0.75

TOKEN_RE = re.compile(r"[a-z0-9]+")

STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "but",
        "by",
        "do",
        "for",
        "from",
        "had",
        "has",
        "have",
        "if",
        "in",
        "into",
        "is",
        "it",
        "its",
        "no",
        "not",
        "of",
        "on",
        "or",
        "our",
        "so",
        "than",
        "that",
        "the",
        "their",
        "then",
        "there",
        "these",
        "they",
        "this",
        "to",
        "was",
        "we",
        "were",
        "what",
        "when",
        "which",
        "who",
        "will",
        "with",
        "you",
        "your",
    }
)


@dataclass(frozen=True)
class SearchHit:
    """One ranked note. ``source`` is the provenance path, not the note file."""

    score: float
    title: str
    source: str
    note_id: str
    tags: tuple[str, ...]
    note: Note


@dataclass
class BM25Index:
    """In-memory BM25 index over a snapshot of notes."""

    notes: list[Note]
    avgdl: float
    df: dict[str, int]
    tf: list[Counter[str]]
    lengths: list[int]
    k1: float = K1
    b: float = B
    _idf: dict[str, float] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        n_docs = len(self.notes)
        for term, freq in self.df.items():
            # Lucene-style IDF: always positive, stable for tiny corpora.
            self._idf[term] = math.log(1.0 + (n_docs - freq + 0.5) / (freq + 0.5))

    def search(self, query: str, top_k: int = 5) -> list[SearchHit]:
        """Score every note and return the top hits."""
        q_terms = tokenize(query)
        if not q_terms or not self.notes:
            return []
        scores = [0.0] * len(self.notes)
        avgdl = self.avgdl or 1.0
        for term in q_terms:
            idf = self._idf.get(term)
            if idf is None:
                continue
            for index, counts in enumerate(self.tf):
                freq = counts.get(term)
                if not freq:
                    continue
                denom = freq + self.k1 * (1.0 - self.b + self.b * self.lengths[index] / avgdl)
                scores[index] += idf * (freq * (self.k1 + 1.0)) / denom
        ranked = sorted(
            ((score, index) for index, score in enumerate(scores) if score > 0.0),
            key=lambda item: item[0],
            reverse=True,
        )
        hits: list[SearchHit] = []
        for score, index in ranked[:top_k]:
            note = self.notes[index]
            hits.append(
                SearchHit(
                    score=score,
                    title=note.title,
                    source=note.source,
                    note_id=note.id,
                    tags=note.tags,
                    note=note,
                )
            )
        return hits


def tokenize(text: str) -> list[str]:
    """Lowercase tokens, stopwords and single characters dropped."""
    return [tok for tok in TOKEN_RE.findall(text.lower()) if tok not in STOPWORDS and len(tok) > 1]


def build_index(notes: list[Note], k1: float = K1, b: float = B) -> BM25Index:
    """Build a BM25 index over ``title + tags + text``."""
    tf: list[Counter[str]] = []
    lengths: list[int] = []
    df: dict[str, int] = defaultdict(int)
    for note in notes:
        tokens = tokenize(note.searchable())
        counts = Counter(tokens)
        tf.append(counts)
        lengths.append(len(tokens))
        for term in counts:
            df[term] += 1
    avgdl = (sum(lengths) / len(lengths)) if lengths else 0.0
    return BM25Index(
        notes=notes,
        avgdl=avgdl,
        df=dict(df),
        tf=tf,
        lengths=lengths,
        k1=k1,
        b=b,
    )


def search(notes: list[Note], query: str, top_k: int = 5) -> list[SearchHit]:
    """Convenience: index once, return top ``top_k`` hits."""
    return build_index(notes).search(query, top_k=top_k)
