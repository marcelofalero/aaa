#!/bin/bash
# Publication helper script
echo "Starting publication process..."

# 1. Run Master Translator (ensure Spanish parity after YAML edits)
pipenv run python3 tools/scripts/master_translator.py

# 2. Propagate to Site Data (generate JSON + Hugo content from YAML)
pipenv run python3 tools/scripts/manage_site_data.py
pipenv run python3 tools/scripts/generate_legacy_skills_json.py

# 4. Build Character Sheet
cd roll20_charsheet && python3 build_sheet.py && cd ..

# 5. Build Site and Audit Search Index
echo "Building site and auditing search index..."
cd site && hugo --gc --minify && cd ..
pipenv run python3 tools/scripts/check_search_index.py || { echo "Search index audit failed! Aborting publication."; exit 1; }

# 6. Execute Publication Script (Git/GitHub workflow)
pipenv run python3 tools/scripts/publish_changes.py

echo "Done!"
