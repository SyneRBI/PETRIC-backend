# FROM synerbi/sirf:edge-gpu AS sirf
# pin to https://github.com/SyneRBI/SIRF-SuperBuild/commit/5f1a7f498bf6f41551c19eb53798b5d33af43eec
FROM ghcr.io/synerbi/sirf@sha256:2ef963a861bf18346da511d80c3a15eb7f154131224367a2c66578101602c6e0 AS sirf
# monai installs torch, so uninstall it
RUN conda install -y monai tensorboard tensorboardx jupytext && pip uninstall -y torch && conda clean -afy
RUN conda install -y cudatoolkit=11.8 && conda clean -afy
#RUN conda install -y -c conda-forge -c nvidia tensorflow-gpu=2.14 && conda clean -afy
RUN pip install --no-cache-dir tensorflow[and-cuda]==2.14
#RUN conda install -y -c pytorch -c nvidia pytorch pytorch-cuda=11.8 && conda clean -afy
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cu118
#RUN pip install --no-cache-dir tensorflow[and-cuda]==2.14 torch --extra-index-url https://download.pytorch.org/whl/cu118
RUN pip install --no-cache-dir git+https://github.com/TomographicImaging/Hackathon-000-Stochastic-QualityMetrics

FROM continuumio/miniconda3:latest AS leaderboard
RUN conda install -y tensorboard && conda clean -afy
RUN pip install tensorboard-plugin-3d

FROM caddy:2.8.4-builder-alpine AS builder
RUN xcaddy build \
  --with github.com/mholt/caddy-webdav
FROM wemakeservices/caddy-gen:1.0.0 AS caddy-gen
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
ARG CADDY_UID=0
ARG CADDY_GID=0
RUN chown -R $CADDY_UID:$CADDY_GID /code/docker-gen/templates/Caddyfile.tmpl /etc/caddy
RUN chmod a+x /usr/bin/forego
USER $CADDY_UID:$CADDY_GID
