---
name: sf-story
description: Turn a rough feature description into a real user story with AC and open questions, then append it to the right unit's stories.md after user approval. Runs codebase-researcher first, then story-writer.
allowed-tools: Read, Write, Bash, Grep, Glob
arguments: feature
---

# /sf-story $feature

Draft a user story for "$feature" and add it to `stories.md` after approval. This is the **first human checkpoint** of the software-factory.

## What you do

1. **Run `codebase-researcher`** on $feature. Capture its full output.
2. **Pick the target unit**:
   - If `specs/units/` doesn't exist (project hasn't been organized yet), use a default file `specs/stories.md` (root-level). Mention `/sf-organize` for later.
   - If `specs/units/` exists, propose the unit based on the researcher's findings and ask the user to confirm or override (single-keystroke confirm).
3. **Run `story-writer`** with: the user's $feature description, the researcher's findings, and (if found) the target unit's existing `stories.md` content for the consistency check.
4. **Receive the story block** from story-writer, plus any consistency-check notes (duplicates, conflicts).
5. **Present to the user** for approval:
   - The story block as-is (with `{{ID}}` placeholder)
   - Any consistency-check notes from story-writer (resolve before writing)
   - The open questions — these must be answered before [[sf-spec]] can run; surface this explicitly
6. **Assign a new story ID** (next available `ST-NNN` in the target file).
7. **Append to `stories.md`** (or split file if it crosses 500 lines — see [[sf-organize]] for split rules).
8. **Report**:
   - The assigned ID
   - The file path it was written to
   - The list of open questions the user still owes answers to
   - The next command: `/sf-spec ST-NNN` (once questions are answered)

## Discipline

- **Do not append a story with unresolved consistency issues.** If story-writer flagged duplicates, surface them and ask the user how to proceed.
- **Open questions are blocking.** Do not silently mark the story `approved` if questions remain; status starts at `proposed` and only becomes `approved` after the user explicitly answers all questions.
- **One story per invocation.** If the user gave a description that's clearly multiple features, split and run sequentially.
- **500-line rule**: if appending pushes `stories.md` past ~500 lines, propose a split: each story becomes `story-NNN.md`, `stories.md` becomes the index. Ask before splitting.

## File-write pattern (no overwrites of existing stories)

- Open the target `stories.md`.
- Append the new story block at the end.
- Update the index section if the file uses index-format.
- Write back. Never modify other stories' contents.
