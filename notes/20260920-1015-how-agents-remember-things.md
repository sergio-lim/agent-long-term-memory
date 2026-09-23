---
id: 20260920-1015-how-agents-remember-things
source: seed/agent-handbook.md
title: How agents remember things
date: 2026-09-20T10:15:00
tags: [agents, memory]
---
An agent that only has the current context window wakes up with amnesia every turn. [[Agent Memory]] is the difference between a clever autocomplete and a colleague who was there last week.

How do agents remember things in practice? They write durable notes outside the prompt: decisions, tool results, and facts, each stamped with a source. At query time they retrieve a handful of those notes instead of hoping the model still has the conversation in its head.

Long-term memory is not a bigger window. It is a store the agent can read after the process restarts.
