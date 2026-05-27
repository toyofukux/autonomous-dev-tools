# Release

How to cut a new version of `autonomous-dev-loop` (or any future plugin in this marketplace).

## Versioning

Semantic: `MAJOR.MINOR.PATCH`.

- **PATCH** — bug fixes in templates, agent prompt clarifications, doc updates that don't change behavior.
- **MINOR** — new skills, new subagents (rare!), new guidelines, additive frontmatter fields, default-behavior changes that are still backward-compatible for existing users.
- **MAJOR** — renaming the `ad-*` prefix, removing skills, changing iteration spec frontmatter incompatibly, removing the human checkpoints.

## Steps

1. **Verify locally**:
   ```bash
   claude --plugin-dir ./plugins/autonomous-dev-loop
   /reload-plugins
   # smoke-test the changed skills
   ```
2. **Run validation**:
   ```bash
   claude plugin validate
   ```
3. **Bump the version** in **both**:
   - `plugins/autonomous-dev-loop/.claude-plugin/plugin.json`
   - `.claude-plugin/marketplace.json` (the plugin entry's `version` field)
   These must match. Mismatched versions break update notifications.
4. **Update the changelog**:
   ```bash
   # at the top of CHANGELOG.md (create if missing):
   ## v0.2.0 — YYYY-MM-DD
   - feat: ...
   - fix: ...
   - docs: ...
   ```
5. **Commit and tag**:
   ```bash
   git commit -m "release: autonomous-dev-loop v0.2.0"
   git tag autonomous-dev-loop-v0.2.0
   git push origin main --tags
   ```
6. **Users update** with `/plugin marketplace update` then `/plugin install autonomous-dev-loop@autonomous-dev-tools` (or it picks up automatically on next session if they have it enabled).

## Don't

- Don't push a release where typecheck/lint/validate fail.
- Don't bump version without a changelog entry.
- Don't tag without bumping both manifests.
- Don't include "WIP" commits in the tagged release — squash or rebase first.

## Pre-release / beta

For experimental changes, use `0.X.Y-beta.N` and tag accordingly. Users opt in by pinning that version in their marketplace cache.

## Yanking a release

If a release ships broken:
1. Tag the previous good commit as `autonomous-dev-loop-v0.2.1` (patch-level bump).
2. Document the regression in `CHANGELOG.md`.
3. Push.
4. Users update.

There is no `git tag --delete` equivalent for marketplace clients that already pulled the bad version — they need to update forward.
