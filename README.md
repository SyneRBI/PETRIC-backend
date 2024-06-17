# PETRIC Backend

Internal support for https://github.com/SyneRBI/PETRIC

The machine `tomography.stfc.ac.uk` runs two separate (technically independent) things I couldn't be bothered to put into different repos.

## GitHub Actions CI self-hosted runner

This has [`runner/petric`](./runner/petric) installed on its `$PATH`

- Runner: [`synerbi@stfc`](https://github.com/organizations/SyneRBI/settings/actions/runners/102)
  + Tags: `docker`, `cuda`
- Sources: [`runner`](./runner), [`docker-compose.yml`](./docker-compose.yml)`:petric`
- Usage: [PETRIC:.github/workflows/run.yml](https://github.com/SyneRBI/PETRIC/blob/main/.github/workflows/run.yml)`:jobs.full`

## TensorBoard server

- Sources: [`docker-compose.yml`](./docker-compose.yml)`:tensorboard`
- Exposes: `/opt/runner/logs`
- Result ("leaderboard"): <https://tomography.stfc.ac.uk>
