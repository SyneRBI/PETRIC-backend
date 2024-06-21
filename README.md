# PETRIC Backend

Internal support for https://github.com/SyneRBI/PETRIC

The machine `tomography.stfc.ac.uk` runs two separate (technically independent) things I couldn't be bothered to put into different repos.

## GitHub Actions CI self-hosted runner

This has [`runner/petric`](./runner/petric) installed on its `$PATH`

- Runner: [`synerbi@stfc`](https://github.com/organizations/SyneRBI/settings/actions/runners/102)
  + Tags: `docker`, `cuda`
- Sources: [`runner`](./runner), [`docker-compose.yml`](./docker-compose.yml)`:petric`
- Usage: [PETRIC:.github/workflows/run.yml](https://github.com/SyneRBI/PETRIC/blob/main/.github/workflows/run.yml)`:jobs.full`

Note that [`runner/petric-full.py`](./runner/petric-full.py) runs `main.Submission` with callbacks writing tensorboard logs to `/opt/runner/logs/TEAM/VERSION`.

## Webserver

### Leaderboard

- Sources: [`docker-compose.yml`](./docker-compose.yml)`:leaderboard`
- Exposes: `/opt/runner/logs`
- Result: <https://petric.tomography.stfc.ac.uk/leaderboard>

### Files

- Sources: [`docker-compose.yml`](./docker-compose.yml)`:leaderboard.labels.virtual.host.directives,caddy.volumes`
- Exposes: `/mnt/share/petric`
- Result: <https://petric.tomography.stfc.ac.uk/data>

> [!TIP]
> Anything placed in <http://stfc.cdcl.ml:9999/lab/tree/share/petric> will be served publicly at the URL above.

<!-- -->

> [!NOTE]
> Relative symlinks are only supported 1 level up (i.e. `/mnt/share/petric/X -> ../X -> /mnt/share/X`)
