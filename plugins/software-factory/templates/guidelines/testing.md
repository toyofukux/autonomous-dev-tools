# Testing guideline

> Tests are the contract. They state what the code promises and stop you from breaking it.

## The three layers

| Layer | Purpose | Who writes |
|---|---|---|
| **Unit** | One function / one component, isolated. Fast, many. | builder (alongside impl) |
| **Integration** | Multiple components together; real DB / real fake-of-service. | builder, when interaction matters |
| **Acceptance** | End-to-end from the user's surface (HTTP, UI, CLI). Verifies the story's AC. | test-verifier |

Unit tests prove components are individually correct. Acceptance tests prove **the feature** is correct. Both are required.

## Non-negotiables

### Coverage
- **Every public function has a unit test.** Private helpers are tested through their public callers.
- **Every story AC has an acceptance test.** Test-verifier reports any AC without coverage.
- **Every failure-path AC has a test.** Happy-path-only is half a job.
- **Every bug fix lands with a regression test** that fails before the fix and passes after.

### Test quality
- Test names describe the **behavior**, not the function: `applyCoupon_rejectsExpiredCode` not `test_applyCoupon_1`.
- One assertion concept per test; multiple `expect` lines are OK if they verify the same behavior.
- AAA: Arrange, Act, Assert — visually separated.
- No conditionals (`if/for`) in tests. Each test exercises one path.
- No sleep / arbitrary timeouts. Use deterministic waits (test framework's `waitFor`, fake clock).

### Test isolation
- No shared mutable state between tests. Each test sets up and tears down.
- DB tests use transactions that roll back, or a fresh schema per test file.
- Network is stubbed in unit/integration. Real network only in dedicated e2e suites that run separately.
- File system writes go to a per-test temp dir.

### Determinism
- No `Math.random` in tests. Inject a seeded RNG.
- No `Date.now` in tests. Inject a clock; use a fake clock.
- No reliance on test execution order.

### Speed
- Unit suite < 30s for a small/medium repo. If it gets slower, profile and fix.
- Parallelize where the framework supports it.
- A test that takes > 1s is a smell; tag it `@slow` and move it out of the default suite.

### Mocking discipline
- **Mock at the boundary**, not deeply. Mock the HTTP client, not the function that uses it.
- **Don't mock what you own** when you can use the real thing cheaply (a real DB in transaction, a real in-process service).
- **Mocks return the format the real thing returns.** Use type-checked mocks where possible.
- **Don't mock value objects.** Constructing a real one is almost always simpler.

## Patterns to follow

- **Fixture builders / factories** for test data. One source of truth per entity.
- **Snapshot tests** for stable serialized output (API responses, rendered components). Update intentionally, not reflexively.
- **Property-based tests** for parsers, serializers, anything with a clean spec.
- **Golden master** for legacy code being refactored: record current output, refactor until output matches.

## Anti-patterns

- Tests that pass because they don't actually assert anything.
- Tests that mirror the implementation (testing internals); refactoring breaks them without behavior changing.
- `try { ... } catch { }` in tests to "make them pass".
- Mocking the function under test.
- Acceptance test that re-tests unit-level concerns.
- Mocking the database when the design requires a real one (the user explicitly forbade this in some projects — see [[feedback]] memories if you have them).

## CI rules

- All tests run on every PR.
- A failing test blocks merge. No `skip` without an issue link.
- Flaky tests are quarantined within 24 hours of first flake and fixed within a week.
- Coverage is **monitored** (don't drop) but not enforced at a hard percentage — coverage games incentivize bad tests.

## Quick self-check

- [ ] Every new function has a unit test.
- [ ] Every story AC has a passing acceptance test (or documented "uncoverable" reason).
- [ ] Every failure path has a test.
- [ ] No `sleep`, `Date.now`, `Math.random`, or unstubbed network in tests.
- [ ] Mocks at boundaries; real things in between where cheap.
- [ ] No flaky tests; if discovered, quarantine same day.

## References

- Working Effectively with Legacy Code (Feathers)
- xUnit Test Patterns (Meszaros)
- Google Testing Blog — "Test Sizes", "Hermetic tests"
- Martin Fowler — "Mocks Aren't Stubs", "Test Pyramid"
