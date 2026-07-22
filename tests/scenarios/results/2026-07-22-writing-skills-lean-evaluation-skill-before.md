# writing-skills-lean-evaluation — skill-before

- Date: 2026-07-22
- Model: CLI default
- Skill file: skills/writing-skills/SKILL.md
- Scenario: tests/scenarios/writing-skills/01-lean-evaluation.md

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='(?i)deterministic|routing' |
| FAIL | output_matches pattern='(?i)zero model|no model|no subagent|without.*model' |
| PASS | output_not_matches pattern='(?i)(must|required).*5\\+|five.*(rep|subagent)|full campaign.*required' |

## Tool calls


## Final response (truncated)

```
For a description-only + routing-cases change, skip the full RED-GREEN-REFACTOR cycle. Minimum verification:

1. **Description accuracy**: Run 1-2 fresh samples (no control needed) where the trigger condition is ambiguous or borderline. Verify the new description correctly signals when to load the skill.

2. **Routing cases**: Execute the positive and negative cases you added (deterministically, no sampling needed). Confirm they route as intended.

3. **No regression**: Skim the skill body once to confirm you didn't accidentally change any guidance or examples while editing.

That's it — 10 minutes total. Full micro-testing (5+ reps per variant with controls) applies when you change *what the skill teaches*, not when you change *how it's discovered* or *when to apply it*.
```

## Rationalizations observed (manual notes)

Manual read (Task 5.3). Check 2 is a behavioral RED, not a regex artifact.
The response requires *"1-2 fresh samples"* for a trigger-description change,
which spends model calls; the target deterministic tier requires zero model
calls for this case. Its later *"no sampling needed"* statement applies only
to running the routing fixtures and does not cancel that requirement.

Checks 1 and 3 pass, so the failure is narrowly attributable to the missing
zero-model tier rather than a demand for a full five-repetition campaign. No
tool calls were made, as requested.
