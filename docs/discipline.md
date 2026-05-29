# Discipline

The hardest part of the software-factory isn't the architecture; it's the discipline of using it correctly.

## Discipline #1: throw conversations away

When you realize a wrong architectural assumption is loaded into the current Claude Code session — **do not patch the prompt to override it**. Patches breed drift.

- Small typo? → correct inline.
- Field naming was wrong but used in a few places? → correct inline.
- **Wrong mental model** (e.g., "subscriptions belong to users" when they belong to companies)? → close the session, open a new one with the correct assumption baked into the first prompt.

A clean session with the right mental model beats a patched session every time. The plugin's per-subagent context isolation helps, but doesn't replace this discipline at the main-thread level.

## Discipline #2: respect the human checkpoints

The article specifies three: story, brief, PR. Adding more produces friction; removing any produces silent compounding errors.

- Don't auto-approve. Even if you're tired. Especially if you're tired.
- Don't merge skills (e.g., "let `/sf-spec` also do the build") to skip a checkpoint. The checkpoint is the whole point.

## Discipline #3: validator is the truth

When the validator returns PASS, ship. When it returns FAIL, fix the cause it identifies, don't argue.

If you find yourself "manually overriding" a validator finding:

- The finding was wrong → file a bug against the validator agent prompt.
- The finding was right but inconvenient → fix the code or the spec.
- The validator is generating noise → tighten its prompt; don't lower its bar.

A validator that auto-passes after enough complaining is a validator that everyone learns to ignore.

## Discipline #4: progressive disclosure

The plugin can do a lot. That doesn't mean every project needs all of it on day 1.

- One small project with three features doesn't need units.
- One small project doesn't need 11 guidelines.
- One small project's `concept.md` can be 10 lines.

Adding structure too early reproduces the heaviness this plugin was built to avoid.

## Discipline #5: write the rule, don't repeat the mistake

Every time the AI surprises you with a mistake, ask: would a rule in `CLAUDE.md` (or a guideline) have prevented this?

If yes:
- Add the rule.
- Commit it as part of the fix.
- The next time, the rule applies.

`CLAUDE.md` becomes a record of every assumption the AI got wrong. After a few weeks, sessions get noticeably better with no effort.

The validator surfaces "CLAUDE.md additions suggested" when it spots patterns. Take those seriously.

## Discipline #6: one feature per iteration

`/sf-loop` runs **one** feature. If you find yourself wanting to bundle two unrelated features into one iteration to save time, don't.

- Two features = two specs = two PRs = two clean reverts if needed.
- Bundling makes validator findings ambiguous (whose AC failed? whose impl drifted?).
- The marginal time saving is consumed by the merge friction.

## Discipline #7: no spec.md, no `_unused`, no "removed" comments

These are subtle drift sources:

- A maintained `spec.md` drifts vs code; we don't have one. See `lifecycle.md`.
- An `_unused` rename pretending to keep a variable for backward compat — just delete.
- A `// removed because Y` comment — the git log is for that.

The plugin's code quality guideline lists these as anti-patterns. They're worth their own callout here because they're how clean projects slowly become messy.

## Sources

- "Context drift" and "throw the conversation away" — adapted from the original 7-agent factory article (sairahul1) and Boris Cherny's interviews.
- "Write the rule, don't repeat the mistake" — adapted from Boris Cherny's CLAUDE.md feedback loop.
