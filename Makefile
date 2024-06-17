.PHONY: all install build tensorboard
all: install build tensorboard
install:
	echo installing CI scripts
	sudo cp runner/petric* /opt/runner/
	sudo chown root:runner runner/petric*
build:
	echo building CI image
	docker compose build petric
tensorboard:
	echo serving CI logs
	docker compose up -d tensorboard
