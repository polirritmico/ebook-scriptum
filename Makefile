SHELL = /bin/bash

.PHONY: default help tests docker locales

SCRIPT_NAME ?= ebook-scriptum
COMMIT_HASH ?= $(shell git rev-parse HEAD | cur -c 1-12)

GREEN = \033[0;32m
NOSTYLE = \033[0m

default: test

help:
	@echo "- Use 'make test' to run all tests and generate a coverage html report"
	@echo "- Use 'make test-only' (default) to run all tests"
	@echo "- Use 'make docker' to generate the docker image"
	@echo -e "  The resulting image will be called '${SCRIPT_NAME}:LAST_COMMIT'"

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

docker:
	@echo -e "$(GREEN)Building Docker Image...$(NOSTYLE)"
	@docker build --tag ${SCRIPT_NAME}:${COMMIT_HASH}
	@echo -e "$(GREEN)Done$(NOSTYLE)"

pot:
	@pybabel extract -o locale/$(SCRIPT_NAME).pot src/*.py __main__.py /usr/lib/python3.12/argparse.py

po-init:
	@pybabel init -i locale/$(SCRIPT_NAME).pot -d locale -l es

po:
	@pybabel update -i locale/$(SCRIPT_NAME).pot -d locale -l es

locales:
	@pybabel compile -d locale
