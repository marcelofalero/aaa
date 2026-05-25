# tools/Makefile — Build & install standalone Python commands to ~/.local/bin

PROJECT_ROOT := $(realpath ..)
PREFIX      ?= $(HOME)/.local
BINDIR      := $(PREFIX)/bin

# Standalone Python commands to compile
PY_COMMANDS = \
	data-manager \
	master-translator \
	manage-site-data \
	generate-legacy-skills \
	check-search-index \
	publish-changes

# Bash wrappers
BASH_COMMANDS = publish

COMMANDS = $(PY_COMMANDS) $(BASH_COMMANDS)
SHIMS_DST = $(addprefix $(BINDIR)/,$(COMMANDS))

.PHONY: all install list clean env build-py build-bash

all: install

# ── Build ──────────────────────────────────────────────────────────────────

build: install
	@echo "Build complete."

# ── Install ────────────────────────────────────────────────────────────────

install: build-py build-bash
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  Installed $(words $(COMMANDS)) commands to $(BINDIR)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "  Make sure $(BINDIR) is in your PATH."

build-bash: $(BINDIR)/publish

$(BINDIR)/publish: shims/publish
	@mkdir -p $(BINDIR)
	sed -e 's|@PROJECT_ROOT@|$(PROJECT_ROOT)|g' $< > $@
	chmod +x $@

# ── Python Compilation (shiv) ──────────────────────────────────────────────

build-py: env
	@mkdir -p $(BINDIR)
	@echo "Compiling standalone executables with shiv..."
	cd $(PROJECT_ROOT) && pipenv run shiv --site-packages tools/.shiv_build --compressed -p '/usr/bin/env python3' -o $(BINDIR)/data-manager -e data_manager:main
	cd $(PROJECT_ROOT) && pipenv run shiv --site-packages tools/.shiv_build --compressed -p '/usr/bin/env python3' -o $(BINDIR)/master-translator -e master_translator:main
	cd $(PROJECT_ROOT) && pipenv run shiv --site-packages tools/.shiv_build --compressed -p '/usr/bin/env python3' -o $(BINDIR)/manage-site-data -e manage_site_data:rebuild_all
	cd $(PROJECT_ROOT) && pipenv run shiv --site-packages tools/.shiv_build --compressed -p '/usr/bin/env python3' -o $(BINDIR)/generate-legacy-skills -e generate_legacy_skills_json:main
	cd $(PROJECT_ROOT) && pipenv run shiv --site-packages tools/.shiv_build --compressed -p '/usr/bin/env python3' -o $(BINDIR)/check-search-index -e check_search_index:main
	cd $(PROJECT_ROOT) && pipenv run shiv --site-packages tools/.shiv_build --compressed -p '/usr/bin/env python3' -o $(BINDIR)/publish-changes -e publish_changes:main

env:
	@echo "Exporting dependencies and building Python package directory..."
	@mkdir -p .shiv_build
	@touch .shiv_build/__init__.py
	cd $(PROJECT_ROOT) && pipenv requirements > tools/requirements.txt
	cd $(PROJECT_ROOT) && pipenv run pip install -r tools/requirements.txt --target tools/.shiv_build/ --upgrade
	cp data_manager.py .shiv_build/
	cp scripts/*.py .shiv_build/

# ── Utility ────────────────────────────────────────────────────────────────

list:
	@echo "Available commands:"
	@for cmd in $(COMMANDS); do printf '  - %s\n' "$$cmd"; done

clean:
	@for cmd in $(COMMANDS); do \
		rm -f $(BINDIR)/$$cmd; \
	done
	rm -rf .shiv_build requirements.txt
	@echo "Removed installed executables from $(BINDIR) and cleaned build artifacts"
