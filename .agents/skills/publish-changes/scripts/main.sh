#!/bin/bash
# Publication helper script
echo "Starting publication process..."

# 1. Sync Markdown to YAML (ensure latest manual edits are captured)
pipenv run python3 tools/scripts/manage_site_data.py

# 2. Run Master Translator (ensure Spanish parity)
pipenv run python3 tools/scripts/master_translator.py

# 3. Final propagation to Site Data
pipenv run python3 tools/scripts/manage_site_data.py
pipenv run python3 tools/scripts/generate_legacy_skills_json.py

# 4. Build Character Sheet
cd roll20_charsheet && python3 build_sheet.py && cd ..

# 5. Execute Publication Script (Git/GitHub workflow)
pipenv run python3 tools/scripts/publish_changes.py

echo "Done!"
