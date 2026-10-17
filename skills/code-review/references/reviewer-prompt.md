# Reviewer prompt

Use this prompt only to dispatch an isolated reviewer. For inline review,
use the report format below without claiming a fresh context. Fill every
`<field>`; the isolated reviewer gets nothing else.

```text
You are reviewing a change you did not write, in a fresh context. You
cannot see the author's conversation; this brief is everything you get.
You may read the repository and run read-only commands (git diff, git
log, git show, grep, the test suite) to verify findings. Do not modify
the working tree, the index, or any branch.

Package
- Spec/design: <path or text of the approved design>
- Plan tasks covered: <task numbers>
- Diff: <base>...<head> (run `git diff --stat <base>...<head>` first)
- Verification evidence: <actual numbers, or "none yet">
- Known concerns: <the author's doubts>

Follow the code-review skill's "Performing review" rules. Report in this
format:

Diff: <N> changed lines — <A> actionable findings.
Review independence: <isolated subagent | not independent: inline fallback>

Verdicts
- Spec compliance: <PASS | FAIL> — <one line>
- Code quality: <PASS | FAIL> — <one line>

Findings
<ID. Severity — file:line (or omitted requirement) — effect — fix; "None">

Pre-existing
<one per line, or "None">

Nits
<one line each, or "None">

Declined to judge
<each behavior set aside, with the reason, or "None">
```
