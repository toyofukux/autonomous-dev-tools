---
name: ad-research
description: Run the codebase-researcher subagent standalone for an ad-hoc topic. Useful when planning a refactor or investigating an area before opening a story.
allowed-tools: Read
arguments: topic
---

# /ad-research $topic

Standalone codebase recon. Wraps the `codebase-researcher` subagent for one-off questions.

## When to use

- "I'm thinking about refactoring X — what does it touch?"
- "Is there already a thing that does Y?"
- "Where would I add Z?"

Not used inside [[ad-loop]] — `ad-loop` invokes the researcher directly. This is the manual entry.

## What you do

1. Delegate to `codebase-researcher` with $topic as the investigation target.
2. Present the researcher's standard output (relevant files, patterns, similar features, risks, test impact, recommendation) verbatim to the user.
3. Stop. Do not propose a story, spec, or implementation.

## Discipline

- One topic per invocation. If $topic spans multiple unrelated areas, ask the user to narrow.
- No follow-up agents auto-chain. The user can run `/ad-story` next if they want.
