#!/bin/bash
# Script to generate a 2-stage smart prompt for the LLM based on a character specification

# Ensure the summary exists
if [ ! -f "tools/character_generator/ai_rules_summary.md" ]; then
    python3 tools/character_generator/build_ai_summary.py
fi

# Optional argument: XP (Advancement Points)
XP_PASSED=${1:-0}

# Read the character specification from stdin
SPEC=$(cat)

# Output the smart prompt to stdout
cat << EOF
You are an expert RPG character creator and system optimizer for the Alternity RPG system.
Your task is to take the following character concept specification and output a strictly valid, mathematically balanced JSON object representing the character state.

DO NOT output any markdown formatting around the final JSON, just the raw JSON object. However, you MUST follow the 2-stage process below and output your thought process/planning BEFORE the final JSON.

### STAGE 1: PLANNING & CREATION BUDGET (70 SP)
Before generating the JSON, output a brief markdown planning section:
1. Identify the chosen Profession and Background from the specification.
2. List the **Mandatory** skills and **Recommended** skills for this concept. **CRITICAL: DO NOT INVENT OR HALLUCINATE SKILLS. YOU MUST ONLY USE SKILLS EXACTLY AS THEY APPEAR IN THE AI RULES SUMMARY.**
3. Assign priorities to these skills (High, Medium, Low).
4. Calculate your Creation Budget: 70 SP (Base) + Flaw bonuses. Spend this budget strictly on broad skills, specialty skills (max 3 ranks), and Perks. Apply a -1 SP discount to any skill Favored by the Profession or Background (e.g. 7 SP becomes 6 SP).

### STAGE 2: ADVANCEMENT / XP BUDGET
The user has passed the following XP / Advancement Points to spend: ${XP_PASSED} AP.
1. After finalizing the Creation SP budget, spend these ${XP_PASSED} AP on advancing the character's skills or abilities.
2. Record these extra skill ranks strictly in the \`advancementSkills\` JSON object (not in the base \`ranks\` property of the \`skills\` object).

---

### AI RULES SUMMARY (REFERENCE)
EOF

cat tools/character_generator/ai_rules_summary.md

cat << 'EOF'

---

### THE FINAL JSON SCHEMA
The final output MUST conform exactly to this structure (use standard lowercase slugs for IDs):

{
  "step": 7,
  "isFinalized": true,
  "bio": {
    "name": "String",
    "player": "String",
    "concept": "String",
    "motivation": "String",
    "attitude": "String",
    "traits": "String"
  },
  "faction": "slug", // e.g., 'orion', 'concord', 'rigunmor'
  "species": "slug", // e.g., 'human', 'tsa', 'weren', 'fraal'
  "background": "slug", // e.g., 'bounty-hunter', 'mercenary'
  "profession": "slug", // e.g., 'free-agent', 'combat-spec', 'diplomat', 'tech-op'
  "abilities": {
    "STR": 10,
    "DEX": 10,
    "CON": 10,
    "INT": 10,
    "WIL": 10,
    "PER": 10
  },
  "skills": {
    "athletics": {
      "ranks": 1,
      "isBroad": true
    },
    "melee-combat": {
      "ranks": 1,
      "isBroad": true
    },
    "pistol": {
      "ranks": 2,
      "isBroad": false,
      "category": "combat"
    }
  },
  "advancementSkills": {
    "pistol": 1 // Only put ranks bought with the passed XP/AP here!
  },
  "perks": [
    { "name": "observant", "level": 1 }
  ],
  "flaws": [
    { "name": "code-of-honor", "level": 1 }
  ],
  "earnedAP": <XP_PASSED_VALUE>
}

---
### CHARACTER SPECIFICATION:
EOF

echo "$SPEC"
