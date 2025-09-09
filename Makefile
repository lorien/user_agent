.PHONY: init venv deps py2-init py2-venv py2-deps dirs clean pytest test release mypy pylint ruff check build

SHELL := /bin/bash
FILES_CHECK_MYPY = user_agent
FILES_CHECK_ALL = $(FILES_CHECK_MYPY) tests
COVERAGE_TARGET = user_agent
PY2_ROOT = /home/user/.pyenv/versions/2.7.18
PY2_VENV = .venv-py27

init: venv deps dirs

py2: py2-venv py2-deps dirs

venv:
	virtualenv -p python3 .env

py2-venv:
	$(PY2_ROOT)/bin/pip install virtualenv
	$(PY2_ROOT)/bin/virtualenv --python=$(PY2_ROOT)/bin/python2.7 $(PY2_VENV)

deps:
	.env/bin/pip install -r requirements_dev.txt
	.env/bin/pip install -e .

py2-deps:
	$(PY2_VENV)/bin/pip install -r requirements_dev.txt
	$(PY2_VENV)/bin/pip install .

dirs:
	if [ ! -e var/run ]; then mkdir -p var/run; fi
	if [ ! -e var/log ]; then mkdir -p var/log; fi

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete
	find -name '__pycache__' -delete

pytest:
	pytest -n30 -x --cov $(COVERAGE_TARGET) --cov-report term-missing

test:
	pytest --cov $(COVERAGE_TARGET) --cov-report term-missing

release:
	git push \
	&& git push --tags \
	&& make build \
	&& twine upload dist/*

mypy:
	mypy --strict $(FILES_CHECK_MYPY)

pylint:
	pylint -j0  $(FILES_CHECK_ALL)

ruff:
	ruff check $(FILES_CHECK_ALL)

coverage:
	pytest -n30 -x --cov $(COVERAGE_TARGET) --cov-report term-missing

check: ruff mypy pylint

build:
	rm -rf *.egg-info
	rm -rf dist/*
	python -m build
