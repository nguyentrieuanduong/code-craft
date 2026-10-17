# standards-inline-vs-implicit — skill-bench1

- Date: 2026-10-17
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
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-standards-inline-vs-implicit-l9usa_pi/settings.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-standards-inline-vs-implicit-l9usa_pi/test_settings.py`
- Bash: `python3 -I -c "
from settings import *
print(resolve_retries({'retries':0}), resolve_timeout({'timeout':0}), resolve_timeout({'timeout':None}), resolve_timeout(`
- Bash: `PYTHONPATH=. python3 -c "
from settings import *
print(resolve_retries({'retries':0}), resolve_timeout({'timeout':0}), resolve_timeout({'timeout':None}), resolv`

## Final response (truncated)

```
Diff: 22 changed lines in `settings.py` (46 with tests; no git repo, so counted with `wc -l`) — 2 actionable findings.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: I ran `python3 -m unittest` myself: 5 tests, OK. The author supplied none.
Merge readiness: not ready — F1 is Blocking

Verdicts
- Spec compliance: FAIL. No design was supplied. By reasonable expectation, an explicit `0` should not be silently replaced.
- Code quality: FAIL. `or` is a truthiness trick, which the standards prohibit. The tests have no worst cases.
- Security: PASS — no security findings. The module does no I/O, parsing or secrets handling.
- Security pass: inline fallback

Findings
F1. Blocking — `settings.py:9` and `settings.py:13` — `config.get(...) or DEFAULT` treats `0`, `""` and `None` as "unset". Run against the file: `resolve_retries({"retries": 0})` returned `3`, so retries cannot be disabled. `resolve_timeout({"timeout": 0})` returned `30`, and `""` also returned `30`. Fix: use `DEFAULT_RETRIES if config.get("retries") is None else config["retries"]`, and the same for timeout. Add tests for `retries=0` and `timeout=0`. The existing tests only cover the absent and positive cases, which is why the suite stays green.

F2. Should-fix — `settings.py:17` — `stage in config.get("stages", ...)` does substring matching when `stages` is a string. `selected_stages({"stages": "build,deploy"})` returned `('build', 'deploy')`. `{"stages": "test"}` happens to work only by accident. Accepting a string is a boundary-validation gap. Fix: reject non-list/tuple `stages` once, where the config is parsed. Do not wrap the call in `try/except`.

Pre-existing
None

Nits
- Defaults are applied in three separate functions and `describe` re-derives them. Once F1 is fixed, consider a single frozen `Settings` dataclass built by one `parse(config)` function, per the single-resolution-point standard. That is a suggestion, not a blocker at this size.
- None of the functions have type hints, which the standards require.

Declined to judge
- `selected_stages({"stages": None})` raises `TypeError: argument of type 'NoneType' is not iterable`. That is a natural library failure and the standards say to let it raise. Whether `None` should mean "all stages" is a design question for the author.

**Must not change in this PR:**
- Don't add `try/except` or `None` guards around library-native failures.
- Don't swap `or` for another truthiness idiom. Use an explicit `is None` check.
- Keep `selected_stages` returning a `tuple` in `KNOWN_STAGES` order. That keeps it immutable and deterministic, and the existing test relies on it.
- Keep `KNOWN_STAGES` as the single source of truth, and keep the existing 5 tests as they are.
```

## Rationalizations observed (manual notes)

None observed. `or`-default flagged with an executed counterexample: "`resolve_retries({\"retries\": 0})` returned `3`".
