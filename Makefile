.PHONY: init venv deps dirs clean pytest test release mypy pylint ruff check build

SHELL := /bin/bash
FILES_CHECK_MYPY = user_agent
FILES_CHECK_ALL = $(FILES_CHECK_MYPY) tests
COVERAGE_TARGET = user_agent

init: venv deps dirs

venv:
	virtualenv -p python3 .env

deps:
	.env/bin/pip install -r requirements_dev.txt
	.env/bin/pip install -e .

dirs:
	if [ ! -e var/run ]; then mkdir -p var/run; fi
	if [ ! -e var/log ]; then mkdir -p var/log; fi

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete
	find -name '__pycache__' -delete

pytest:
	pytest -n30 -x --cov $(COVERAGE_TARGET) --cov-report term-missing

test: check pytest
	tox -e check-minver

#release:
#	git push \
#	&& git push --tags \
#	&& make build \
#	&& twine upload dist/*

mypy:
	mypy --strict $(FILES_CHECK_MYPY)

pylint:
	pylint -j0  $(FILES_CHECK_ALL)

ruff:
	ruff check $(FILES_CHECK_ALL)

coverage:
	pytest -n30 -x --cov $(COVERAGE_TARGET) --cov-report term-missing

eradicate:
	tox -e eradicate -- flake8 -j auto --eradicate-whitelist-extend="" $(FILES_CHECK_ALL)

check: ruff mypy pylint

build:
	rm -rf *.egg-info
	rm -rf dist/*
	python -m build --sdist
