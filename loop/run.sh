#!/usr/bin/env bash
set -euo pipefail
# PETRIC
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
# PETRIC2
submissions=(
Casper@MaGeZ
Beavers@pwals_SI_prov
Beavers@qntrnar_SI_prov
Beavers@qntrnar_utb3
PATRIC@kernels
PATRIC@kernelVOIs
Speedy@pd1
Speedy@pd2
Speedy@psv
SRDP@testrun
Storm-PET@algorithm-1
Storm-PET@algorithm-2
Storm-PET@algorithm-3
TARTARUGA@gssb
TARTARUGA@gssb1
)
test -d PETRIC || git clone git@github.com:SyneRBI/PETRIC2 PETRIC

export NB_GID=$(getent group runner | cut -d: -f3)
for sub in "${submissions[@]}" ; do
  team=$(echo $sub | cut -d '@' -f1)
  tag=$(echo $sub | cut -d '@' -f2)
  git -C PETRIC remote add $team git@github.com:SyneRBI/PETRIC2-$team || :
  git -C PETRIC fetch --tags $team $tag -f
  git -C PETRIC checkout $tag

  sudo chgrp -Rc $NB_GID PETRIC
  sudo chmod -Rc g+w PETRIC
  docker run --rm --gpus all -u root -e NB_GID --no-healthcheck -e GITHUB_REPOSITORY=SyneRBI/PETRIC2-$team -e GITHUB_REF_NAME=$(git -C PETRIC describe --tags) \
    -e TQDM_MININTERVAL=1 \
    -e NUMEXPR_MAX_THREADS=24 \
    -e PETRIC_SKIP_DATA=1 \
    -e PETRIC_SRCDIR=/mnt/share/petric/2 \
    -v /mnt/share-public/petric:/mnt/share/petric:ro \
    -v /opt/runner/logs/2:/logs:rw \
    -v .:/w:rw -w /w/PETRIC \
    ghcr.io/synerbi/sirf:petric2 /w/run-main.sh \
    ../petric-run.py
  git -C PETRIC restore .
done
