.PHONY: all install build up
all: install build up
install:
	echo installing CI scripts
	sudo cp runner/petric* /opt/runner/
	sudo chown root:runner /opt/runner/petric*
	sudo chmod -c go-w /opt/runner/petric*
	sudo chmod -c a+rx /opt/runner/petric*
build:
	echo building CI image
	# docker pull synerbi/sirf:edge-gpu
	docker compose build --pull
up: /opt/runner/logs/0_THRESHOLDS
	echo serving website
	docker compose up -d
	sleep 5
	docker compose logs petric
	docker compose rm -f
DCRUN=docker run --rm --user root -e GITHUB_REPOSITORY=SyneRBI/PETRIC-None -e GITHUB_REF_NAME=None -e RUNNER_GID=$(shell id -g) -e NUMEXPR_MAX_THREADS=24 -v ./runner:/w -w /w
/opt/runner/logs/0_THRESHOLDS: runner/thresholds.py
	sudo rm -rf $@
	$(DCRUN) -v /mnt/share:/mnt/share:ro -v /opt/runner:/o:rw synerbi/sirf:ci ./thresholds.sh
eval:
	$(DCRUN) -v /opt/runner:/o:ro synerbi/sirf:ci ./eval_thresholds.sh
