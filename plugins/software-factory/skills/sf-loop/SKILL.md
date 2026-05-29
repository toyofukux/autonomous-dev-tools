---
name: sf-loop
description: Run the full software-factory chain end-to-end from a feature description to an open PR. Pauses at the three human checkpoints (story approval, brief approval, PR review).
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
arguments: feature
---

# /sf-loop $feature

End-to-end orchestrator. Type one prompt, get a PR.

## What this is

Convenience wrapper that runs:
[[sf-research]] → [[sf-story]] → ⏸ approve → [[sf-spec]] → ⏸ approve → [[sf-dev]] → [[sf-verify]] → [[sf-validate]] → (on FAIL: [[sf-fix]], retry up to 3) → [[sf-pr]] → ⏸ approve

You stay in the loop for **3 human checkpoints**. Everything else runs on its own.

## Preconditions

- `specs/` exists (run [[sf-init]] or [[sf-bootstrap]] first if not).
- Working tree is clean.

## What you do

1. **Run [[sf-story]] $feature**. Pause for story approval. Answer any open questions the story-writer surfaced.
2. **Run [[sf-spec]] <story-id>**. Pause for brief approval. Answer the spec's Questions section.
3. **Run [[sf-dev]] <spec-id>**. Sequential by default; if the user passed `--parallel`, use the parallel flow.
4. **Run [[sf-verify]] <spec-id>**.
5. **Run [[sf-validate]] <spec-id>**.
6. **On FAIL**: run [[sf-fix]] <spec-id> following the 3-attempt rule. After fix, loop back to step 4. If 3 attempts exhausted, stop and present everything to the user.
7. **On PASS**: run [[sf-pr]] <spec-id>. Pause for PR review.

## Pause semantics

At each checkpoint, the orchestrator prints what was produced, waits for the user's `approve` / `change X` / `abort` response, and only proceeds on explicit `approve` (or equivalent). Implicit silence is not approval.

## Discipline

- **Do not skip checkpoints.** Even if the user said "auto-approve everything" earlier in the session, each [[sf-loop]] run starts fresh.
- **Do not call subagents directly.** Always go through the named ad-* skills so the same updates to spec status / file writes happen consistently.
- **One feature per run.** If $feature describes multiple unrelated features, ask the user to invoke [[sf-loop]] separately for each.

## Failure modes

- **Story-writer needs more info** → pause and ask the user.
- **Spec-writer leaves blocking open questions** → pause; the spec body should not be invented around them.
- **Builder surfaces API mismatch** → pause; route to [[sf-fix]] or spec amendment.
- **Validator FAIL after 3 attempts** → stop hard; require human decision.
