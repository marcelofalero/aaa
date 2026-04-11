# Agent Guidelines for RPG Rulebook Site

1. **Self-Contained Specialty Skills:** When transcribing rulebook text, generic text bonuses or sidebars that apply broadly to multiple specialty skills (like "Entertainment Skill Rank Benefit") must be duplicated and **integrated into each applicable specialty skill's section**. Because this is a reference site used mid-play, players looking at a specific skill should not have to scroll entirely elsewhere to find their relevant bonuses and mechanics. 
2. **Tables:** Do NOT duplicate large tables into specialty skills. Since all the specialty skills will be rendered on the same page as the broad skill, the player doesn't have to leave the page to see the table. If a specialty skill refers to a table, a markdown link to it is sufficient, or just leave it at the top of the broad skill section if it naturally fits there.
3. **Terminology Consistency:** Always replace mentions of "hero" with "character" unless otherwise explicitly instructed. 
4. **Format Preservation:** Use the standardized Markdown conventions established on the site (e.g., `▶` or `⊗` for modifiers, bolding instead of bulleted lists when sentences naturally flow, etc.).
5. **Translation:** When translating always check @content/notes/terminology_mapping.md for the correct translation of terms.
6. **Git Workflow:** Always use the GitHub CLI (`gh`) for code changes. Create a feature branch, commit your changes, and then use `gh pr create --fill` followed by `gh pr merge --merge --delete-branch` to finalize the work into the `main` branch.
