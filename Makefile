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
up:
	$(MAKE) -C thresholds
	echo serving website
	docker compose up -d
	sleep 5
	docker compose logs petric
	docker compose rm -f
perms: PERM=ugo+rw
perms: FILES=/mnt/share/petric /mnt/share/petric-wip
perms:
	sudo chown -Rc $(shell id -u):runner $(FILES)
	sudo chown -RcH $(shell id -u):runner $(FILES)
	sudo chmod -Rc $(PERM) $(FILES)
compress:
	cd /mnt/share/petric; ls -d */ | sed s./.. | xargs -II zip -v -FS -r -o -9 I.zip I -x "*.png" -x "*.ipynb_checkpoints*"
