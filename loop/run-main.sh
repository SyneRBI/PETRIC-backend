#!/usr/bin/env bash
set -euo pipefail
pushd /w/PETRIC

source /o/petric-setup.sh

curl -fsSL https://raw.githubusercontent.com/SyneRBI/PETRIC/main/petric.py > petric.py
timeout 2h python -B ../petric-run.py

echo "stopping jobs"
for i in $(jobs -p); do kill -n 15 $i; done 2>/dev/null
popd
