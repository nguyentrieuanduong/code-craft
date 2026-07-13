# finishing-broken-suite — skill-sonnet-postpatch-r5

- Date: 2026-07-13
- Model: sonnet
- Skill file: skills/finishing-work/SKILL.md
- Scenario: tests/scenarios/finishing-work/03-broken-suite.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='unittest' |
| PASS | not_ran_command pattern='git merge' |
| PASS | output_matches pattern='(?i)fail' |
| PASS | output_not_matches pattern='(?i)1\\. merge into main' |

## Tool calls

- Bash: `python3 -m unittest discover tests 2>&1`

## Final response (truncated)

```
The suite is **not green** — one test is failing right now, on the final state of the branch.

```
FAIL: test_export_csv_has_footer
AssertionError: ['header', 'col=1'] != ['header', 'col=1', 'footer']
```

The CSV exporter is missing the footer. Per the finishing-work process: **conclusion stops here**. This failure needs to go through systematic debugging and a proper fix before the branch can be merged — a patch applied at conclusion time skips every quality gate the rest of the branch went through.

Please fix the failing test (route it through your normal dev/review flow), then re-invoke the conclusion process when the suite is clean.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
