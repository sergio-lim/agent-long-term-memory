---
id: 20260922-1405-testing-retrieval-quality
source: seed/eval-notes.md
title: Testing retrieval quality
date: 2026-09-22T14:05:00
tags: [testing, retrieval]
---
Retrieval is a product. Test it with canned queries: "how do agents remember things" should rank the durable-memory notes above a random prompt snippet.

Keep a tiny golden set: query, expected note ids, and a minimum score gap. Because [[BM25]] is deterministic, the same corpus and query always produce the same ranking. That makes CI honest without mocking an embedding API.
