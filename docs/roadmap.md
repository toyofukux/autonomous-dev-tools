# Roadmap

Future plugins and capabilities — not yet built, ordered by likely usefulness.

## Future plugins (in this marketplace)

### `external-research`
A second researcher that complements `codebase-researcher` — fetches relevant docs, library references, recent best practices, blog posts. Triggered from `/sf-spec` when the change involves an unfamiliar API or pattern. Uses Context7 MCP and WebFetch.

### `payments-integration`
A domain-specialist plugin: a `payments-builder` subagent + skills + guidelines for safe integration with Stripe / PayPal / etc. Encodes idempotency, webhook signature verification, PCI scope reduction, reconciliation patterns. Useful when the team's payments specialist isn't always available.

### `migrations-curator`
A subagent specialized in safe database migration design — checks lock impact, proposes online-DDL alternatives, designs two-phase rollouts. Plugs into `/sf-spec` and `/sf-validate`.

### `incident-response`
On-call helper. `/ir-start <incident-id>` opens a structured incident timeline, suggests next investigations, surfaces relevant runbooks. Pairs with the observability guideline.

### `release-orchestrator`
Drives multi-step release deploys (feature flag ramps, canary, dark launches). Reads the iteration spec's "Release steps" section and progresses through them with health checks.

## Future capabilities (in `software-factory`)

### `/sf-guideline import <url>`
Pull a guideline from a community repo. Validates the file structure; copies into `specs/guidelines/`.

### `/sf-loop --parallel` actually parallel
Today's `--parallel` flag is implemented as serial-with-conflict-check. Make it actually run two worktrees concurrently with background subagents and merge afterward. Requires careful conflict handling.

### `/sf-retro <since>`
Generate a retrospective from completed iteration specs (before they were deleted, captured from git history). Aggregates: most common validator findings → suggested CLAUDE.md additions; cycle times; stories that re-opened.

### `/sf-budget`
Per-feature cost tracking. Each iteration logs token usage and wall time; `/sf-budget` summarizes.

### LSP integration
For supported languages, run the language server inside subagent sessions so they get real-time type info instead of running `tsc --noEmit` at the end.

### Background monitors
A `monitors/` config that watches the dev server's error log and pings the main thread when an unexpected error surfaces during `/sf-dev`.

## Future docs / templates

- `templates/guidelines/i18n.md` — internationalization
- `templates/guidelines/accessibility.md` — split from `ui.md` as a deeper standalone
- `templates/guidelines/cost.md` — cloud cost discipline (matches the existing `cost-ops` motif)
- `docs/migrating-existing-project.md` — playbook for adopting the plugin on a > 10k LOC project

## Anti-roadmap (things we will NOT do)

- A `spec.md` maintainer skill (deliberate; see `lifecycle.md`).
- A 9th main-flow subagent without removing one.
- An "auto-merge PR" capability (the third human checkpoint is sacred).
- Tight coupling to a single editor (VS Code, JetBrains). This plugin runs in Claude Code; integrations live elsewhere.
