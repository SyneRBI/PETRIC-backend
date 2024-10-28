rank:
	docker run --rm -u root -e GITHUB_REPOSITORY=SyneRBI/PETRIC-None -e GITHUB_REF_NAME=None -e RUNNER_GID=$(shell id -g) -e NUMEXPR_MAX_THREADS=24 -v /opt/runner:/o:ro -v .:/w -w /w synerbi/sirf:ci ./compute.sh
