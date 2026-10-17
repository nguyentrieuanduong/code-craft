# standards-inline-vs-implicit — skill-codex-bench1

- Date: 2026-10-17
- Harness: Codex CLI (`codex exec`), scratch fallback driver
- Model: Codex config default
- Skill file: skills/coding-standards/SKILL.md

- Tool-order and command checks: NOT EVALUATED by this driver

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='(?i)truthy|truthiness|falsy|is None|zero' |
| PASS | output_not_matches pattern='(?i)(extract|split|expand|unroll)[^.]{0,80}(one-?liner|comprehension|generator expression|ternary|inline)' |

## Final response (truncated)

```
Diff: unavailable; this workspace has no Git metadata — 4 actionable findings.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: `python3 -m unittest` ran 5 tests successfully; direct input checks reproduced the issues below.
Merge readiness: **not ready**

### Verdicts

- Spec compliance: not verified — no design or expected value ranges were supplied.
- Code quality: fail — configuration resolution is split across functions and lacks type hints.
- Security: blocking — raw `stages` input is not type validated at the boundary.
- Security pass: inline fallback.

### Must change

1. **Blocking — [settings.py:9](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-standards-inline-vs-implicit-o6wcpd8h/settings.py:9), [settings.py:13](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-standards-inline-vs-implicit-o6wcpd8h/settings.py:13):** `or` silently replaces explicit zero values: `{"retries": 0}` resolves to `3`, and `{"timeout": 0}` resolves to `30`. Default only when absent or `None`; reject zero explicitly if it is invalid. Add tests for both cases.
2. **Blocking — [settings.py:17](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-standards-inline-vs-implicit-o6wcpd8h/settings.py:17):** `{"stages": "buildtest"}` is accepted and resolves to `("build", "test")`. Validate the input type before membership checks.
3. **Should-fix — [settings.py:8](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-standards-inline-vs-implicit-o6wcpd8h/settings.py:8):** Defaults and derivations are spread across resolvers; `describe` resolves stages again. The supplied standard requires one parse step producing an immutable, fully resolved config, with boundary logging of the raw and resolved values.
4. **Should-fix — [settings.py:8](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-standards-inline-vs-implicit-o6wcpd8h/settings.py:8):** All four functions lack the required Python parameter and return type hints.

### Must not change

Keep concise, readable inline expressions: the ternary in [describe](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-standards-inline-vs-implicit-o6wcpd8h/settings.py:22) needs no expansion, and the default checks need no one-use helper. Preserve unknown-stage filtering unless the product requirement changes; [the test](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-standards-inline-vs-implicit-o6wcpd8h/test_settings.py:16) explicitly expects it.
```

## Rationalizations observed (manual notes)

None in checked behavior. Template deviation: findings under "### Must change" instead of the report's "Findings" section; "Diff: unavailable; this workspace has no Git metadata".
