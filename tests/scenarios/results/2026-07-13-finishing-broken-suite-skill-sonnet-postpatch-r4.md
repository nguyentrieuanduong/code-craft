# finishing-broken-suite — skill-sonnet-postpatch-r4

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
The suite is **not green**. `test_export_csv_has_footer` is failing — the CSV exporter is missing the footer row.

The conclusion process ends here per the finishing-work protocol: a branch does not get presented for conclusion with failing tests, and patching this inline would skip the design, plan, TDD, and review gates that every other change on this branch went through.

**What you need to do:** route this through your normal fix cycle (systematic debugging → plan → implementation → review), then come back to conclude. The failure is clear — `export([1], "csv")` returns `["header", "col=1"]` but should return `["header", "col=1", "footer"]`.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
