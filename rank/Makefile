rank:
	docker run --rm -u root -e NB_GID=$(shell getent group runner | cut -d: -f3) -e GITHUB_REPOSITORY=SyneRBI/PETRIC2-None -e GITHUB_REF_NAME=None -e NUMEXPR_MAX_THREADS=24 -e PETRIC_SKIP_DATA=1 -v /opt/runner:/o:ro -v /opt/runner/logs/2:/logs:ro -v /mnt/share-public/petric/2:/share -v .:/w -w /w ghcr.io/synerbi/sirf:petric2 ./compute.sh
