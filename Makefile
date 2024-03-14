module_name=blah

init:
	pip install pipenv --upgrade
	@$(MAKE) dev-deps
.PHONY: init

deps:
	pipenv sync
.PHONY: deps

dev-deps:
	pipenv sync --dev
.PHONY: dev-deps

check: type-check style-check
.PHONY: check

type-check:
	pipenv -q run mypy ${module_name}
.PHONY: type-check

style-check:
	pipenv -q run pylint ${module_name} --score n
	pipenv -q run flake8 ${module_name}
.PHONY: style-check
