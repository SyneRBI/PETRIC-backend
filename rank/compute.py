import logging
from collections import defaultdict
from pathlib import Path, PurePath

import matplotlib.pyplot as plt
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
LNAME = [
    ("Siemens_Vision600_ZrNEMAIQ", "Vision600_ZrNEMA"),
    ("NeuroLF_Esser_Dataset", "NeuroLF_Esser"),
    ("Mediso_NEMA_IQ_lowcounts", "Mediso_NEMA_lowcounts"),
    ("Siemens_Vision600_Hoffman", "Vision600_Hoffman"),
    ("GE_D690_NEMA_IQ", "D690_NEMA"),
    ("GE_DMI4_NEMA_IQ", "DMI4_NEMA"),
]
LNAME = {v:k for k,v in LNAME}


def fmt_time(seconds: float):
    return "--:--" if np.isposinf(seconds) or np.isnan(seconds) else tqdm.format_interval(seconds)


def slug(repo_name):
    """escape for use in shields.io badge labels"""
    return str(repo_name).replace("-", "--").replace("_", "__")


def repo(algo_name):
    """markdown link"""
    team, algo = algo_name.split("/", 1)

    return (f"[![{algo_name}](https://img.shields.io/badge/{slug(team)}-{slug(algo)}-black?style=social&logo=GitHub)]"
            f"(https://github.com/SyneRBI/PETRIC-{team}/tree/{algo})")


def tb_log(algo_name, dataset_name):
    """markdown link"""
    team, algo = algo_name.split("/", 1)

    return f"[![{algo_name}/{dataset_name}](https://img.shields.io/badge/{slug(team)}-{slug(algo)}-black?logo=tensorflow)](https://petric.tomography.stfc.ac.uk/tensorboard/?pinnedCards=%5B%7B%22plugin%22%3A%22scalars%22%2C%22tag%22%3A%22RMSE_whole_object%22%7D%5D&runFilter={team}/{algo}/{dataset_name}%24%7CTHRESHOLD#timeseries)"


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
    tee_file = Path("/share/provisional.md")
    tee = tee_file.open("w")
    tee_file.chmod(0o664)

    def print_tee(*args):
        print(*args)
        tee.write(" ".join(args) + "\n")

    logging.basicConfig(level=logging.INFO)
    # {"dataset.name": [((time, distance_above_thresh_avg, time_stderr), "algo"), ...], ...}
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
                # time, distance_above_thresh_avg, time_stderr
                if times_distances:
                    times, distances = [t for t, _ in times_distances], [d for _, d in times_distances]
                    tds = np.median(times), np.mean(distances), np.std(times, ddof=1) / np.sqrt(len(times))
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

    print_tee("""For each [dataset](/data), each submitted algorithm is run multiple times.\\
[Algorithms are ranked](https://github.com/SyneRBI/PETRIC/wiki#metrics-and-thresholds) by median time taken to reach the thresholds.\\
If thresholds are not met, the fallback ranks by average distance above the thresholds.
""")

    # calculate ranks
    ranks: dict[str, list[int]] = defaultdict(list)
    scale_dist = 54321
    for dataset_name, time_algos in timings.items():
        time_algos.sort()
        print_tee(f"## [{dataset_name}](https://petric.tomography.stfc.ac.uk/data/{LNAME[dataset_name]})")
        print_tee('<div class="row"><div class="column">\n')
        print_tee("Rank|Algorithm|Time|Time (stderr)|Dist > thresh (avg)")
        print_tee("---:|:--------|---:|------------:|------------------:")
        for rank, ((t, d, s), algo_name) in enumerate(time_algos, start=1):
            print_tee(f"{rank}|{tb_log(algo_name, dataset_name)}|{fmt_time(t)}|{fmt_time(s)}|{d:.2f}")
            ranks[algo_name].append(rank)
        print_tee(f"""
</div><div class="column">Reference image slice<div class="imgContainer">

![](https://petric.tomography.stfc.ac.uk/data-raw/{LNAME[dataset_name]}/PETRIC/reference_image_slices.png)

</div></div></div>
""")

    print_tee("## Leaderboard")
    print_tee("\n![](ranks.svg)\n")
    ranks = sorted(ranks.items(), key=lambda algo_rank: sum(algo_rank[1]))
    for i, (algo_name, _) in enumerate(ranks, start=1):
        print_tee(f"{i}) {repo(algo_name)}")

    plt.figure(figsize=(6, 4), dpi=60)
    c = ['#f1f1f1', '#a8a8a8', '#ef6c00']
    plt.title("Figure 1: Average rank across all datasets", color=c[0])
    labels = [algo_name for algo_name, _ in ranks]
    y = [np.mean(rank) for _, rank in ranks]
    yerr = [np.std(rank, ddof=1) / np.sqrt(len(rank)) for _, rank in ranks]
    x = range(len(y))
    plt.barh(x, y, xerr=yerr, align='center', color=c[2])
    ax = plt.gca()
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    ax.set_xlim(1)
    ax.set_yticks(x, labels)
    ax.tick_params(colors=c[0])
    ax.tick_params(color=c[1])
    [ax.spines[s].set_color(c[1]) for s in ax.spines]
    plt.tight_layout()
    img = Path("/share/ranks.svg")
    plt.savefig(img, transparent=True)
    img.chmod(0o664)
