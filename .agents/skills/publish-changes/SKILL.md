---
name: publish-changes
description: Synchronizes site data, performs automated Spanish translation, and publishes changes to GitHub using a PR/merge workflow.
---

# Publish Changes Skill

This skill automates the end-to-end workflow for updating the Alternity RPG rulebook site data and keeping the repository in sync.

## When to use this skill
- Use this when the user says "publish changes", "push updates", or "deploy my work".
- Use this after making significant changes to the skill database (YAML or Markdown).

## Workflow
1.  **Sync Site Data**: Run `python3 ../../../sources/scripts/manage_site_data.py` to ensure Markdown edits are synced to `skills.yaml`.
2.  **Automated Translation**: Execute the master translation script to ensure Spanish parity with terminology mapping.
3.  **Site & Sheet Build**: Rebuild the JSON search index and the Roll20 character sheet.
4.  **Git Automation**: Create a timestamped feature branch, commit all changes, and push to origin.
5.  **PR Lifecycle**: Create a Pull Request using `gh pr create` and merge it using `gh pr merge`.

## Scripts
This skill relies on the following scripts in the `scripts/` directory:
- `publish_changes.py`: Manages the Git/GitHub workflow.
- `master_translator.py`: Handles the Google Translate + Terminology Mapping pipeline.
- `generate_legacy_skills_json.py`: Rebuilds the Roll20 skill index.

## Example Interaction
- **User**: "I'm done with the Medical Science updates. Publish them."
- **Agent**: "Triggering the `publish-changes` skill. I will sync the site data, translate the new content to Spanish, and create a Pull Request for you."
