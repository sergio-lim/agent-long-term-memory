# Evaluation harness

Test memory like you test a search box. A golden query list is ten lines long and worth more than a dashboard.

Include at least one query about how agents remember things, one about provenance, and one that should miss (so you know the index is not always saying yes).

## Regression on ingest

After `--ingest-all` the corpus grows. Re-run the golden queries. New notes may outrank old ones; that is not always a bug, but a rank flip should be visible in CI or a heartbeat.
