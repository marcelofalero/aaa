import sys
import os
import argparse
import yaml

def load_file(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return f.read().strip()
    return ""

def generate_step1_prompt(concept):
    return f"""You are an expert RPG character creator for the Alternity RPG system.
Your task is to take the user's raw concept and generate a highly detailed biography and concept specification.

RAW CONCEPT:
{concept}

TASK:
Write a markdown response detailing the character's:
- Name
- Concept (1 sentence)
- Motivation
- Attitude
- Traits (physical or personality)

Do not output JSON, just a structured markdown overview of who this character is.
"""

def generate_step2_prompt(step1_out, rules_summary):
    return f"""You are an expert RPG character creator. You are in Step 2: Foundations.
Based on the character biography generated in Step 1, select the appropriate Faction, Species, Background, and Profession.
Then, allocate the character's Ability Scores (STR, DEX, CON, INT, WIL, PER).

STEP 1 BIOGRAPHY:
{step1_out}

RULES:
- Humans get 60 ability points to distribute among the 6 stats (min 4, max 14).
- Other species have different limits (see Rules Summary).
- Borealis Humans get +1 INT (max 15). Orion Humans get +1 PER. Union of Sol gets +2 free points (62 total).

RULES SUMMARY:
{rules_summary}

TASK:
Output a markdown summary defining:
- Faction (slug)
- Species (slug)
- Background (slug)
- Profession (slug)
- Ability Scores (STR, DEX, CON, INT, WIL, PER)
Briefly explain your choices.
"""

def generate_step3_prompt(step1_out, step2_out, rules_summary):
    return f"""You are an expert RPG character creator. You are in Step 3: Skill Priorities.
Based on the character's foundations, determine which skills are Mandatory vs Recommended.

BIOGRAPHY:
{step1_out}

FOUNDATIONS:
{step2_out}

RULES:
- Identify any "Favored Skills" based on the chosen Profession and Background from the Rules Summary.
- List Broad and Specialty skills that fit the concept perfectly.
- REMEMBER: You MUST ONLY select skills that exist in the Rules Summary. Do not invent skills.

RULES SUMMARY:
{rules_summary}

TASK:
Output a markdown list of High Priority, Medium Priority, and Low Priority skills. Explicitly name the broad skill and the specialty skill (e.g., `technical-science` -> `repair`).
"""

def generate_step4_prompt(step2_out, step3_out, rules_summary):
    return f"""You are an expert RPG character creator. You are in Step 4: BP Budget & Trait Assignment.
You have 70 BP (Build Points) to spend on the traits prioritized in Step 3.

FOUNDATIONS:
{step2_out}

SKILL PRIORITIES:
{step3_out}

RULES:
- You have 70 BP base.
- You may select Flaws to gain bonus BP (+3 BP per flaw).
- You may select Perks which cost BP.
- Broad skills cost their listed base cost to unlock (Rank 1).
- Specialty skills cost their listed base cost PER RANK (Max 3 ranks at creation).
- Favored skills cost 1 BP less than their base cost (e.g., a 7 BP skill becomes 6 BP).
- You MUST spend all BP. Math must balance perfectly.

RULES SUMMARY:
{rules_summary}

TASK:
Output a strict mathematical breakdown of how the 70 BP (+ Flaw bonuses) is spent. List the cost of every trait purchased.
"""

def generate_step5_prompt(step1, step2, step3, step4):
    return f"""You are an expert RPG character creator. You are in Step 5: Final Profile Assembly.
Review all the previous steps and compile them into the final structured output formats.

BIOGRAPHY: {step1}
FOUNDATIONS: {step2}
SKILL PRIORITIES: {step3}
BP MATH: {step4}

TASK:
Output exactly two code blocks:
1. A ```json block containing the Character Profile (Bio, Foundations, Abilities).
2. A ```csv block containing ALL purchased traits with dual snapshots (creation vs current ranks).

### 1. PROFILE JSON SCHEMA
```json
{{
  "step": 7,
  "isFinalized": true,
  "bio": {{ "name": "...", "player": "...", "concept": "...", "motivation": "...", "attitude": "...", "traits": "..." }},
  "faction": "slug",
  "species": "slug",
  "background": "slug",
  "profession": "slug",
  "earnedXP": 0,
  "abilities": {{ "STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIL": 10, "PER": 10 }}
}}
```

### 2. DUAL-RANK CSV
The CSV MUST be wrapped in a ```csv code block.
It MUST contain exactly these headers: slug, type, creation_ranks, current_ranks, as, parent

Type Key:
bs = Broad Skill
ss = Specialty Skill
p = Perk
f = Flaw
pbs = Psionic Broad
ps = Psionic Specialty
fx = FX Power

Example output:
```csv
slug,type,creation_ranks,current_ranks,as,parent
technical-science,bs,1,1,INT,skills
repair,ss,1,5,INT,technical-science
innate-psionics,p,1,1,WIL,perks
impulsive,f,1,1,WIL,flaws
```
"""

def main():
    parser = argparse.ArgumentParser(description="Character Generation Pipeline")
    parser.add_argument("step", type=int, help="Pipeline step (1-5)")
    parser.add_argument("--out", type=str, default="output", help="Directory to store intermediate state")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    
    rules_path = "tools/character_generator/ai_rules_summary.md"
    rules = load_file(rules_path) if os.path.exists(rules_path) else "RULES MISSING"

    if args.step == 1:
        concept = load_file(os.path.join(args.out, "concept.txt"))
        print(generate_step1_prompt(concept))
    elif args.step == 2:
        step1 = load_file(os.path.join(args.out, "step1.md"))
        print(generate_step2_prompt(step1, rules))
    elif args.step == 3:
        step1 = load_file(os.path.join(args.out, "step1.md"))
        step2 = load_file(os.path.join(args.out, "step2.md"))
        print(generate_step3_prompt(step1, step2, rules))
    elif args.step == 4:
        step2 = load_file(os.path.join(args.out, "step2.md"))
        step3 = load_file(os.path.join(args.out, "step3.md"))
        print(generate_step4_prompt(step2, step3, rules))
    elif args.step == 5:
        step1 = load_file(os.path.join(args.out, "step1.md"))
        step2 = load_file(os.path.join(args.out, "step2.md"))
        step3 = load_file(os.path.join(args.out, "step3.md"))
        step4 = load_file(os.path.join(args.out, "step4.md"))
        print(generate_step5_prompt(step1, step2, step3, step4))

if __name__ == "__main__":
    main()
