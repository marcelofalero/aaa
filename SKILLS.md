# Agent Skills

This document defines specialized skills that AI agents can use to perform complex tasks in this repository.

## Skill: Publish Changes

Automates the synchronization, translation, and publication of skill data to the repository.

### Requirements
- Python 3
- `gh` CLI (authenticated)
- `ruamel.yaml` (installed in `sources/scripts/venv`)
- `deep-translator` (installed in `sources/scripts/venv`)

### Usage Instructions
When requested to "publish changes" or "push updates":
1.  **Preparation**: Ensure all manual edits to Markdown files in `site/content/skills/` are complete.
2.  **Execution**: Run the `./publish.sh` script from the root directory.
    - This script will:
        - Sync Markdown edits to the central `skills.yaml`.
        - Perform automated Spanish translation using `master_translator.py`.
        - Rebuild the character sheet and site JSON data.
        - Create a new Git branch with a timestamp.
        - Push changes and create a Pull Request.
3.  **Finalization**: The script will attempt to merge the PR. If it fails (e.g., conflicts or auto-merge disabled), the agent must manually merge using `gh pr merge <id> --merge --delete-branch`.
4.  **Verification**: Confirm to the user that the PR has been merged and the site data is synchronized.

---
