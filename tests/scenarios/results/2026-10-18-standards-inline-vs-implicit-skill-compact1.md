# standards-inline-vs-implicit — skill-compact1

- Date: 2026-10-18
- Model: sonnet
- Skill file: skills/coding-standards/SKILL.md
- Scenario: tests/scenarios/coding-standards/01-inline-vs-implicit.md

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='(?i)truthy|truthiness|falsy|is None|zero' |
| PASS | output_not_matches pattern='(?i)(extract|split|expand|unroll)[^.]{0,80}(one-?liner|comprehension|generator expression|ternary|inline)' |

## Tool calls

- Glob: ``
- Read: `/Users/apollo/projects/code-craft/skills/code-review/SKILL.md`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-standards-inline-vs-implicit-5f7leza8/settings.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-standards-inline-vs-implicit-5f7leza8/test_settings.py`
- Bash: `ls -la && wc -l *.py && python3 -m unittest 2>&1 | tail -5; ls REVIEW.md AGENTS.md CLAUDE.md 2>&1`

## Final response (truncated)

```
Diff: 46 changed lines (no git repo, so this is the full size of both files) — 3 actionable findings.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: `python3 -m unittest` run by me: 5 tests, OK. No design or spec was supplied.
Merge readiness: not ready — 3 should-fix findings

Verdicts
- Spec compliance: NOT JUDGED. There is no spec, and `REVIEW.md`, `AGENTS.md` and `CLAUDE.md` don't exist. I judged by what a reasonable user would expect.
- Code quality: FAIL. Truthiness defaulting, no type hints, no single resolution point, and test gaps.
- Security: PASS, no security findings. The code does no I/O, parsing, or auth.
- Security pass: inline fallback

Findings
1. Should-fix: `settings.py:9` and `settings.py:13`. `config.get(...) or DEFAULT` treats `0` the same as absent. `resolve_retries({"retries": 0})` returns `3`, so a user who turns retries off gets three. Replace with `DEFAULT_RETRIES if config.get("retries") is None else config["retries"]`. This is still one line, and the rule is readable as written. `{"retries": None}` still falls back to the default.
2. Should-fix: `settings.py:8-22`. This breaks two coding standards.
   - No function has type hints.
   - Defaults are applied in three separate functions, with no single parse step. The standard calls for one frozen, fully resolved config (`@dataclass(frozen=True)` with `timeout`, `retries`, `stages: tuple[str, ...]`) built once and logged raw and resolved. `describe` and the callers would then read only that object.
3. Should-fix: `test_settings.py`. These cases are missing:
   - `describe` with no stages. The `"no stages selected"` branch has no test, so breaking it wouldn't fail anything.
   - `selected_stages({})`, which should return all `KNOWN_STAGES`.
   - A configured `retries` value.
   - `retries: 0`, once finding 1 is decided. Add the failing test first.

Pre-existing
None

Nits
- `settings.py:17`: `stage in config.get("stages", ...)` does substring matching if `stages` is a string, and raises `TypeError` if it is `None`. Fix this in the single parse step from finding 2, because this is the system boundary where validation belongs.

Declined to judge
- `timeout: 0` falls back to 30 today. It could mean "no timeout", or it could be invalid. The author must say which. Whichever they pick, the parse step should reject or honor `0` explicitly instead of defaulting it by accident.
- Silently dropping unknown stages like `"lint"` is asserted by a test, so I treated it as intended. Say so if it should raise instead.

**Must not change before merge**
- Don't wrap `config.get` or the tuple building in `try/except`. Library-native failures should raise, and the standards say to catch once at the job boundary.
- Keep `selected_stages` returning a tuple in `KNOWN_STAGES` order. It is immutable, and `test_selected_stages_filters_to_known` depends on the ordering.
- Keep the module constants as they are. They are immutable and not mutable global state.
- Don't add a helper or library for the two resolvers. Two similar lines don't justify an abstraction. Only the single resolved-config object from finding 2 is warranted.
```

## Rationalizations observed (manual notes)

- Unchecked difference: the truthiness finding went from "F1. Blocking" to "1. Should-fix". The classification rule puts a standards violation at Should-fix, so this matches the rule. Does not weaken a rule.
