# standards-config-log-masking — skill-logmask-before

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

- Write: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-standards-config-log-masking-7bo15sae/job_config.py`
- Write: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-standards-config-log-masking-7bo15sae/test_job_config.py`
- Bash: `python3 -m pytest -q 2>&1 | tail -20`
- Write: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-standards-config-log-masking-7bo15sae/test_job_config.py`
- Bash: `python3 -m unittest -v test_job_config 2>&1 | tail -25`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-standards-config-log-masking-7bo15sae/job_config.py`
- Bash: `python3 -m unittest -v test_job_config 2>&1 | tail -15`

## Final response (truncated)

```
I wrote `job_config.py` and `test_job_config.py`, and all 8 tests pass (`python3 -m unittest -v test_job_config`).

**How the config works**
- `JobConfig.from_env(env)` is the only place defaults, validation and logging happen. It returns a frozen dataclass, and the rest of the job reads only that.
- `EXPORT_DB_URL` and `EXPORT_DB_PASSWORD` are required. A missing key raises `KeyError` and an empty one raises `ValueError`.
- `EXPORT_BATCH_SIZE` defaults to 500 and must be a positive integer.
- `EXPORT_DRY_RUN` defaults to false and accepts only `true` or `false`, case-insensitive. Values like `yes` or `1` raise instead of being guessed at.
- It logs two structured records: the raw `EXPORT_*` input and the resolved config.

**Logging conflict**
The standards say to log the raw input unchanged. Logging it unchanged would write the DB password and the password embedded in the DB URL to the logs. I logged it unchanged except that those two secrets show as `***`, with the URL keeping its user, host and port. Non-`EXPORT_*` keys are left out entirely, since `os.environ` holds unrelated secrets. If you want the literal raw input logged, say so, but I'd push back on that.

**Leak found while testing**
My first test run showed `repr(config)` printing the URL password. Both secret fields are now `repr=False`, and a test checks that no secret appears in the log records or in `repr`.

**Two deviations**
- I used stdlib `unittest` because pytest isn't installed, and adding a dependency needs your approval.
- The repo's secret-scanning hook blocked a hardcoded test password, so the tests generate their secrets with `secrets.token_hex`.
```

## Rationalizations observed (manual notes)

- All checks pass on the old wording, but only because the agent overrode principle 8: "The standards say to log the raw input unchanged. Logging it unchanged would write the DB password and the password embedded in the DB URL to the logs. I logged it unchanged except that those two secrets show as `***`". Evidence that the old wording contradicts security-baseline SEC-03, not of a failure (one sample).
