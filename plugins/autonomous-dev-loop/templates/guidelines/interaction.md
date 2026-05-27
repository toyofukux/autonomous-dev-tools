# Interaction guideline

> Keyboard, touch, focus, motion. The mechanics of how users move through the app.

## Non-negotiables

### Keyboard
- **Every interactive element is keyboard-reachable.** Tab moves through, Shift+Tab reverses.
- **Tab order matches reading order.** Don't reshuffle with `tabIndex`.
- **`tabIndex="-1"`** to remove from tab order when programmatically focused (modals, popovers).
- **Never use `tabIndex` > 0** — it breaks the document order for everyone.
- **Enter / Space activate buttons.** Enter submits forms. Esc closes dialogs and popovers.
- **Arrow keys** within composite widgets (menus, tabs, lists). Match the platform pattern.
- **Skip links** ("Skip to main content") for keyboard users on heavy pages.

### Focus
- **Visible focus ring** on every focusable element. Don't suppress with `outline: none` without a replacement.
- **Focus the right thing** on route change (main heading or main landmark).
- **Focus trapped** inside modal dialogs until closed.
- **Focus restored** to the trigger after a modal closes.
- **Don't steal focus** for non-modal updates.

### Touch
- **Touch targets ≥ 44×44 px** (iOS HIG) or 48×48 px (Material).
- **Spacing between targets ≥ 8 px** to prevent mistaps.
- **Touch feedback** within 100ms (highlight, ripple, or scale).
- **Hover-only affordances** are forbidden on touch. Either show always or behind a visible trigger.
- **Tap delay** removed (`touch-action: manipulation` or modern viewport meta).

### Pointer / hover
- **Hover reveals supplementary info**, never required for task completion.
- **Tooltips** appear after a short delay (300–500ms); dismiss instantly on leave/Esc.

### Gestures
- **Standard gestures only** unless there's a compelling reason. Swipe-back, pinch-zoom, scroll.
- **Discoverable.** Hidden gestures get an onboarding hint.
- **Reversible.** Every gesture has a button equivalent.

### Drag and drop
- **Keyboard alternative required.** dnd-kit and ProseMirror-style libraries provide this.
- **Visible drop zones** during drag.
- **Cancellable** with Esc.

### Scrolling
- **Don't hijack scroll.** No "scroll-jacking" of the OS scroll behavior.
- **Sticky elements** (headers, action bars) are sparing; they reduce visible content area.
- **Infinite scroll** has a "Load more" alternative for keyboard users and accessibility.
- **Save scroll position** on back navigation.

### Animation & motion
- **Respect `prefers-reduced-motion`.** Disable non-essential animations.
- **Purposeful motion only.** Animations communicate state (open/close, success, drag).
- **Duration**: 100–150ms for UI feedback, 200–300ms for transitions, never > 500ms unless artistic intent.
- **Easing**: enter decelerate, exit accelerate, move standard.
- **No autoplay** of audio/video without explicit user trigger.

### Form interactions
- **Submit on Enter** within single-field forms (search, login). Multi-field forms require explicit submit.
- **Validate on blur**, not per keystroke (reduces anxiety; matches mental model of "finishing a field").
- **Show success** after submit, not just absence of error.
- **Autofocus** the first field on a single-purpose page (login, search). Not on pages with hero content.
- **Persistent labels** above or beside the input. Float-label is OK only when accessibility is verified.

### Selection
- **Click to select** in lists; modifier keys for multi-select match platform (Cmd/Ctrl, Shift).
- **Right-click context menus** appear at the click position, not the screen edge.
- **Double-click** opens; single-click selects. Match platform expectations.

### Loading & blocking
- **Block input** during a destructive in-flight action (don't let user click "Delete" twice).
- **Don't block** during cheap UI work (debounce instead).
- **Cancellable** for long operations.

## Patterns to follow

- **Optimistic updates** for high-success cheap actions, with subtle visual cue.
- **Two-finger swipe** = back (when natural to the platform).
- **Long-press** = reveal contextual actions on touch (requires visual hint).

## Anti-patterns

- Custom focus ring suppression with no replacement.
- Drag without keyboard alternative.
- Hover-only menus on touch.
- Tooltips on touch (they don't trigger; the info gets lost).
- `tabIndex="3"` reshuffles.
- Disabled buttons that don't explain.

## Quick self-check

- [ ] Tab through the whole page; every interactive element reachable in document order.
- [ ] Visible focus on every element.
- [ ] Enter / Space / Esc / arrows work where expected.
- [ ] Touch targets ≥ 44px; ≥ 8px spacing.
- [ ] Hover is never the only path to an action.
- [ ] Drag has a keyboard alternative.
- [ ] Motion respects `prefers-reduced-motion`.
- [ ] No scroll hijacking.

## References

- WAI-ARIA Authoring Practices Guide (APG)
- Inclusive Components (Heydon Pickering)
- Apple HIG — Gestures
- Material Design — Motion
- Smart Interface Design Patterns (Vitaly Friedman)
