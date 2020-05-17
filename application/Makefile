.PHONY: run
run:
	poetry run waitress-serve --call sample:wsgi.main

.PHONY: mypy
mypy:
	poetry run mypy sample

.PHONY: flake8
flake8:
	poetry run flake8 sample tests

.PHONY: test
test:
	poetry run pytest tests --cov=sample --cov-report term-missing --durations 5

.PHONY: test-all
test-all:
	$(MAKE) mypy
	$(MAKE) flake8
	$(MAKE) test
