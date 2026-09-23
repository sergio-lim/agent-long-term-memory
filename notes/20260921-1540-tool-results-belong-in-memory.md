---
id: 20260921-1540-tool-results-belong-in-memory
source: seed/tools-playbook.md
title: Tool results belong in memory
date: 2026-09-21T15:40:00
tags: [agents, tools, memory]
---
[[Tools]] return facts the model did not know: a test log, a file hash, a calendar slot. If those facts live only in the tool message, the next session cannot see them.

Ingest the summary, not the raw dump. Store the command or path as `source` so a later agent can replay or distrust the result. Memory without the tool provenance is just another hallucination with extra steps.
