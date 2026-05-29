# Authoring a new skill

Skills are the user-facing entry points. They orchestrate subagents.

## File layout

```text
plugins/software-factory/skills/ad-<verb>/SKILL.md
```

For supporting files (scripts, references), add siblings under the same directory and reference them with `${CLAUDE_SKILL_DIR}`.

## Required frontmatter

```yaml
---
name: ad-<verb>
description: One sentence — when should Claude use this skill, and what does it do?
---
```

`description` is what Claude reads when deciding whether to auto-invoke. Be specific. Mention input/output and the trigger condition.

## Optional frontmatter

```yaml
allowed-tools: Read, Write, Bash, Grep, Glob
arguments: feature                # named positional argument; use $feature in body
paths: specs/**/*.md              # auto-activate only when working under these paths
disable-model-invocation: true    # only user-typeable; Claude won't auto-invoke
```

## Body conventions

1. **Open with a 1-sentence purpose line.**
2. **Sections in this order**: Preconditions → What you do (numbered) → Discipline → Edge cases / Failure modes.
3. **Reference other skills with `[[sf-other]]`** so renames stay traceable.
4. **Reference subagents by name** ("Delegate to `spec-writer`...").
5. **State the next-command recommendation** at the end so the user knows what's next.

## Discipline (what you must check before merging a new skill)

- The skill does one thing. If you describe its job with "and", split.
- Tool allowlist is the minimum the skill needs. Don't add `Bash` if it doesn't shell out.
- The skill is idempotent or asks before overwriting.
- The skill fails loudly. No silent no-ops.
- The skill respects the human-checkpoint model: don't chain past a checkpoint without explicit approval.
- The skill is testable: a tester can dry-run it on a sample project and see what changes.

## Don't write a skill that

- Replaces a checkpoint with auto-approval.
- Combines two subagents' jobs ("backend + frontend in one prompt") — that defeats the factory model.
- Writes to a `spec.md` file in `units/` — see `lifecycle.md`.
- Imports from `~/.claude` automatically.
