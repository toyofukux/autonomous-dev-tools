# Observability guideline

> If it isn't observable, it isn't debuggable. If it isn't debuggable, on-call pays for it at 3am.

## The three signals

- **Logs** — discrete events with structured context. Use for postmortem investigation.
- **Metrics** — numeric time-series. Use for dashboards, alerts, capacity planning.
- **Traces** — request spans across services. Use to understand cross-service latency and dependency paths.

Every change should ask: does the new behavior need representation in any of these?

## Non-negotiables

### Logs
- **Structured.** JSON or your framework's structured format. Never `printf` style for production logs.
- **Levels used consistently**: ERROR (user-impacting, page-worthy), WARN (degraded or recoverable), INFO (state transitions, user actions worth a trail), DEBUG (developer-only, off in prod).
- **Correlation IDs**: every log line includes the request ID (and trace ID if traced). Generated at the edge, propagated end-to-end.
- **Never log secrets, PII, payment payloads, full request bodies.** Use the redactor (see [[security]]).
- **Context, not just message**: include user/tenant ID, resource ID, operation name. `"checkout failed"` is useless; `"checkout failed | userId=42 | tenantId=acme | orderId=O-991 | reason=card_declined"` is debuggable.

### Metrics
- **RED for services**: Rate, Errors, Duration. Per endpoint.
- **USE for resources**: Utilization, Saturation, Errors. Per CPU, memory, disk, queue.
- **Business KPIs** as metrics where relevant (checkouts/min, signups/hour) — not just technical.
- **Labels are bounded.** Avoid high-cardinality labels (user ID, request ID). Cardinality explosion is the #1 metrics cost driver.

### Traces
- Every external call (DB, cache, queue, HTTP) creates a span.
- Span name = operation; attributes = parameters worth filtering on. Don't put bodies in spans.
- Trace sampling: 100% on errors, low % on success in high-volume systems.

### Alerts
- **Alert on symptoms users feel** (latency, error rate, availability), not causes (CPU, memory).
- **Every alert is actionable.** If on-call wakes up and there's nothing to do, the alert is wrong.
- **Run-book linked** in every alert. The link points to a doc that says "if you see this, do X".
- **Burn rate alerts** for SLOs (not single-threshold-on-error-rate).

### Dashboards
- One dashboard per service / per critical user journey.
- Top of dashboard: SLO compliance, error budget remaining.
- Then: RED metrics. Then: USE for backing resources. Then: business KPIs.

## "Logs for self-improvement"

Every spec's Backend section has a `### Logs for self-improvement` field. The intent: log events with enough structure that **future AI analysis** can mine them for quality issues — what failed, why, for whom, under what conditions.

Concrete pattern:

```json
{
  "event": "checkout.coupon.applied",
  "user_id": "U-42",
  "tenant_id": "acme",
  "coupon_id": "SAVE10",
  "outcome": "success",
  "discount_amount": 10.00,
  "ts": "2026-05-27T14:00:00Z",
  "request_id": "...",
  "trace_id": "..."
}
```

Outcomes are enums (`success`, `expired`, `not_applicable`, `duplicate`, `system_error`). This makes retrospective queries trivial.

## Patterns to follow

- **Log once at the boundary**, not at every layer. Excessive logging is its own outage.
- **Stable event names** (`checkout.coupon.applied`) for queryable trails. Don't change them lightly; once dashboards depend on them, renames break things.
- **Sampling** rather than dropping in high-volume systems.

## Anti-patterns

- `console.log` left in production code.
- Logging an error AND throwing it (creates duplicate entries; choose one).
- Catching an exception, logging "an error occurred", and continuing as if normal.
- Alerts that fire daily and are ignored daily (alert fatigue).
- High-cardinality labels in Prometheus / Datadog metrics.

## Quick self-check

- [ ] All new errors logged with structured context (user, tenant, resource).
- [ ] All new external calls have spans.
- [ ] All new endpoints contribute to RED metrics.
- [ ] Business-meaningful outcomes have a stable event name.
- [ ] No secrets / PII in any new log line.
- [ ] If a new alert is added: it's symptom-based, actionable, run-book linked.

## References

- Google SRE Book (chapters: Monitoring Distributed Systems, Practical Alerting)
- OpenTelemetry docs
- Charity Majors / Honeycomb on observability vs monitoring
- The RED method (Tom Wilkie), The USE method (Brendan Gregg)
