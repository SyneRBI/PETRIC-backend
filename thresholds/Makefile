/opt/runner/logs/0_THRESHOLDS: draw.sh draw.py
	sudo rm -rf $@
	docker run --rm -u root -e GITHUB_REPOSITORY=SyneRBI/PETRIC-None -e GITHUB_REF_NAME=None -e RUNNER_GID=$(shell getent group runner | cut -d: -f3) -e NUMEXPR_MAX_THREADS=24 -v /mnt/share-public:/mnt/share:ro -v /opt/runner:/o:rw -v .:/w -w /w synerbi/sirf:ci ./draw.sh
