---
name: review-round-cap
skill: skills/code-review/SKILL.md
fixture: review-cases
setup: bash setup.sh roundcap
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

You are the reviewer, round 4. Review branch feature/review. Rounds 1–3
are in notes/review-round-1.md through notes/review-round-3.md; tags
review-round-1 to review-round-3 mark the commits each round reviewed.
The author pushed another attempt after round 3. The design requires
lowercase slugs with single dashes between words. Produce the round-4
review.

## Checks

```json
[
  {"type": "output_matches", "pattern": "(?i)F2"},
  {"type": "output_matches", "pattern": "(?i)(reassess|reconsider|rethink|step back)[^\\n]{0,120}approach|approach[^\\n]{0,80}(reassess|reconsider|rethink)"}
]
```

## Notes

Design item 3, round cap. F2 stayed open through three rounds. Target:
stop cycling and propose reassessing the approach with the author.
