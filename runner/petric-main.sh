#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")"/petric-setup.sh

curl -fsSL https://raw.githubusercontent.com/SyneRBI/PETRIC/main/petric.py > petric.py
timeout 2h python -B petric.py

echo "stopping jobs"
for i in $(jobs -p); do kill -n 15 $i; done 2>/dev/null
