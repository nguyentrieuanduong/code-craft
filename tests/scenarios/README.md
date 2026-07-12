# Skill eval scenarios

Pressure-test corpus for the suite's skills, per `writing-skills`: a skill
change is code, and this directory holds its tests. Each scenario is a
realistic task with combined pressures (time, sunk cost, authority) and
machine-checkable assertions encoding the **target** behavior.

## Layout

```
tests/scenarios/
  <skill-name>/NN-<slug>.md   # scenarios for that skill
  fixtures/<name>/            # workspace templates (copied per run)
  results/                    # eval evidence, committed (see CONTRIBUTING.md)
  run.py                      # headless runner (stdlib only)
```

## Scenario format

```markdown
---
name: unique-scenario-name
skill: skills/<name>/SKILL.md      # repo-relative, injected in the skill arm
fixture: py-calculator             # optional, dir under fixtures/
setup: bash setup.sh large         # optional, runs in the workspace
max_turns: 30                      # optional
---

## Prompt
<the user message, written with 3+ pressures; force action, not description>

## Checks
```json
[{"type": "output_matches", "pattern": "(?i)split"}, ...]
```

## Notes
<expected baseline failure, which recommendation the checks encode, pressures used>
```

Frontmatter values are single-line. Check types:

| Type | Args | Passes when |
|---|---|---|
| `output_matches` / `output_not_matches` | `pattern` | final response text matches / doesn't |
| `file_exists` / `file_not_exists` | `glob` (workspace-relative) | a matching file exists / doesn't |
| `file_matches` / `file_not_matches` | `glob`, `pattern` | some matching file's content matches / none does |
| `anywhere_matches` | `glob`, `pattern` | final text OR a matching file matches |
| `ran_command` / `not_ran_command` | `pattern` | some Bash command matches / none does |
| `test_written_before_source` | `test_glob`, `source_glob` | first Write/Edit to a test file precedes any to source |
| `files_untouched` | `glob` | no Write/Edit touched a matching path |

Checks encode the **target** behavior. A baseline (no-skill) run is expected
to violate them — that is the RED evidence. A skill run must pass all of
them. Scenarios written for a pending wording change (marked in Notes) are
the failing-test-first for that edit: RED with current wording, GREEN after.

## Running

```bash
python3 tests/scenarios/run.py --dry-run                 # validate corpus
python3 tests/scenarios/run.py --arm both                # full RED/GREEN run
python3 tests/scenarios/run.py tests/scenarios/finishing-work/01-*.md \
    --arm skill --label current                          # one scenario

# A/B wording eval: current wording vs edited wording
python3 tests/scenarios/run.py tests/scenarios/finishing-work/*.md \
    --arm skill --label before
python3 tests/scenarios/run.py tests/scenarios/finishing-work/*.md \
    --arm skill --skill-override /tmp/finishing-work-edited.md --label after
```

Requirements and caveats:

- Needs the `claude` CLI. The agent under test executes model-chosen shell
  commands inside a disposable temp workspace — keep fixtures self-contained
  and review a scenario before running it.
- **Contamination:** if the code-craft plugin (or any always-on skill setup)
  is installed globally, it leaks into baseline arms. Use `--isolate` (fresh
  `CLAUDE_CONFIG_DIR`; requires `ANTHROPIC_API_KEY`) or run on a profile
  without the plugin.
- The suite targets lower-capability models: run evals with `--model sonnet`
  and `--model haiku`, not only the default.
- One rep per arm is a smoke signal, not proof — writing-skills prescribes
  5+ reps for wording micro-tests. State the rep count in the results file.
- In-session alternative: dispatch fresh subagents with the scenario prompt
  (skill text pasted in for the skill arm) and apply the checks manually —
  same corpus, same results convention.

## Results convention

`results/YYYY-MM-DD-<scenario>-<arm>[-<label>].md`, committed to the repo.
The runner writes the check table, tool-call list, and truncated final
response; fill in the "Rationalizations observed" section by hand after
reading the transcript — verbatim quotes are what feed rationalization
tables (see `writing-skills`).

Runner internals are regression-tested in `tests/test_scenarios.py` (no API
calls); run `python3 -m unittest discover tests`.
