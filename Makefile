.PHONY: clean upload test build venv deps docs viewdoc

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete
	find -name __pycache__ -delete

upload:
	python setup.py sdist upload

build: venv deps

venv:
	virtualenv --no-site-packages --python=python3 .env

deps:
	.env/bin/pip install -r requirements_dev.txt

docs:
	cd docs; make html

viewdoc:
	x-www-browser docs/build/html/index.html
