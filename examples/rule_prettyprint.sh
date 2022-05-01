#!/usr/bin/env bash

EXAMPLES="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "${EXAMPLES}")"

"${ROOT}/main.py" \
    "${EXAMPLES}/rule.art" \
    --brush none \
    --tick 0 \
    --no-clear \
    --no-iteration \
    | python "${EXAMPLES}/rule_prettyprint.py"
