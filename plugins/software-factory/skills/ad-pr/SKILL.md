---
name: ad-pr
description: Finalize an iteration — transfer Decisions to the unit's ADR, mark stories done, delete the iteration spec, open a PR with the validator's CLAUDE.md suggestions surfaced. Third human checkpoint.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
arguments: spec_id
---

# /ad-pr $spec_id

Open the PR. **Third (and final) human checkpoint** of the loop.

## Preconditions

- `specs/iterations/$spec_id.md` exists with `status: pr` (validator PASS).
- Git branch checked out for this iteration (typically `feat/$spec_id` from [[ad-dev]]).
- `gh` CLI available and authenticated.

## What you do

1. **Read the iteration spec** — capture:
   - Linked story IDs
   - `Decisions` section
   - `Logs for self-improvement` section
   - `Release steps` section
   - The validator's CLAUDE.md suggestions (from `specs/iterations/$spec_id/validation-report.md`)
2. **For each linked story**:
   - Locate its file (search `specs/units/*/stories.md` or `specs/stories.md`)
   - Update its `Status:` line to `done`
   - Update its `Specs:` line to include `$spec_id`
3. **Transfer Decisions to the unit's ADR**:
   - For each `D-N` entry in the spec's Decisions section, create a new `ADR-NNN` entry at the top of the appropriate `specs/units/<unit>/decision-record.md`
   - Use the format from `decision-record.md.tmpl`; cite `$spec_id` in the header
4. **Optionally transfer Logs-for-improvement** to the unit's `observability.md` (create if missing) — only if the spec's section has more than a placeholder.
5. **Delete the iteration spec directory**:
   - `rm -r specs/iterations/$spec_id.md specs/iterations/$spec_id/` (the spec itself + the children: backend-summary.md, validation-report.md)
   - These are now redundant; the git log + ADR + acceptance tests are the durable record.
6. **Stage and commit** the doc updates (story status, ADR, observability) on the current branch.
7. **Open the PR** with this body template:

```markdown
## Summary
{from spec's Summary section}

## Stories shipped
- ST-NNN: {one-line intent}

## What changed
{spec's Diff expectation table, condensed}

## Release steps
{spec's Release steps verbatim, as a checklist}

## Suggested CLAUDE.md additions
{validator's CLAUDE.md suggestions, if any; otherwise omit}

## Validation
- Acceptance tests: {N} passing
- Validator verdict: PASS
- Validator report: (deleted with the iteration spec; see git log for full text)

🤖 Generated with the software-factory plugin
```

8. **Run `gh pr create`** with the body above. Use `--draft` if the user wants a final review pass before requesting reviewers; ask once.
9. **Present** the PR URL and stop. Do not merge automatically.

## Abandon mode

`/ad-pr --abandon $spec_id`:
- Stops without opening a PR
- Reverts story Status to `approved` (so the spec can be re-attempted later)
- Deletes the iteration spec directory
- Leaves the branch alone (the user decides whether to discard)

## Discipline

- **Do not push or merge silently.** The user reviews the PR before it ships.
- **Do not omit the ADR transfer** — that's the only durable record of why we did this.
- **Do not omit the iteration-spec deletion** — keeping it after merge causes drift, which is exactly what the model is supposed to prevent.
- **Do not amend the user's commits.** Make a new commit for the doc updates.
