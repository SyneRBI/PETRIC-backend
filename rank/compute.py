import logging
from collections import defaultdict
from pathlib import Path, PurePath
from time import time

import numpy as np
from tensorboard.backend.event_processing.event_accumulator import SCALARS, EventAccumulator
from tqdm import tqdm

from petric import QualityMetrics

log = logging.getLogger(Path(__file__).stem)
DATASET_WHITELIST = {
    'NeuroLF_Esser', 'Vision600_Hoffman', 'Vision600_ZrNEMA', 'D690_NEMA', 'Mediso_NEMA_lowcounts', 'DMI4_NEMA'}
TAG_BLACKLIST = {"AEM_VOI_VOI_whole_object"}
LOGDIR = Path("/o/logs")
TAGS = {"RMSE_whole_object", "RMSE_background", "AEM_VOI"}
assert set(QualityMetrics.THRESHOLD.keys()) == TAGS


def fmt_time(seconds: float):
    return "--:--" if np.isposinf(seconds) or np.isnan(seconds) else tqdm.format_interval(seconds)


def scalars(ea: EventAccumulator, tag: str) -> list[tuple[float, float]]:
    """[(value, time), ...]"""
    steps = [s.step for s in ea.Scalars(tag)]
    assert steps == sorted(steps)
    return [(scalar.value, scalar.wall_time) for scalar in ea.Scalars(tag)]


def valid(tensorboard_logfile: PurePath) -> bool:
    """False if invalid/empty logfile"""
    ea = EventAccumulator(str(tensorboard_logfile), size_guidance={SCALARS: 0})
    ea.Reload()
    return len({"RMSE_whole_object", "RMSE_background"}.intersection(ea.Tags()['scalars'])) == 2


def pass_time(tensorboard_logfile: PurePath) -> tuple[float, float]:
    """
    - time at which thresholds were met (minus any metrics calculation time offset).
    - average distance above thresholds.
    """
    ea = EventAccumulator(str(tensorboard_logfile), size_guidance={SCALARS: 0})
    ea.Reload()

    try:
        start_scalar = ea.Scalars("reset")[0]
    except KeyError:
        log.error("KeyError: reset: not using accurate relative time for %s", tensorboard_logfile.relative_to(LOGDIR))
        start = 0.0
    else:
        assert start_scalar.value == 0
        assert start_scalar.step == -1
        start = start_scalar.wall_time

    tag_names: set[str] = {tag for tag in ea.Tags()['scalars'] if any(tag.startswith(i) for i in TAGS)}
    if (skip := TAG_BLACKLIST & tag_names):
        log.warning("skipping tags: %s", skip)
        tag_names -= skip
    tags = {tag: scalars(ea, tag) for tag in tag_names}

    metrics: np.ndarray = [tags.pop("RMSE_whole_object"), tags.pop("RMSE_background")]
    thresholds = [
        QualityMetrics.THRESHOLD["RMSE_whole_object"],
        QualityMetrics.THRESHOLD["RMSE_background"],] + [QualityMetrics.THRESHOLD["AEM_VOI"]] * len(tags)
    metrics.extend(tags.values())
    metrics = np.array(metrics).T # [(value, time), step, (RMSE, RMSE, VOI, ...)]

    # average distance away from threshold
    avg_dist_thresh = (metrics[0, -1] - thresholds).mean()
    try:
        i = QualityMetrics.pass_index(metrics[0], thresholds)
    except IndexError:
        return np.inf, avg_dist_thresh
    return metrics[1, i] - (start or metrics[1, 0]), avg_dist_thresh


if __name__ == '__main__':
    tee_file = Path(f"ranks-{time()}.md")
    tee = tee_file.open("w")
    tee_file.chmod(0o664)

    def print_tee(*args):
        print(*args)
        tee.write(" ".join(args) + "\n")

    logging.basicConfig(level=logging.INFO)
    # {"dataset.name": [((time, distance_above_thresh_avg, std_time), "algo"), ...], ...}
    timings: dict[str, list[tuple[tuple[float, float, float], str]]] = defaultdict(list)

    # LOGDIR / "team" / "algo" / "dataset" / "events.out.tfevents.*"
    for team in LOGDIR.glob("*/"):
        if team.name == '0_THRESHOLDS':
            continue
        for algo in team.glob("*/"):
            for dataset in algo.glob("*/"):
                if dataset.name not in DATASET_WHITELIST:
                    continue
                for logfile in dataset.glob("events.out.tfevents.*"):
                    if not valid(logfile):
                        log.warning("rm %s", logfile)
                        # logfile.unlink()
                times_distances = [
                    pass_time(logfile) for logfile in dataset.glob("events.out.tfevents.*") if valid(logfile)]
                # time, distance_above_thresh_avg, stdev_time
                if times_distances:
                    times, distances = [t for t, _ in times_distances], [d for _, d in times_distances]
                    tds = np.median(times), np.mean(distances), np.std(times, ddof=1)
                else:
                    tds = np.inf, np.inf, np.inf
                timings[dataset.name].append((tds, f"{team.name}/{algo.name}"))

    # insert `time=np.inf` for each team's missing algos
    algos = {algo_name for time_algos in timings.values() for _, algo_name in time_algos}
    for dataset_name, time_algos in timings.items():
        missing = algos - {algo_name for _, algo_name in time_algos}
        for algo_name in missing:
            log.error("FileNotFoundError: logfile for %s/%s", algo_name, dataset_name)
        time_algos.extend(((np.inf, np.inf, np.inf), algo_name) for algo_name in missing)

    # calculate ranks
    ranks: dict[str, int] = defaultdict(int)
    for dataset_name, time_algos in timings.items():
        time_algos.sort()
        print_tee("##", dataset_name)
        print_tee("Rank|Algorithm|Time|Time (stdev)|Avg > thresh")
        print_tee("---:|---------|---:|-----------:|-----------:")
        N = len(time_algos)
        rank = 1
        for (t, d, s), algo_name in time_algos:
            if np.isposinf(t):
                _rank = N
            else:
                _rank = rank
                rank += 1
            print_tee(f"{_rank}|{algo_name}|{fmt_time(t)}|{fmt_time(s)}|{d:.2f}")
            ranks[algo_name] += _rank
        print_tee("")

    print_tee("## Leaderboard")
    for i, (algo_name, _) in enumerate(sorted(ranks.items(), key=lambda algo_rank: algo_rank[1]), start=1):
        print_tee(f"{i}) {algo_name}")
