# Changelog

## Unreleased

- **breaking**: renamed plugin `autonomous-dev-loop` → `software-factory`
- **breaking**: renamed skill prefix `ad-*` → `sf-*` (e.g. `/sf-loop`, `/sf-spec`)
- ci: replaced broken `curl | sh` Claude-install step with `scripts/validate.py` (pure-Python static validator)
- fix: `scripts/rename-prefix.sh` now uses `perl` instead of BSD-incompatible `sed \b` (silent failure on macOS)

## v0.1.0 — 2026-05-27

Initial release (as `autonomous-dev-loop` with `ad-*` prefix; renamed pre-publish in Unreleased above).

### software-factory plugin

- 8 subagents: `codebase-researcher`, `story-writer`, `spec-writer`, `backend-builder`, `frontend-builder`, `test-verifier`, `validator`, `bootstrap-explorer`
- 14 skills (all `/software-factory:sf-*`): `sf-init`, `sf-bootstrap`, `sf-research`, `sf-story`, `sf-spec`, `sf-dev`, `sf-verify`, `sf-validate`, `sf-fix`, `sf-pr`, `sf-loop`, `sf-summary`, `sf-guideline`, `sf-organize`
- 7 document templates: SPEC.md index, concept, arch, stories, decision-record, spec-iteration, CLAUDE.md
- 11 baseline guidelines: security, performance, testing, observability, api, db, ui, ux, interaction, code-style, git
- Pre-commit secrets-blocker hook (bundled, opt-in install)

### Tooling

- `scripts/new-plugin.sh` — scaffold a new plugin in this marketplace
- `scripts/rename-prefix.sh` — rename the skill prefix across a plugin
- `.github/workflows/validate.yml` — CI for marketplace + plugin validation
