#!/usr/bin/env bash
set -euo pipefail
curl -fsSLO https://raw.githubusercontent.com/SyneRBI/PETRIC2/main/petric.py
curl -fsSL https://raw.githubusercontent.com/SyneRBI/PETRIC2/main/SIRF_data_preparation/dataset_settings.py -o SIRF_data_preparation/dataset_settings.py
PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}" python -B "$@"
