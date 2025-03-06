SHELL = /bin/bash

.PHONY: default help tests docker locales

APP_NAME ?= ebook-scriptum
COMMIT_HASH ?= $(shell git rev-parse HEAD | cut -c 1-8)

DOCKER_MOUNT_POINT ?= $(shell pwd):/tts
DOCKER_CONTAINER ?= transmuter
DOCKER_IMAGE ?= rocm-tts

GREEN = \033[0;32m
NOSTYLE = \033[0m

default: test

help:
	@echo "- Use 'make test' (default) to run all tests and generate a coverage html report"
	@echo "- Use 'make test-only' to only run all tests"
	@echo "- Use 'make docker-build' to generate the docker image"
	@echo -e "  Current IMAGE: '${DOCKER_IMAGE}:${COMMIT_HASH}'"
	@echo "- Use 'make docker' to generate and run the docker container"
	@echo -e "  Current CONTAINER: '${DOCKER_CONTAINER}'"

test-only:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "not in env. Run 'source .venv/bin/activate'"; \
		exit 1; \
	else \
		python -m coverage run -m pytest; \
	fi

test: test-only
	@python -m coverage report -m
	@python -m coverage html
	@echo -e "Check: " $(shell pwd)"/htmlcov/index.html"

docker-build:
	@echo -e "$(GREEN)Building Docker Image...$(NOSTYLE)"
	@docker build --tag ${APP_NAME}:${COMMIT_HASH} .
	@echo -e "$(GREEN)Done$(NOSTYLE)"

docker:
	@docker run -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --device=/dev/kfd --device=/dev/dri --group-add video --ipc=host --shm-size 8G --name $(DOCKER_CONTAINER) -v $(DOCKER_MOUNT_POINT) $(DOCKER_IMAGE)

pot:
	@pybabel extract -o locale/$(APP_NAME).pot src/*.py __main__.py /usr/lib/python3.12/argparse.py

po-init:
	@pybabel init -i locale/$(APP_NAME).pot -d locale -l es

po:
	@pybabel update -i locale/$(APP_NAME).pot -d locale -l es

locales:
	@pybabel compile -d locale
