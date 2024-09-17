define HELP


This Makefile contains commands for the multiverse project.

Usage:

make help                   - Show this help dialogue

make clean                  - Removes all generated files
make install                - Refreshes the `poetry.lock` file and installs all dependencies

make test                   - Runs a pytest suit

make run                    - Runs the project on the terminal

endef

export HELP


.PHONY: help
help:
	@echo "$$HELP"


.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	rm -rf .pytest_cache
	find . -name '__pycache__' -delete

.PHONY: install
install: clean
	poetry lock
	poetry install


.PHONY: test
test: clean
	poetry run pytest


.PHONY: run
run:
	poetry run python main.py
