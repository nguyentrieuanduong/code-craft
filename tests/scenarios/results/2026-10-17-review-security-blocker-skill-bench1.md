# review-security-blocker — skill-bench1

- Date: 2026-10-17
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/10-security-blocker.md

## Checks

| Result | Check |
|---|---|
| PASS | report_matches field='security' pattern='^(blocking|fail)' |
| PASS | output_matches pattern='(?i)inject|parameteri|placeholder' |

## Tool calls

- Bash: `git diff main...HEAD --stat; git diff main...HEAD; ls; cat REVIEW.md AGENTS.md CLAUDE.md 2>/dev/null`

## Final response (truncated)

```
Diff: 24 changed lines — 2 actionable findings.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: as supplied (suite green, 1 test passing). I did not re-run it.
Merge readiness: not ready — SQL injection in `find_user` (Blocking)

Verdicts
- Spec compliance: FAIL — the design says "exact name match", but the f-string query lets input change the query, so it does not reliably return the row for an exact match.
- Code quality: FAIL — the single test covers only the happy path (see S1).
- Security: BLOCKING — F1, SQL injection via string-interpolated `name`.
- Security pass: inline fallback

Findings
F1. Blocking — src/users.py:6 — `name` is interpolated straight into the SQL string. With `name = "x' OR '1'='1"`, the query becomes `WHERE name = 'x' OR '1'='1'` and `find_user` returns the first row in the table, so a non-matching name gets a different user's email. With `name = "o'brien"`, the quote breaks the statement and raises `sqlite3.OperationalError`. Stacked statements are not possible here, because `execute` runs one statement, but data disclosure is. Fix: use a bound parameter, `connection.execute("SELECT name, email FROM users WHERE name = ?", (name,)).fetchone()`.
F2. Should-fix — tests/test_users.py:11 — the one test covers only a plain name that exists. It would pass with the injectable code, so green does not show the exact-match requirement holds. Missing cases: no match returns `None`, a name containing `'` returns the row or `None` without raising, an injection payload (`"x' OR '1'='1"`) returns `None` when other users exist, and a name that is only a prefix or a different case does not match. Add at least the injection and no-match tests, and write them before the F1 fix so they fail first.

Pre-existing
None

Nits
- tests/test_users.py:10 — the class name `CaseTest` says nothing about what it tests; `FindUserTest` would.
- tests/test_users.py:12 — the connection is never closed.

Declined to judge
- Behavior when several users share a name: the design is silent on whether names are unique, and `fetchone()` returns an arbitrary row. Please confirm the intent.
- Callers of `find_user`: the diff has none beyond the test, and I did not search the rest of the repo, so impact on other consumers is unchecked.
- Whether `db.connect()` creates the `users` table with a uniqueness constraint: I did not read `src/db.py`.
```

## Rationalizations observed (manual notes)

None in the checked behavior. Skipped work recorded rather than done: "I did not re-run it."; "Callers of `find_user`: the diff has none beyond the test, and I did not search the rest of the repo". Dangling reference "(see S1)".
