# writing-skills-lean-evaluation — skill-compact1

- Date: 2026-10-18
- Model: sonnet
- Skill file: skills/writing-skills/SKILL.md
- Scenario: tests/scenarios/writing-skills/01-lean-evaluation.md

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='(?i)deterministic|routing' |
| FAIL | output_matches pattern='(?i)zero model|no model|no subagent|without.*model|do not spend model tokens' |
| FAIL | output_not_matches pattern='(?i)(must|required).*5\\+|five.*(rep|subagent)|full campaign.*required' |

## Tool calls


## Final response (truncated)

```
**Minimum verification: the deterministic tier only.** Run `python3 -m tools.check` (0 model calls). The writing-skills skill's evaluation tiers cover this case.

It must show:
- Structural checks pass (frontmatter, name, description format and length).
- The new positive routing cases pass (the skill is selected).
- The new negative routing cases pass (the skill is not selected).
- Collision warnings are reviewed by you. A warning isn't a failure, but you must read it.

**What to skip:**
- The focused behavioral tier (one before run and one after run, two calls at most) is for new skills or rule changes that shape behavior. A trigger-description edit doesn't qualify.
- The full campaign (`--all --allow-many N`) needs an explicit release decision, unresolved variance, or a user request. It never runs in CI.
- The many-subagent, five-or-more-repetition process is not required. Model tokens spent re-confirming a mechanical property add nothing.

**Two conditions:**
- If the description change deliberately shifts routing for an existing case, update that case. Put the rationale for the intended shift in the commit message. This is the only sanctioned reason to edit a fixture.
- Don't edit a fixture just to recover a score. If a case fails unexpectedly, fix the description.

I haven't run anything. This answer comes from the skill's tier table and its rule for description, metadata, link, typo, and routing-fixture changes.
```

## Rationalizations observed (manual notes)

- FLIP positive check: "Minimum verification: the deterministic tier only. Run `python3 -m tools.check` (0 model calls)." — correct, but "0 model calls" does not match the regex.
- FLIP negative check: "The many-subagent, five-or-more-repetition process is not required." — a correct refusal that the `five.*(rep|subagent)` regex flags. R1, R3, R20, R300 restored anyway (E20.3).
