---
name: ad-summary
description: Generate (don't maintain) a current-state digest for a unit or the whole project, drawn from concept/arch/stories/ADRs/code. Output is for reading; never persisted as a spec.md.
allowed-tools: Read, Grep, Glob
arguments: target
---

# /ad-summary $target

On-demand digest of "what does $target do today". $target is a unit name (e.g., `checkout`) or `all` for the whole project.

## Why this exists

We do not maintain a `spec.md` per unit, because it drifts. Instead, when a digest is needed (onboarding, planning, retro), this skill generates one **from the durable sources**:
- `specs/concept.md` (high-level context)
- `specs/arch.md` (architectural context)
- `specs/units/$target/stories.md` (functional surface)
- `specs/units/$target/decision-record.md` (why decisions)
- the actual code + tests under the unit's directories (the truth)

The output is **printed to chat**, not written to disk. If you want it as a file for a meeting, copy-paste it yourself.

## What you do

1. **Locate the unit** (or all units if $target == `all`).
2. **Read the durable sources** listed above.
3. **Run `codebase-researcher`** scoped to the unit's directories to capture current implementation patterns.
4. **Compose the digest** in this format:

```markdown
# Summary — {unit or project}
(generated YYYY-MM-DD HH:MM — regenerate as needed; never edited by hand)

## What it does
{1–3 sentences from concept.md + unit's primary stories}

## Current capabilities
- {one bullet per shipped story (Status: done)}

## In-flight
- {one bullet per in-progress iteration spec for this unit, if any}

## Key decisions (recent first)
- ADR-N (YYYY-MM-DD): {one-line}

## Implementation map
- Entry points: {paths}
- Core services: {paths}
- Tests: {paths}

## Known limitations & next likely work
- {from arch.md "Known limitations" + open stories with Status: proposed/approved}
```

5. **Print to chat. Do not write a file.** If the user asks "save this", ask them what filename and confirm — then write only as a one-off, not as a persistent doc.

## Discipline

- **Never write to `specs/units/<u>/spec.md`** — that file doesn't exist by design.
- **Always tag the digest with the generation timestamp** so readers know it's a snapshot.
- **No editorializing.** Report what's there; don't recommend changes.
