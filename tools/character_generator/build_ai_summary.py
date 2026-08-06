import yaml
import json
import os

def load_yaml(filepath):
    try:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    except:
        return {}

def build_summary():
    out = []
    out.append("# ALTERNITY RPG AI RULES SUMMARY")
    out.append("This is an AI-optimized reference containing all mechanics needed to build and advance characters.")
    
    # SPECIES & FACTIONS
    out.append("\n## SPECIES & FACTIONS LORE & TENDENCIES")
    out.append("### SPECIES (Including Free Broad Skills & Perks)")
    out.append("- **Human:** Versatile. Free Broads: `athletics`, `vehicle-operation`, `stamina`, `knowledge`, `awareness`, `interaction`.")
    out.append("- **Fraal:** Ancient, psionically gifted. Free Broads: `awareness`, `resolve`, `vehicle-operation`, `knowledge`, `interaction`, `telepathy`.")
    out.append("- **Mechalus:** Cybernetic. Free Broads: `athletics`, `vehicle-operation`, `stamina`, `knowledge`, `awareness`, `computer-science`. Free Perks: `cybernetic_interface`.")
    out.append("- **Sesheyan:** Winged hunters. Free Broads: `melee-combat`, `acrobatics`, `stamina`, `knowledge`, `awareness`, `interaction`.")
    out.append("- **T'sa:** Fast tinkers. Free Broads: `athletics`, `covert-ops`, `stamina`, `knowledge`, `awareness`, `interaction`.")
    out.append("- **Weren:** Large furry warriors. Free Broads: `athletics`, `melee-combat`, `stamina`, `knowledge`, `awareness`, `interaction`.")
    
    out.append("\n### HUMAN FACTIONS")
    out.append("- **Austrin-Ontis:** Pragmatic survivalists focusing on practicality and resilience.")
    out.append("- **Borealis Republic:** Progressive innovators focusing on education and technology.")
    out.append("- **Orion League:** Opportunistic free traders and fast-talking merchants.")
    out.append("- **Rigunmor Star Consortium:** Ruthless megacorporation hyper-focused on efficiency and wealth.")
    out.append("- **Thuldan Empire:** Highly militarized and disciplined, valuing physical perfection.")
    out.append("- **Union of Sol:** Diverse traditionalists maintaining Earth's rich cultures.")
    out.append("- **Voidcorp:** Bureaucratic corporate drones heavily reliant on AI and process.")
    out.append("- **Galactic Concord:** Peacekeeping diplomats focused on stellar unity and defense.")
    
    base_dir = "sources/data_sources"
    
    # 1. Core Creation Rules
    out.append("\n## CREATION RULES")
    out.append("- **Budget:** 70 BP (Build Points). Flaws add BP (e.g. +3). Perks cost BP.")
    out.append("- **Favored Skills:** If a skill is favored by Profession or Background, its base BP cost is reduced by 1 (e.g. a 7 BP skill becomes 6 SP).")
    out.append("- **Skill Ranks:** Broad skills cost BP to unlock (Rank 1). Specialty skills cost BP *per rank*. Max 3 ranks per specialty skill at creation.")
    
    # 2. Advancement Rules & Titles
    out.append("\n## ADVANCEMENT RULES & TITLES")
    out.append("After creation, characters use XP (Advancement Points). Total XP dictates Title and limits.")
    out.append("- **Rookie** (0 XP): Max Skill Rank 5, Max Broads 5, +0 Ability Points.")
    out.append("- **Seasoned** (50 XP): Max Skill Rank 8, Max Broads 7, +1 Ability Point.")
    out.append("- **Veteran** (100 XP): Max Skill Rank 10, Max Broads 9, +2 Ability Points.")
    out.append("- **Exemplar** (200 XP): Max Skill Rank 12, Max Broads 11, +3 Ability Points.")
    out.append("- **Legend** (300 XP): Max Skill Rank 12, Max Broads 13, +4 Ability Points.")
    out.append("\n**AP Cost Scaling for Specialty Skills:**")
    out.append("- Ranks 1 to 5: baseCost (e.g. 2 or 3 XP)")
    out.append("- Ranks 6 to 8: baseCost + 2")
    out.append("- Ranks 9 to 10: baseCost + 4")
    out.append("- Ranks 11+: baseCost + 6")

    # 3. Skills
    out.append("\n## SKILLS (Costs and Categories)")
    skills_data = load_yaml(os.path.join(base_dir, 'skills.yaml'))
    for broad_slug, broad_data in skills_data.get('items', {}).items():
        cat = broad_data.get('category', 'Other')
        out.append(f"- **{broad_slug}** (Broad, {broad_data.get('cost', 3)} BP, {cat})")
        for spec_slug, spec_data in broad_data.get('items', {}).items():
            out.append(f"  - {spec_slug} ({spec_data.get('cost', 3)} SP/rank)")

    # 4. Perks & Flaws
    out.append("\n## PERKS")
    perks_data = load_yaml(os.path.join(base_dir, 'perks.yaml'))
    for perk_slug, perk_data in perks_data.get('items', {}).items():
        en_desc = perk_data.get('localized', [{}])[0].get('en', {}).get('description', '')
        short_desc = en_desc.split('.')[0].replace('\n', ' ') + '.' if en_desc else ''
        target_note = " [REQUIRES TARGET SKILL IN 'parent' CSV COLUMN]" if "skill" in perk_slug else ""
        out.append(f"- **{perk_slug}** (Cost: {'/'.join(map(str, perk_data.get('cost', [3])))} BP){target_note}: {short_desc}")
        
    out.append("\n## FLAWS")
    flaws_data = load_yaml(os.path.join(base_dir, 'flaws.yaml'))
    for flaw_slug, flaw_data in flaws_data.get('items', {}).items():
        en_desc = flaw_data.get('localized', [{}])[0].get('en', {}).get('description', '')
        short_desc = en_desc.split('.')[0].replace('\n', ' ') + '.' if en_desc else ''
        out.append(f"- **{flaw_slug}** (Bonus: +{'/'.join(map(str, flaw_data.get('bonus', [3])))} BP): {short_desc}")
        
    # 5. Backgrounds
    out.append("\n## BACKGROUNDS (Favored Skills)")
    bg_data = load_yaml(os.path.join(base_dir, 'backgrounds.yaml'))
    for bg_slug, bg_obj in bg_data.get('items', {}).items():
        en_data = bg_obj.get('localized', [{}])[0]
        out.append(f"- **{bg_slug}**: {bg_obj.get('favored_broad_skill', '')} {en_data.get('favored_specialty_skills', '')}")

    # 6. Equipment
    out.append("\n## EQUIPMENT (Weapons & Armor)")
    out.append("Just reference these if the user concept requires gear. No strict AP/SP costs for equipment, usually bought with credits in-game.")
    weap_data = load_yaml(os.path.join(base_dir, 'weapons.yaml'))
    out.append("- **Weapons**: " + ", ".join(list(weap_data.get('items', {}).keys())[:20]) + " ...")
    arm_data = load_yaml(os.path.join(base_dir, 'armor.yaml'))
    out.append("- **Armor**: " + ", ".join(list(arm_data.get('items', {}).keys())[:15]) + " ...")

    with open('tools/character_generator/ai_rules_summary.md', 'w') as f:
        f.write("\n".join(out))

if __name__ == "__main__":
    build_summary()
