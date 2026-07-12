---
name: releasing-safely
description: >-
  Use when rolling out any change to a shared or production environment —
  deploys, releases, feature flags, config changes, schema or data
  migrations. Don't use for local-only or test-environment changes.
---

# Releasing Safely

A release is an experiment on real users. Run it like one: smallest real
exposure first, evidence before expansion, rollback rehearsed before stage
one. Deploy and config mechanics — not exotic logic bugs — sank Knight
($440M in 45 minutes), CrowdStrike (~8.5M machines), Cloudflare, and
Facebook (docs/anti-patterns.md §10–11).

## Before the first stage (hard gate)

- **Rollback is rehearsed, not theoretical.** State the exact command that
  reverts THIS release and verify it exists before deploying anything. If
  the change cannot be rolled back (destructive migration), stop and
  restructure until it can.
- **Schema/data changes follow expand–contract.** Old and new code must both
  run against the schema at every step: add-new → migrate → switch →
  remove-old, each step released separately. Never a breaking migration in
  one step.
- **Smoke checks are named up front** — which command, which endpoints,
  which baseline the numbers are compared against.

## The ladder: canary → bake → promote

1. Deploy to the smallest real slice first (canary: one instance or ≤5%).
2. Verify with evidence: run the named smoke checks, compare error rates
   against baseline, report the numbers.
3. **Stop after the canary.** An instant-green smoke check is a snapshot,
   not a bake. Promotion to the next ring — and to the fleet — happens only
   after the canary has baked under real traffic AND the user gives an
   explicit go-ahead. Never expand exposure in the same action as the
   canary: report the canary evidence, state the rollback command, and ask.
4. Any regression at any stage: **roll back first, debug after.** The fleet
   is not a debugging environment.

## Config, flags, and data are code

A config, flag, or data change gets the same rigor as code: reviewed,
tested, and released down the same ladder. Feature flags get an owner and
an expiry date at creation; an expired or repurposed flag is a live bug —
one fired eight-year-dead code at Knight (docs/anti-patterns.md §10).

## Forbidden rationalizations

| Excuse | Reality |
|--------|---------|
| "Traffic is low, push it everywhere" | Low traffic shrinks the sample, not the blast radius. The canary costs minutes either way. |
| "QA signed off, it's safe" | QA validated the artifact, not production. Only the canary validates production. |
| "Canary smoke is green — promote now" | A snapshot is not a bake. Real traffic needs time to hit the paths that hurt; get the go-ahead first. |
| "Rollback is easy, we'll figure it out if needed" | Unrehearsed rollback fails exactly when needed — Knight's improvised revert spread the defect to all 8 servers. |
| "It's just a config/flag change" | Config took Facebook down for ~6h; a repurposed flag ended Knight in 45 minutes. Same ladder. |
