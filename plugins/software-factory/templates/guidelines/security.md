# Security guideline

> The floor, not the ceiling. Every change must pass these. Higher bars belong in product-specific docs.

## When this applies

Every code change. The validator checks these and severity-tags violations as Critical.

## Non-negotiables

### Authentication & authorization
- Every protected endpoint verifies the caller's identity at the boundary, not deep in the call stack.
- Authorization is **deny by default**. New endpoints/queries require an explicit auth check; missing one is a Critical defect.
- Use roles or scopes from the framework's auth layer; do not hand-roll permission checks per route.
- Re-verify ownership on every mutation: "does this user own this resource?" — even after auth.

### Tenant isolation (multi-tenant systems)
- Every query that touches tenant data includes `tenant_id` (or equivalent) in the WHERE clause. There are no exceptions for "internal-only" code.
- Add this as a query-builder constraint or repository wrapper so it's hard to bypass.
- The validator searches for queries against tenant tables without a tenant filter. If you find a legitimate exception (cross-tenant admin tool), document it in the function's docstring with the words "CROSS-TENANT INTENTIONAL".

### Secrets handling
- Secrets come from environment / secret manager only. Never from source, never from request bodies.
- **Never log**: API keys, tokens, passwords, payment payloads, request/response bodies that may contain PII.
- Use the project's redaction helper at the logger boundary. If there is no redactor, write one before logging any structured payload.
- `.env`, `*.key`, `*.pem`, `secrets.*` are blocked by the pre-commit hook. Don't try to bypass.

### Input validation
- Validate at every boundary: HTTP request, queue message, file upload, webhook payload, CLI arg.
- Use the project's schema validator (Zod, Pydantic, etc.). Reject early; do not coerce silently.
- Validate length, type, charset, and **range** — not just shape.
- Reject unknown fields by default (strict mode). Permissive parsing leaks intent.

### Output / error handling
- Never expose raw stack traces or DB errors to clients. Wrap in a typed error response with a stable code.
- Log the full error server-side with request ID for correlation.
- 5xx errors must page only on patterns, not single events (see observability guideline).

### Dependencies
- Audit new dependencies before adding (`npm audit` / `pip-audit` / `cargo audit`).
- Pin versions; don't accept `^` for security-critical packages (auth, crypto, payments).
- Remove unused dependencies in the same PR they become unused.

### Crypto
- Never roll your own. Use the platform's primitives (Node `crypto`, Python `cryptography`, Go `crypto`).
- For passwords: bcrypt / argon2 only. Cost factor tuned for ~100ms.
- For sessions: secure, httpOnly, sameSite=lax cookies; short-lived access + refresh tokens.
- Never compare secrets with `==`; use constant-time compare.

### File uploads
- Validate MIME type AND magic bytes; don't trust extensions or `Content-Type` alone.
- Store outside the web root; serve through a signed URL or an authorizing proxy.
- Cap size at the proxy/load balancer; don't rely on app-layer checks alone.

### CSRF / CORS
- State-changing endpoints require either same-site cookies + SameSite enforcement, or CSRF token, or both for legacy compatibility.
- CORS allowlist is explicit; never `*` for credentialed requests.

### SQL injection / NoSQL injection
- Use parameterized queries / prepared statements / ORM with bind variables. **Never** string-concat user input into queries.
- Where dynamic table/column names are needed, validate against an allowlist.

### XSS
- Use the framework's auto-escaping for templated output.
- For `dangerouslySetInnerHTML` (or equivalent), sanitize with DOMPurify or equivalent and document why raw HTML is necessary.
- Content Security Policy header configured to disallow inline scripts (`'unsafe-inline'`) and require nonces.

### Rate limiting & abuse
- All public endpoints have a rate limit. Default: per-IP and per-account.
- Authentication endpoints have an additional lockout/exponential backoff after N failed attempts.

## Patterns to follow

- **Defense in depth**: an auth check at the route AND at the service AND at the query layer. Three flat tires is more than one.
- **Fail closed**: when an auth/policy check errors, deny access; do not fall through to "allow".
- **Audit log for mutations on sensitive data** (PII, billing, permissions). Include actor, target, timestamp, before/after summary.

## Anti-patterns (Critical findings)

- Plaintext passwords or tokens anywhere (DB, logs, env files committed).
- A query against a tenant table with no tenant scoping.
- An endpoint that mutates state without an auth check.
- Logging request bodies that may contain PII or secrets.
- `eval`, `Function()`, `exec`, shell-out with unsanitized input.
- Disabled TLS verification (`rejectUnauthorized: false`) outside dev-only paths clearly marked.

## Quick self-check before opening a PR

- [ ] Every new endpoint has an auth check at the boundary.
- [ ] Every new query against tenant data includes tenant scoping.
- [ ] No new logger statements include raw request/response bodies.
- [ ] All user input goes through a schema validator before reaching business logic.
- [ ] New dependencies are pinned and audited.
- [ ] If touching crypto, use platform primitives.

## References

- OWASP Top 10 (current edition) — https://owasp.org/Top10/
- OWASP Cheat Sheet Series — authentication, session management, input validation, CSRF, XSS
- Google's Web Security Fundamentals
- Stripe's API & infrastructure security writeups
