# finishing-broken-suite — skill-sonnet-postpatch-r2

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
The suite is **failing**. Conclusion stops here.

**Failure:** `test_export_csv_has_footer` — the CSV exporter returns `['header', 'col=1']` but the test expects `['header', 'col=1', 'footer']`. The footer is missing from the CSV export path.

This needs to go through your normal fix → review cycle before the branch can be concluded. I won't patch it inline here — an unreviewed fix at conclusion time skips every quality gate the rest of this branch went through.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
