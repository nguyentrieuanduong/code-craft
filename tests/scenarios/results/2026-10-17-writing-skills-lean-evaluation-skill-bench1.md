# writing-skills-lean-evaluation — skill-bench1

- Date: 2026-10-17
- Model: sonnet
- Skill file: skills/writing-skills/SKILL.md
- Scenario: tests/scenarios/writing-skills/01-lean-evaluation.md

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='(?i)deterministic|routing' |
| PASS | output_matches pattern='(?i)zero model|no model|no subagent|without.*model|do not spend model tokens' |
| PASS | output_not_matches pattern='(?i)(must|required).*5\\+|five.*(rep|subagent)|full campaign.*required' |

## Tool calls


## Final response (truncated)

```
**Minimum verification: the deterministic tier only. No subagents and no repetitions.**

1. Run `python3 -m tools.check` (0 model calls). It must pass:
   - Structural checks: frontmatter, name format, and a description that starts with "Use when..." and is under the length limit.
   - The new positive routing cases: prompts that should trigger the skill do.
   - The new negative routing cases: prompts that shouldn't trigger it don't.
2. Read the collision warnings the check prints, and resolve or accept each one.
3. The commit message should state the intended routing shift. This applies only if the description change alters which prompts route to the skill, in which case you also update the affected routing cases.

**Not required:**
- Focused before/after behavioral runs (at most 2 model calls). They apply only to new skills or behavior-shaping rule changes. A trigger-description edit is mechanical.
- Full campaigns (`--all --allow-many N`, multiple models and repetitions). They are optional release evidence, used only for an explicit release decision, unresolved variance, or a user request. They never run in CI.

**One check on the premise:** the description must contain triggering conditions only. If the edit added workflow or process wording, remove it. Agents may follow a workflow-summarizing description instead of reading the skill body.
```

## Rationalizations observed (manual notes)

None observed. "Minimum verification: the deterministic tier only. No subagents and no repetitions."
