.PHONY: all install build up
all: install build up
install:
	echo installing CI scripts
	sudo cp runner/petric* /opt/runner/
	sudo chown root:runner runner/petric*
	sudo chmod go-w runner/petric*
build:
	echo building CI image
	docker compose build petric
up:
	echo serving website
	docker compose up -d caddy ftp leaderboard
