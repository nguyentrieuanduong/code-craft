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
  run.py                      # headless runner
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
| `test_written_before_source` | `test_glob`, `source_glob` | first write to a test file precedes any to source. Writes are Write/Edit calls or Bash writes the runner can read: redirection, `tee`, `cp`/`mv`/`install`/`ln` (last argument), `touch`, `truncate`, `dd of=`, `sed -i`, `perl -i`, and Python `open(…)` in a writing mode or `.write_text` in code that runs (`python -c`, a heredoc fed to python), with a literal or literal-assigned path; `bash -c`/`sh -c` strings and `sudo`/`env` wrappers are unwrapped, and a word starting with `#` ends the line as a comment. Other writers (patch, git apply, rsync, shutil), writes behind backticks, and writes inside nested double quotes within a multi-line `$( … )` are not seen. NOT EVALUATED when a write names a matching file but its target cannot be read, or one command writes both; a NOT EVALUATED check does not count as failed |
| `files_untouched` | `glob` | no Write/Edit touched a matching path |
| `report_matches` / `report_not_matches` | `field` or `section`, `pattern`, optional `severity` (section only) | the code-review report parsed from the final text has a field value / a section item matching `pattern` (case-insensitive) — or, for the `_not_` form, does not; both fail when no report is found. Fields: the template labels plus derived `changed lines` and `actionable`; sections: findings, pre-existing, nits, declined to judge. See `parse_report` in `run.py` |
| `report_actionable_count` | none | the report's `actionable` count (digits or one–ten) equals the open Findings items whose lead names Blocking or Should-fix; items marked addressed, resolved, or fixed are not counted; fails when no count is found |

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

Each run writes two files, both committed to the repo:

- `results/YYYY-MM-DD-<scenario>-<arm>[-<label>].md` — the check table,
  tool-call list, and truncated final response. Fill in the
  "Rationalizations observed" section by hand after reading the transcript
  — verbatim quotes are what feed rationalization tables (see
  `writing-skills`).
- The matching `.evidence.json` — the complete final response and every
  tool input, for comparing runs without truncation.

Before writing either file, the runner replaces text matching the
secret-scan hook's patterns (`hooks/scan-secrets.py`) with
`[REDACTED: <kind>]`, removing a private key block (PEM or PGP) through its END
line.
Patterns miss unknown formats and some known ones: AWS secret access keys,
JWT or Bearer tokens, a key glued to a preceding letter or digit, a secret
split across two strings, and password forms such as `db_password = "..."`
or an unquoted `PASSWORD=...`. Read both files before staging them.
`tests/test_scenarios.py` also fails when any committed result file matches
a secret pattern; it cannot catch the formats listed above.
Results written by anything other than `run.py` are redacted only if that
writer calls `run.redact_secrets`. The scratch Codex driver's 2026-10-17
files (`*-skill-codex-bench1.*`) are not redacted at all. Its 2026-10-18
files (`*-skill-codex-compact1.*`, `*-skill-codex-compact2.*`) pass the final
response through `run.redact_secrets`, with the same patterns and gaps. They
hold no tool-call evidence, so the manual read is still required.

Runner internals are regression-tested in `tests/test_scenarios.py` (no API
calls); run `python3 -m unittest discover tests`.
