---
name: ad-guideline
description: Add a bundled guideline (security, performance, testing, observability, api, db, ui, ux, interaction, code-style, git) to the project's specs/guidelines/. Use `list` to see what's available; `import <url>` is reserved for future use.
allowed-tools: Read, Write, Bash, Grep, Glob
arguments: name
---

# /ad-guideline $name

Copy a bundled guideline into `specs/guidelines/$name.md`. Opt-in; nothing is pre-installed.

## Available guidelines

Run `/ad-guideline list` to see the current bundle. As of this release:

- `security` — auth, tenant isolation, secrets, input validation, OWASP highlights
- `performance` — complexity budgets, query plans, payload size, caching
- `testing` — unit/integration/acceptance split, fixtures, flake control
- `observability` — structured logs, traces, metrics, alerts
- `api` — REST conventions, versioning, error envelopes, idempotency
- `db` — schema design, indexing, migrations, transactions
- `ui` — composition, design tokens, accessibility
- `ux` — interaction states, error handling, empty/loading
- `interaction` — keyboard, touch, focus, motion
- `code-style` — naming, comments, error handling, file size
- `git` — commit hygiene, branch naming, PR description, hooks

## What you do

1. **Resolve $name** against the bundle. If `list`, print the table above and stop.
2. **Check target**: if `specs/guidelines/$name.md` already exists, ask before overwriting.
3. **Copy** `${CLAUDE_PLUGIN_ROOT}/templates/guidelines/$name.md` to `specs/guidelines/$name.md`.
4. **Optionally update** `specs/SPEC.md` to link to the new guideline under its "How we work" section (offer; don't force).
5. **Report** what was added and mention that subagents (spec-writer, builders, validator) will pick it up automatically from `specs/guidelines/` on subsequent runs.

## Discipline

- **Do not modify the bundled source** — copy only. If the user wants to customize, they edit the project copy.
- **Never auto-install all guidelines.** Each one is a deliberate adoption decision.
- **`import <url>` is reserved.** If the user passes a URL, tell them this feature is on the roadmap (`docs/roadmap.md`) and not yet implemented.

## Suggesting additions

[[ad-validate]] and [[ad-pr]] surface "Suggested guideline additions" when the validator finds repeated patterns. Encourage the user to invoke `/ad-guideline $name` based on those suggestions.
