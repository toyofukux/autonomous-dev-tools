# Changelog

## v0.1.0 — 2026-05-27

Initial release.

### software-factory plugin

- 8 subagents: `codebase-researcher`, `story-writer`, `spec-writer`, `backend-builder`, `frontend-builder`, `test-verifier`, `validator`, `bootstrap-explorer`
- 14 skills (all `/software-factory:ad-*`): `ad-init`, `ad-bootstrap`, `ad-research`, `ad-story`, `ad-spec`, `ad-dev`, `ad-verify`, `ad-validate`, `ad-fix`, `ad-pr`, `ad-loop`, `ad-summary`, `ad-guideline`, `ad-organize`
- 7 document templates: SPEC.md index, concept, arch, stories, decision-record, spec-iteration, CLAUDE.md
- 11 baseline guidelines: security, performance, testing, observability, api, db, ui, ux, interaction, code-style, git
- Pre-commit secrets-blocker hook (bundled, opt-in install)

### Tooling

- `scripts/new-plugin.sh` — scaffold a new plugin in this marketplace
- `scripts/rename-prefix.sh` — rename the `ad-*` prefix across a plugin
- `.github/workflows/validate.yml` — CI for marketplace + plugin validation
