# Tool use and memory

[[Tools]] are the agent's hands. Memory is the agent's notebook. Hands without a notebook repeat the same work. A notebook without hands is a wiki nobody updates.

Log the tool name, the argument, and a short result. Do not paste a 4k-line stack trace into a note.

## Idempotent actions

If a tool is safe to replay, store the command as the source. If it is not (send email, charge a card), store a receipt and refuse to invent a second one from memory.
