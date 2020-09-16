PYTHON_MAJOR_MINOR := $(shell python -c "import sys; print('{0}{1}'.format(*sys.version_info))")
REQUIREMENTS_TXT = requirements$(PYTHON_MAJOR_MINOR).txt

.PHONY: core-requirements
core-requirements:
	pip install pip setuptools pip-tools

.PHONY: update-requirements
update-requirements: core-requirements
	pip install -U pip setuptools pip-tools
	pip-compile -U requirements.in -o $(REQUIREMENTS_TXT)

.PHONY: requirements
requirements: core-requirements
	pip-sync $(REQUIREMENTS_TXT)

.PHONY: clean-pyc
clean-pyc: requirements
	find . -iname "*.pyc" -delete
	find . -iname "__pycache__" -delete

.PHONY: develop
develop: requirements
	python setup.py develop

reports:
	mkdir -p $@

.PHONY: pycodestyle
pycodestyle: reports
	set -o pipefail && $@ ATEMStreamingXML | tee reports/$@.report

.PHONY: flake8
flake8: reports
	set -o pipefail && $@ ATEMStreamingXML | tee reports/$@.report

.PHONY: check8
check8: develop pycodestyle flake8

.PHONY: test
test: check check8
	py.test -v

.PHONY: dev-build
dev-build: clean-pyc
	python setup.py dev_build

.PHONY: release-build
release-build: clean-pyc
	python setup.py release_build
