TEST_PATH = ./tests/
FLAKE8_EXCLUDE = venv,.venv,.eggs,.tox,.git,__pycache__,*.pyc
PROJECT = pyesios
AUTHOR = "Santiago Peñate Vera"

.PHONY: build docs clean install docker-build

clean:
	@find . -name '*.pyc' -exec rm --force {} +
	@find . -name '*.pyo' -exec rm --force {} +
	@find . -name '*~' -exec rm --force {} +
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -f *.sqlite
	@rm -rf .cache

startup:
	pip install --upgrade pip
	which poetry >/dev/null || pip install poetry

init: startup
	poetry install

init-dev: startup
	poetry install --with 'tests' --with 'dev' --with 'docs'

init-docs: startup
	poetry install --with 'docs'

docs:
	if ! [ -d "./docs" ]; then poetry run sphinx-quickstart -q --ext-autodoc --sep --project $(PROJECT) --author $(AUTHOR) docs; fi
	poetry run sphinx-apidoc -f -o ./docs/source ./$(PROJECT)
	poetry run sphinx-build -E -a -b html ./docs/source ./docs/build/html

test:
	poetry run pytest ${TEST_PATH}

test-coverage:
	poetry run pytest --cov=$(PROJECT) ${TEST_PATH} --cov-report term-missing

check:
	poetry run isort --check --diff .
	poetry run ruff .

lint-fix:
	poetry run isort .
	poetry run ruff . --fix

update:
	poetry update
	
build: update check test docs
	poetry build

release: build
	poetry publish
