SHELL=/bin/bash -euo pipefail

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

install:
	poetry install

build-py:
	cd pip && python setup.py sdist

release:
	poetry run scripts/build.py
	make build-py

dist: release
