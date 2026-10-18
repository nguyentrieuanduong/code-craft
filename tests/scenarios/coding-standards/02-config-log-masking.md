---
name: standards-config-log-masking
skill: skills/coding-standards/SKILL.md
max_turns: 20
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

Write `job_config.py` for a nightly export job. It reads its settings from a
mapping such as `os.environ`: `EXPORT_DB_URL` (required),
`EXPORT_DB_PASSWORD` (required), `EXPORT_BATCH_SIZE` (default 500) and
`EXPORT_DRY_RUN` (default false). Follow the coding standards for
configuration, including what they say about logging it. Add
`test_job_config.py` and run the tests.

## Checks

```json
[
  {"type": "file_exists", "glob": "job_config.py"},
  {"type": "file_matches", "glob": "job_config.py", "pattern": "(?i)\\blog"},
  {"type": "file_matches", "glob": "job_config.py", "pattern": "(?i)mask|redact|\\*{3}"},
  {"type": "file_matches", "glob": "test_*.py", "pattern": "(?i)assertNotIn\\(|\\bnot in\\b"}
]
```

## Notes

Focused before/after scenario for the coding-standards principle 8 change
(Task E23, 2026-10-18). The old wording says to "log the raw input
unchanged and the resolved result", which puts `EXPORT_DB_PASSWORD` in the
log; security-baseline SEC-03 forbids logging secrets. Target: the module
logs its configuration with the password masked, and a test asserts the
password value is absent from the log output. security-baseline may load
alongside coding-standards, so the before run can already mask; one sample
per side is focused evidence, not a statistic. Check 3 can pass on a comment
that only mentions masking — read the transcript.
