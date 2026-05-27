# autonomous-dev-loop

A lightweight 7-agent factory for Claude Code. Story → spec → backend → frontend → verify → validate, with three human checkpoints in between.

Adapted from sairahul1's "Software Factory" article, with our own additions:
- `units/` and ADR for medium-scale projects (opt-in)
- iteration spec lifecycle (created per iteration, deleted on merge)
- `/ad-bootstrap` for existing projects
- explicit performance + scope sections in the spec template
- bundled industry-grade guidelines

## Install

```text
/plugin marketplace add toyofukux/autonomous-dev-tools
/plugin install autonomous-dev-loop@autonomous-dev-tools
```

## First use

```text
# new project
/autonomous-dev-loop:ad-init

# existing project
/autonomous-dev-loop:ad-bootstrap

# run a feature end-to-end
/autonomous-dev-loop:ad-loop "describe your feature in one sentence"
```

## The 14 skills (all namespaced `/autonomous-dev-loop:ad-*`)

| Skill | Purpose |
|---|---|
| `ad-init` | Scaffold new project's `specs/` |
| `ad-bootstrap` | Reverse-engineer `specs/` from existing project |
| `ad-research` | Standalone codebase recon |
| `ad-story` | Draft a user story |
| `ad-spec` | Generate a technical brief |
| `ad-dev` | Implement (backend → frontend) |
| `ad-verify` | Write acceptance tests |
| `ad-validate` | Report gaps vs spec |
| `ad-fix` | Route findings back to right builder |
| `ad-pr` | Open PR, transfer decisions to ADR |
| `ad-loop` | Full chain orchestrator |
| `ad-summary` | On-demand current-state digest |
| `ad-guideline` | Add a bundled guideline |
| `ad-organize` | Propose unit split |

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
plugins/autonomous-dev-loop/
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
claude --plugin-dir ./plugins/autonomous-dev-loop
/reload-plugins
```

## Further reading

- `docs/discipline.md` — the rules that make this work
- `docs/lifecycle.md` — how iteration specs flow and why nothing is maintained as `spec.md`
- `docs/naming.md` — the `ad-*` convention
- `docs/authoring-skill.md` / `docs/authoring-agent.md` — how to extend
- `docs/roadmap.md` — what's coming
