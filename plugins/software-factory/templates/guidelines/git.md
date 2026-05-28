# Git guideline

> Commits are letters to your future self and your reviewers. Write them like you mean it.

## Non-negotiables

### Branch naming
- `main` is always shippable. No direct commits.
- Feature branches: `feat/<spec-id>` for software-factory iterations (e.g., `feat/spec-20260527-checkout-coupon`).
- Other prefixes: `fix/`, `chore/`, `docs/`, `refactor/`, `experiment/`.
- Short, kebab-case, descriptive. No personal names.

### Commit hygiene
- **One logical change per commit.** Reviewers should be able to read the diff and understand the why from the message alone.
- **No mixed concerns.** Don't bundle a refactor with a feature. Don't fix typos in unrelated files in the same commit.
- **Tests with code, in the same commit.** A commit that adds a feature but no tests is incomplete.
- **No commits that don't build / don't pass type-check.** Each commit is a valid intermediate state.

### Commit messages

```
<type>: <short summary in imperative mood, ≤ 72 chars>

<empty line>

<body: why this change exists, what alternatives were considered, any callouts>

<empty line>

<footer: refs, breaking-change notes, co-author>
```

- **Types**: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `perf`, `style`, `build`, `ci`, `revert`.
- **Subject in imperative mood**: "Add coupon validation", not "Added" or "Adds".
- **No period** at the end of subject.
- **Body wraps at ~72 chars**. Explains WHY. Not necessary for trivial changes.
- **Footer** for issue/spec refs (`Refs: spec-20260527-checkout-coupon`), breaking changes (`BREAKING CHANGE: ...`), co-authors.

### When to rebase vs merge
- **Rebase locally** to keep your branch up to date with main while in development.
- **Merge (with --no-ff or squash, per repo convention)** into main via PR.
- **Never force-push to main** or to a shared branch.
- **Never `git reset --hard` on someone else's branch.**

### Pull requests
- **One PR per spec / one PR per logical change.**
- **PR title and body** match the spec's Summary and Diff expectation.
- **Description includes**:
  - Summary (what & why)
  - Stories shipped (with IDs)
  - Test plan (what was verified)
  - Validator verdict
  - Rollback plan if applicable
- **Draft until ready**. Don't request reviews on incomplete PRs.
- **Resolve all CI failures and review comments before merging.**

### Code review
- **Be specific in comments.** "Consider X because Y" beats "weird".
- **Suggest, don't dictate**, unless safety-critical.
- **Block on safety issues** (security, data loss, breaking change). Comment on style.
- **Approve when ready, not when "looks fine"**. Approval = you'd merge it yourself.

### Pre-commit hooks
- **Secrets blocker** mandatory (the plugin ships one at `hooks/pre-commit-secrets.json`).
- **Formatter** runs on staged files (prettier / black / gofmt).
- **Linter** runs on staged files; fixable issues auto-fixed, others block.
- **Quick tests** (unit only) on the changed file's tree, if fast enough.
- **Never `--no-verify`** without a documented reason — if a hook is failing, fix the underlying issue.

### Tags & releases
- Semantic versioning (`vMAJOR.MINOR.PATCH`).
- Tagged releases include a changelog generated from commits since the last tag.
- For this plugin: bump `version` in both `marketplace.json` and `plugin.json` together with the tag.

### Things you should not commit
- Secrets, keys, `.env` files.
- Generated artifacts that belong to build output (`dist/`, `build/`, `node_modules/`).
- Editor-specific config (`.idea/`, `.vscode/settings.json`) — keep `.vscode/extensions.json` only.
- OS metadata (`.DS_Store`, `Thumbs.db`).
- Backup files (`*~`, `*.bak`).

The plugin ships a `pre-commit-secrets.json` hook that blocks the obvious ones.

## Patterns to follow

- **Atomic commits.** Small enough that the message titles the diff.
- **Commit early, push often.** A WIP push is better than a hard drive failure.
- **`git rebase -i` to clean up before opening a PR** (squash WIPs, fix typos in messages).
- **`git bisect` to find regressions.** Worth the practice.

## Anti-patterns

- "WIP" / "fix" / "update" commits in main history.
- Squashing 10 unrelated changes into one PR.
- `git push --force` to a shared branch.
- `git add .` without reviewing the staged set.
- Skipping hooks routinely.
- Bumping version without changelog.

## Quick self-check

- [ ] Branch name follows convention.
- [ ] Each commit builds, tests pass, one logical change.
- [ ] Commit messages: type prefix, imperative subject, body explains why.
- [ ] PR title + body explain the change.
- [ ] No secrets, no generated artifacts staged.
- [ ] All CI green; reviewer comments resolved.

## References

- Conventional Commits (https://www.conventionalcommits.org/)
- Tim Pope, "A Note About Git Commit Messages"
- Pro Git (Chacon, Straub) — chapters on rebasing, history rewriting
- Google's "Engineering Practices: Code Review"
