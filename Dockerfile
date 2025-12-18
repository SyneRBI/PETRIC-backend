# pin to https://github.com/SyneRBI/SIRF-SuperBuild/commit/60ffabee4a98bf5697145d81d3bc3fa568251d6c
FROM ghcr.io/synerbi/sirf@sha256:04e7cfabbdc1955e66998c127eaead5d62e2648157ad130112ad29689046123e AS sirf
RUN conda install -y tensorboard tensorboardx jupytext && conda clean -afy
RUN pip install --no-cache-dir git+https://github.com/Project-MONAI/MONAI@1.5.1 torch tensorflow[and-cuda]==2.20 --extra-index-url https://download.pytorch.org/whl/cu128
RUN pip install --no-cache-dir git+https://github.com/TomographicImaging/Hackathon-000-Stochastic-QualityMetrics
RUN echo 'cuda-version 12.8.*' >> "${CONDA_DIR}/conda-meta/pinned"
COPY <<apt-install.sh /usr/local/bin/start-notebook.d
if test \$UID -eq 0 -a -f apt.txt; then
  apt-get update
  xargs -a apt.txt apt-get install -y
fi
apt-install.sh
COPY <<15source-sirf.sh <<25conda-pip-install.sh <<35gadgetron.sh /usr/local/bin/before-notebook.d/
source /opt/SIRF-SuperBuild/INSTALL/bin/env_sirf.sh
15source-sirf.sh
if test -f environment.yml; then
  sed -i '/^name:.*/d' environment.yml
  if test \$UID -eq 0; then
    sudo --preserve-env --set-home --user "${NB_USER}" mamba env update -n base -f environment.yml
  else
    mamba env update -n base -f environment.yml
  fi
fi
if test -f requirements.txt; then
  if test \$UID -eq 0; then
    sudo --preserve-env --set-home --user "${NB_USER}" pip install -r requirements.txt
  else
    pip install -r requirements.txt
  fi
fi
25conda-pip-install.sh
pushd /opt/SIRF-SuperBuild
test -x ./INSTALL/bin/gadgetron && ./INSTALL/bin/gadgetron >& ~/gadgetron.log&
popd
35gadgetron.sh

FROM continuumio/miniconda3:latest AS leaderboard
RUN conda install -y tensorboard && conda clean -afy
RUN pip install tensorboard-plugin-3d
