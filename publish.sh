#!/bin/bash
# Publication helper script
echo "Starting publication process..."

# 1. Run Master Translator (ensure Spanish parity after YAML edits)
master-translator

# 2. Propagate to Site Data (generate JSON + Hugo content from YAML)
manage-site-data
generate-legacy-skills

# 4. Build Character Sheet
cd roll20_charsheet && python3 build_sheet.py && cd ..

# 5. Build Site and Audit Search Index
echo "Building site and auditing search index..."
cd site && hugo --gc --minify && cd ..
check-search-index || { echo "Search index audit failed! Aborting publication."; exit 1; }

# 6. Execute Publication Script (Git/GitHub workflow)
publish-changes

echo "Done!"
