# The agent loop

An agent is a loop: observe, retrieve, think, act, write. The retrieve and write steps are what turn a stateless model into something that can remember.

Without a write step, every tool result dies at the end of the turn. Without retrieve, the write step is a diary nobody reads.

## Working memory is not long-term memory

Working memory is the prompt. It is fast and expensive. Long-term memory is files. It is slow and cheap. Keep the last actions in working memory and spill facts that must survive a restart.

If you stuff the whole diary into the prompt you will hit the window and lose the beginning. That is amnesia with extra tokens.
