---
id: 20260922-0830-decision-records-as-notes
source: seed/adr-guide.md
title: Decision records are memory
date: 2026-09-22T08:30:00
tags: [decisions, memory, provenance]
---
An architecture decision record is already a memory format: context, choice, consequences, date. Agents forget why they picked BM25 over embeddings unless that choice is a note.

Write the decision as markdown. Tag it `decisions`. Link the rejected alternative in the body. When a future agent asks "why not embeddings?", retrieval should surface this record and its source, not a reconstructed vibe.
