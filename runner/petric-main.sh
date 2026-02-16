#!/usr/bin/env bash
set -euo pipefail
curl -fsSLO https://raw.githubusercontent.com/SyneRBI/PETRIC2/main/petric.py
timeout 2h python -B petric.py
