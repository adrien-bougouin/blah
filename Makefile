.DEFAULT_GOAL := help

SHELL := /usr/bin/env bash

modules := blah blah_ptt
system_program_dependencies := pyenv pipenv ffmpeg
system_library_dependencies := ffmpeg libsndfile portaudio

# Text display styles
success_style	:= $(shell tput bold 2>&1; tput setaf 2 2>&1)
failure_style := $(shell tput bold 2>&1; tput setaf 1 2>&1)
bold_style := $(shell tput bold 2>&1)
reset_style := $(shell tput sgr 0 2>&1)

## Install production dependencies.
deps:
	pipenv sync
.PHONY: deps

## Install development dependencies.
dev-deps:
	pipenv sync --dev
.PHONY: dev-deps

## Run type checkers and style checkers.
check: style-check type-check
.PHONY: check

## Run style checkers.
style-check:
	pipenv -q run pylint $(modules) --score n
	pipenv -q run flake8 $(modules)
.PHONY: style-check

## Run type checkers.
type-check:
	pipenv -q run mypy $(modules)
.PHONY: type-check

## Remove generated files.
clean:
	rm -rf $(addsuffix /__pycache__, $(modules))
	rm -rf $(addsuffix /**/__pycache__, $(modules))
	rm -rf .mypy_cache
	@read -p $$'$(bold_style)Remove virtual Python environment too?$(reset_style) (y/N) ' confirm; \
		if [[ $${confirm} == y ]]; then \
			$(MAKE) clean-venv; \
		fi
.PHONY: clean

## Remove virtual Python environment.
clean-venv:
	pipenv --rm
.PHONY: clean-venv

## Run examples.
examples:
	$(eval temp_directory := $(shell mktemp -d))
	$(eval temp_model := $(temp_directory)/mode.bin)
	@echo "== Training =========================================================="
	pipenv -q run train --config examples/train/config.toml $(temp_model)
	@echo "== Analysis =========================================================="
	@$(MAKE) temp_model="$(temp_model)" $(foreach audio, $(wildcard examples/analyze/*.wav), example-analyze-$(notdir $(audio)))
.PHONY: examples

example-analyze-%:
	pipenv -q run analyze --model $(temp_model) examples/analyze/$* | awk '{ print "$(basename $*) -> " $$0 }'
.PHONY: example-analyze-%

## Verify system compatibilities.
doctor: $(addprefix find-program-, $(system_program_dependencies)) $(addprefix find-library-, $(system_library_dependencies))
	@exit $(if $(shell echo $(missing_dependencies) | grep true), 1, 0)
.PHONY: doctor

find-program-%:
	$(eval missing_dependencies ?= false)
	@echo -n -e "Looking for $(bold_style)$*$(reset_style)..."
	$(eval found := $(if $(shell command -v $*), true, false))
	@echo -e $(if $(shell echo $(found) | grep true), " $(success_style)Found$(reset_style)", " $(failure_style)Not found$(reset_style)")
	$(eval missing_dependencies += $(if $(shell echo $(found) | grep true), false, true))
.PHONY: find-program-%

find-library-%:
	$(eval missing_dependencies ?= false)
	@echo -n -e "Looking for $(bold_style)$*$(reset_style)..."
	$(eval found := false)
ifneq (, $(shell command -v brew))
	$(eval found := $(if $(shell brew list | grep $*), true, false))
endif
	@echo -e $(if $(shell echo $(found) | grep true), " $(success_style)Found$(reset_style)", " $(failure_style)Not found$(reset_style)")
	$(eval missing_dependencies += $(if $(shell echo $(found) | grep true), false, true))
.PHONY: find-library-%

## Show this help.
help:
	@echo "Usage: make [<target>]"
	@echo "       pipenv run <command> [<command_args>]"
	@echo
	@echo "Make targets:"
	@grep -zo "^\(## .*\n\)\+[^:]*:" $(MAKEFILE_LIST) \
		| tr '\n' ':' | sed -E 's/:+$$/\n/' | sed 's/::##/\n##/g' \
		| sed -E 's/^(.*):([^:]+)$$/  $(bold_style)\2$(reset_style)\1/' \
		| sed -E 's/:?## /\n\t/g'
	@echo
	@echo "Pipenv commands:"
	@pipenv -q scripts | tail -n +3 | sed -E 's/^([^ ]+) +(.*)$$/  $(bold_style)\1$(reset_style)\n\tRun \`\2\` in virtual Python environment./'
.PHONY: help

%:
	@echo -e "Error: No rule to make target \`$*\`.\n"
	@$(MAKE) help
