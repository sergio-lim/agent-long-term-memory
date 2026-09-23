# memory

18 notes linked as **tag** `memory`.

## Notes

- **[BM25 is enough for a few thousand notes](../notes/20260921-0900-bm25-for-offline-retrieval.md)** — source: `seed/retrieval-notes.md` · `20260921-0900-bm25-for-offline-retrieval`
  - tags: `memory`, `retrieval`
  - _[[BM25]] ranks a note by how rare a query term is in the corpus and how often it appears in that note, with a length penalty. No embeddings, no API key, no ANN index. For a persona…_

- **[Compiled wiki and backlinks](../notes/20260922-1611-compiled-wiki-and-backlinks.md)** — source: `seed/wiki-notes.md` · `20260922-1611-compiled-wiki-and-backlinks`
  - tags: `wiki`, `memory`
  - _A folder of notes is a haystack. A compiled [[Wiki]] is a map: one page per tag and per wikilink entity, each listing the notes that mention it and the source those notes came from…_

- **[Decision records are memory](../notes/20260922-0830-decision-records-as-notes.md)** — source: `seed/adr-guide.md` · `20260922-0830-decision-records-as-notes`
  - tags: `decisions`, `memory`, `provenance`
  - _An architecture decision record is already a memory format: context, choice, consequences, date. Agents forget why they picked BM25 over embeddings unless that choice is a note.  W…_

- **[Episodic notes](../notes/20260923-3756-episodic-notes.md)** — source: `sources/memory-layers.md` · `20260923-3756-episodic-notes`
  - tags: `memory`, `tools`
  - _Write them after a session: who said what, which tool ran, what failed. Timestamp them. They go stale on purpose._

- **[Evaluation harness](../notes/20260923-bf83-evaluation-harness.md)** — source: `sources/eval-harness.md` · `20260923-bf83-evaluation-harness`
  - tags: `agents`, `memory`, `provenance`, `retrieval`, `testing`
  - _Test memory like you test a search box. A golden query list is ten lines long and worth more than a dashboard.  Include at least one query about how agents remember things, one abo…_

- **[Forgetting is a feature](../notes/20260923-1044-forgetting-is-a-feature.md)** — source: `seed/forgetting.md` · `20260923-1044-forgetting-is-a-feature`
  - tags: `agents`, `memory`
  - _Infinite memory is a junk drawer. Agents remember better when old, unused notes stop crowding BM25. Forgetting can be a tag (`stale`), a date cutoff, or a human deleting a file.  D…_

- **[Heartbeat memory maintenance](../notes/20260923-1302-heartbeat-memory-maintenance.md)** — source: `seed/ops-notes.md` · `20260923-1302-heartbeat-memory-maintenance`
  - tags: `agents`, `memory`, `tools`
  - _A heartbeat is a cheap periodic pass: compile the wiki, drop notes that lost their source file, and surface contradictions. It is a [[Tools]] job, not a chat.  Maintenance should b…_

- **[How agents remember things](../notes/20260920-1015-how-agents-remember-things.md)** — source: `seed/agent-handbook.md` · `20260920-1015-how-agents-remember-things`
  - tags: `agents`, `memory`
  - _An agent that only has the current context window wakes up with amnesia every turn. [[Agent Memory]] is the difference between a clever autocomplete and a colleague who was there l…_

- **[Idempotent actions](../notes/20260923-7eab-idempotent-actions.md)** — source: `sources/tool-use.md` · `20260923-7eab-idempotent-actions`
  - tags: `memory`, `tools`
  - _If a tool is safe to replay, store the command as the source. If it is not (send email, charge a card), store a receipt and refuse to invent a second one from memory._

- **[Memory layers](../notes/20260923-8b27-memory-layers.md)** — source: `sources/memory-layers.md` · `20260923-8b27-memory-layers`
  - tags: `agents`, `memory`, `retrieval`
  - _Treat memory as layers, not as one pile. Episodic notes capture "what happened". Semantic notes capture "what is true". Procedural notes capture "how we do this".  An agent that mi…_

- **[Provenance beats a vibes memory](../notes/20260920-1430-provenance-beats-a-vibes-memory.md)** — source: `seed/provenance-essay.md` · `20260920-1430-provenance-beats-a-vibes-memory`
  - tags: `memory`, `provenance`
  - _A vector blob that says "the user likes short answers" is a rumor. [[Provenance]] is the habit of keeping the path back to the file, the message, or the page that justified the not…_

- **[Query hygiene](../notes/20260923-6dd8-query-hygiene.md)** — source: `sources/retrieval-notes.md` · `20260923-6dd8-query-hygiene`
  - tags: `agents`, `memory`, `retrieval`, `testing`
  - _Lowercase, drop stopwords, keep codes and versions (`k1`, `bm25`, `gpt`). Repeat the title in the searchable field so a note named "How agents remember things" wins the obvious que…_

- **[Semantic notes](../notes/20260923-0d5b-semantic-notes.md)** — source: `sources/memory-layers.md` · `20260923-0d5b-semantic-notes`
  - tags: `memory`, `provenance`
  - _Facts that should still be true next month: stack choices, names of systems, constraints. These are the notes [[Provenance]] has to protect, because a wrong semantic note poisons e…_

- **[Session memory versus long-term notes](../notes/20260921-1112-session-vs-long-term.md)** — source: `seed/memory-essay.md` · `20260921-1112-session-vs-long-term`
  - tags: `agents`, `memory`
  - _Session memory is the chat transcript: cheap, ordered, and gone when the session ends. Long-term notes survive restarts. Agents remember things across days only if someone copies t…_

- **[The agent loop](../notes/20260923-7acb-the-agent-loop.md)** — source: `sources/agent-loop.md` · `20260923-7acb-the-agent-loop`
  - tags: `agents`, `memory`, `retrieval`, `tools`
  - _An agent is a loop: observe, retrieve, think, act, write. The retrieve and write steps are what turn a stateless model into something that can remember.  Without a write step, ever…_

- **[Tool results belong in memory](../notes/20260921-1540-tool-results-belong-in-memory.md)** — source: `seed/tools-playbook.md` · `20260921-1540-tool-results-belong-in-memory`
  - tags: `agents`, `tools`, `memory`
  - _[[Tools]] return facts the model did not know: a test log, a file hash, a calendar slot. If those facts live only in the tool message, the next session cannot see them.  Ingest the…_

- **[Tool use and memory](../notes/20260923-d1fc-tool-use-and-memory.md)** — source: `sources/tool-use.md` · `20260923-d1fc-tool-use-and-memory`
  - tags: `agents`, `memory`, `tools`, `wiki`
  - _[[Tools]] are the agent's hands. Memory is the agent's notebook. Hands without a notebook repeat the same work. A notebook without hands is a wiki nobody updates.  Log the tool nam…_

- **[Working memory is not long-term memory](../notes/20260923-c348-working-memory-is-not-long-term-memory.md)** — source: `sources/agent-loop.md` · `20260923-c348-working-memory-is-not-long-term-memory`
  - tags: `agents`, `memory`, `prompts`, `tools`
  - _Working memory is the prompt. It is fast and expensive. Long-term memory is files. It is slow and cheap. Keep the last actions in working memory and spill facts that must survive a…_

## Backlinks

Every line above is a backlink: the wiki page does not own the fact,
the **source** on the note does.
