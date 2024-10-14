#!docker run --rm --user root -v /mnt/share:/mnt/share:ro -v /opt/runner:/o:rw synerbi/sirf:ci python
from pathlib import Path
from time import time

from tensorboardX import SummaryWriter

from petric import QualityMetrics

tb = SummaryWriter(logdir="/o/logs/0_THRESHOLDS")
voi_names = {i.stem[4:] for i in Path("/mnt/share/petric").glob("*/PETRIC/VOI_*.hv")}
t = int(time())

for tic in (0, 60 * 60):
    for i in voi_names - {'whole_object', 'background'}:
        tb.add_scalar(f"AEM_VOI_{i}", QualityMetrics.THRESHOLD["AEM_VOI"], tic, t + tic)
    tb.add_scalar("RMSE_whole_object", QualityMetrics.THRESHOLD["RMSE_whole_object"], tic, t + tic)
    tb.add_scalar("RMSE_background", QualityMetrics.THRESHOLD["RMSE_background"], tic, t + tic)
