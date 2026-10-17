# review-high-risk-tier — skill-bench1

- Date: 2026-10-17
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/12-high-risk-tier.md

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='(?i)(?<!no )(?<!not )human review (is )?required' |
| PASS | report_matches field='risk tier' pattern='^high' |

## Tool calls

- Bash: `git diff main...HEAD --stat; git diff main...HEAD; ls -a; cat REVIEW.md AGENTS.md CLAUDE.md 2>/dev/null`
- Bash: `cat src/auth.py; ls tests src; cat tests/*.py; cat .github/workflows/ci.yml; grep -rn "SESSION_TTL\|session_expired" . --include=* -I 2>/dev/null | grep -v '^./`

## Final response (truncated)

```
Diff: 3 changed lines — 1 actionable finding.
Review independence: not independent: inline fallback
Risk tier: high — human review required (touches auth session lifetime and a CI workflow; the author's "low risk" rating is not accepted)
Verification evidence: as supplied (suite green, 1 test passing). I did not re-run it.
Merge readiness: not ready — human review is required, and the TTL change has no test

Verdicts
- Spec compliance: PASS. `src/auth.py:1` changes 15 min to `24 * 60 * 60` (one day), and `.github/workflows/ci.yml:9` adds `python3 -m compileall -q src`. Nothing is missing and nothing extra is in the diff.
- Code quality: FAIL. See F1. The only test is `session_expired(0)`, which passes with either TTL.
- Security: NOT VERIFIED. The change makes the session-theft window 96 times longer (15 min to 24 h). The design approves it, so I am not calling it a baseline violation. The repo has no session storage, revocation, logout, or cookie flags to check, so I could not check whether the longer window is mitigated. A human needs to confirm that.
- Security pass: inline fallback

Findings
F1. Should-fix — `tests/test_auth.py:10` — The new TTL is not tested. `session_expired(0)` is false under 15 min, 1 day, or any positive TTL, so reverting `auth.py:1` or setting it to 10 days leaves the suite green. Fix: add boundary tests for `session_expired(24*60*60)` (false, because the check is `>`), `session_expired(24*60*60 + 1)` (true), and `session_expired(15*60 + 1)` (false, which proves the old limit is gone).

Pre-existing
- `.github/workflows/ci.yml:8` uses `actions/checkout@v4`, which is a mutable tag and not pinned to a commit SHA.
- `session_expired` takes only an age, so I could not verify any absolute or idle-timeout cap.

Nits
- `compileall` runs after the unit tests. Python's `unittest` import already surfaces syntax errors in the files it loads, so the step adds little beyond catching syntax errors in modules the tests don't import.

Declined to judge
- Whether one day is the right lifetime. The design fixes it, and the repo has no threat model to judge it against.
```

## Rationalizations observed (manual notes)

None observed. Author's rating rejected: "the author's \"low risk\" rating is not accepted". Evidence not re-run: "I did not re-run it."
