# PETRIC Backend

Internal support for [SyneRBI/PETRIC](https://github.com/SyneRBI/PETRIC).

The machine `tomography.stfc.ac.uk` runs two separate (technically independent) things I couldn't be bothered to put into different repos.

## GitHub Actions CI self-hosted runner

This has [`runner/petric`](./runner/petric) installed on its `$PATH`

- Runner: [`synerbi@stfc`](https://github.com/organizations/SyneRBI/settings/actions/runners/102)
  + Tags: `docker`, `cuda`
- Sources: [`runner`](./runner), [`docker-compose.yml`](./docker-compose.yml)`:petric`, [`Dockerfile`](./Dockerfile)
- Usage: [PETRIC:.github/workflows/run.yml](https://github.com/SyneRBI/PETRIC/blob/main/.github/workflows/run.yml)`:jobs.full`

> [!TIP]
> [`petric.py`](https://github.com/SyneRBI/PETRIC/blob/main/petric.py) runs `main.Submission` with callbacks writing tensorboard logs to `/opt/runner/logs/TEAM/VERSION`.

<!-- <br/> -->

> [!NOTE]
> [`thresholds.py`](./runner/thresholds.py) generates hardcoded tensorboard logs in `/opt/runner/logs/0_THRESHOLDS`.

## Webserver

### Leaderboard

- Sources: [`docker-compose.yml`](./docker-compose.yml)`:leaderboard`
- Exposes: `/opt/runner/logs`
- Result: <https://petric.tomography.stfc.ac.uk/leaderboard>

### Files

- Sources: [`docker-compose.yml`](./docker-compose.yml)`:leaderboard.labels.virtual.host.directives,caddy.volumes`
- Exposes: `/mnt/share/petric`, `/mnt/share/petric-wip`
- Result: <https://petric.tomography.stfc.ac.uk/data>, [/data-wip](https://petric.tomography.stfc.ac.uk/data-wip)

> [!TIP]
> [/data](https://petric.tomography.stfc.ac.uk/data)
> - web browser: read-only
> - [NAS on windows](https://support.microsoft.com/en-us/windows/map-a-network-drive-in-windows-29ce55d1-34e3-a7e2-4801-131475f9557d) or [DavFS on linux](https://askubuntu.com/questions/498526/mounting-a-webdav-share-by-users): writable with authentication
>
> [/data-wip](https://petric.tomography.stfc.ac.uk/data-wip)
> - web browser: read-only with authentication
> - NAS/DavFS: writable with authentication

<!-- <br/> -->

> [!NOTE]
> Relative symlinks are only supported 1 level up (i.e. `/mnt/share/petric/X -> ../X -> /mnt/share/X`)
