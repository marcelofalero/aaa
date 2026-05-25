# Data Review and Processing Guide

## Objective
The goal is to manually review all data sources (currently focusing on **Skills**) to ensure absolute accuracy, eliminate hallucinations, and maintain consistent formatting between the English source material and the Spanish translation.

## Reference Materials
- **Source Text:** `sources/chapters/page_XXX.md` (OCR/Markdown extracts from the original books).
- **Target Data:** `sources/data_sources/*.yaml` (The files used to generate the site).
- **Terminology Mapping:** `site/content/notes/terminology-mapping.md` (Must be followed strictly for all translations).

## Workflow per Entry
1. **Source Research:** Locate the original text in `sources/chapters/`.
2. **English Review:**
   - Compare the YAML `en` entry with the source.
   - Remove any text not present in the original (hallucinations).
   - Ensure Markdown formatting is clean and consistent.
   - Use "character" instead of "hero" per project mandates.
3. **Spanish Translation:**
   - Translate the *fixed* English version into Spanish.
   - Use the **Terminology Mapping** for all game-specific terms (e.g., "Check" -> "Tirada", "Ordinary" -> "Ordinario").
4. **Validation:**
   - Run the linter: `pipenv run python3 tools/scripts/data_linter.py sources/data_sources/<file>.yaml`
   - Run the formatter: `pipenv run python3 tools/scripts/data_formatter.py sources/data_sources/<file>.yaml`

## Review Workflow
1. **Pull YAML to Markdown:** `data-manager skill pull --overwrite`
2. **Edit Markdown** in `sources/skills/<skill>/` (one file per broad skill + specialties)
3. **Check drift:** `data-manager skill diff -v`
4. **Push approved changes:** `data-manager skill push --commit`
5. **Validate:** Run the linter: `pipenv run python3 tools/scripts/data_linter.py sources/data_sources/skills.yaml`
6. **Format:** `pipenv run python3 tools/scripts/data_formatter.py skills`

## Current Status
- **Acrobatics:** COMPLETED (EN and ES reviewed/fixed).
- **Administration:** COMPLETED (English reviewed/fixed).
- **Animal Handling:** COMPLETED (English reviewed/fixed).
- **Awareness:** COMPLETED (English reviewed/fixed).
- **Business:** COMPLETED (English reviewed/fixed).
- **Armor Operation:** COMPLETED (English and Spanish reviewed/fixed).
- **Athletics:** COMPLETED (English reviewed/fixed).
- **Computer Science:** COMPLETED (English reviewed/fixed).
- **Covert Ops:** COMPLETED (English reviewed/fixed).
- **Creativity:** COMPLETED (English reviewed/fixed).
- **Deception:** COMPLETED (English reviewed/fixed).
- **Demolitions:** DRAFTED (Pending Review).
- **Entertainment:** DRAFTED (Pending Review).
- **Heavy Weapons:** DRAFTED (Pending Review).
- **Interaction:** DRAFTED (Pending Review).
- **Investigate:** DRAFTED (Pending Review).
- **Knowledge:** DRAFTED (Pending Review).
- **Law:** DRAFTED (Pending Review).
- **Leadership:** DRAFTED (Pending Review).
- **Next Up:** Life Science (Broad Skill).
.
