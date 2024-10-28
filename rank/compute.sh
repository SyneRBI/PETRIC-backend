#!/usr/bin/env bash
set -euo pipefail

source /o/petric-setup.sh

curl -fsSL https://raw.githubusercontent.com/SyneRBI/PETRIC/main/petric.py > /tmp/petric.py
PYTHONPATH="/tmp${PYTHONPATH:+:$PYTHONPATH}" PETRIC_SKIP_DATA=1 python -B compute.py

echo "stopping jobs"
for i in $(jobs -p); do kill -n 15 $i; done 2>/dev/null
