# pin to https://github.com/SyneRBI/SIRF-SuperBuild/commit/60ffabee4a98bf5697145d81d3bc3fa568251d6c
FROM ghcr.io/synerbi/sirf@sha256:04e7cfabbdc1955e66998c127eaead5d62e2648157ad130112ad29689046123e AS sirf
RUN conda install -y tensorboard tensorboardx jupytext && conda clean -afy
RUN pip install --no-cache-dir git+https://github.com/Project-MONAI/MONAI@1.5.1 torch tensorflow[and-cuda]==2.20 --extra-index-url https://download.pytorch.org/whl/cu128
RUN pip install --no-cache-dir git+https://github.com/TomographicImaging/Hackathon-000-Stochastic-QualityMetrics

FROM continuumio/miniconda3:latest AS leaderboard
RUN conda install -y tensorboard && conda clean -afy
RUN pip install tensorboard-plugin-3d
