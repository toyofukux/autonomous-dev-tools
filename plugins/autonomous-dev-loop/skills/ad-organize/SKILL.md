---
name: ad-organize
description: Propose splitting accumulated stories into units (or restructuring existing units). Analyzes specs/stories.md or all specs/units/*/stories.md, proposes clusters, asks the user to confirm, then physically moves stories.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# /ad-organize

Refactor the `specs/units/` tree based on accumulated stories.

## When to use

- Project has been using flat `specs/stories.md` and it's getting large or topically mixed.
- An existing unit's `stories.md` has crossed ~500 lines (the file-size split trigger).
- A unit is doing two unrelated things and you want to split it.

## What you do

1. **Scan the current state**:
   - If `specs/stories.md` exists (no units yet), read it.
   - If `specs/units/*/stories.md` exist, read all.
2. **Detect triggers**:
   - **No units yet + >10 stories** → propose initial unit split.
   - **Existing unit's `stories.md` > 500 lines** → propose file-split (each story to `story-NNN.md`, `stories.md` becomes index).
   - **Unit with stories that fall into ≥2 disjoint topic clusters** → propose unit split.
3. **Cluster the stories** by topic (use semantic groupings: actor + capability area). Propose unit names (kebab-case, ≤2 words, prefer domain over feature).
4. **Present proposal**:
   - Current state summary
   - Proposed structure (tree)
   - For each move: which story → which unit/file
   - Risks (e.g., "this story straddles two units; suggest splitting into ST-X and ST-Y" — only if user agrees)
5. **On approval**, execute:
   - Create new unit directories with `stories.md` + `decision-record.md` from templates
   - Move/copy story blocks (preserve IDs; do not renumber)
   - When splitting `stories.md` into `story-NNN.md` files: rewrite `stories.md` as an index pointing to the new files
   - Update any iteration specs in `specs/iterations/` that referenced the moved stories' files (update their `units:` frontmatter)
6. **Report** the new tree and recommend re-running [[ad-summary]] to verify.

## Discipline

- **Preserve story IDs.** Never renumber. The IDs are referenced from iteration specs, ADRs, and PR history.
- **Never delete stories.** Moves only.
- **One unit-split proposal at a time.** Don't bundle multiple structural changes in one run.
- **File-split rule**: when splitting `stories.md` to files, each `story-NNN.md` contains exactly one story (frontmatter + body). The parent `stories.md` becomes:
  ```markdown
  ---
  unit: <unit>
  index: true
  ---
  # Stories — <unit>
  - [ST-001](./story-001.md): {intent line}
  - [ST-002](./story-002.md): {intent line}
  ```

## What you do NOT do

- You do **not** re-author stories. Move content verbatim.
- You do **not** combine stories. Splits and moves only.
- You do **not** touch `decision-record.md` entries. Decisions stay with the unit they were made in (if the story moves to a new unit, the decision still references the original).
