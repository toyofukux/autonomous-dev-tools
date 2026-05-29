---
name: sf-fix
description: Route validator findings back to the right builder (backend / frontend / spec-writer) and re-run the chain from there. Enforces the 3-attempt cap with staged strategies.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
arguments: spec_id
---

# /sf-fix $spec_id

When [[sf-validate]] or [[sf-verify]] reports failure, route the findings to the right agent and re-run only the necessary part of the chain.

## Preconditions

- `specs/iterations/$spec_id.md` exists with `status: failed`.
- A validator report at `specs/iterations/$spec_id/validation-report.md` OR a verifier failure (the test-verifier's report stored in chat or attached as a file).

## The 3-attempt rule

| Attempt | Strategy | Route-back |
|---|---|---|
| 1 | **Impl-only fix.** Validator's findings go to the named builder; spec stays untouched. | backend-builder OR frontend-builder |
| 2 | **Impl + micro-edit to spec.** Allowed: typo fix, missing AC added, clarification. Not allowed: scope changes, new sections. | spec-writer (micro-edit) → builder |
| 3 | **Human intervention required.** Stop. Present the validator's findings, the spec, and the story; ask the user: "fix code, fix spec, or drop?" | none — user decides |

The spec's `attempts` frontmatter counter tracks this. [[sf-validate]] increments it on FAIL.

## What you do

1. **Read the validator's report** (or verifier failure).
2. **Inspect `attempts` in the spec frontmatter**:
   - `attempts == 0 or 1` → execute Attempt 1 strategy
   - `attempts == 2` → execute Attempt 2 strategy
   - `attempts >= 3` → **stop**. Present everything to the user and exit. Do not auto-fix.
3. **For Attempt 1**:
   - Look at validator's `Cause` and `Route back to`.
   - Delegate to the named builder with the validator report as input ("here are the findings; fix only these, in scope of the spec").
   - When the builder finishes, mark `status: verifying` and tell the user to re-run [[sf-verify]] → [[sf-validate]].
4. **For Attempt 2**:
   - Delegate to `spec-writer` with the validator report and a tight prompt: "produce a micro-edit (no scope change) that resolves these findings, OR refuse if the only fix is a scope change."
   - If spec-writer refuses, escalate to Attempt 3 immediately.
   - On a micro-edit, present the diff to the user, get approval, then route to the appropriate builder.
5. **For Attempt 3**: stop. Output a clear prompt:
   > 3 attempts exhausted. Choose:
   > - **fix-code** — last validator report attached; reopen [[sf-fix]] only after manual changes
   > - **fix-spec** — edit `specs/iterations/$spec_id.md` directly, then re-run [[sf-dev]]
   > - **drop** — abandon this iteration (`/sf-pr --abandon $spec_id`)

## Discipline

- **Never call a different builder than the validator routed to.** Validator's `Cause` and `Route back to` is authoritative for Attempt 1.
- **Never quietly change attempts counter** — it's the cap that protects the user from infinite loops.
- **Spec micro-edits in Attempt 2 must show a diff before applying.**
- **Do not chain into [[sf-verify]] or [[sf-validate]] automatically.** The user decides when to re-validate.
