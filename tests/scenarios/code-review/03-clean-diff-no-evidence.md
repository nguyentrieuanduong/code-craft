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
  {"type": "output_not_matches", "pattern": "(?i)(?<!not )(?<!n't )(ready to merge|merge-ready|safe to merge)"},
  {"type": "output_matches", "pattern": "(?i)diff:? *\\d+ changed lines"},
  {"type": "output_matches", "pattern": "(?i)\\b(0|no|zero) actionable findings?"}
]
```

## Notes

The control scenario: a correct, fully tested clamp() with no author
evidence. Each check traces to a design item; later tasks append theirs.
- checks 1–4 (B1, design item 1): the review runs, names the missing
  evidence, and does not call the diff merge-ready.
- checks 5–6 (B2, design item 2): summary line with size and an explicit
  zero count.
