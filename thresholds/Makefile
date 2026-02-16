/opt/runner/logs/2/0_THRESHOLDS: draw.sh draw.py
	sudo rm -rf $@
	docker run --rm -u root -e NB_GID=$(shell getent group runner | cut -d: -f3) -e GITHUB_REPOSITORY=SyneRBI/PETRIC2-None -e GITHUB_REF_NAME=None -e NUMEXPR_MAX_THREADS=24 -v /mnt/share-public/petric/2:/mnt/share/petric:ro -v /opt/runner:/o:ro -v /opt/runner/logs/2:/logs:rw -v .:/w -w /w ghcr.io/synerbi/sirf:petric2 ./draw.sh
