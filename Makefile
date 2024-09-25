.PHONY: all install build up
all: install build up
install:
	echo installing CI scripts
	sudo cp runner/petric* /opt/runner/
	sudo chown root:runner /opt/runner/petric*
	sudo chmod go-w /opt/runner/petric*
	sudo chmod a+rx /opt/runner/petric*
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
/opt/runner/logs/0_THRESHOLDS: runner/thresholds.py build
	sudo rm -rf $@
	docker run --rm --user root -v .:/w -w /w -v /mnt/share:/mnt/share:ro -v /opt/runner:/o:rw synerbi/sirf:ci python $<
