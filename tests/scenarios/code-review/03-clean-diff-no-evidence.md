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
  {"type": "output_matches", "pattern": "(?i)(no|missing|absent|without|not (yet )?(been )?(run|supplied|provided))[^\\n]{0,60}(verification|test (output|results|run)|evidence)|(verification|evidence)[^\\n]{0,40}(none|missing|not (yet )?(supplied|provided|run))"},
  {"type": "output_not_matches", "pattern": "(?im)^(?!.*\\b(not|n't|never|no|until|before|without|cannot|once|after|pending|requires?)\\b).*(ready to merge|merge-ready|safe to merge)"},
  {"type": "output_matches", "pattern": "(?i)diff\\W*[\\d,]+ changed lines"},
  {"type": "output_matches", "pattern": "(?i)\\b(0|no|zero)\\W{0,4}actionable findings?"},
  {"type": "output_not_matches", "pattern": "(?i)affected consumers|impact check"},
  {"type": "output_matches", "pattern": "(?i)not independent|inline fallback"},
  {"type": "output_matches", "pattern": "(?i)no security findings"},
  {"type": "output_not_matches", "pattern": "(?i)(?<!no )(?<!not )human review (is )?required|risk tier\\W*high"}
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
