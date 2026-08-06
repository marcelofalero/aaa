#!/bin/bash
# Script to generate a Chain-of-Thought (CoT) markdown prompt for character generation

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./tools/character_generator/build_cot_prompt.sh <concept_file.md> <out_dir> [XP_value]"
    exit 1
fi

CONCEPT_FILE=$1
CONCEPT=$(cat "$CONCEPT_FILE")
OUT_DIR=$2
XP_PASSED=${3:-0}

mkdir -p "$OUT_DIR"
OUT_FILE="$OUT_DIR/prompt.md"


# Ensure the summary exists
if [ ! -f "tools/character_generator/ai_rules_summary.md" ]; then
    python3 tools/character_generator/build_ai_summary.py
fi

cat << EOF > "$OUT_FILE"
You are an expert RPG character creator and system optimizer for the Alternity RPG system.
Your task is to take the user's character concept and systematically build a mathematically perfect character JSON.

To ensure accuracy, you MUST use a Chain-of-Thought approach. You will output a single markdown document containing specific sections. Do not skip any section.

### REQUIRED OUTPUT FORMAT:

# Step 1: Biography & Concept
[Write a structured overview of the character's Name, Concept, Motivation, Attitude, and Traits based on the prompt]

# Step 2: Foundations
[Select and explain the chosen Faction, Species, Background, and Profession. Then, allocate the base Ability Scores following species limits and faction bonuses. 
CRITICAL RULE FOR ABILITY SCORES: DO NOT just assign 10s across the board. You MUST min-max and prioritize abilities based on the Profession and Concept. For example, a Tech-Op needs high INT (13-14) and might dump WIL or PER to 8 or 9. Make the distribution interesting and optimal. Humans get 60 points total to spend before faction bonuses.]

# Step 3: Skill Priorities
[Identify Favored Skills based on Profession/Background. List the Mandatory, Recommended, and Low Priority Broad and Specialty skills. ONLY use skills explicitly listed in the AI RULES SUMMARY below. DO NOT hallucinate skills.]

# Step 4: BP Budget & Math (Creation Snapshot)
[You have exactly 70 BP (Build Points) + any bonus BP from Flaws. Spend them on the prioritized skills and Perks.
CRITICAL RULES FOR MATH:
1. Favored skills cost 1 BP less than their base cost.
2. The 6 Broad Skills listed under your Species in the AI RULES SUMMARY are completely FREE (0 BP to unlock). You only pay for specialty ranks under them.
3. Explicitly list the cost of every skill purchased. Your math MUST balance perfectly to 0 remaining BP.
4. Record these creation choices into the \`creation\` snapshot block.]

# Step 5: Advancement Math (Current Snapshot)
[You have exactly ${XP_PASSED} XP (Advancement Points). If XP is 0, the \`current\` snapshot is identical to \`creation\`.
Otherwise, spend XP on Specialty Skills based on the XP Cost Scaling rules in the summary (e.g. Ranks 1-5 cost base, Ranks 6-8 cost base+2).
Explicitly show the math and XP spent. Record the final upgraded stats and ranks into the \`current\` snapshot block.]

# Step 6: Final JSON
[Output the final, fully valid JSON object inside a \`\`\`json block. It must perfectly match the BP Math from Step 4 and XP Math from Step 5, using the dual-snapshot schema (\`creation\` and \`current\`).]

---

### AI RULES SUMMARY (REFERENCE)
EOF

cat tools/character_generator/ai_rules_summary.md >> "$OUT_FILE"

cat << EOF >> "$OUT_FILE"

---

### CHARACTER CONCEPT:
EOF

echo "$CONCEPT" >> "$OUT_FILE"
echo "Prompt written to $OUT_FILE"
