FROM synerbi/sirf:edge-gpu
RUN conda install -y tensorboard tensorboardx jupytext
RUN pip install git+https://github.com/TomographicImaging/Hackathon-000-Stochastic-QualityMetrics
