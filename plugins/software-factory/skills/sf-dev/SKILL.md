---
name: sf-dev
description: Implement an approved spec by running backend-builder then frontend-builder in sequence. Backend writes backend-summary.md as the API contract for frontend. Add --parallel to opt into worktree-based parallel dev (advanced).
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
arguments: spec_id
---

# /sf-dev $spec_id

Implement the approved brief. Default: sequential (backend → frontend). Optional: `--parallel` for worktree-based parallelism.

## Preconditions

- `specs/iterations/$spec_id.md` exists with `status: approved`.
- Working tree is clean (or user has explicitly confirmed otherwise).

## Default flow (sequential)

1. **Update spec status** to `developing` (frontmatter `status:` field).
2. **Run `backend-builder`** with:
   - The spec at `specs/iterations/$spec_id.md`
   - The researcher's findings (re-fetch by running researcher if cache stale)
   - The project's `CLAUDE.md` and relevant guidelines
3. **After backend-builder finishes**:
   - Verify `specs/iterations/$spec_id/backend-summary.md` was created. If not, the builder failed to produce the contract — stop and report.
   - Capture builder's final report (files added/modified, test results).
4. **Run `frontend-builder`** with:
   - The spec
   - `backend-summary.md` (as API contract — this is critical)
   - Researcher findings + CLAUDE.md + guidelines
5. **If frontend-builder surfaces an API mismatch**: stop. Show the mismatch to the user. They choose:
   - Re-run `backend-builder` with the frontend's feedback as a fix
   - Update the spec via [[sf-fix]]
   - Abandon the iteration
6. **Compile both builders' reports** and surface to the user. Next command: `/sf-verify $spec_id`.

## Parallel flow (`--parallel`)

Opt-in. Requires the spec's Diff expectation to have zero overlap between backend and frontend owners (the spec-writer should have arranged this; we check).

1. **Pre-flight check**: validate the Diff expectation has no file owned by both `backend` and `frontend`. If overlap exists, refuse and tell the user to either re-run `/sf-spec` (to separate the shared types into a "shared" pre-step) or run sequential.
2. **Create worktrees**:
   - `git worktree add ../wt-$spec_id-be feat/$spec_id-be`
   - `git worktree add ../wt-$spec_id-fe feat/$spec_id-fe`
3. **Run backend-builder in the BE worktree** (background-capable).
4. **When backend-builder writes `backend-summary.md`**, copy it into the FE worktree and start frontend-builder there.
5. **When both finish**, merge both branches into `feat/$spec_id`. Conflict resolution falls back to sequential if conflicts exist.
6. **Clean up worktrees**.

`--parallel` is documented but not the default. The sequential flow is the article-aligned baseline.

## Spec frontmatter transitions

- `approved` → `developing` (at start)
- `developing` → `verifying` (after both builders pass typecheck+lint+unit tests)
- on failure: `developing` → `failed` (orchestrator stops; user uses [[sf-fix]])

## Discipline

- **Never start `/sf-verify` or `/sf-validate` automatically.** This skill stops at `verifying`.
- **Capture test output verbatim** — don't paraphrase. Builders' summaries already report pass/fail; do not mark the iteration `verifying` if any test failed.
- **Do not edit the spec body** — if the spec is wrong, that's an [[sf-fix]] flow.
- **Do not skip backend-summary.md**. If backend-builder didn't write it, that's an error to escalate, not patch around.
