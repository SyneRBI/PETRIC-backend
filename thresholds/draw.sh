#!/usr/bin/env bash
set -euo pipefail
curl -fsSL https://raw.githubusercontent.com/SyneRBI/PETRIC2/main/petric.py > /tmp/petric.py
PYTHONPATH="/tmp${PYTHONPATH:+:$PYTHONPATH}" PETRIC_SKIP_DATA=1 python -B draw.py
