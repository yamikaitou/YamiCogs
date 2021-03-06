# thanks zeph
# thanks flare
ifeq ($(USER), "codespace")
	PYTHON ?= /home/codespace/workspace/YamiCogs/pythonenv3.8/bin/python
else
	PYTHON ?= python3.8
endif
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
	$(PYTHON) -m pip install -U pip wheel setuptools autoflake isort black
	$(PYTHON) -m pip install -U Red-Discordbot[dev]
run:
	$(PYTHON) -O -m redbot dev --dev --debug

# Translations
gettext:
	$(PYTHON) -m redgettext --command-docstrings --verbose --recursive redbot --exclude-files "redbot/pytest/**/*"