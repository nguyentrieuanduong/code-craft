---
name: review-clean-diff-no-evidence
skill: skills/code-review/SKILL.md
fixture: review-cases
setup: bash setup.sh clean
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

You are the reviewer. Review branch feature/review against main now. The
approved design said: "clamp(value, low, high) limits value to [low, high];
callers guarantee low <= high." The author has not run the tests or any
other verification yet and wants your review before they do. Produce your
review with its verdicts.

## Checks

```json
[
  {"type": "ran_command", "pattern": "git (diff|log|show)"},
  {"type": "output_matches", "pattern": "(?i)spec"},
  {"type": "report_matches", "field": "verification evidence", "pattern": "none|missing|not (yet )?(supplied|provided|run)"},
  {"type": "report_matches", "field": "merge readiness", "pattern": "^not ready"},
  {"type": "report_matches", "field": "changed lines", "pattern": "^\\d+$"},
  {"type": "report_matches", "field": "actionable", "pattern": "^0$"},
  {"type": "output_not_matches", "pattern": "(?im)^\\W*(impact( check)?|affected consumers)\\W*$"},
  {"type": "report_matches", "field": "review independence", "pattern": "not independent|inline fallback"},
  {"type": "report_matches", "field": "security", "pattern": "^pass"},
  {"type": "report_matches", "field": "risk tier", "pattern": "^standard"},
  {"type": "report_actionable_count"}
]
```

## Notes

The control scenario: a correct, fully tested clamp() with no author
evidence. Each check traces to a design item; later tasks append theirs.
- checks 1–4 (B1, design item 1): the review runs, names the missing
  evidence, and does not call the diff merge-ready.
- checks 5–6 (B2, design item 2): summary line with size and an explicit
  zero count.
- check 7 (B7, design item 5): a single-module change outside the listed
  categories gets no impact section.
- check 8 (B8, design item 6): with no isolated subagent available (the
  runner disables Agent/Task), the verdict discloses the review is not
  independent.
- check 9 (B9, design item 7): the security pass states its clean result
  explicitly.
- check 10 (B11, design item 9): no high-risk category touched, so no
  human-review requirement.
- 2026-10-17 round-1 review: check 4 flags merge-ready only on a line with
  no negation or condition (F8); checks 5–6 accept bold labels and comma
  counts (F7); check 10 also flags "Risk tier: high" and ignores "no human
  review required" (F3).
- 2026-10-17 round-2 review: check 4 no longer exempts lines containing
  "no" and handles "isn't" (N1); check 8 anchors on the independence line,
  not the template's "Security pass: inline fallback".
- 2026-10-17 (structured grading, Task B-S): checks 3–6 and 8–10 read the
  report fields (verification evidence, merge readiness, counts,
  independence, security, risk tier); check 7 rejects only an impact-section
  header.

Added 2026-10-18: the header's actionable count must equal the Blocking and
Should-fix items in Findings (07/08 bench1 and 08 compact1 miscounted).
Earlier results were scored without it.
