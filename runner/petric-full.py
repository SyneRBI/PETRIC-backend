import os
from pathlib import Path
from time import time

import numpy as np
from cil.optimisation.utilities import callbacks as cbks
from cil.optimisation.algorithms import Algorithm
import tensorflow as tf


from main import Submission, submission_callbacks

TEAM = os.getenv("GITHUB_REPOSITORY", "SyneRBI/PETRIC-unknown").split("/PETRIC-", 1)[-1]
VERSION = os.getenv("GITHUB_REF_NAME", "UNKNOWN")

class Timeout(cbks.Callback):
    def __init__(self, seconds=300, **kwargs):
        super().__init__(**kwargs)
        self.limit = time() + seconds
    def __call__(self, *_, **__):
        if time() > self.limit:
            raise StopIteration

class TensorBoard(cbks.Callback):
    def __init__(self, log_dir=f"/o/logs/{TEAM}/{VERSION}", **kwargs):
        super().__init__(**kwargs)
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        self.writer = tf.summary.FileWriter(log_dir=log_dir)
    def __call__(self, algorithm: Algorithm):
        summary = tf.Summary(value=[tf.Summary.Value(tag="loss", simple_value=algorithm.get_last_loss())])
        self.writer.add_summary(summary, algorithm.iteration)


data = "TODO"
metrics = [cbks.ProgressCallback(), Timeout(), TensorBoard()]

algo = Submission(data)
algo.run(np.inf, callbacks=metrics + submission_callbacks)
