# Artifact lifecycle

How docs flow through the software-factory, in chronological order.

## Slow-changing (created once, updated occasionally)

- `specs/concept.md` — created by `/sf-init`. Edited rarely, when the product's "why" shifts.
- `specs/arch.md` — created by `/sf-init` or `/sf-bootstrap`. Updated when module boundaries or stack change.
- `specs/guidelines/*.md` — added opt-in via `/sf-guideline <name>`. Edited as the team's standards evolve.
- `CLAUDE.md` (project root) — created by `/sf-init` (if absent). Updated continuously as Claude makes surprise mistakes; every surprise → a new rule. Validator surfaces suggestions.

## Per-unit (long-lived)

- `specs/units/<u>/stories.md` — append-only mostly; `Status:` flips inline.
  - When > 500 lines → `/sf-organize` splits into `story-NNN.md` files; `stories.md` becomes an index.
- `specs/units/<u>/decision-record.md` — append-only ADR log. New entries on top.
- `specs/units/<u>/observability.md` — optional; created when a spec's "Logs for self-improvement" earns persistence.

## Per-iteration (ephemeral)

This is the part that surprises people: **iteration specs are deleted on PR merge.**

| Phase | File | State |
|---|---|---|
| `/sf-spec` | `specs/iterations/spec-YYYYMMDD-slug.md` | created with `status: drafted` |
| user answers questions | same | `status: approved` |
| `/sf-dev` | + `specs/iterations/spec-YYYYMMDD-slug/backend-summary.md` | spec `status: developing` |
| `/sf-verify` | (acceptance test file added in project's test dir) | spec `status: verifying` |
| `/sf-validate` | + `specs/iterations/spec-YYYYMMDD-slug/validation-report.md` | spec `status: validating` or `failed` |
| `/sf-fix` | spec `attempts` incremented; possibly micro-edits to spec | re-route |
| `/sf-pr` | **everything in `specs/iterations/spec-YYYYMMDD-slug*/` is deleted** | story `Status: done`; ADR appended |

The decisions, observations, and changes that mattered are preserved in:
- The unit's `decision-record.md` (the why)
- The unit's `stories.md` updated `Status: done` (the what)
- The codebase + acceptance tests (the how)
- Git history (the when)

The iteration spec was a working document. After merge, keeping it is drift waiting to happen.

## Why no maintained `spec.md`

A `spec.md` that describes "what the system does today" has to be updated every PR. The work nobody wants to do. The doc drifts. The drift fools the next person.

Instead:
- Stable surface: `concept.md`, `arch.md`, `stories.md`, ADRs.
- Volatile surface: code + tests (always true by definition).
- On-demand digest: `/sf-summary <unit>` regenerates a current-state view from the above, never persisted.

This is the plugin's most important opinion. Don't introduce a `spec.md` "just for reference"; it will rot within weeks.

## What if I want to ship a stable spec document?

Wait until the project is past initial growth. Then make a deliberate decision: pin a snapshot for a release, and treat it as a one-off changelog-style artifact under `specs/releases/v1.md`. Don't try to keep it live.
