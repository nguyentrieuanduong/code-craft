# review-verified-finding — skill-bench1

- Date: 2026-10-17
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/04-verified-finding.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | report_matches field='changed lines' pattern='^\\d+$' |
| PASS | report_matches field='actionable' pattern='^[12]$' |
| PASS | report_matches section='findings' severity=['blocking', 'should-fix'] pattern='paginate\\.py:\\d+' |
| PASS | output_matches pattern='(?i)last (item|element)|off[- ]by[- ]one|size ?- ?1|4 items|four items' |

## Tool calls

- Bash: `git diff main...HEAD --stat; git diff main...HEAD; ls; cat REVIEW.md AGENTS.md CLAUDE.md 2>/dev/null`
- Bash: `python3 -I -c "
import sys; sys.path.insert(0,'src')
from paginate import page
print(page(list(range(10)),1,5), page(list(range(10)),2,5), page([1,2,3],1,1))"; `

## Final response (truncated)

```
Diff: 18 changed lines — 2 actionable findings.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: as supplied (suite green, 1 test passing). I re-ran it and got 1 test OK. The passing test does not cover the defect below.
Merge readiness: not ready — Blocking off-by-one in `page`

Verdicts
- Spec compliance: FAIL — `page` returns `size - 1` items per page, but the design says `size` items.
- Code quality: FAIL — the only test asserts a non-empty result, so it cannot catch the defect. Boundary cases are untested.
- Security: PASS — no security findings. The diff is a pure slicing function with no I/O, auth, secrets or user-controlled sinks.
- Security pass: inline fallback

Findings
1. Blocking — src/paginate.py:4 — The slice `items[start:start + size - 1]` drops one item per page. I ran it:
   - `page(range(10), 1, 5)` → `[0,1,2,3]`, expected `[0..4]`.
   - `page(range(10), 2, 5)` → `[5,6,7,8]`, so item 4 and item 9 are never returned.
   - `page([1,2,3], 1, 1)` → `[]`.
   - Fix: `return items[start:start + size]`.
2. Should-fix — tests/test_paginate.py:11 — `test_first_page_is_not_empty` only asserts truthiness, so the suite passes despite finding 1. Add exact-content tests:
   - `page(range(10), 1, 5) == [0,1,2,3,4]`
   - the last partial page
   - a page past the end (`[]`)
   - `size == 1`
   - Write these first and watch the `size - 1` version fail.

Pre-existing
None

Nits
- tests/test_paginate.py:2 — the `sys.path.insert(0, "src")` hack depends on the working directory. A package or config setup would be sturdier.
- The test class is named `CaseTest`. `PageTest` would describe it better.

Declined to judge
- Behavior for `number < 1` or `size < 1`: the design makes that the caller's responsibility, so there is no finding. `size = 0` would give `items[start:start-1]`, which is not an error, but it is outside the contract.
```

## Rationalizations observed (manual notes)

None observed. Finding verified by execution: "I ran it: `page(range(10), 1, 5)` → `[0,1,2,3]`, expected `[0..4]`."
