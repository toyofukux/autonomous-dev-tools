# API guideline

> APIs are contracts. Once shipped, every caller depends on them. Design like you'll regret the choice.

## Non-negotiables

### Versioning
- **URL versioning** (`/v1/...`) or **header versioning**, but pick one and use it everywhere.
- Breaking changes require a new version. Definitions of "breaking":
  - Removing a field
  - Renaming a field
  - Changing a field's type or semantics
  - Adding a required input
  - Changing default behavior
- Non-breaking (safe within a version):
  - Adding new endpoints
  - Adding new optional fields to requests
  - Adding new fields to responses (callers must tolerate unknown fields)

### Resource naming
- Plural nouns, kebab-case: `/v1/invoices`, `/v1/payment-methods`.
- Hierarchy reflects ownership: `/v1/invoices/{id}/payments`.
- Verbs only as RPC-style actions on a resource: `POST /v1/invoices/{id}/send-reminder`. Don't overuse.

### HTTP methods
- `GET` — safe, idempotent, no side effects. Cacheable.
- `POST` — create, or non-idempotent action. Side effects.
- `PUT` — full replace. Idempotent.
- `PATCH` — partial update. JSON Merge Patch or JSON Patch; document which.
- `DELETE` — idempotent (deleting twice yields the same final state).

### Status codes
- `200 OK` — success with response body.
- `201 Created` — success with `Location` header pointing to the new resource.
- `204 No Content` — success with no body (DELETE, idempotent updates).
- `400 Bad Request` — malformed request (parse/schema error).
- `401 Unauthorized` — no/invalid credentials.
- `403 Forbidden` — authenticated but not allowed.
- `404 Not Found` — resource doesn't exist OR caller has no permission to know (avoid information leak).
- `409 Conflict` — state conflict (duplicate, version mismatch).
- `422 Unprocessable Entity` — semantically invalid input (validation failed).
- `429 Too Many Requests` — rate limited; include `Retry-After`.
- `500 Internal Server Error` — server bug.
- `503 Service Unavailable` — overloaded/maintenance; include `Retry-After`.

### Error envelope
- Stable shape for all error responses. Example:
  ```json
  {
    "error": {
      "code": "coupon_expired",
      "message": "This coupon is no longer valid.",
      "request_id": "req_abc123",
      "details": [{ "field": "coupon", "issue": "expired_at_2026-04-01" }]
    }
  }
  ```
- `code` is a stable enum; clients switch on it. `message` is human-readable; not for switching.
- Never leak stack traces, SQL, internal paths.

### Pagination
- Cursor-based for large or frequently-updated collections. `?cursor=xxx&limit=50`.
- Response includes `next_cursor` and `has_more`.
- Default page size cap (e.g., 50). Maximum cap (e.g., 200). Reject beyond max.

### Filtering, sorting
- `?filter[status]=active&filter[tenant_id]=acme`
- `?sort=-created_at,name`
- Document allowed fields; reject unknown filter/sort keys.

### Idempotency
- All mutating endpoints that can have client retry pressure accept an `Idempotency-Key` header.
- Server stores the key+result for ≥ 24h; re-requests within the window return the original result.
- Document this per endpoint.

### Authentication
- Bearer tokens in `Authorization: Bearer <token>`.
- Tokens scoped (`read:invoices`, `write:invoices`). No god tokens.
- Token rotation supported; document the rotation procedure for clients.

### Rate limiting
- `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` headers.
- `429` with `Retry-After` when exceeded.
- Limits documented per endpoint; per-account and per-IP both enforced.

### Content negotiation
- `Accept: application/json` (default). `Content-Type: application/json` for requests with bodies.
- UTF-8 throughout.

## Schema discipline

- Validate strictly. Unknown fields rejected by default.
- Use ISO 8601 for dates/times (`"2026-05-27T14:00:00Z"`). Always UTC.
- Use decimal strings for money (`"10.00"`), never floats.
- Booleans are `true`/`false`. Don't reuse strings (`"yes"`, `"1"`).
- Use enums (string) where possible; document allowed values.

## Patterns to follow

- **Expand pattern** for related resources: `?expand=customer,payment_method`.
- **Sparse fieldsets**: `?fields=id,name` to reduce payload.
- **Webhooks** for events: signed, retried with backoff, ordered-or-not documented.
- **Long-running ops**: return `202 Accepted` with `Location` pointing to a status resource.

## Anti-patterns

- Returning `200` with `{"error": "..."}` in the body. Use proper status codes.
- Sending arbitrary `X-*` debug fields in responses. Logging is for that.
- `GET` with side effects.
- Authentication via query string (`?token=...`); use headers.

## OpenAPI / contract first

- Maintain an OpenAPI (Swagger) spec or equivalent. Generate clients from it.
- Schema validation enforced server-side (don't trust the contract; verify).

## Quick self-check

- [ ] Resource paths plural kebab-case.
- [ ] Methods used correctly (GET safe, idempotent operations idempotent).
- [ ] Status codes follow the table above.
- [ ] All errors use the stable envelope; include `request_id`.
- [ ] Mutating endpoints accept `Idempotency-Key`.
- [ ] Pagination is cursor-based on large collections.
- [ ] Schema validation strict; unknown fields rejected.
- [ ] Auth via Authorization header; scoped tokens.

## References

- Stripe API Reference (still the gold standard)
- Microsoft REST API Guidelines
- Google API Design Guide
- RFC 7807 (Problem Details for HTTP APIs)
- RFC 6749 (OAuth 2.0)
