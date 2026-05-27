# Authoring a new subagent

Subagents are the workers. Each has one job, its own context window, and a strict tool allowlist.

## File layout

```text
plugins/autonomous-dev-loop/agents/<noun>.md
```

The filename's basename is the agent name (must match the `name` frontmatter field).

## Required frontmatter

```yaml
---
name: <noun>
description: One sentence — when should Claude delegate to this agent?
---
```

`description` is what Claude reads when deciding whether to delegate. It must clearly distinguish this agent from siblings. "Use to ..." is a good opener.

## Optional frontmatter

```yaml
tools: Read, Grep, Glob              # allowlist (recommended: explicit)
model: inherit                        # or sonnet, opus, haiku
color: blue                           # UI hint
memory: project                       # persistent agent memory directory
isolation: worktree                   # auto-create a git worktree
permissionMode: acceptEdits           # auto-accept file edits in scope
```

For most plugin subagents, use `model: inherit` (uses parent's model). Set explicit models only when the work genuinely needs more or less capability.

## Body conventions (system prompt)

This is the **system prompt** the subagent runs under. Write it carefully.

Sections in this order:

1. **One-line purpose.**
2. **What you receive** — inputs.
3. **What you produce** — outputs (with format).
4. **Rules you do not break** — non-negotiables.
5. **What you do NOT do** — explicit non-goals.
6. **Tools you may use** — the line about allowlist.

## The seven-agent invariant

This plugin commits to **8 subagents** (the 7 from the article + `bootstrap-explorer`). Adding a 9th means consolidating two existing ones, or you're drifting.

Before adding a new subagent, justify:
- Why an existing agent can't take this work.
- Why a skill (which can orchestrate multiple existing agents) doesn't suffice.
- What the new agent's strict scope is.

## Discipline

- Tool allowlist matches what the agent's body says it can do. Inconsistency causes confusing failures.
- Read-only critique agents (researcher, validator) have **no** Edit/Write/Bash.
- Builder agents have Edit/Write/Bash; their scope is enforced by prompt + the validator's scope-drift check.
- Description should distinguish from every other agent's description. Test by reading all 8 descriptions and asking "would Claude pick the right one?".

## Don't write a subagent that

- Has overlapping responsibilities with another (refactor instead).
- Has unbounded scope ("does general implementation").
- Can modify files outside its strict boundary (validator/researcher in particular).
- Reads its own outputs in a loop (the orchestrator handles routing).
