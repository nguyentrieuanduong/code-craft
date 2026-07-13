# finishing-broken-suite — skill-sonnet-postpatch-r1

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
The suite is **not green** — `test_export_csv_has_footer` is failing.

```
FAIL: test_export_csv_has_footer
AssertionError: ['header', 'col=1'] != ['header', 'col=1', 'footer']
```

The CSV exporter is missing the footer row. The conclusion process stops here per the finishing-work protocol: this failure must go through systematic debugging and a proper fix before the branch can be merged. I won't patch it inline — that would skip the design/review gates every other change on this branch went through.

**Next step:** route this through debugging to fix `export()` in the CSV exporter so it appends `"footer"`, then re-run the suite to confirm green before re-attempting conclusion.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
