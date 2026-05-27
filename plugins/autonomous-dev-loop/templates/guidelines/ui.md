# UI guideline

> Distinctive, accessible, predictable. In that order, when they conflict.

## Non-negotiables

### Accessibility (WCAG 2.2 AA floor)
- **Semantic HTML.** `<button>` for actions, `<a>` for navigation. Never `<div onClick>` for interactive elements.
- **Keyboard reachable.** Every interactive element is in tab order with visible focus.
- **Focus management.** Open a dialog → trap focus inside. Close → return to the trigger.
- **Color contrast.** 4.5:1 for body text, 3:1 for large text and UI components.
- **Labels.** Every form input has a programmatic label (not just placeholder).
- **Status announcements.** Dynamic content changes use `aria-live` regions.
- **Touch targets** ≥ 44×44 px on mobile.

### Component design
- **One responsibility per component.** If you can't describe it in one sentence, split.
- **Props are the contract.** Avoid `children` doing magical things; explicit slots when needed.
- **Controlled vs uncontrolled — pick one per component.** Document which.
- **No business logic in components.** Components render; logic lives in hooks or services.

### Design tokens
- **Colors, spacing, type, radii, shadows** come from a tokens layer. Never hardcode hex / px values in components.
- A new visual decision either uses an existing token or adds a new one to the tokens layer.

### Layout
- **Mobile-first.** Base styles target the smallest viewport; media queries scale up.
- **No fixed pixel widths** for main content areas. Use max-width with fluid behavior.
- **Whitespace is a feature.** Density is configurable per surface (compact for data tables, comfortable for forms).

### State
- Every UI state is named and intentional:
  - **Loading** (with skeleton or spinner; never blank)
  - **Empty** (with explanation and primary action)
  - **Error** (with cause and recovery action)
  - **Success** (with what changed and next step)
- The empty state matters as much as the loaded state. Design both.

### Forms
- Inline validation **after blur**, not after each keystroke (anti-anxiety).
- Errors are specific: "Email must be valid (e.g. name@example.com)", not "Invalid email".
- Submit button labels are verbs: "Save changes", not "Submit".
- Disabled buttons explain why on focus / hover.
- Autosave where the user would expect it; clearly indicated.

### Performance
- Initial JS budget per route (e.g., ≤ 200KB gzipped).
- Above-the-fold rendered without blocking on data when possible (skeleton, then fill).
- Images: AVIF/WebP with fallback; correct sizes via `srcset`; explicit `width`/`height` to avoid CLS.
- Defer non-critical scripts.

### Animation & motion
- Respect `prefers-reduced-motion`. Disable non-essential motion.
- Animation duration 100–250ms for UI feedback. Longer is rude.
- Easing matches semantic: enter (decelerate), exit (accelerate), move (standard).

## Patterns to follow

- **Compound components** for related groups (`<Menu>`, `<Menu.Item>`).
- **Headless UI primitives** (Radix, Headless UI) for accessibility-correct behavior; style on top.
- **Container/presentational split** when shared rendering with different data sources.
- **Error boundaries** at route level; never let a render error crash the whole tree.

## Anti-patterns

- Custom dropdown / dialog from scratch when a vetted primitive exists. (Accessibility will be wrong.)
- Inline styles that bypass tokens.
- "Disabled" state with no explanation.
- Modal-on-modal UX.
- Spinners that spin forever; always set a timeout fallback.
- `dangerouslySetInnerHTML` without sanitization.

## Quick self-check

- [ ] Every interactive element is `<button>` / `<a>` / `<input>` etc.
- [ ] Tab order and focus visible.
- [ ] Color contrast meets AA.
- [ ] Loading / empty / error states designed.
- [ ] Tokens used for colors / spacing / type.
- [ ] Images sized; reduced-motion respected.
- [ ] No business logic in components.

## References

- WCAG 2.2 Quick Reference
- Inclusive Components (Heydon Pickering)
- Refactoring UI (Adam Wathan, Steve Schoger)
- Material Design 3 guidelines
- Apple Human Interface Guidelines
- Radix UI / Headless UI documentation
