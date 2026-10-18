# review-impact-consumer — skill-compact1

- Date: 2026-10-18
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
- Bash: `cat src/invoice.py; ls src tests; cat src/catalog.py 2>/dev/null; grep -rn "pricing\|CURRENCY\|invoice" src tests | grep -v "^src/pricing.py"; cd src && python3`
- Bash: `cd src && python3 -c "
import invoice
invoice.invoice_line('x', 3)" 2>&1 | tail -2`
- Bash: `python3 -c "
import invoice
invoice.invoice_line('x', 3)" 2>&1 | tail -2`

## Final response (truncated)

```
Diff: 6 changed lines — 2 actionable findings.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: as supplied (suite green, 1 test passing). I could not confirm this independently. The suite only covers `price()` directly, and it never imports `invoice`.
Merge readiness: not ready — `invoice_line` still calls `price()` with the old signature and raises `TypeError`.

Verdicts
- Spec compliance: FAIL — the design says "every caller passes the currency it displays", and the one caller, `invoice.py`, was not updated.
- Code quality: FAIL — no test covers the caller, so a green suite hides the break.
- Security: PASS — no security findings
- Security pass: inline fallback

Findings
1. Blocking — src/invoice.py:5 — `invoice_line("x", 3)` calls `price(amount)` with no currency and raises `TypeError: price() missing 1 required positional argument: 'currency'`. I reproduced this. Fix: pass the currency the invoice displays. Either add a `currency` parameter to `invoice_line` and forward it, or pass `CURRENCY` explicitly. The design doesn't say which currency an invoice displays, so the author must decide.
2. Should-fix — tests/ (no `invoice_line` test) — nothing fails when a caller of `price()` breaks, which is how this change got through with a green suite. Fix: add a test that `invoice_line` returns `"<item>: <amount> <currency>"` for the chosen currency.

Pre-existing
- src/pricing.py:1 and src/catalog.py:1,5 — `CURRENCY = "USD"` stays as a module-level default. `currency_label()` still reports "Prices in USD", independent of whatever currency callers now pass to `price()`. This is not a `price()` caller, so the design doesn't cover it. Track it in case labels and prices can diverge.

Nits
- None

Declined to judge
- Which currency `invoice_line` should use, and whether `currency_label()` should follow it. The design is silent, so I can't tell the intent. Any test for finding 2 should assert only that the currency passed in appears in the output.
```

## Rationalizations observed (manual notes)

- Unchecked difference: bench1 ends with "Impact check (public interface change): I searched for callers of `price(`. There are three …"; compact1 finds the same broken consumer (`src/invoice.py:5`, Blocking) but prints no consumer list. The impact-check rule (inventory R16) is verbatim. May weaken adherence to a verbatim rule; reported to the user; accepted as variance with the rule text unchanged (2026-10-18).
