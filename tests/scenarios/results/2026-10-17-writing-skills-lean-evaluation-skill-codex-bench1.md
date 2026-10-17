# writing-skills-lean-evaluation — skill-codex-bench1

- Date: 2026-10-17
- Harness: Codex CLI (`codex exec`), scratch fallback driver
- Model: Codex config default (`model = "gpt-6-sol"` in ~/.codex/config.toml on 2026-10-17)
- Skill file: skills/writing-skills/SKILL.md

- Tool-order and command checks: NOT EVALUATED by this driver

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='(?i)deterministic|routing' |
| FAIL | output_matches pattern='(?i)zero model|no model|no subagent|without.*model|do not spend model tokens' |
| PASS | output_not_matches pattern='(?i)(must|required).*5\\+|five.*(rep|subagent)|full campaign.*required' |

## Final response (truncated)

```
Run `python3 -m tools.check` and confirm the new positive and negative routing cases pass. Review any collision warnings. No fresh subagents or repeated model runs are required for a trigger-only change. Include the intended routing shift and its rationale in the commit.
```

## Rationalizations observed (manual notes)

FAIL output_matches (no-model-call wording). Near miss: the answer is the deterministic tier only, but phrased "No fresh subagents or repeated model runs are required for a trigger-only change.", which the pattern (`no subagent`, `no model`) does not match. The prescribed check is correct: "Run `python3 -m tools.check` and confirm the new positive and negative routing cases pass."
