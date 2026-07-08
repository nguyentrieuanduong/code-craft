---
name: security-baseline
description: >-
  Use whenever writing code that touches data, networking, auth, user input,
  configuration, or infrastructure, and before every commit.
---

# Security Baseline

These rules are **blocking constraints**, not advice. Code violating one does
not ship, does not get committed with a TODO, and does not wait for review to
be caught.

## The eight rules

**SEC-01 Encryption everywhere** — encryption at rest for all data stores;
TLS 1.2+ in transit. No plaintext transport, even "internal".

**SEC-02 Secrets never in code** — environment variables or a secret manager
only. No keys, tokens, passwords, or connection strings in source, config
files under version control, or logs. `.env*` files gitignored.

**SEC-03 Structured, safe logging** — timestamp, level, correlation ID,
message. NEVER log secrets, tokens, passwords, or PII. Access logging enabled
at load balancers / gateways.

**SEC-04 HTTP security headers** — CSP (strict, no `unsafe-inline` as a
starting point), HSTS, `X-Content-Type-Options: nosniff`,
`X-Frame-Options: DENY`, Referrer-Policy.

**SEC-05 Input validation at every boundary** — validate type, length, format;
whitelist, not blacklist; schema validators (Zod, pydantic) at the edge. File
uploads: size + MIME + extension checks. SQL: parameterized queries only —
string concatenation into a query is an automatic stop.

**SEC-06 Least-privilege access** — IAM without wildcards; specific resources
and actions; scoped conditions. Applies to service accounts, DB users, and
API scopes alike.

**SEC-07 Deny-by-default networking** — no `0.0.0.0/0` ingress except load
balancer 80/443; private endpoints for cloud services; explicit allow lists.

**SEC-08 Server-side authorization** — deny by default; role checks on the
server, never only the client; IDOR prevention (verify the requester owns the
resource); restricted CORS; JWT signature + expiry validation. Auth tokens in
httpOnly cookies, not localStorage. CSRF tokens on state-changing requests.

## Pre-commit security checklist

- [ ] `grep` the diff for key-like strings (`sk-`, `api_key`, `password`,
      `secret`, `token=`, private key headers)
- [ ] No debug prints / console.log left in
- [ ] Every new input path has validation at the boundary
- [ ] Every new query is parameterized
- [ ] Every new endpoint checks authorization server-side
- [ ] No new dependency added without stating why (supply-chain surface)

## Forbidden rationalizations

| Excuse | Reality |
|--------|---------|
| "It's an internal tool, auth can wait" | Internal tools leak. Every breach post-mortem contains this sentence. |
| "I'll rotate the hardcoded key later" | Committed secrets live in git history forever. Never commit one. |
| "This input comes from our own frontend" | Attackers do not use your frontend. Validate server-side. |
| "Wildcard permissions unblock me now" | Scoping later never happens. Scope now. |
