---
name: ad-spec
description: Turn one or more approved stories into a technical brief at specs/iterations/spec-YYYYMMDD-slug.md by delegating to spec-writer. Second human checkpoint. Requires the story's open questions to be answered first.
allowed-tools: Read, Write, Bash, Grep, Glob
arguments: story_ids
---

# /ad-spec $story_ids

Generate the technical brief for the given story (or stories) and write it to `specs/iterations/`. This is the **second human checkpoint**.

`$story_ids` is one or more story IDs separated by commas (e.g., `ST-017` or `ST-017,ST-019`).

## What you do

1. **Locate the stories** in the appropriate `stories.md` (search across units if needed). If any story is not in `approved` status (i.e., open questions remain), stop and tell the user to answer them in `stories.md` first.
2. **Run `codebase-researcher`** (or reuse a recent run if the user opts to). Pass the story IDs as the investigation target.
3. **Run `spec-writer`** with:
   - The verbatim story texts
   - The researcher's findings
   - The project's `CLAUDE.md`
   - Any matching `guidelines/*.md`
4. **Receive the spec content** from spec-writer.
5. **Compute the spec ID and filename**:
   - `spec_id = spec-YYYYMMDD-<slug>` where YYYYMMDD is today's date and `<slug>` is a kebab-case 3–5 word summary derived from the story.
   - Path: `specs/iterations/<spec_id>.md`
6. **Write the brief** to that path. Status starts as `drafted`.
7. **Present to the user for approval**:
   - Show the brief in full (or via path if too long for chat).
   - Highlight the Questions section explicitly.
   - Ask the user to either:
     - approve as-is (status → `approved`), or
     - answer questions, then we update the Decisions section and approve.
8. **On approval**, update the spec's `status:` frontmatter to `approved` and the `Decisions` section with any answers the user gave. Update each linked story's status to `speccing` in its `stories.md`.
9. **Report** the spec ID and the next command: `/ad-dev <spec-id>`.

## Discipline

- **Question section must be empty (or only listing user-input choices) before status becomes `approved`.** Spec-writer leaves no implementation question — those must be self-resolved.
- **Do not start `/ad-dev` automatically.** Approval here is human-required.
- **One iteration per spec.** If the user wants to bundle unrelated stories, push back — separate specs are easier to validate and revert.

## Filename slug generation

- Lowercase, kebab-case
- Drop articles (a, the) and pronouns
- 3–5 words from the story's "I want ..." clause
- Examples:
  - "buyer apply coupon at checkout" → `checkout-coupon`
  - "admin export user list as CSV" → `admin-export-users-csv`
