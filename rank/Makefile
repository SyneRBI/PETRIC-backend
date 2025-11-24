rank:
	docker run --rm -u root -e GITHUB_REPOSITORY=SyneRBI/PETRIC2-None -e GITHUB_REF_NAME=None -e RUNNER_GID=$(shell getent group runner | cut -d: -f3) -e NUMEXPR_MAX_THREADS=24 -v /opt/runner:/o:ro -v /opt/runner/logs/2:/logs:ro -v /mnt/share-public/petric/2:/share -v .:/w -w /w ghcr.io/synerbi/sirf:petric2 ./compute.sh
