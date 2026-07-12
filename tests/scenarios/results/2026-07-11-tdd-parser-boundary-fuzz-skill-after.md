# tdd-parser-boundary-fuzz — skill-after

- Date: 2026-07-11
- Model: session default (no override)
- Skill file: skills/test-driven-development/SKILL.md (R7 edit: "Input
  boundaries get a fuzz/property test" as What-to-test item 3)
- Scenario: tests/scenarios/test-driven-development/02-parser-boundary-fuzz.md
- Method: in-session subagent (Agent tool), skill text injected verbatim;
  checks applied manually — file checks verified by grep against the sandbox
  workspace plus a fresh suite run, order/command checks against the
  self-reported ACTIONS TAKEN list. 1 rep per wording = smoke signal, not
  proof (writing-skills prescribes 5+ reps).

## Checks

| Result | Check |
|---|---|
| PASS | test_written_before_source test_glob='test_*.py' source_glob='calculator.py' (self-reported order: every cycle test-first) |
| PASS | file_matches glob='test_*.py' pattern='(?i)hypothesis|property|fuzz|random' (grep: 3 lines; seeded `random.Random(20260712)` fuzz test) |
| PASS | file_matches glob='test_*.py' pattern='(?i)ValueError|invalid' (grep: 4 lines) |
| PASS | ran_command pattern='unittest|pytest' |

GREEN: 4/4 (was 3/4 before the edit — see the skill-before file).
Independent verification: `python3 -m unittest` in the sandbox → 7 tests,
OK.

## Actions (self-reported by subagent, condensed)

1. Inventory; probed for `hypothesis` (absent — skill's fallback clause
   used); baseline green; git init + baseline commit
2. Cycles 1–3 (happy paths "45s"/"2h"/"1h30m"), each RED watched → minimal
   GREEN → full suite → commit
3. Cycles 4–5 (no-token garbage, then embedded garbage/decimals/negatives/
   spaces), RED watched → GREEN → commit
4. Cycle 6: seeded fuzz test — 500 constructed-valid inputs vs an
   independent oracle + 2,000 arbitrary printable strings asserting
   parse-or-ValueError; passed immediately (no production code, so no
   iron-law violation), committed
5. REFACTOR on green: derived both regexes from `_SECONDS_PER_UNIT`;
   8 commits total

## Final response (truncated)

```
parse_duration is in calculator.py, built test-first in six RED/GREEN
cycles plus one refactor, each committed. The suite: 7 tests, all passing.

On "keep it quick — happy path": I didn't stop there [...] the error tests
caught real silent-failure modes on the way: before validation existed,
"abc" returned 0, "-5s" returned 5 (sign dropped), and "4.5s" returned 5.
Since this parses raw CLI input, I also added one seeded fuzz test (no
hypothesis installed, so a random.Random(20260712) loop): 500 generated
valid durations must parse to an independently computed total, and 2,000
arbitrary printable strings must either parse or raise ValueError — nothing
else escapes. It passed immediately, which is the point: it's a regression
net [...]
```

## Rationalizations observed (manual notes)

None. The fuzz item fired precisely on its trigger ("this parses raw CLI
input" → "Since this parses raw CLI input, I also added one seeded fuzz
test") and the fallback clause prevented the obvious stall — the agent
probed for `hypothesis`, found it absent, and used the seeded-`random`
path without asking. It asserted exactly the invariant the skill names
(valid shapes parse against an oracle; everything else raises the
documented error). Compared to the before run, the edit added generated-
input coverage on top of (not instead of) the hand-picked worst cases.
