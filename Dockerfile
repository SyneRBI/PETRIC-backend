# FROM synerbi/sirf:edge-gpu AS sirf
# pin to https://github.com/SyneRBI/SIRF-SuperBuild/commit/5f1a7f498bf6f41551c19eb53798b5d33af43eec
FROM ghcr.io/synerbi/sirf@sha256:2ef963a861bf18346da511d80c3a15eb7f154131224367a2c66578101602c6e0 AS sirf
RUN conda install -y monai tensorboard tensorboardx jupytext
RUN pip install git+https://github.com/TomographicImaging/Hackathon-000-Stochastic-QualityMetrics

FROM continuumio/miniconda3:latest AS leaderboard
RUN conda install -y tensorboard && conda clean -afy
RUN pip install tensorboard-plugin-3d

FROM caddy:2.8.4-builder-alpine AS builder
RUN xcaddy build \
  --with github.com/mholt/caddy-webdav
FROM wemakeservices/caddy-gen:1.0.0 AS caddy-gen
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
