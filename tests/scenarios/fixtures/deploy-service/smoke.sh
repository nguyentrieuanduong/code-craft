#!/usr/bin/env bash
# Fake post-deploy smoke checks: reads the fake deploy state, reports healthy.
set -euo pipefail
if [[ ! -f deploy_log.txt ]]; then
  echo "smoke: nothing deployed yet" >&2
  exit 1
fi
echo "smoke: checking login, checkout, refund against: $(tail -1 deploy_log.txt)"
echo "smoke: 3/3 endpoints healthy; error rate 0.02% (baseline 0.02%)"
