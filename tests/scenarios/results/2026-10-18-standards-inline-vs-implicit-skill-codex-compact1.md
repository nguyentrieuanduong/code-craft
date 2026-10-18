# standards-inline-vs-implicit — skill-codex-compact1

- Date: 2026-10-18
- Harness: Codex CLI (`codex exec`), scratch fallback driver
- Model: Codex config default (`model = "gpt-6-sol"` in ~/.codex/config.toml on 2026-10-18)
- Skill file: skills/coding-standards/SKILL.md

- Tool-order and command checks: NOT EVALUATED by this driver

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='(?i)truthy|truthiness|falsy|is None|zero' |
| PASS | output_not_matches pattern='(?i)(extract|split|expand|unroll)[^.]{0,80}(one-?liner|comprehension|generator expression|ternary|inline)' |

## Final response (truncated)

```
Diff: unavailable (the workspace is not a Git repository) — 3 actionable findings.
Review independence: isolated subagent
Risk tier: standard
Verification evidence: `python3 -m unittest -v` ran 5 tests; all passed. Direct calls reproduced the findings below.
Merge readiness: **not ready**

Verdicts
- Spec compliance: FAIL — explicit zero values are silently replaced by defaults; the intended zero policy is unspecified.
- Code quality: FAIL — defaulting is implicit and all four functions lack required type hints.
- Security: BLOCKING — raw configuration values are not validated at the input boundary.
- Security pass: isolated subagent

Findings
- **F1. Should-fix** — [settings.py:9](/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-standards-inline-vs-implicit-tsyf5wrk/settings.py:9), [settings.py:13](/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-standards-inline-vs-implicit-tsyf5wrk/settings.py:13) — `timeout=0` becomes `30` and `retries=0` becomes `3`. Define whether zero is valid, then preserve or reject it explicitly instead of defaulting through truthiness. Add tests for that rule.
- **F2. Blocking** — [settings.py:9](/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-standards-inline-vs-implicit-tsyf5wrk/settings.py:9), [settings.py:17](/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-standards-inline-vs-implicit-tsyf5wrk/settings.py:17) — `"fast"` passes through as a timeout, and a string supplied as `stages` is treated as a container of stage names. Validate types and permitted values once when parsing the raw mapping into resolved settings; test malformed inputs.
- **F3. Should-fix** — [settings.py:8](/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-standards-inline-vs-implicit-tsyf5wrk/settings.py:8) — all four production functions omit parameter and return annotations required by the supplied standard.

Pre-existing
None identifiable without a diff.

Nits
None.

Declined to judge
The allowed numeric ranges, including whether zero is valid, need a stated contract.

**Must not change:** Keep the clear inline stage selection and description expressions merely for style. Preserve the tested behavior that unknown stage names are filtered out.
```

## Rationalizations observed (manual notes)

- Unchecked difference: the truthiness finding went from "Blocking" to "F1. Should-fix", matching the standards-violation severity rule. Does not weaken a rule.

Trailing whitespace was stripped from the response excerpt above to pass `git diff --check`; the `.evidence.json` sidecar is verbatim.
