# thanks zeph
# thanks flare
PYTHON ?= .venv/bin/python3
DIFF := $(shell git diff --name-only --staged "*.py" "*.pyi")
ifeq ($(DIFF),)
	DIFF := $(shell git ls-files "*.py" "*.pyi")
endif

lint:
	$(PYTHON) -m flake8 --count --select=E9,F7,F82 --show-source $(DIFF)
stylecheck:
	$(PYTHON) -m autoflake --check --imports aiohttp,discord,redbot $(DIFF)
	$(PYTHON) -m isort --check-only $(DIFF)
	$(PYTHON) -m black --check $(DIFF)
reformat:
	$(PYTHON) -m autoflake --in-place --imports=aiohttp,discord,redbot $(DIFF)
	$(PYTHON) -m isort $(DIFF)
	$(PYTHON) -m black $(DIFF)
reformatblack:
	$(PYTHON) -m black $(DIFF)
update:
	$(PYTHON) -m pip install -U pip wheel setuptools autoflake isort black flake8 pre-commit cookiecutter Red-DiscordBot redgettext==3.4.2
run:
	$(PYTHON) -O -m redbot yamicogs --dev --debug --disable-intent presences
new:
	$(PYTHON) -m cookiecutter .utils/yamicog

# Translations
gettext:
	$(PYTHON) -m redgettext --command-docstrings --verbose --recursive .
