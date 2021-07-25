SHELL=/bin/bash -euo pipefail

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

install:
	poetry install

clean:
	rm -rf dist

release: clean
	mkdir -p dist
	poetry run scripts/build.py > dist/terms.json

dist: release
