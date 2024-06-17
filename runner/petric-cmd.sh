#!/usr/bin/env bash
set -euo pipefail

# ROOT commands

if test $UID -eq 0; then
  if test -f apt.txt; then
    apt-get update
    xargs -a apt.txt apt-get install -y
  fi
  exec su "$NB_USER" "$0" -- "$@"
  exit 0 # techincally not required as `exec` replaces the running process
fi

# NB_USER commands

test -f .bashrc && . .bashrc

if test -f environment.yml; then
  conda install --file environment.yml
fi
if test -f requirements.txt; then
  pip install -r requirements.txt
fi

SB_PATH=$(dirname "$(dirname "$SIRF_PATH")")
echo "start gadgetron"
pushd "${SB_PATH}"
test -x ./INSTALL/bin/gadgetron && ./INSTALL/bin/gadgetron >& ~/gadgetron.log&
popd

python /o/petric-full.py

echo "stopping jobs"
for i in $(jobs -p); do kill -n 15 $i; done 2>/dev/null
