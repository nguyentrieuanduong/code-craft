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

Frontmatter uses strict YAML and supports standard scalar styles. Check types:

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
# Default: deterministic, zero model calls
python3 -m tools.check

# Focused behavior edit: one selected scenario, one sequential call
python3 tests/scenarios/run.py path/to/scenario.md --arm skill --reps 1

# Optional full campaign: explicit and never CI
# 13 scenarios x 2 arms x 5 reps = 130 authorized calls
python3 tests/scenarios/run.py --all --arm both --reps 5 --allow-many 130
```

`Agent` and `Task` are disabled inside the runner. A focused before/after pair
is capped at two calls unless numeric `--allow-many N` is at least the printed
planned total.

Model-run caveats:

- Focused and full runs need the `claude` CLI. The agent under test executes
  model-chosen shell
  commands inside a disposable temp workspace — keep fixtures self-contained
  and review a scenario before running it.
- **Contamination:** if the code-craft plugin (or any always-on skill setup)
  is installed globally, it leaks into baseline arms. Use `--isolate` (fresh
  `CLAUDE_CONFIG_DIR`; requires `ANTHROPIC_API_KEY`) or run on a profile
  without the plugin.
- A focused sample is bounded behavioral evidence, not a statistical claim.
  Multi-model and repeated runs belong only to an explicitly authorized full
  campaign.

## Results convention

`results/YYYY-MM-DD-<scenario>-<arm>[-<label>].md`, committed to the repo.
The runner writes the check table, tool-call list, and truncated final
response; fill in the "Rationalizations observed" section by hand after
reading the transcript — verbatim quotes are what feed rationalization
tables (see `writing-skills`).

Runner internals are regression-tested in `tests/test_scenarios.py` (no API
calls); run `python3 -m unittest discover tests`.
