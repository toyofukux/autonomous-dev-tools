---
name: ad-verify
description: Write acceptance tests for an implemented spec by delegating to test-verifier. Acceptance tests only (not unit) — those were the builders' responsibility.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
arguments: spec_id
---

# /ad-verify $spec_id

Run the test-verifier to write acceptance tests against the story's AC.

## Preconditions

- `specs/iterations/$spec_id.md` exists with `status: verifying` (i.e., [[ad-dev]] completed successfully).
- Both builders' summary reports are available.

## What you do

1. **Load context**:
   - The spec at `specs/iterations/$spec_id.md`
   - The linked stories (with their AC)
   - Backend-builder and frontend-builder final reports
   - `specs/iterations/$spec_id/backend-summary.md`
2. **Delegate to `test-verifier`** with all of the above.
3. **Receive the acceptance test file** and the coverage report.
4. **Write the test file** to the project's acceptance-test location (which the test-verifier should have inferred from existing conventions).
5. **Run the test suite** (`bash` with the project's test command from CLAUDE.md).
6. **Update spec frontmatter**:
   - All AC covered & passing → `status: validating`
   - At least one AC failing → `status: failed`, route the user to [[ad-fix]]
   - At least one AC genuinely uncoverable → `status: validating` but include the gaps in the report; the validator will read them
7. **Report**:
   - The coverage table (every AC's status)
   - The verdict (PASS / FAIL / INCOMPLETE)
   - Next command: `/ad-validate $spec_id` (on PASS or INCOMPLETE) or `/ad-fix $spec_id` (on FAIL)

## Discipline

- **No patching of implementation code in this step.** Test-verifier's role is to test, not fix.
- **Don't lower the bar.** If an AC genuinely can't be tested (e.g., needs a live external payment provider), mark uncovered with reason. Don't write a fake passing test.
- **Don't add tests for things not in the AC.** Out-of-scope items don't get tests here.
