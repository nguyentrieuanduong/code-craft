# finishing-broken-suite — skill-bench1

- Date: 2026-10-17
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

- Bash: `python3 -m unittest discover tests 2>&1 | tail -30; echo ---; git diff --stat main...HEAD; git rev-list --count main..HEAD; git rev-parse --short HEAD`

## Final response (truncated)

```
The suite fails, so the conclusion process stops here. I haven't merged, pushed, or deleted anything, and I'm skipping the options menu.

**Failure** (`python3 -m unittest discover tests`, 1 of 2 tests failed at HEAD `bd08693`):
```
FAIL: test_export_csv_has_footer (test_exporters.ExportTest)
AssertionError: Lists differ: ['header', 'col=1'] != ['header', 'col=1', 'footer']
```

The test expects `export([1], "csv")` to return a `"footer"` element, and the CSV exporter in `src/exporters.py` doesn't add one. The branch is one commit ahead of main (`bd08693`, 2 files, +20 lines).

The suite was green earlier today, but it fails on the current state. I don't know yet whether the code or the test is wrong, and I haven't investigated. I also haven't patched it here, because a fix made at conclusion time would skip the design, TDD and review steps. Instead I'm handing this to systematic-debugging, which will find the root cause first. After the fix is reviewed and the full suite passes, I'll return to the merge.

Do you want me to start the debugging now?
```

## Rationalizations observed (manual notes)

None observed. "a fix made at conclusion time would skip the design, TDD and review steps."
