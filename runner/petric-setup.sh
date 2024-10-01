#!/usr/bin/env bash
set -euo pipefail

# ROOT commands

if test $UID -eq 0; then
  if test -f apt.txt; then
    apt-get update
    xargs -a apt.txt apt-get install -y
  fi

  # change NB_USER primary GID
  OLD_GID=$(id -g "$NB_USER")
  groupadd -g $RUNNER_GID runner
  usermod -g runner "$NB_USER"
  usermod -aG $OLD_GID "$NB_USER"

  exec su -w GITHUB_REPOSITORY,GITHUB_REF_NAME "$NB_USER" "$0" -- "$@"
  exit 0 # technically not required as `exec` replaces the running process
fi

# NB_USER commands

export PATH="/opt/conda/bin:$PATH"
set +u
source /opt/SIRF-SuperBuild/INSTALL/bin/env_sirf.sh
set -u

if test -f environment.yml; then
  sed -i '/^name:.*/d' environment.yml
  conda env update -n base
fi
if test -f requirements.txt; then
  pip install -r requirements.txt
fi

SB_PATH=$(dirname "$(dirname "$SIRF_PATH")")
echo "start gadgetron"
pushd "${SB_PATH}"
test -x ./INSTALL/bin/gadgetron && ./INSTALL/bin/gadgetron >& ~/gadgetron.log&
popd
