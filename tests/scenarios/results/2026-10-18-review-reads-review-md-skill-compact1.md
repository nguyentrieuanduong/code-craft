# review-reads-review-md — skill-compact1

- Date: 2026-10-18
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/13-review-md.md

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='REVIEW\\.md' |
| PASS | report_matches section='findings' severity=['blocking'] pattern='--times' |

## Tool calls

- Bash: `git diff main...HEAD --stat; git diff main...HEAD; ls; cat REVIEW.md AGENTS.md CLAUDE.md 2>/dev/null`
- Bash: `cat src/*.py; ls -R tests; cat tests/*.py; git log --stat main..HEAD | head -30; python3 -m pytest -q 2>&1 | tail -5`
- Bash: `python3 -m unittest discover -s tests 2>&1 | tail -4`

## Final response (truncated)

```
Diff: 6 changed lines — 3 actionable findings.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: as supplied (suite green, 1 test). I re-ran it with `python3 -m unittest discover -s tests`: 1 test, OK.
Merge readiness: not ready — documented `--times` flag doesn't exist, and `--shout` has no behavior.

Verdicts
- Spec compliance: FAIL — `--shout` is parsed but never changes any output, and the diff adds an unapproved `--times` to the docs.
- Code quality: FAIL — the only test covers positional parsing, so nothing fails if `--shout` is broken.
- Security: PASS — no security findings
- Security pass: inline fallback

Findings
1. Blocking — README.md:3-6 — The README documents `--times N`, but `build_parser` in src/cli.py has no `--times`. `greet ada --times 3` exits with an argparse "unrecognized arguments" error. REVIEW.md makes a documented flag the CLI lacks a Blocking finding. The design doesn't mention `--times`, so it is also scope creep (commit a449ad3 says "Add --shout and --times"). Fix: delete the `--times` line from the README and the usage string, or implement it under its own approved design.
2. Blocking — src/cli.py:7 — The design says `--shout` "prints the greeting in capitals". The diff only registers the flag. No code anywhere prints a greeting, so `greet ada --shout` produces no capitalised output. Fix: add the greeting output and uppercase it when `args.shout` is set, for example `print(msg.upper() if args.shout else msg)`.
3. Should-fix — tests/test_cli.py — No test fails if `--shout` is removed or ignored. Add a test asserting `parse_args(["ada", "--shout"]).shout is True` and that the default is False. Add one asserting the greeting output is uppercased once finding 2 is fixed. Both assert only what the design states.

Pre-existing
None

Nits
None

Declined to judge
- None. The design doesn't say whether `--times` is wanted. I made no judgment on that. The Blocking finding rests on the README documenting a flag the CLI lacks, not on whether `--times` is a good idea.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
