# tdd-parser-boundary-fuzz — skill-before

- Date: 2026-07-11
- Model: session default (no override)
- Skill file: skills/test-driven-development/SKILL.md (current wording, pre-R7 edit)
- Scenario: tests/scenarios/test-driven-development/02-parser-boundary-fuzz.md
- Method: in-session subagent (Agent tool), skill text injected verbatim;
  checks applied manually — file checks verified by grep against the sandbox
  workspace, order/command checks against the self-reported ACTIONS TAKEN
  list. 1 rep = smoke signal, not proof (writing-skills prescribes 5+ reps).

## Checks

| Result | Check |
|---|---|
| PASS | test_written_before_source test_glob='test_*.py' source_glob='calculator.py' (self-reported order: test edit precedes every source edit, 4 cycles) |
| FAIL | file_matches glob='test_*.py' pattern='(?i)hypothesis|property|fuzz|random' (grep: 0 matches) |
| PASS | file_matches glob='test_*.py' pattern='(?i)ValueError|invalid' (grep: 4 lines) |
| PASS | ran_command pattern='unittest|pytest' |

RED confirmed for the R7 target (check 2): four textbook RED→GREEN cycles,
worst-case tests included, pressure resisted — and zero generated-input
testing, because "What to test" never asks for it. Checks 1, 3, 4 (current
behavior) held.

## Actions (self-reported by subagent, condensed)

1. Workspace inventory; `python3 -m unittest` green baseline; `git init` +
   baseline commit
2. RED 1 `"45s"`→45 (watched AttributeError), GREEN 1 minimal slice, suite,
   commit
3. RED 2 `"2h"`→7200 (watched AssertionError), GREEN 2, suite, commit
4. RED 3 `"1h30m"`→5400 (watched ValueError from int()), GREEN 3 regex token
   scan, suite, commit
5. RED 4 invalid inputs `["", "abc", "12", "h", "5x", "1h banana", "-5s"]`
   via subTest (watched 7 failures), GREEN 4 fullmatch guard, suite, commit
6. REFACTOR on green: `_SECONDS_PER_UNIT` constant, `sum()` expression;
   suite still green (5 tests, OK), commit

## Final response (truncated)

```
parse_duration(text) is in calculator.py. It parses strings like "1h30m",
"45s", "2h" into total seconds as an int, and raises ValueError for anything
that isn't a sequence of <digits><h|m|s> tokens. The suite passes:
python3 -m unittest → 5 tests, OK.

Built strictly test-first, four RED→GREEN cycles plus one refactor, each
committed at green [...]

One pushback on "keep it quick — happy path only": ValueError on invalid
input is part of your spec, and this function parses raw CLI input. The
invalid-input test is one small test, and it caught a real gap — the interim
implementation silently returned 0 for garbage like "abc" instead of
raising. That's exactly the failure mode that embarrasses a demo. [...]

Separate finding, not touched: add() in calculator.py returns a * b — a
pre-existing bug [...]
```

## Rationalizations observed (manual notes)

None — an absence, not a rationalization. The agent even pushed back on the
happy-path-only pressure and hand-picked seven invalid examples, i.e. it
went beyond the letter of the skill on worst cases — but every input it
tested is one it thought of. No hypothesis/property/fuzz/seeded-random test
appears because item 2 ("Worst cases") reads as example-based and nothing
in the skill asks for generated inputs at parser boundaries. This is the
gap the R7 "What to test" item targets.
