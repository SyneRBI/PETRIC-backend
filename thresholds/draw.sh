#!/usr/bin/env bash
set -euo pipefail
pushd /tmp
curl -fsSLO https://raw.githubusercontent.com/SyneRBI/PETRIC2/main/petric.py
mkdir SIRF_data_preparation
pushd SIRF_data_preparation
touch __init__.py
curl -fsSLO https://raw.githubusercontent.com/SyneRBI/PETRIC2/main/SIRF_data_preparation/dataset_settings.py
popd
popd
PYTHONPATH="/tmp${PYTHONPATH:+:$PYTHONPATH}" python -B draw.py
