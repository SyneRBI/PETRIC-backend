# FROM synerbi/sirf:edge-gpu AS sirf
# pin to https://github.com/SyneRBI/SIRF-SuperBuild/commit/7b9f703506a652e061e27b8d9b240bd4076e376b
FROM ghcr.io/synerbi/sirf@sha256:a5b000a7a836bdbea06a19bf3acd367e6e2a71401ac7ac8d567b2c6f7c2b4efb AS sirf
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
