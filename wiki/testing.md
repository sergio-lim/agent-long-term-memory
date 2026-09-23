# testing

8 notes linked as **tag** `testing`.

## Notes

- **[Decision records for agents](../notes/20260923-affa-decision-records-for-agents.md)** — source: `sources/adr-style.md` · `20260923-affa-decision-records-for-agents`
  - tags: `agents`, `decisions`, `retrieval`, `testing`
  - _A decision note has four fields in the body: context, options, choice, consequences. The frontmatter already has date and source.  Agents love to re-litigate settled choices. Retri…_

- **[Evaluation harness](../notes/20260923-bf83-evaluation-harness.md)** — source: `sources/eval-harness.md` · `20260923-bf83-evaluation-harness`
  - tags: `agents`, `memory`, `provenance`, `retrieval`, `testing`
  - _Test memory like you test a search box. A golden query list is ten lines long and worth more than a dashboard.  Include at least one query about how agents remember things, one abo…_

- **[Evaluation prompts](../notes/20260923-9c92-evaluation-prompts.md)** — source: `sources/prompt-packs.md` · `20260923-9c92-evaluation-prompts`
  - tags: `prompts`, `testing`
  - _Keep the judge prompt next to the task prompt. Changing one without the other is how evals quietly lie. Tag both `prompts` and `testing`._

- **[Lexical retrieval first](../notes/20260923-f711-lexical-retrieval-first.md)** — source: `sources/retrieval-notes.md` · `20260923-f711-lexical-retrieval-first`
  - tags: `retrieval`, `testing`
  - _Start with [[BM25]] over markdown. You can print the score, you can explain a miss, and you can snapshot the index as "whatever files are in notes/".  A miss that you can explain i…_

- **[Query hygiene](../notes/20260923-6dd8-query-hygiene.md)** — source: `sources/retrieval-notes.md` · `20260923-6dd8-query-hygiene`
  - tags: `agents`, `memory`, `retrieval`, `testing`
  - _Lowercase, drop stopwords, keep codes and versions (`k1`, `bm25`, `gpt`). Repeat the title in the searchable field so a note named "How agents remember things" wins the obvious que…_

- **[Regression on ingest](../notes/20260923-222a-regression-on-ingest.md)** — source: `sources/eval-harness.md` · `20260923-222a-regression-on-ingest`
  - tags: `ingest`, `testing`
  - _After `--ingest-all` the corpus grows. Re-run the golden queries. New notes may outrank old ones; that is not always a bug, but a rank flip should be visible in CI or a heartbeat._

- **[Testing retrieval quality](../notes/20260922-1405-testing-retrieval-quality.md)** — source: `seed/eval-notes.md` · `20260922-1405-testing-retrieval-quality`
  - tags: `testing`, `retrieval`
  - _Retrieval is a product. Test it with canned queries: "how do agents remember things" should rank the durable-memory notes above a random prompt snippet.  Keep a tiny golden set: qu…_

- **[When embeddings help](../notes/20260923-b1ee-when-embeddings-help.md)** — source: `sources/retrieval-notes.md` · `20260923-b1ee-when-embeddings-help`
  - tags: `retrieval`, `testing`
  - _Use vectors when the user never shares tokens with the note. Until the corpus is large enough that lexical search collapses, do not add a model just to look modern._

## Backlinks

Every line above is a backlink: the wiki page does not own the fact,
the **source** on the note does.
