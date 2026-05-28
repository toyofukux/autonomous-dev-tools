# Database guideline

> The schema outlives the code. Design it deliberately; change it carefully.

## Non-negotiables

### Schema design
- **Tenant ID column** on every tenant-scoped table. Indexed. Enforced in repository layer.
- **Soft deletes** (`deleted_at`) for user-facing entities; hard deletes only for genuinely transient data.
- **Created/updated timestamps** on every table (UTC).
- **Foreign keys with explicit ON DELETE / ON UPDATE behavior** (`CASCADE`, `RESTRICT`, `SET NULL` — pick deliberately).
- **NOT NULL by default.** Nullable is opt-in, with a documented meaning ("absent" vs "explicitly null").
- **Money as integer cents** (or DECIMAL), never FLOAT.
- **UUIDs** for public-facing IDs; sequential IDs for internal joins are fine and faster.

### Indexes
- Every FK column has an index.
- Every column used in `WHERE` (or `JOIN` predicates) on tables > 10k rows has an index — confirmed via EXPLAIN.
- Composite indexes match query patterns. Order matters: most selective first.
- **No over-indexing.** Each index costs write throughput. Drop unused (check pg_stat_user_indexes).

### Migrations
- **Backward-compatible by default.** Old code must work against the new schema during deployment.
- Two-step destructive changes:
  - Step 1 (this release): add new column, dual-write.
  - Step 2 (next release): switch reads, then drop old column.
- **Never** in one migration: rename a column AND change a constraint AND backfill. Split.
- Long-running migrations use online tools (Postgres `CREATE INDEX CONCURRENTLY`, gh-ost, pt-osc).
- Migrations are reviewed for **lock impact**. `ALTER TABLE` can take an exclusive lock; check pg_locks docs for your version.
- Every migration has a documented rollback. Test the rollback in staging.

### Transactions
- Use them where invariants span multiple writes.
- Keep transactions short. No external I/O inside a transaction (no HTTP calls, no S3 puts).
- Set explicit isolation level when defaults are wrong (READ COMMITTED is Postgres default; SERIALIZABLE for invariants that span reads).

### Concurrency
- Optimistic locking via a `version` column for entities updated from multiple sources.
- Pessimistic `SELECT FOR UPDATE` for queue-like patterns; bounded.
- Idempotency keys at the API layer prevent duplicate inserts under client retries.

### Queries
- **No N+1.** Joins, batched fetches, or eager loading. The validator scans for queries-in-loops.
- **`SELECT *` is forbidden** in code. List columns explicitly.
- **No `LIKE '%term%'`** on large columns without a trigram index (Postgres) or full-text search.
- Window functions and CTEs are first-class; use them where they simplify intent.

### Constraints
- Push invariants down to the DB where possible: `CHECK`, `UNIQUE`, `NOT NULL`, FK.
- Application-layer enforcement supplements but does not replace DB constraints.

### Backups & restore
- Automated daily backups, tested monthly with a real restore drill.
- Point-in-time recovery for critical DBs.
- Backups encrypted at rest.

### Observability
- Slow query log on; review weekly.
- `pg_stat_statements` (or equivalent) for query mix analysis.
- Connection pool saturation alerts.

## Patterns to follow

- **Repository / DAO layer** owns SQL. Application code never builds raw SQL.
- **Read replicas** for analytics / reporting; primary for writes and critical reads.
- **Event sourcing** or **outbox pattern** for cross-service state propagation; don't write to a queue and a DB in the same transaction without a 2PC pattern.
- **Time-bucketed tables** or partitioning for high-volume time-series data.

## Anti-patterns

- Storing JSON blobs that should be normalized columns "for flexibility".
- Storing dates as strings.
- `enum` types added eagerly — they're harder to alter than a lookup table.
- `DELETE FROM big_table WHERE old` in one statement; chunk it.
- "Just one quick `UPDATE` in production".

## Quick self-check

- [ ] All new tables have tenant_id (if tenant-scoped), timestamps, NOT NULL defaults.
- [ ] All new columns used in WHERE/JOIN have indexes confirmed by EXPLAIN.
- [ ] All money columns are integer or DECIMAL.
- [ ] Migration is backward-compatible OR explicitly two-step.
- [ ] Migration rollback documented and tested.
- [ ] No `SELECT *`; no `LIKE '%x%'` on large columns without a real text-search index.
- [ ] DB constraints enforce invariants (UNIQUE, FK, CHECK).

## References

- Use The Index, Luke
- Postgres docs (especially "Performance Tips", "Concurrency Control", "MVCC")
- "Designing Data-Intensive Applications" — Kleppmann
- Strong's "Database Refactoring Patterns"
