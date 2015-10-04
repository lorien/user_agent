clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete

upload:
	python setup.py sdist upload

test:
	./test.py

build: venv deps

venv:
	virtualenv --no-site-packages --python=python3.4 .env

deps:
	.env/bin/pip install -r requirements_dev.txt

docs:
	cd docs; make html

viewdocs:
	xdg-open docs/build/html/index.html
	
.PHONY: clean upload test build venv deps docs
