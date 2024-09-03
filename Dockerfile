FROM synerbi/sirf:edge-gpu AS sirf
RUN conda install -y tensorboard tensorboardx jupytext
RUN pip install git+https://github.com/TomographicImaging/Hackathon-000-Stochastic-QualityMetrics

FROM caddy:2.8.4-builder-alpine AS builder
RUN xcaddy build \
  --with github.com/mholt/caddy-webdav
FROM wemakeservices/caddy-gen:1.0.0 AS caddy-gen
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
