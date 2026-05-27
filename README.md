# autonomous-dev-tools

A Claude Code plugin marketplace for autonomous development.

The first plugin, **`autonomous-dev-loop`**, ships a lightweight 7-agent factory adapted from sairahul1's "Software Factory" article. One developer + seven focused subagents = a coordinated team that takes a feature description and ends at a reviewed PR with three human checkpoints in between.

## Install

In Claude Code:

```text
/plugin marketplace add toyofukux/autonomous-dev-tools
/plugin install autonomous-dev-loop@autonomous-dev-tools
```

## What you get

After install, these commands are available (namespaced under the plugin):

| Phase | Skill | What it does |
|---|---|---|
| setup | `/ad-init` | Scaffold `specs/` in a new project |
| setup | `/ad-bootstrap` | Reverse-engineer `specs/` from an existing project |
| loop | `/ad-loop <feature>` | Run the full chain end-to-end |
| step | `/ad-research <topic>` | Codebase recon (read-only) |
| step | `/ad-story <feature>` | Draft a user story with AC and open questions |
| step | `/ad-spec <story-id>` | Turn the story into a technical brief |
| step | `/ad-dev <spec-id>` | Implement (backend then frontend, both with unit tests) |
| step | `/ad-verify <spec-id>` | Write acceptance tests against the story's AC |
| step | `/ad-validate <spec-id>` | Compare implementation vs story+brief, report gaps |
| step | `/ad-fix <spec-id>` | Feed validator findings back to the right builder |
| step | `/ad-pr <spec-id>` | Transfer decisions to ADR, delete iteration spec, open PR |
| extra | `/ad-summary <unit>` | Generate (don't maintain) a current-state digest for a unit |
| extra | `/ad-guideline <name>` | Add a project guideline file from the bundled library |
| extra | `/ad-organize` | Propose splitting accumulated stories into units |

## Three human checkpoints

1. **Story** — you read and approve the story before any technical work happens.
2. **Brief** — you read and approve the technical brief before any code is written.
3. **PR** — you read and approve the PR before it ships.

Everything between runs on its own.

## Design philosophy

- **Progressive disclosure**: `/ad-init` ships the bare minimum (`concept.md`, `arch.md`, `iterations/`). `units/`, `guidelines/`, and observability docs appear only when you opt in.
- **No maintained `spec.md`**: the SSoT for "what the system does today" lives in concept + arch + stories + ADRs + code. When you need a digest, `/ad-summary` generates one.
- **Strict tool scoping per agent**: backend can never accidentally touch the frontend, the validator can never patch code.
- **One developer, one prompt** is enough to start the chain; you stay in the loop where your judgment matters and the agents handle everything in between.

## Develop the plugin

```bash
# load the plugin from this repo in a test session
claude --plugin-dir ./plugins/autonomous-dev-loop

# reload after edits
/reload-plugins

# validate the marketplace + plugin
claude plugin validate
```

See `docs/` for authoring guidance:

- `docs/naming.md` — the `ad-*` convention and how to rename
- `docs/lifecycle.md` — iteration spec lifecycle
- `docs/discipline.md` — when to throw the conversation away vs patch
- `docs/authoring-skill.md` — how to write a new skill
- `docs/authoring-agent.md` — how to write a new subagent
- `docs/roadmap.md` — future plugins (external-research, payments-integration, ...)
- `docs/release.md` — versioning and release procedure

## Credits

Heavily inspired by [sairahul1's 7-agent factory article](https://x.com/sairahul1) and the broader spec-driven workflow community (Pimzino, shinpr, lbruton, Boris Cherny's interviews). Where we differ from these prior arts is documented in `docs/lifecycle.md` and `docs/discipline.md`.
