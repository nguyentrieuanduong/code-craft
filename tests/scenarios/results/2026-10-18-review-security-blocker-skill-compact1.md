# review-security-blocker — skill-compact1

- Date: 2026-10-18
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/10-security-blocker.md

## Checks

| Result | Check |
|---|---|
| PASS | report_matches field='security' pattern='^(blocking|fail)' |
| PASS | output_matches pattern='(?i)inject|parameteri|placeholder' |

## Tool calls

- Bash: `git diff main...HEAD --stat && git diff main...HEAD && ls -a && cat REVIEW.md AGENTS.md CLAUDE.md 2>/dev/null`
- Bash: `cat src/db.py; git log --oneline main..HEAD; python3 -m unittest discover -s tests 2>&1 | tail -5; python3 - <<'E'
import sys; sys.path.insert(0,"src")
from db `

## Final response (truncated)

```
Diff: 24 changed lines — 3 actionable findings.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: as supplied (1 test passing). I also re-ran it: 1 test, OK.
Merge readiness: not ready — SQL injection (Blocking), plus no negative-case tests.

Verdicts
- Spec compliance: FAIL. An exact-name match works for plain names. Names containing a quote raise `OperationalError`, and a crafted name returns another user's row.
- Code quality: FAIL. The only test is the happy path. No test fails if matching stops being exact or if the lookup breaks on hostile input.
- Security: BLOCKING. SQL injection in `src/users.py:6`.
- Security pass: inline fallback

Findings
1. Blocking — src/users.py:6 — `name` is interpolated into the SQL with an f-string. I ran `find_user(c, "x' OR '1'='1")` against a table holding only `ada`. It returned `('ada', 'ada@example.com')`, so a non-matching name returned a row. `find_user(c, "o'brien")` raised `sqlite3.OperationalError: near "brien": syntax error`. Both break "exact name match", and the first lets any caller read arbitrary rows, including via UNION on other tables. Fix: `connection.execute("SELECT name, email FROM users WHERE name = ?", (name,)).fetchone()`.
2. Should-fix — tests/test_users.py:11 — no negative-case tests: a missing user should return `None`, and a name with a quote should not raise or leak. Add a test for an injection payload (`"x' OR '1'='1"` → `None`) and one for `"o'brien"` stored and found. Both assert only what the design states. The payload test fails today.
3. Should-fix — tests/test_users.py:10 — the class is named `CaseTest`, which says nothing about what it covers. Rename it to `FindUserTest`.

Pre-existing
- src/db.py:6 — the `users.name` column has no index or uniqueness constraint. `fetchone()` therefore returns an arbitrary row when names are duplicated. The design is silent on this, so I'm not counting it.

Nits
- tests/test_users.py:6 — `sys.path.insert` is fragile. Configure the test path in the runner instead.

Declined to judge
- Behavior for duplicate names. The design says "the row", and that doesn't settle which row to return when several match.
- Case sensitivity. SQLite's `=` on TEXT is case-sensitive by default, which matches "exact". I'm noting it, not judging it.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
