# tools

7 notes linked as **tag** `tools`.

## Notes

- **[Episodic notes](../notes/20260923-3756-episodic-notes.md)** — source: `sources/memory-layers.md` · `20260923-3756-episodic-notes`
  - tags: `memory`, `tools`
  - _Write them after a session: who said what, which tool ran, what failed. Timestamp them. They go stale on purpose._

- **[Heartbeat memory maintenance](../notes/20260923-1302-heartbeat-memory-maintenance.md)** — source: `seed/ops-notes.md` · `20260923-1302-heartbeat-memory-maintenance`
  - tags: `agents`, `memory`, `tools`
  - _A heartbeat is a cheap periodic pass: compile the wiki, drop notes that lost their source file, and surface contradictions. It is a [[Tools]] job, not a chat.  Maintenance should b…_

- **[Idempotent actions](../notes/20260923-7eab-idempotent-actions.md)** — source: `sources/tool-use.md` · `20260923-7eab-idempotent-actions`
  - tags: `memory`, `tools`
  - _If a tool is safe to replay, store the command as the source. If it is not (send email, charge a card), store a receipt and refuse to invent a second one from memory._

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
