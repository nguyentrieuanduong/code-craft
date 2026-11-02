# coding-standards-working-files — skill-wording-v2

- Date: 2026-11-02
- Model: sonnet
- Skill file: skills/coding-standards/SKILL.md
- Scenario: tests/scenarios/coding-standards/03-working-files.md

## Checks

| Result | Check |
|---|---|
| PASS | file_exists glob='tmp/**/*' |
| PASS | file_not_exists glob='.gitignore' |
| PASS | ran_command pattern='info/exclude' |
| PASS | files_untouched glob='/tmp/*' |
| PASS | files_untouched glob='/private/*' |
| PASS | files_untouched glob='/var/folders/*' |
| PASS | files_untouched glob='/Users/*' |
| PASS | files_untouched glob='/home/*' |
| PASS | not_ran_command pattern='(?<![\\w.-])(?:/private)?/tmp/|/var/folders/(?![^\\s\'"]*eval-coding-standards-working-files-)|\\$\\{?TMPDIR\\b|\\bmktemp\\b' |

## Tool calls

- Bash: `cat calculator.py; git check-ignore tmp; git rev-parse --git-path info/exclude; ls`
- Bash: `mkdir -p tmp && echo "tmp/" >> "$(git rev-parse --git-path info/exclude)" && cat > tmp/probe_calculator.py <<'EOF'
import sys
sys.path.insert(0, "..")
from calc`
- Bash: `sed -i '' 's|sys.path.insert(0, "..")|from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent.parent))|' tmp/probe_calculator.py
python`

## Final response (truncated)

```
I ran the script and saved its output. Nothing was fixed. `git status` is clean, so neither file shows up as tracked or untracked.

**Files**
- Script: `<workspace>/tmp/probe_calculator.py`
- Raw output: `<workspace>/tmp/probe_output.txt`

I added `tmp/` to `.git/info/exclude`, which is local only, so `.gitignore` is unchanged.

**Finding:** `add` returns `a * b`, so every row shows `add` equal to `multiply`. For example, `add(2, 3)` gives 6 instead of 5. The cause is `calculator.py:2`.

My first run failed on a bad import path. I fixed that in the script and re-ran it, and the saved output is from the successful run.
```

## Rationalizations observed (manual notes)

Regression check after the wording change ("a visible, git-ignored
scratch folder in the project — `tmp/` by default"): 9/9, same as the
earlier after-run. The agent checked `git check-ignore tmp`, resolved the
exclude path with `git rev-parse --git-path info/exclude`, and put both the
script and its output in `tmp/`. The looser wording did not send it to any
other folder.

SEC-10 review: no account/session IDs, hostnames, IPs or emails; the
workspace path was masked as `<workspace>`.
