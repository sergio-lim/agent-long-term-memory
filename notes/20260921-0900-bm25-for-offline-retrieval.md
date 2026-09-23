---
id: 20260921-0900-bm25-for-offline-retrieval
source: seed/retrieval-notes.md
title: BM25 is enough for a few thousand notes
date: 2026-09-21T09:00:00
tags: [memory, retrieval]
---
[[BM25]] ranks a note by how rare a query term is in the corpus and how often it appears in that note, with a length penalty. No embeddings, no API key, no ANN index. For a personal agent with hundreds or a few thousand markdown notes it is deterministic and good.

Embeddings help when the query and the note share no tokens ("how do agents remember things" vs "durable episodic store"). That is a roadmap item, not a day-one dependency. Start with lexical search you can explain.
