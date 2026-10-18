# finishing-broken-suite — skill-compact1

- Date: 2026-10-18
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

- Bash: `python3 -m unittest discover tests 2>&1 | tail -30; echo "---"; git diff --stat main...HEAD; git rev-list --count main..HEAD; git rev-parse --short HEAD`

## Final response (truncated)

```
The suite fails, so the conclusion process stops here. I'm skipping the options menu and I won't merge.

**Failure** (`python3 -m unittest discover tests`, 1 of 2 tests failed):
```
FAIL: test_export_csv_has_footer (test_exporters.ExportTest)
  tests/test_exporters.py line 10:
  self.assertEqual(export([1], "csv"), ["header", "col=1", "footer"])
AssertionError: ['header', 'col=1'] != ['header', 'col=1', 'footer']
```
`export([1], "csv")` returns no `"footer"` element.

**State:**
- Branch `feature/export-formats` is at `408e27b`, 1 commit ahead of `main`.
- The diff is small: 2 files, 20 insertions, in `src/exporters.py` and `tests/test_exporters.py`.
- Your "green earlier today" run doesn't match the current HEAD. Either the code or the test changed afterwards, or the earlier run was on different state.

I haven't patched this inline, even though it may be a one-line fix. A change made at conclusion time would skip the design, TDD and review gates, so it would be unreviewed.

**Next step:** hand off to systematic-debugging. It will establish whether the code is missing the footer or the test expectation is wrong, then fix it through the normal gates. Once the suite is green and reviewed, I'll rerun finishing-work and present the merge options. Should I start the debugging pass?
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
