# review-impact-consumer — skill-bench1

- Date: 2026-10-17
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/09-impact-consumer.md

## Checks

| Result | Check |
|---|---|
| PASS | report_matches section='findings' severity=['blocking', 'should-fix'] pattern='invoice\\.py' |
| PASS | report_not_matches section='findings' pattern='^\\W*(blocking|should-fix|nit)?\\W*(src/)?catalog\\.py' |

## Tool calls

- Bash: `git diff main...HEAD --stat; git diff main...HEAD; ls; cat REVIEW.md AGENTS.md CLAUDE.md 2>/dev/null`
- Grep: ``
- Bash: `cat src/invoice.py; ls src tests; grep -rn "invoice\|CURRENCY" src tests; python3 -m unittest discover -s tests 2>&1 | tail -5; PYTHONPATH=src python3 -c "impor`
- Bash: `PYTHONPATH=src python3 -c "import invoice; print(invoice.invoice_line('x', 3))" 2>&1 | tail -2`

## Final response (truncated)

```
Diff: 6 changed lines — 1 actionable finding.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: as supplied (suite green, 1 test). I reran it: 1 test, OK. The suite has no test for `invoice.py`, so it can't catch the finding below.
Merge readiness: not ready — `invoice_line` is broken by the signature change.

Verdicts
- Spec compliance: FAIL — the design says every caller passes the currency it displays, but `invoice.py` still calls `price(amount)`.
- Code quality: FAIL — the signature change was made without updating its consumer, and no test covers `invoice_line`. The one changed test is fine.
- Security: PASS — no security findings. The diff only changes string formatting, with no I/O, auth, or input handling.
- Security pass: inline fallback

Findings
1. Blocking — src/invoice.py:5 — `invoice_line("x", 3)` raises `TypeError: price() missing 1 required positional argument: 'currency'` (reproduced). Fix: give `invoice_line` a `currency` parameter and pass it through to `price(amount, currency)`. If invoices are always USD, pass `CURRENCY` explicitly instead. The design asks for each caller to pass the currency it displays, so ask the author which one is intended. Add a test for `invoice_line`.

Pre-existing
- src/pricing.py:1 — the `CURRENCY = "USD"` global is now unused by `price`. `src/catalog.py:5` still uses it for its "Prices in {CURRENCY}" header, so a caller can display one currency in the header and pass a different one to `price`. This predates the diff and isn't a defect on its own.

Nits
None

Declined to judge
- Whether `invoice_line` should take the currency as a parameter or use the `CURRENCY` constant. The design doesn't say which, so the author needs to decide.

Impact check (public interface change): I searched for callers of `price(`. There are three: `src/invoice.py:5` (not updated, Finding 1), `tests/test_pricing.py:10` (updated), and the definition itself. `src/catalog.py` imports only `CURRENCY`, so it is unaffected.
```

## Rationalizations observed (manual notes)

None observed. Impact check named all callers: "There are three: `src/invoice.py:5` (not updated, Finding 1), `tests/test_pricing.py:10` (updated), and the definition itself."
