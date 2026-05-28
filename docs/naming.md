# Naming convention

## Skills

Every skill in `plugins/software-factory/skills/` is named **`ad-<verb>`**.

- `ad` = autonomous development.
- `<verb>` is a single short imperative: `init`, `bootstrap`, `story`, `spec`, `dev`, `verify`, `validate`, `fix`, `pr`, `loop`, `summary`, `guideline`, `organize`.

When installed via plugin, the command becomes `/software-factory:ad-<verb>`. The double-prefix is intentional:

- It guards against name collision if a user ever copies a skill out of the plugin and into their own `.claude/skills/`.
- It keeps the brand grouped (autocomplete will surface all `ad-*` skills together).

## Subagents

Subagents use descriptive nouns (no prefix): `codebase-researcher`, `story-writer`, `spec-writer`, `backend-builder`, `frontend-builder`, `test-verifier`, `validator`, `bootstrap-explorer`.

Plugin namespacing handles isolation; no extra prefix is needed.

## Templates

User-facing template files end in `.tmpl` to make their purpose obvious in directory listings (`stories.md.tmpl`, `spec-iteration.md.tmpl`, ...). Skills strip the suffix when copying.

## Guidelines

Bundled guideline files live at `templates/guidelines/<name>.md` (no `.tmpl` — they're copied as-is). User-project copies live at `specs/guidelines/<name>.md`.

## Renaming

If you ever need to change the `ad-` prefix (rebrand, conflict with another plugin):

```bash
scripts/rename-prefix.sh software-factory ad zz
```

This:
- Renames `skills/ad-*/` → `skills/zz-*/`
- Updates `[[ad-*]]` references in SKILL.md and agent bodies
- Updates README and docs

Bump the plugin's `version` after a rename — it's a breaking change for users.
