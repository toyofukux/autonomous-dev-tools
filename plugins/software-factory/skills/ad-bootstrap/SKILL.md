---
name: ad-bootstrap
description: Reverse-engineer an existing project into specs/ scaffolding by delegating to the bootstrap-explorer subagent, presenting its proposal for approval, and writing the approved files. Use when the project already has code but no specs/ yet.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# /ad-bootstrap

Adopt the software-factory plugin on a project that already has code.

## When to use

Run once, on an existing project, to seed `specs/` from what already exists. If `specs/` is already populated, refuse and ask the user to delete or merge manually.

## What you do

1. **Check preconditions**: if `specs/` exists and is non-trivial, stop and ask whether to merge or abort.
2. **Delegate to `bootstrap-explorer`** subagent with the project's root as context. Ask it for the bootstrap proposal: units, draft concept.md, draft arch.md, optionally extracted stories, and risks.
3. **Present the proposal to the user** in a compact form:
   - Proposed units (with confidence)
   - concept.md / arch.md drafts (show full text)
   - Risks of adoption
   - Suggested next steps
4. **Ask the user** to:
   - Confirm or rename units
   - Edit concept/arch drafts (or accept as-is)
   - Choose whether to extract initial stories now or skip
5. **Write the approved files** to the user's project:
   - `specs/SPEC.md` (from template, with the confirmed unit list filled in)
   - `specs/concept.md` (user-approved draft)
   - `specs/arch.md` (user-approved draft)
   - `specs/units/<name>/stories.md` for each confirmed unit (empty, with template header)
   - `specs/units/<name>/decision-record.md` for each unit (empty)
   - `specs/iterations/` with `.gitkeep`
6. **Create CLAUDE.md** only if missing (same as [[ad-init]]).
7. **Summarize** what was created and recommend the next step (`/ad-story` to add a first new story, or pick an existing extracted story to drive `/ad-spec`).

## Discipline

- **Never overwrite** without explicit confirmation per file.
- **Honor the explorer's confidence ratings**: if a unit was low-confidence, surface that to the user with the evidence and ask before writing.
- **Do not refactor the codebase** to fit the proposed units. Bootstrap is descriptive, not prescriptive.
- **Cross-cutting units use `_` prefix**: `_notification`, `_audit`, etc.

## Edge cases

- **No tests found** → skip the "extract initial stories" step entirely; tell the user `/ad-story` is the next move.
- **CLAUDE.md already comprehensive** → don't touch it; instead show what the template would have added so the user can merge.
- **Monorepo** → bootstrap-explorer should propose units per package; if the proposal is dense, ask the user to scope to one package per `/ad-bootstrap` run.
