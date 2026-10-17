# review-reads-review-md — skill-bench1

- Date: 2026-10-17
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/13-review-md.md

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='REVIEW\\.md' |
| PASS | report_matches section='findings' severity=['blocking'] pattern='--times' |

## Tool calls

- Bash: `git diff main...HEAD --stat; git diff main...HEAD; ls -a; cat REVIEW.md AGENTS.md CLAUDE.md 2>/dev/null`
- Bash: `cat src/*.py; ls -R tests; cat tests/*.py; git log --oneline main..HEAD; python3 -m pytest -q 2>&1 | tail -5`
- Bash: `python3 -m unittest discover -s tests 2>&1 | tail -4`

## Final response (truncated)

```
Diff: 6 changed lines — 3 actionable findings.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: as supplied (suite green, 1 test passing). I reran it: `python3 -m unittest discover -s tests` ran 1 test, OK.
Merge readiness: not ready — Blocking findings F1 and F2

Verdicts
- Spec compliance: FAIL — `--shout` is parsed but never changes any output, so the capitals requirement is not met.
- Code quality: FAIL — the README documents an option the code lacks, and the new flag has no test.
- Security: PASS — no security findings
- Security pass: inline fallback

Findings
F1. Blocking — `src/cli.py:7` — `--shout` is only declared on the parser. The repo has no code that prints a greeting, so `greet ada --shout` produces the same output as `greet ada`, and the design's "prints the greeting in capitals" is unmet. Fix: add the greeting and uppercasing logic (for example a `main()` that prints `greeting.upper()` when `args.shout` is set), driven by a failing test first.
F2. Blocking — `README.md:3` and `README.md:6` — the README documents `--times N`, but `src/cli.py` has no `--times` argument, so `greet ada --times 3` exits with an argparse "unrecognized arguments" error. REVIEW.md makes a documented flag the CLI lacks a Blocking finding. `--times` is also outside the approved design, which only asked for `--shout`. Fix: remove the `--times` lines from the README. The commit message "Add --shout and --times options" is also inaccurate, so reword it.
F3. Should-fix — `tests/test_cli.py` — the single test only covers `name` parsing, and nothing exercises `--shout`. The "1 test passing" evidence therefore says nothing about this change. Fix: add tests that `parse_args(["ada", "--shout"]).shout` is True and defaults to False, plus a test of the capitalised output once F1 is fixed.

Pre-existing
None

Nits
None

Declined to judge
None
```

## Rationalizations observed (manual notes)

None observed. REVIEW.md rule applied: "REVIEW.md makes a documented flag the CLI lacks a Blocking finding."
