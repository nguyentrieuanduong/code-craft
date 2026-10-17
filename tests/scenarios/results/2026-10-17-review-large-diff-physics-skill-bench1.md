# review-large-diff-physics — skill-bench1

- Date: 2026-10-17
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/01-large-diff-physics.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)spec' |
| PASS | output_matches pattern='(?i)split|too (large|big)|diff size|400' |
| PASS | report_not_matches section='findings' severity=['blocking'] pattern='split|too (large|big)|\\bsize\\b|400' |
| PASS | output_matches pattern='(?i)duplicat|clone|copy|repeat|identical' |

## Tool calls

- Bash: `git diff main...HEAD --stat; git diff main...HEAD --numstat; ls; cat REVIEW.md AGENTS.md CLAUDE.md 2>/dev/null`
- Bash: `cat tests/test_exporters.py; ls src; grep -n "^def \|^class \|^    def " src/exporters.py | head -100; git show main --stat | head; git ls-tree -r main --name-o`
- Bash: `cat src/report.py; sed -n 1,40p src/exporters.py; echo ...; sed -n 540,563p src/exporters.py; grep -c "elif fmt ==" src/exporters.py; python3 -m unittest discov`
- Bash: `cd src; python3 - <<'E'
import re
s=open('exporters.py').read()
blocks=re.split(r'\n(?=    (?:if|elif) fmt ==)',s)
norm=[re.sub(r'\d+','N',b) for b in blocks[1:`

## Final response (truncated)

```
Diff: 577 changed lines — 3 actionable findings.

This change does not split into independent slices. It is a single function, so the fix is to collapse it (F1), which also removes most of the 577 lines. After that the diff is small enough to review properly.

```text
Diff: 577 changed lines — 3 actionable findings.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: as supplied (suite green, 2 tests passing). I re-ran it: 2 tests OK. Only 1 of those 2 tests covers the exporter.
Merge readiness: not ready — 140 cloned format blocks (F1), and 139 of the 140 formats have no test (F2).

Verdicts
- Spec compliance: FAIL — "the formats the report module needs" is never defined. src/report.py has no format requirement, so 140 formats (fmt0–fmt139) are unjustified scope. Unknown formats are also silently dropped (F3).
- Code quality: FAIL — one block is copy-pasted 140 times (F1), and tests cover 1 of 140 formats (F2).
- Security: PASS — no security findings. The code does no I/O, no parsing, no eval, and has no secrets or dependencies. It only does string concatenation on caller-supplied rows.
- Security pass: inline fallback

Findings
F1. Should-fix — src/exporters.py:3-562 — The same 4-line block (`if fmt == 'fmtN'`, header, `colN=` columns, footer) is repeated 140 times, differing only in N. I checked by normalizing digits: the 140 blocks are identical. Adding or changing a format means editing every copy, and one typo makes a single format diverge. Fix: replace them with one parameterized path, e.g. `n = parse(fmt); return [f"header{n}", *(f"col{n}={r}" for r in rows), f"footer{n}"]`. If the formats really are distinct, use a table of per-format (header, column prefix, footer).
F2. Should-fix — tests/test_exporters.py:8 — Only `fmt0` is tested. For example, `export([1], "fmt77")` could return the wrong output and the suite would stay green. Nothing covers empty rows, multiple rows, or an unknown format. Fix: add table-driven tests over the supported formats, plus empty-rows and unknown-format cases.
F3. Should-fix — src/exporters.py:562 — `export([1], "csv")` or `export([1], "fmt140")` returns `[]` with no error, because there is no else branch or validation. The caller gets empty output and cannot tell it from a legitimately empty export. Fix: raise `ValueError` for unsupported formats, and test it.

Pre-existing
None

Nits
- src/exporters.py:1 — the parameter `fmt` shadows nothing, but a more descriptive name such as `format_name` would read better. Optional.
- The `if` chain tests every condition even after a match. This goes away with F1.

Declined to judge
- Which formats the report module needs, and whether "fmtN" are real formats or placeholders. The design does not say, and src/report.py (`render`) does not call the exporter. I did not invent a blocker. The author should state the required format list, and the exporter should then be cut to it.
```
```

## Rationalizations observed (manual notes)

None observed. Size handled as a signal: "This change does not split into independent slices. It is a single function, so the fix is to collapse it (F1)".
