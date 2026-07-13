# finishing-broken-suite — skill-sonnet-postpatch-r3

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
The suite is **not green**. The conclusion process ends here.

**Failure:** `test_export_csv_has_footer` in `tests/test_exporters.py:10`

The CSV exporter returns `['header', 'col=1']` but the test expects `['header', 'col=1', 'footer']` — the footer is missing from the CSV export path.

This needs to go through the normal fix cycle (systematic-debugging → plan → TDD → review) before the branch can be concluded. I will not patch it inline here, as that skips every quality gate the rest of this branch went through.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
