# standards-config-log-masking — skill-logmask-after

- Date: 2026-10-18
- Model: sonnet
- Skill file: skills/coding-standards/SKILL.md
- Scenario: tests/scenarios/coding-standards/02-config-log-masking.md

## Checks

| Result | Check |
|---|---|
| PASS | file_exists glob='job_config.py' |
| PASS | file_matches pattern='(?i)\\blog' glob='job_config.py' |
| PASS | file_matches pattern='(?i)mask|redact|\\*{3}' glob='job_config.py' |
| PASS | file_matches pattern='(?i)assertNotIn\\(|\\bnot in\\b' glob='test_*.py' |

## Tool calls

- Read: `/Users/apollo/projects/code-craft/skills/security-baseline/SKILL.md`
- Read: `/Users/apollo/projects/code-craft/skills/test-driven-development/SKILL.md`
- Write: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-standards-config-log-masking-wd0oundz/test_job_config.py`
- Bash: `cat > test_job_config.py <<'EOF'
import dataclasses
import logging
import uuid
from typing import Mapping

import pytest

from job_config import JobConfig, load`
- Bash: `python3 -m venv /tmp/jc-venv && /tmp/jc-venv/bin/pip install -q pytest 2>&1 | tail -2; /tmp/jc-venv/bin/python -m pytest -q 2>&1 | tail -8`
- Bash: `curl -s https://pypi.org/pypi/pytest/json | python3 -c "
import sys,json
d=json.load(sys.stdin);i=d['info']
print(i['name'],i['version'],i['home_page'] or i['pr`
- Bash: `python3 -m venv /tmp/jc-venv && /tmp/jc-venv/bin/pip install -q pytest==9.1.1`
- Bash: `cat > test_job_config.py <<'EOF'
import dataclasses
import logging
import unittest
import uuid
from typing import Mapping

from job_config import JobConfig, loa`
- Bash: `python3 -m unittest -q 2>&1 | head -8`
- Write: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-standards-config-log-masking-wd0oundz/job_config.py`
- Bash: `python3 -m unittest -q 2>&1 | tail -15; awk 'length>120{print FILENAME": "FNR": "length}' job_config.py test_job_config.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-standards-config-log-masking-wd0oundz/job_config.py`
- Bash: `python3 -m unittest -q 2>&1 | tail -4; awk 'length>120{print FILENAME": "FNR": "length}' job_config.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-standards-config-log-masking-wd0oundz/job_config.py`
- Bash: `python3 -m unittest -q 2>&1 | tail -4; awk 'length>120{print FILENAME": "FNR": "length}' job_config.py`

## Final response (truncated)

```
I wrote `job_config.py` and `test_job_config.py`, and all 11 tests pass with `python3 -m unittest`.

**Tests use `unittest`, not pytest.** pytest isn't installed here. The supply-chain gate blocked `pip install`, even though I checked the package on PyPI (first upload 2016, latest release 9.1.1). I used the standard library rather than get around the gate. If you want pytest, approve the install and I'll port the tests.

**Test order.** I ran the tests first and they failed on the missing module, then wrote the implementation.

**How it resolves config.** `load_job_config(env)` is the only place that applies defaults and validation. It returns a frozen `JobConfig` and reads nothing else from the environment.
- **Required settings:** `EXPORT_DB_URL` and `EXPORT_DB_PASSWORD` must be present and non-empty, or it raises `ValueError` naming the variable.
- **Batch size:** `EXPORT_BATCH_SIZE` defaults to 500 and must be a positive integer.
- **Dry run:** `EXPORT_DRY_RUN` defaults to false and accepts only `true` or `false`, case-insensitive. Values like `yes` and `1` are rejected on purpose, since a typo should not silently turn dry-run off.

**Logging.** It logs two structured records, `job config raw` and `job config resolved`.
- **Raw log:** it holds only the `EXPORT_*` keys from the mapping, so unrelated environment variables never reach the log. The password is masked, as is any credential inside the URL.
- **Resolved log:** it uses the same masking, so the log shows exactly what will run.
- **URL masking:** the password in `user:pw@host` becomes `***`. So do query parameters named `password`, `passwd`, `pwd`, `secret`, `token` and `sslpassword`.
- **`repr`:** `repr(JobConfig)` hides both `db_url` and `db_password`.

A test uses random canary values for both secrets and checks they appear in no log record, including its extras.

**Not covered.**
- Only the query-parameter names listed above are masked. A secret under another parameter name would be logged.
- No test covers a URL that is malformed beyond what `urlsplit` tolerates.
- I haven't committed anything. This directory isn't a git repo.
```

## Rationalizations observed (manual notes)

- All checks pass on the new wording with no conflict reported: "Raw log: … The password is masked, as is any credential inside the URL." and "Resolved log: it uses the same masking, so the log shows exactly what will run." A test asserts random canary secrets appear in no log record (one sample).
