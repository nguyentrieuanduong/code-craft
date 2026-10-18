# writing-skills-lean-evaluation — skill-compact2

- Date: 2026-10-18
- Model: sonnet
- Skill file: skills/writing-skills/SKILL.md
- Scenario: tests/scenarios/writing-skills/01-lean-evaluation.md

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='(?i)deterministic|routing' |
| PASS | output_matches pattern='(?i)zero model|no model|no subagent|without.*model|do not spend model tokens' |
| FAIL | output_not_matches pattern='(?i)(must|required).*5\\+|five.*(rep|subagent)|full campaign.*required' |

## Tool calls


## Final response (truncated)

```
**Minimum verification: the deterministic tier only, with zero model calls.**

1. Run `python3 -m tools.check`.
2. It must pass the structural checks, the new positive routing cases, and the new negative routing cases.
3. Read any collision warnings it prints and review each one by hand.

Don't run a subagent fleet or five-plus repetitions. The writing-skills tier table says description, metadata, link, typo, and routing-fixture changes stop after the deterministic tier. A model run would only reconfirm something the routing cases already check. A focused before/after scenario (two runs at most) is only for new skills or behavior-shaping rule changes. A full campaign needs an explicit release decision, unresolved variance, or a request from you, plus a numeric `--allow-many N` budget.

**Commit requirement:** if the new description deliberately shifts routing, so that existing routing cases change, update those cases. Put the rationale for the intended shift in the commit message. This is the only sanctioned reason to edit fixtures.

**Description check:** it must start with "Use when…", be in third person, and state triggers only, with no workflow summary. I can't confirm that without seeing the text.
```

## Rationalizations observed (manual notes)

- FAIL negative check persists: "Don't run a subagent fleet or five-plus repetitions." — a correct refusal that `five.*(rep|subagent)` matches. Positive check now passes ("with zero model calls"). User decision 2026-10-18: accepted as a check-regex artifact.
- Unchecked differences vs bench1: none material; same tier, same routing-case and commit-rationale conditions.
