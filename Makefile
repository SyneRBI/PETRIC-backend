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
	docker pull synerbi/sirf:edge-gpu
	docker compose build --pull petric
up:
	echo serving website
	docker compose up -d caddy leaderboard
