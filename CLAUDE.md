# Repo: autonomous-dev-tools

You are working in the marketplace repo that distributes the `software-factory` plugin. This repo's job is to **author** the plugin, not to use it.

## Layout

```
.claude-plugin/marketplace.json     # the marketplace catalog
plugins/software-factory/        # the (currently only) plugin
  .claude-plugin/plugin.json
  agents/                           # 8 subagent definitions
  skills/                           # 14 ad-* skills
  templates/                        # files the skills copy into user projects
  hooks/                            # bundled hooks (e.g. pre-commit secrets)
scripts/                            # repo-level helpers
docs/                               # plugin authoring docs
.github/workflows/validate.yml      # CI: claude plugin validate
```

## Hard rules

1. **Skill names**: every skill in `plugins/software-factory/skills/` is named `ad-<verb>`. Never drop the prefix; never use a different prefix. See `docs/naming.md`.
2. **Subagent tool scoping is non-negotiable**. Backend builder must never list frontend tools, validator must never list write tools, etc. The whole point of the factory is the scoping; loosening it defeats the design.
3. **Templates are user-facing artifacts**. When editing `templates/`, ask "would a first-time user understand this in 5 minutes?" If no, simplify.
4. **No `spec.md` anywhere**. We never instruct skills/subagents to maintain a `spec.md` file. The SSoT model is distributed (see `docs/lifecycle.md`).
5. **Progressive disclosure**. New plugin features are opt-in by default. Don't make any feature mandatory unless every single-feature project needs it on day 1.
6. **Reference the article's discipline**. The 7-agent factory's value comes from strict separation of concerns. When in doubt, re-read `docs/discipline.md`.

## Workflow

- For substantive changes, open a PR. The repo follows its own discipline (one commit per logical change, message in English).
- Run `claude plugin validate` (or the CI workflow) before pushing.
- Bump `version` in both `marketplace.json` and `plugin.json` on user-visible changes.

## What NOT to do

- Do not pull skill/agent definitions from `~/.claude/` automatically. Guideline content may be informed by personal rules, but the plugin's skills/agents are authored fresh.
- Do not add a `spec.md` template, even if asked. Redirect to `concept.md` + `stories.md` + ADR.
- Do not add subagent #9 without removing or merging an existing one. 7 is the target.
- Do not commit secrets (the pre-commit hook in `plugins/software-factory/hooks/` is the safety net, not the only line of defense).
