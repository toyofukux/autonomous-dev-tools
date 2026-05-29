---
name: sf-validate
description: Run validator subagent to compare implementation against story and brief, producing a Critical/Important/Minor report with file:line. Read-only; never patches.
allowed-tools: Read, Bash, Grep, Glob
arguments: spec_id
---

# /sf-validate $spec_id

Generate the validation report. Last machine check before the human PR review.

## Preconditions

- `specs/iterations/$spec_id.md` exists with `status: validating` (i.e., [[sf-verify]] passed or marked uncoverable AC).

## What you do

1. **Load context**:
   - The spec and linked stories
   - Backend + frontend builder reports
   - The test-verifier's coverage report
   - The project's `CLAUDE.md` and any guidelines
2. **Delegate to `validator`** with all the above. Validator does its full check pass.
3. **Receive the report** (Critical / Important / Minor / Scope drift / Coverage gaps / CLAUDE.md additions suggested / Verdict / Cause attribution).
4. **Persist the report** alongside the spec at `specs/iterations/$spec_id/validation-report.md` (overwrite on re-runs; keep only the latest).
5. **Update spec frontmatter** based on verdict:
   - PASS → `status: pr` (ready for [[sf-pr]])
   - FAIL → `status: failed`, with `attempts` incremented
6. **Present the report** to the user. On FAIL:
   - Show the validator's cause attribution and recommended route-back
   - Ask the user: "fix and re-run, or abandon iteration?"
   - If `attempts >= 3`, **always** stop and require human decision (see [[sf-fix]] for the 3-attempt rule)
7. **On PASS**, next command: `/sf-pr $spec_id`.

## Discipline

- **The validator is honest.** If it returns "no issues", trust it and proceed. Do not pad findings.
- **Do not invoke any builder from here.** That's [[sf-fix]]'s job.
- **Capture the validator's CLAUDE.md suggestions verbatim** so [[sf-pr]] can include them in the PR body.
