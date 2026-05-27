---
name: ad-init
description: Initialize a new project's specs/ directory with the minimum viable structure for the autonomous-dev-loop. Creates concept.md, arch.md, SPEC.md index, iterations/ directory, and adds a CLAUDE.md if missing. Does NOT create units/ or guidelines/ — those are opt-in.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# /ad-init

Scaffold a fresh `specs/` directory for a brand-new project.

## When to use

Run once, at the very start of a project, before any feature work. If `specs/` already exists, refuse and suggest [[ad-bootstrap]] instead.

## What you do

1. **Check preconditions**:
   - If `specs/` exists, stop and tell the user to use `/ad-bootstrap`.
   - If the project has no `package.json` / `pyproject.toml` / equivalent, ask the user what stack to assume before filling templates.
2. **Gather minimal facts** from the user (one round of questions, tight):
   - Project name and one-line concept (will go into `concept.md`).
   - Primary user role (for the concept's "who it's for").
   - Stack basics — language, backend framework, frontend framework, DB, queue, hosting (for `arch.md` and `CLAUDE.md`).
   - Test commands (for `CLAUDE.md`).
3. **Copy templates** to the user's project, substituting placeholders from the gathered facts. Source templates live in `${CLAUDE_PLUGIN_ROOT}/templates/`. Targets:
   - `${CLAUDE_PLUGIN_ROOT}/templates/SPEC.md.tmpl` → `specs/SPEC.md`
   - `${CLAUDE_PLUGIN_ROOT}/templates/concept.md.tmpl` → `specs/concept.md`
   - `${CLAUDE_PLUGIN_ROOT}/templates/arch.md.tmpl` → `specs/arch.md`
   - `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md.tmpl` → `./CLAUDE.md` (only if not present)
4. **Create empty directories**: `specs/iterations/`. Add a `.gitkeep`.
5. **Do not create**: `specs/units/`, `specs/guidelines/`. These appear only when [[ad-organize]] or [[ad-guideline]] is run.
6. **Add the pre-commit secret hook suggestion** to the user's output, with the command they'd run to install it from `${CLAUDE_PLUGIN_ROOT}/hooks/pre-commit-secrets.json`. Do not install hooks automatically.
7. **Summarize**: print the file tree you created and the next recommended command (`/ad-loop "describe your first feature"` or `/ad-story` if they want stepwise).

## Discipline

- **Progressive disclosure**: do not create folders the user did not ask for. If the user mentions wanting guidelines, mention `/ad-guideline <name>` instead of pre-creating them.
- **Idempotency**: if any target file exists, stop and ask before overwriting.
- **No silent overwrites of CLAUDE.md**. If one exists, show a diff and ask the user to merge manually.

## Output structure

```text
specs/
├── SPEC.md
├── concept.md
├── arch.md
└── iterations/
    └── .gitkeep
CLAUDE.md  (created only if missing)
```
