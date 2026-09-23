---
id: 20260923-222a-regression-on-ingest
source: sources/eval-harness.md
title: Regression on ingest
date: 2026-09-23T16:09:12
tags: [ingest, testing]
---
After `--ingest-all` the corpus grows. Re-run the golden queries. New notes may outrank old ones; that is not always a bug, but a rank flip should be visible in CI or a heartbeat.
