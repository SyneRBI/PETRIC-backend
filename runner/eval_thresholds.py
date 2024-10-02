#!docker run --rm --user root -v /opt/runner:/o:ro synerbi/sirf:ci python
from collections import defaultdict
from pathlib import Path

import numpy as np
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator, SCALARS

from petric import QualityMetrics

LOGDIR = Path("/o/logs")
TAGS = {"RMSE_whole_object", "RMSE_background", "AEM_VOI"}
assert set(QualityMetrics.THRESHOLD.keys()) == TAGS

def scalars(ea: EventAccumulator, tag: str):
    steps = [s.step for s in ea.Scalars(tag)]
    assert steps == sorted(steps)
    return [(scalar.value, scalar.wall_time) for scalar in ea.Scalars(tag)]

def valid(tensorboard_logfile: str) -> bool:
    ea = EventAccumulator(str(tensorboard_logfile), size_guidance={SCALARS: 0})
    ea.Reload()
    return len({"RMSE_whole_object", "RMSE_background"}.intersection(ea.Tags()['scalars'])) == 2

def pass_time(tensorboard_logfile: str) -> float:
    ea = EventAccumulator(str(tensorboard_logfile), size_guidance={SCALARS: 0})
    ea.Reload()

    try:
        start = ea.Scalars("reset")[0]
    except KeyError:
        start = None
    else:
        assert start.value == 0
        assert start.step == -1
        start = start.wall_time

    tags = {tag for tag in ea.Tags()['scalars'] if any(tag.startswith(i) for i in TAGS)}
    tags = {tag: scalars(ea, tag) for tag in tags}

    metrics = [tags.pop("RMSE_whole_object"), tags.pop("RMSE_background")]
    thresholds = [
        QualityMetrics.THRESHOLD["RMSE_whole_object"],
        QualityMetrics.THRESHOLD["RMSE_background"],
    ] + [QualityMetrics.THRESHOLD["AEM_VOI"]] * len(tags)
    metrics.extend(tags.values())
    metrics = np.array(metrics).T # [(value, time), step, (RMSE, RMSE, VOI, ...)]

    try:
        i = QualityMetrics.pass_index(metrics[0], thresholds)
    except IndexError:
        return np.inf
    return metrics[1][i] - (start or metrics[1][0])

if __name__ == '__main__':
    timings = defaultdict(list) # {"dataset.name": [(time: float, "algo"), ...], ...}

    for team in LOGDIR.glob("*/"):
        if team.name == '0_THRESHOLDS':
            continue
        for algo in team.glob("*/"):
            for dataset in algo.glob("*/"):
                t = np.median([pass_time(logfile) for logfile in dataset.glob("events.out.tfevents.*") if valid(logfile)])
                timings[dataset.name].append((t, f"{team.name}/{algo.name}"))

    algos = {algo for time_algos in timings.values() for _, algo in time_algos}
    for time_algos in timings.values():
        missing = algos - {algo for _, algo in time_algos}
        time_algos.extend((np.inf, algo) for algo in missing)

    ranks = defaultdict(int)
    for dataset, time_algos in timings.items():
        time_algos.sort()
        print(dataset)
        print("=" * len(dataset))
        N = len(time_algos)
        rank = 1
        for t, algo in time_algos:
            if np.isposinf(t):
                _rank = N
            else:
                _rank = rank
                rank += 1
            print(f"{_rank}: {algo}")
            ranks[algo] += _rank
        print("\n")

    print("Leaderboard")
    print("===========")
    for algo, _ in sorted(ranks.items(), key=lambda algo_rank: algo_rank[1]):
        print(algo)
