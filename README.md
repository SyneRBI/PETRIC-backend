# PETRIC Backend

Internal support for [SyneRBI/PETRIC](https://github.com/SyneRBI/PETRIC).

The machine `tomography.stfc.ac.uk` runs two separate (technically independent) things I couldn't be bothered to put into different repos.

## 1. GitHub Actions CI self-hosted runner

This has [`runner/petric`](./runner/petric) installed on its `$PATH`

- Runner: [`synerbi@stfc`](https://github.com/organizations/SyneRBI/settings/actions/runners/102)
  + Tags: `docker`, `cuda`
- Sources: [`runner`](./runner), [`docker-compose.yml`](./docker-compose.yml)`:petric`, [`Dockerfile`](./Dockerfile)
- Usage: [PETRIC:.github/workflows/run.yml](https://github.com/SyneRBI/PETRIC/blob/main/.github/workflows/run.yml)`:jobs.full`

> [!TIP]
> [`petric.py`](https://github.com/SyneRBI/PETRIC/blob/main/petric.py) runs `main.Submission` with callbacks writing TensorBoard logs to `/opt/runner/logs/TEAM/VERSION`.

## 2. Webserver

Created by `docker compose up -d`.

### Leaderboard

- Sources: [`docker-compose.yml`](./docker-compose.yml)`:leaderboard`
- Exposes: `/opt/runner/logs`
- Result: <https://petric.tomography.stfc.ac.uk/leaderboard>

#### Thresholds

A horizontal line in the leaderboard graphs.

- Sources: [`thresholds`](./thresholds)
- Exposes: `/opt/runner/logs/0_THRESHOLDS`

### Files

- Sources: [`docker-compose.yml`](./docker-compose.yml)`:leaderboard.labels.virtual.host.directives,data,data-wip`
- Exposes: `/mnt/share-public/petric`, `/mnt/share-public/petric-wip`
- Result: <https://petric.tomography.stfc.ac.uk/data>, [/data-wip](https://petric.tomography.stfc.ac.uk/data-wip)

> [!TIP]
> [/data-wip](https://petric.tomography.stfc.ac.uk/data-wip) needs authentication (username & password)

## 3. Utils

### Ranking

Computes submission rankings based on TensorBoard logs.

- Sources: [`rank`](./rank)

### Manual runner loop

Runs all submitted algorithms on all data.

- Sources: [`loop`](./loop)
