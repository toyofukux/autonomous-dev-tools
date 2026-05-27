# Code style guideline

> Boring is good. Code that reads like prose ages well; clever code ages badly.

## Non-negotiables

### Naming
- **Functions and variables in natural English.** No abbreviations except established ones (`url`, `id`, `db`).
- **Booleans start with `is`/`has`/`can`/`should`** (`isActive`, `hasPermission`).
- **Functions are verbs** (`applyCoupon`, `fetchUser`). Avoid `get` for non-trivial work; reserve for cheap accessors.
- **Variables are nouns** (`order`, `pendingPayments`).
- **Constants in UPPER_SNAKE_CASE** for genuine constants; otherwise camelCase.
- **Classes / types in PascalCase**.
- **Files**:
  - kebab-case is the safe default (works in URLs, case-insensitive filesystems).
  - PascalCase for files that export a single same-named component/class is acceptable per framework convention.
  - Match the project's existing convention; don't mix.
- **No reserved words** as identifiers: `delete`, `new`, `class`, `import`, `export`. Use `remove`, `create`, `kind`, etc.

### Comments
- **Default: no comments.** Well-named identifiers and small functions are self-documenting.
- Add a comment **only when WHY is non-obvious**: a hidden constraint, a workaround for a specific bug, a subtle invariant.
- **Never restate WHAT** the code does. The code already does that.
- **No `// added by X`, `// for ticket #Y`, `// TODO before deploy`** in production code. Those rot.
- **Docstrings** for public library APIs and complex algorithms. Brief; one short paragraph max.

### Function size
- **One screen, one function.** If you scroll, it's too long.
- **Single responsibility.** If you describe it with "and", split.
- **Early return over nested if.** Reduce indentation depth.

### Error handling
- **Don't catch and swallow.** Either handle (with logged context) or let it propagate.
- **Don't catch generic `Error`** unless you immediately re-throw a more specific one.
- **Errors are values, not exceptions, where the language supports it** (Result<T, E>, Either, Option).
- **Validate at boundaries** (input parsing, external APIs). Trust internal callers.

### Modules / imports
- **One concept per file.** Prefer many small files over one omnibus.
- **Imports grouped**: standard library, third-party, project (in that order).
- **No circular dependencies.** The repo has tooling (madge / dep-cruiser) — keep it green.
- **No layer violations.** Routes don't import DB modules directly; go through services.

### Types (typed languages)
- **No `any` / `unknown` without a comment explaining why.** `unknown` is preferred to `any`.
- **Discriminated unions** for state with variants. Avoid type fields without enforcement.
- **Branded types** for ID strings that should not be mixed (`UserId` vs `OrderId`).
- **Inference where it's clear; annotation where it's not.** Public function signatures are always annotated.

### Mutability
- **Prefer immutable data structures.** Functional updates over in-place mutation.
- **`const` by default**; `let` only when reassignment is needed.
- **Don't mutate function parameters.**
- **No global state.** Pass dependencies; use DI containers for cross-cutting (logger, db).

### Async
- **`async`/`await` over `.then`** for new code.
- **No floating promises.** Every async call is awaited or explicitly fire-and-forget with a comment.
- **Concurrent fan-out** uses `Promise.all` / `gather` / `errgroup`; sequential when ordering matters.

### Magic numbers / strings
- **Named constants** for any number that has meaning (`MAX_RETRIES = 3`, not `if (count < 3)`).
- **Enums or const objects** for finite string sets.

### Dead code
- **Delete it immediately.** If it's commented out, it's gone — version control remembers.
- **No `_unused` rename of variables.** Just delete.
- **No backward-compat shims for code that isn't shipped.**

### File size
- **A source file > 500 lines is a smell.** Investigate splitting.
- **A function > 80 lines is a smell.** Investigate splitting.

## Patterns to follow

- **Composition over inheritance.** Inheritance for genuine "is-a" only (rare).
- **Builder / factory** for objects with > 4 construction parameters.
- **Result / Either** for fallible operations in functional codebases.
- **Newtype / branded types** for IDs and units.

## Anti-patterns

- Using `delete` / `new` / reserved words as identifiers.
- A 500-line function.
- A try/catch that catches `Error`, logs "an error", and continues.
- A boolean parameter that flips behavior (`createUser(true)` — what does true mean? Pass an enum).
- Mutating shared state from multiple places.
- Comment that says "// don't change this".

## Quick self-check

- [ ] Names natural English, no reserved words, booleans prefixed.
- [ ] Functions are verbs, fit on a screen, single responsibility.
- [ ] No `any` (or commented why).
- [ ] No dead code, no commented-out blocks.
- [ ] No floating promises.
- [ ] Errors handled at the right layer; not swallowed.
- [ ] No magic numbers / strings.

## References

- Clean Code (Robert C. Martin) — naming, function size
- Refactoring (Martin Fowler) — code smells, when to extract
- Google Engineering Practices (eng-practices.googlesource.com)
- Effective Java / Effective TypeScript (Joshua Bloch / Dan Vanderkam)
- "The Wrong Abstraction" — Sandi Metz
