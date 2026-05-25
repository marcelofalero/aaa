# tools/Makefile — Build & install shim commands to ~/.local/bin
#
# Usage:
#   make install          # Install all commands to ~/.local/bin
#   make install PREFIX=~/custom  # Install to custom prefix
#   make list             # List available commands

PROJECT_ROOT := $(realpath ..)
PREFIX      ?= $(HOME)/.local
BINDIR      := $(PREFIX)/bin

# All installable commands (shim name → script it wraps)
COMMANDS = \
	data-manager \
	publish \
	master-translator \
	manage-site-data \
	generate-legacy-skills \
	check-search-index

SHIMS_SRC = $(addprefix shims/,$(COMMANDS))
SHIMS_DST = $(addprefix $(BINDIR)/,$(COMMANDS))

.PHONY: all install list clean $(COMMANDS)

all: install

# ── Build ──────────────────────────────────────────────────────────────────

build: install
	@echo "Build complete. (Shim scripts are the build artifacts — no compilation needed.)"

# ── Install ────────────────────────────────────────────────────────────────

install: $(SHIMS_DST)
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  Installed $(words $(COMMANDS)) commands to $(BINDIR)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@printf '  %-30s → %s\n' 'Command' 'What it runs'
	@printf '  %-30s   %s\n' '-------' '------------'
	@printf '  %-30s → %s\n' 'data-manager <domain> <cmd>' 'tools/data_manager.py'
	@printf '  %-30s → %s\n' 'publish'                     'publish.sh (full pipeline)'
	@printf '  %-30s → %s\n' 'master-translator'           'tools/scripts/master_translator.py'
	@printf '  %-30s → %s\n' 'manage-site-data'            'tools/scripts/manage_site_data.py'
	@printf '  %-30s → %s\n' 'generate-legacy-skills'      'tools/scripts/generate_legacy_skills_json.py'
	@printf '  %-30s → %s\n' 'check-search-index'          'tools/scripts/check_search_index.py'
	@echo ""
	@echo "  Make sure $(BINDIR) is in your PATH."
	@echo "  Add this to your ~/.bashrc or ~/.zshrc if needed:"
	@echo '    export PATH="$$HOME/.local/bin:$$PATH"'

# Template rule: replace @PROJECT_ROOT@ placeholder with the real path
$(BINDIR)/%: shims/%
	@mkdir -p $(BINDIR)
	sed -e 's|@PROJECT_ROOT@|$(PROJECT_ROOT)|g' $< > $@
	chmod +x $@

# ── Utility ────────────────────────────────────────────────────────────────

list:
	@echo "Available commands:"
	@for cmd in $(COMMANDS); do printf '  - %s\n' "$$cmd"; done

clean:
	@for cmd in $(COMMANDS); do \
		rm -f $(BINDIR)/$$cmd; \
	done
	@echo "Removed installed shims from $(BINDIR)"
