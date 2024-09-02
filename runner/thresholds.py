#!docker run --rm --user root -v /mnt/share:/mnt/share:ro -v /opt/runner:/o:rw synerbi/sirf:ci python
from pathlib import Path
from tensorboardX import SummaryWriter
from time import time

tb = SummaryWriter(logdir="/o/logs/0_THRESHOLDS")
voi_names = {i.stem[4:] for i in Path("/mnt/share/petric").glob("*/PETRIC/VOI_*.hv")}
t = int(time())

for tic in (0, 10*60):
    for i in voi_names - {'whole_object', 'background'}:
        tb.add_scalar(f"AEM_VOI_{i}", 0.005, tic, t + tic)
    tb.add_scalar("RMSE_whole_object", 0.01, tic, t + tic)
    tb.add_scalar("RMSE_background", 0.01, tic, t + tic)
