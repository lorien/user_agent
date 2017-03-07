.PHONY: clean upload build venv deps viewdoc

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete
	find -name __pycache__ -delete

upload:
	git push --tags; python setup.py sdist upload

build: venv deps

venv:
	virtualenv --no-site-packages --python=python3 .env

deps:
	.env/bin/pip install -r requirements_dev.txt

viewdoc:
	x-www-browser docs/build/html/index.html
