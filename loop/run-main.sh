#!/usr/bin/env bash
set -euo pipefail
curl -fsSLO https://raw.githubusercontent.com/SyneRBI/PETRIC2/main/petric.py
PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}" PETRIC_SKIP_DATA=1 python -B "$@"
