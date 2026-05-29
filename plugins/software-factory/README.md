# software-factory

A lightweight 7-agent factory for Claude Code. Story → spec → backend → frontend → verify → validate, with three human checkpoints in between.

Adapted from sairahul1's "Software Factory" article, with our own additions:
- `units/` and ADR for medium-scale projects (opt-in)
- iteration spec lifecycle (created per iteration, deleted on merge)
- `/sf-bootstrap` for existing projects
- explicit performance + scope sections in the spec template
- bundled industry-grade guidelines

## Install

```text
/plugin marketplace add toyofukux/autonomous-dev-tools
/plugin install software-factory@autonomous-dev-tools
```

## First use

```text
# new project
/software-factory:sf-init

# existing project
/software-factory:sf-bootstrap

# run a feature end-to-end
/software-factory:sf-loop "describe your feature in one sentence"
```

## The 14 skills (all namespaced `/software-factory:ad-*`)

| Skill | Purpose |
|---|---|
| `sf-init` | Scaffold new project's `specs/` |
| `sf-bootstrap` | Reverse-engineer `specs/` from existing project |
| `sf-research` | Standalone codebase recon |
| `sf-story` | Draft a user story |
| `sf-spec` | Generate a technical brief |
| `sf-dev` | Implement (backend → frontend) |
| `sf-verify` | Write acceptance tests |
| `sf-validate` | Report gaps vs spec |
| `sf-fix` | Route findings back to right builder |
| `sf-pr` | Open PR, transfer decisions to ADR |
| `sf-loop` | Full chain orchestrator |
| `sf-summary` | On-demand current-state digest |
| `sf-guideline` | Add a bundled guideline |
| `sf-organize` | Propose unit split |

## The 8 subagents

| Agent | Role | Tools |
|---|---|---|
| `codebase-researcher` | Map relevant code before building | Read, Grep, Glob |
| `story-writer` | Write story + AC + open questions | Read |
| `spec-writer` | Write technical brief | Read, Grep, Glob |
| `backend-builder` | Implement backend + unit tests | Read, Edit, Write, Bash, Grep, Glob |
| `frontend-builder` | Implement frontend + component tests | Read, Edit, Write, Bash, Grep, Glob |
| `test-verifier` | Write acceptance tests | Read, Edit, Write (tests only), Bash, Grep, Glob |
| `validator` | Report gaps vs spec | Read, Grep, Glob |
| `bootstrap-explorer` | Reverse-engineer existing project | Read, Grep, Glob |

## Three human checkpoints

1. **Story** — read & approve before any technical work.
2. **Brief** — read & approve before any code is written.
3. **PR** — read & approve before merge.

That's it. Everything else runs on its own.

## Layout

```text
plugins/software-factory/
├── .claude-plugin/plugin.json
├── agents/                  # 8 subagent definitions
├── skills/                  # 14 ad-* skills
├── templates/               # files skills copy into user projects
│   ├── SPEC.md.tmpl
│   ├── concept.md.tmpl
│   ├── arch.md.tmpl
│   ├── stories.md.tmpl
│   ├── decision-record.md.tmpl
│   ├── spec-iteration.md.tmpl
│   ├── CLAUDE.md.tmpl
│   └── guidelines/          # 11 bundled guidelines
└── hooks/
    └── pre-commit-secrets.json
```

## Develop locally

```bash
claude --plugin-dir ./plugins/software-factory
/reload-plugins
```

## Further reading

- `docs/discipline.md` — the rules that make this work
- `docs/lifecycle.md` — how iteration specs flow and why nothing is maintained as `spec.md`
- `docs/naming.md` — the `ad-*` convention
- `docs/authoring-skill.md` / `docs/authoring-agent.md` — how to extend
- `docs/roadmap.md` — what's coming
