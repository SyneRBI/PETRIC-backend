#!/usr/bin/env bash
set -euo pipefail
submissions=(
MaGeZ@ALG3
MaGeZ@ALG2
MaGeZ@ALG1
UCL-EWS@EWS_SAGA
SOS@SAGA_final2
SOS@SVRG_final
Tomo-Unimib@LP_final
UCL-EWS@EWS_GD
UCL-EWS@EWS_SGD
)

test -d PETRIC || git clone git@github.com:SyneRBI/PETRIC

for sub in "${submissions[@]}" ; do
  team=$(echo $sub | cut -d '@' -f1)
  tag=$(echo $sub | cut -d '@' -f2)
  git -C PETRIC remote add $team git@github.com:SyneRBI/PETRIC-$team || :
  git -C PETRIC checkout $tag || git fetch --tags $team
  git -C PETRIC checkout $tag

  sudo chgrp -Rc runner PETRIC
  sudo chmod -Rc g+w PETRIC
  docker run --rm --gpus all -u root --no-healthcheck -e GITHUB_REPOSITORY=SyneRBI/PETRIC-$team -e GITHUB_REF_NAME=$(git -C PETRIC describe --tags) \
    -e TQDM_MININTERVAL=1 \
    -e NUMEXPR_MAX_THREADS=24 \
    -e RUNNER_GID=$(getent group runner | cut -d: -f3) \
    -v /mnt/share-public:/mnt/share:ro \
    -v /opt/runner:/o:rw \
    -v .:/w:rw -w /w \
    synerbi/sirf:ci \
    /w/run-main.sh
  git -C PETRIC restore .
done
