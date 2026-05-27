# Performance guideline

> Performance is a feature. Treat it like one: design budgets, measure, regress-test.

## Non-negotiables

### Complexity budgets
- Every public function declares its complexity in comments when not obviously O(1) or O(N).
- No hidden O(N²) or worse in hot paths. The validator flags nested loops over user-scoped collections.
- Set explicit budgets for hot paths in the spec's Performance section.

### Database
- **No N+1 queries.** Use joins, batched fetches (DataLoader), or eager loading. The validator scans for query-in-loop patterns.
- Every query that returns more than 100 rows is paginated (cursor preferred over offset for large tables).
- Every query against a non-trivial table has an index that the planner uses. Confirm with EXPLAIN; don't assume.
- Adding indexes? Measure write-cost impact too. Document the trade-off in the spec.
- Long-running migrations use online schema changes (pt-osc, gh-ost, Postgres `CREATE INDEX CONCURRENTLY`).

### Payloads
- API response size budgets per endpoint. List endpoints paginate by default (page size ≤ 50).
- Trim response fields to what the caller needs. Avoid leaking internal-only fields.
- Compress responses > 1KB (gzip / brotli at the proxy).
- Image and asset budgets per page documented in `ui.md`.

### Caching
- Cache reads where the data tolerates the staleness. Document the staleness window.
- Cache invalidation is part of the design, not an afterthought. Pick one: TTL, event-driven, or versioned key.
- Cache keys include all dimensions the result depends on (tenant, user, locale, version). Missing a dimension causes data leaks across users.

### Concurrency
- I/O is async. CPU-bound work is offloaded to workers, not blocking the request loop.
- Connection pools sized to the database's limits, not the application's optimism.
- Background work has timeouts and retry caps.

### Front-end performance
- Initial JS bundle budget set per route (e.g., ≤ 200KB gzipped).
- Largest Contentful Paint < 2.5s on a 3G network simulation in CI.
- Defer non-critical scripts (`type=module`, `defer`, dynamic import).
- Image formats: AVIF/WebP with fallback; responsive sizes via `srcset`.

### Memory & resources
- Streaming over buffering for large I/O.
- Bounded queues, not unbounded. Drop or backpressure when full.
- Connection cleanup in `finally` blocks (or context managers / `using`).

## Patterns to follow

- **Measure before optimizing.** Profile the actual hot path; don't guess.
- **Budget per feature.** Every spec's Performance section declares p50/p95 latency, payload size, and growth assumptions.
- **Regression tests.** Critical paths have a synthetic latency / throughput test that runs in CI.

## Anti-patterns

- Loading entire tables into memory to filter in code.
- `SELECT *` then projecting in the application layer.
- A retry loop with no max attempts or no exponential backoff.
- A cache with no eviction or no max size.
- Polling at < 1s intervals when push is available.

## Quick self-check

- [ ] No nested loops over user-controlled collections without explicit complexity comment.
- [ ] No N+1 (use joins / batch / DataLoader).
- [ ] All list endpoints paginate.
- [ ] New tables have indexes for every query pattern; trade-off noted.
- [ ] Hot path has p50/p95 numbers in the spec.
- [ ] Bundle / payload budget honored.

## References

- Brendan Gregg's USE Method
- Use The Index, Luke (https://use-the-index-luke.com/)
- Google Web Vitals
- The Twelve-Factor App (concurrency, processes)
- Designing Data-Intensive Applications (Kleppmann)
