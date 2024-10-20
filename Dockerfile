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
