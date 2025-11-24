# pin to https://github.com/SyneRBI/SIRF-SuperBuild/commit/5f1a7f498bf6f41551c19eb53798b5d33af43eec
#FROM ghcr.io/synerbi/sirf@sha256:2ef963a861bf18346da511d80c3a15eb7f154131224367a2c66578101602c6e0 AS sirf
# pin to https://github.com/SyneRBI/SIRF-SuperBuild/pull/946
FROM ghcr.io/synerbi/sirf:petric2-base AS sirf
RUN conda install -y tensorboard tensorboardx jupytext && conda clean -afy
RUN pip install --no-cache-dir git+https://github.com/Project-MONAI/MONAI@1.5.1 torch tensorflow[and-cuda]==2.20 --extra-index-url https://download.pytorch.org/whl/cu128
RUN pip install --no-cache-dir git+https://github.com/TomographicImaging/Hackathon-000-Stochastic-QualityMetrics

FROM continuumio/miniconda3:latest AS leaderboard
RUN conda install -y tensorboard && conda clean -afy
RUN pip install tensorboard-plugin-3d
