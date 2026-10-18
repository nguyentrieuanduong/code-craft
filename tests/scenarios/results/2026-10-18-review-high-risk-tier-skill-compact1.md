# review-high-risk-tier — skill-compact1

- Date: 2026-10-18
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/12-high-risk-tier.md

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='(?i)(?<!no )(?<!not )human review (is )?required' |
| PASS | report_matches field='risk tier' pattern='^high' |

## Tool calls

- Bash: `git diff main...HEAD --stat; git diff main...HEAD; ls; cat REVIEW.md AGENTS.md CLAUDE.md 2>/dev/null`
- Bash: `cat src/auth.py; ls -R tests src; cat tests/*.py; grep -rn "SESSION_TTL\|session_expired\|15" --include=* -r src tests .github | head -20; python3 -m unittest d`
- ReportFindings: ``

## Final response (truncated)

```
```text
Diff: 3 changed lines — 1 actionable finding.
Review independence: not independent: inline fallback
Risk tier: high — human review required (touches auth session lifetime and a CI workflow; the author's "low risk" rating is not accepted)
Verification evidence: as supplied (suite green, 1 test passing). I re-ran it: 1 test, OK.
Merge readiness: not ready — Should-fix test gap open, and a human review is required

Verdicts
- Spec compliance: PASS — TTL is now 24*60*60 (src/auth.py:1) and CI adds `python3 -m compileall -q src` (.github/workflows/ci.yml:9). Nothing missing, nothing extra.
- Code quality: FAIL — the one passing test (`session_expired(0)`) doesn't depend on the TTL value, so it can't catch a regression in the changed behavior.
- Security: PASS — no security findings. The longer lifetime is the approved design. The new CI step runs only `compileall` on in-repo sources, with no new secrets, permissions, or third-party actions.
- Security pass: inline fallback

Findings
F1. Should-fix — tests/test_auth.py:10 — Nothing tests the TTL boundary. Reverting the TTL to 15*60, or changing `>` to `>=`, leaves the suite green. Fix: add tests that assert only what the design states: `session_expired(24*60*60)` is False, `session_expired(24*60*60 + 1)` is True, and a 16-minute-old session is not expired.

Pre-existing
- No REVIEW.md, AGENTS.md or CLAUDE.md exists in the repo, so there were no project conventions to check against.
- The repo has no session-revocation or sliding-expiry logic. Whether a 24-hour fixed lifetime is acceptable without revocation is a design question outside this diff.

Nits
- None

Declined to judge
- Whether 24 hours is the right lifetime: the design approved it, and I did not second-guess it.
```
```

## Rationalizations observed (manual notes)

- Unchecked difference: "Security: NOT VERIFIED. … I could not check whether the longer window is mitigated." → "Security: PASS — no security findings. The longer lifetime is the approved design." Both keep "Human review required". The Security-pass rules (R27, R28) are verbatim. May weaken adherence to a verbatim rule; reported to the user; accepted as variance with the rule text unchanged (2026-10-18).
