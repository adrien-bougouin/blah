SHELL := bash

.DEFAULT_GOAL :=help

modules := blah blah-ptt
system_dependencies := ffmpeg libsndfile portaudio

## Setup the production environment.
init:
ifeq ($(shell command -v pipenv), "")
	pip install pipenv --upgrade
endif
	@$(MAKE) deps
.PHONY: init

## Setup the development environment.
dev-init: init dev-deps
.PHONY: init

## Install production dependencies.
deps:
	pipenv sync
.PHONY: deps

## Install development dependencies.
dev-deps:
	pipenv sync --dev
.PHONY: dev-deps

## Run type checkers and style checkers.
check: type-check style-check
.PHONY: check

## Run type checkers.
type-check:
	pipenv -q run mypy $(modules)
.PHONY: type-check

## Run style checkers.
style-check:
	pipenv -q run pylint $(modules) --score n
	pipenv -q run flake8 $(modules)
.PHONY: style-check

## Remove generated files.
clean:
	rm -rf $(addsuffix /__pycache__, $(modules))
	rm -rf $(addsuffix /**/__pycache__, $(modules))
	rm -rf .mypy_cache
	@read -p $$'\033[1mRemove virtual Python environment too?\033[0m (y/N) ' confirm; \
		if [[ $${confirm} == y ]]; then \
			$(MAKE) clean-venv; \
		fi
.PHONY: clean

## Remove virtual Python environment.
clean-venv:
	pipenv --rm
.PHONY: clean-venv

## Verify system compatibilities.
doctor: $(addprefix find-, $(system_dependencies))
	@exit $(if $(shell echo $(missing_dependencies) | grep true), 1, 0)
.PHONY: doctor

find-%:
	$(eval missing_dependencies ?= false)
	@echo -n -e "Looking for \033[1m$*\033[0m..."
	$(eval found := false)
ifneq ($(shell command -v brew), "")
	$(eval found := $(if $(shell brew list | grep $*), true, false))
endif
	@echo -e $(if $(shell echo $(found) | grep true), " \033[1;32mFound\033[0m", " \033[1;31mNot found\033[0m")
	$(eval missing_dependencies += $(if $(shell echo $(found) | grep true), false, true))
.PHONY: find-%

## Run examples.
examples:
	$(eval temp_directory := $(shell mktemp -d))
	$(eval temp_model := $(temp_directory)/mode.bin)
	@echo "== Training =========================================================="
	pipenv -q run train --config examples/train/config.toml $(temp_model)
	@echo "== Analysis =========================================================="
	pipenv -q run analyze --model $(temp_model) examples/analyze/python.wav
	pipenv -q run analyze --model $(temp_model) examples/analyze/library.wav
	pipenv -q run analyze --model $(temp_model) examples/analyze/test.wav
	pipenv -q run analyze --model $(temp_model) examples/analyze/audio.wav
.PHONY: examples

## Show this help.
help:
	@echo "Usage: make [<target>]"
	@echo "       pipenv run <command> [<command_args>]"
	@echo
	@echo "Targets:"
	@grep -zo "^\(## .*\n\)\+[^:]*:" $(MAKEFILE_LIST) \
		| tr '\n' ':' | sed -E 's/:+$$/\n/' | sed 's/::##/\n##/g' \
		| sed -E 's/^(.*):([^:]+)$$/  \x1b[1m\2\x1b[0m\1/' \
		| sed -E 's/:?## /\n\t/g'
	@echo
	@echo "Commands:"
	@pipenv -q scripts | tail -n +3 | sed -E 's/^([^ ]+) +(.*)$$/  \x1b[1m\1\x1b[0m\n\tRun \`\2\` in virtual Python environment./'
.PHONY: help
