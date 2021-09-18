SHELL=/bin/bash -euo pipefail

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

install:
	poetry install

build-py:
	cd pip; \
	sed -i -r "s/__version__\s+=\s(\"|').*?(\"|')/__version__ = '${RELEASE_VERSION}'/1" covid_19_terms/__init__.py; \
 	python setup.py sdist bdist_wheel

release:
	poetry run scripts/build.py
	make build-py

dist: release
