#!/bin/bash
# Publication helper script
echo "Starting publication process..."

# 1. Sync Markdown to YAML (ensure latest manual edits are captured)
python3 sources/scripts/manage_site_data.py

# 2. Run Master Translator (ensure Spanish parity)
sources/scripts/venv/bin/python3 sources/scripts/master_translator.py

# 3. Final propagation to Site Data
python3 sources/scripts/manage_site_data.py
python3 sources/scripts/generate_legacy_skills_json.py

# 4. Build Character Sheet
cd roll20_charsheet && python3 build_sheet.py && cd ..

# 5. Build Site and Audit Search Index
echo "Building site and auditing search index..."
cd site && hugo --gc --minify && cd ..
python3 sources/scripts/check_search_index.py || { echo "Search index audit failed! Aborting publication."; exit 1; }

# 6. Execute Publication Script (Git/GitHub workflow)
python3 sources/scripts/publish_changes.py

echo "Done!"
