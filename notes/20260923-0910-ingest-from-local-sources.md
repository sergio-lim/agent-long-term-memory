---
id: 20260923-0910-ingest-from-local-sources
source: seed/ingest-guide.md
title: Ingest from local sources
date: 2026-09-23T09:10:00
tags: [ingest, provenance]
---
Ingest means: read a local markdown file, split it on headings, and write one note per section with the path and timestamp in frontmatter. No crawler, no remote fetch, no key.

`ingest_url` only accepts a filesystem path or a `file://` URL so the demo stays offline. If you want the open web in this store, download the page yourself and drop it in `sources/`.
