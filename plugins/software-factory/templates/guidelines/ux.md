# UX guideline

> Behavior the user feels. Default to honesty, latency awareness, and reversibility.

## First principles

1. **Tell the user what happened.** Every action produces a visible result or confirmation.
2. **Show progress.** If it'll take >1s, show progress; if >10s, show ETA or a way to leave and come back.
3. **Make the right thing easy and the wrong thing hard.** Defaults matter more than labels.
4. **Allow undo.** Almost everything destructive should have an undo within 30s.
5. **Don't lie.** "Almost done" must mean almost done.

## Non-negotiables

### Latency feedback (the Nielsen thresholds)
- **< 100ms** → feels instant; no feedback needed.
- **100ms–1s** → feels responsive; a brief visual change is enough.
- **1s–10s** → show progress (spinner with a label, or a skeleton).
- **> 10s** → show ETA or background it; let the user navigate away.

### Error handling
- Errors describe **what failed**, **why** if known, and **what to do next**.
  - Bad: "An error occurred."
  - Good: "Couldn't save your changes — your session expired. Click here to sign in again, then we'll keep your edits."
- **Preserve user input** on validation failure. Never make them retype.
- **Distinguish recoverable vs unrecoverable**. Recoverable: show the action. Unrecoverable: explain who to contact.
- **Errors don't blame the user.** "Email must contain @" not "Invalid input".

### Empty states
- Empty state = onboarding moment. Explain what this surface will eventually show, and the primary action that gets the user there.
- Don't show "No data" with no further help.

### Confirmation & destructive actions
- **Destructive actions** (delete, send, publish) are confirmed when the action can't be undone within the session.
- **Confirmation describes the consequence**: "Delete 'Q4 Report'? This deletes 3 connected revisions too."
- **Don't double-confirm** non-destructive actions. "Are you sure?" is friction; reserve it.

### Undo, not confirm
- Where possible, prefer undo over confirm. Send the email, show "Sent · Undo (10s)". Users move faster and feel safer.

### Onboarding
- The first session **succeeds** at something within 60s. If success requires connecting an integration, do that step first and acknowledge done.
- Empty states ARE onboarding for repeat surfaces.
- Tooltips are not onboarding; they're recall aids.

### Notifications
- Three categories:
  - **Toast** — ephemeral, success/info, auto-dismiss in 3–5s.
  - **Banner** — persistent until resolved, in-context.
  - **Alert** — modal, blocks until acknowledged. Reserve for genuinely blocking events.
- Don't notify what the user just did themselves (no "You clicked Save").

### Permissions, paywalls, gates
- Explain **why** the permission is needed before asking the OS for it.
- Explain **what's locked** behind the paywall and what unlocks it.
- Don't surprise the user with a paywall after they invested time. Show price/limit upfront.

### Search & filters
- Search returns results as the user types after a small debounce.
- Empty results explain why and offer alternatives ("No results for 'foob' — did you mean 'food'?").
- Filters are reversible (clear button on each, "clear all").
- URL reflects filter state so it's shareable.

### Multi-step flows
- Show progress (step N of M).
- Allow going back without losing data.
- Show what's required vs optional.

### Internationalization
- Plan for plural rules per language (ICU MessageFormat).
- Dates, numbers, currencies follow user's locale, not the server's.
- Avoid string concatenation; use named placeholders.

## Patterns to follow

- **Optimistic UI** for actions with high success rate and cheap rollback (likes, sorts, edits in a list).
- **Pending state** for irreversible writes (payments) — show "saving...", then "saved · undo".
- **Skeleton screens** rather than spinners for content surfaces.
- **Confirm by typing the name** for very destructive actions ("type the project name to delete").

## Anti-patterns

- Spinners that spin forever.
- Errors with no recovery action.
- Modal-on-modal.
- Disabled buttons with no explanation.
- Forms that lose user input on error.
- "Save" buttons that don't say what's being saved.
- 4-second toast notifications with critical information.

## Quick self-check

- [ ] Every async action has a visible response within 100ms.
- [ ] Every error states the cause and the next action.
- [ ] Every destructive action is confirmable OR undoable (one of, not neither).
- [ ] Empty states explain and offer a primary action.
- [ ] Forms preserve input on validation failure.
- [ ] Multi-step flows show progress and allow back without data loss.

## References

- Don Norman — The Design of Everyday Things
- Nielsen Norman Group — usability heuristics, response time research
- Refactoring UI (Wathan, Schoger)
- Stripe Docs / Linear / Notion for state design references
