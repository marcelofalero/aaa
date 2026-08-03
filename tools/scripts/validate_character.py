#!/usr/bin/env python3
"""
Character JSON Rulebook Validator

Validates character JSON files against canonical rulebook mandates:
1. Build Points (BP / Creation Points): Remaining BP MUST be 0 for finalized characters.
2. Specialty Creation Rank Cap: Creation ranks for any specialty skill CANNOT exceed 3.
3. Broad Skill Cap: Max 5 broad skills at creation (excluding species/faction free broads).
4. Broad vs Specialty Hierarchy: Broad & specialty skills must match skills-table.json definitions.
   Specialty skills require their parent broad skill to be trained.
5. Favored Skill Discounting: Favored broads/specialties cost standardCost - 1 (min 1).
6. Campaign Advancement Points (AP) & Rank Scaling: Campaign ranks accrue proper AP costs
   with rank scaling penalties (Ranks 6-8: +2 AP, Ranks 9-10: +4 AP, Ranks 11+: +6 AP).
7. Ability Bounds & Profession Requirements.
"""

import sys
import json
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SKILLS_TABLE_PATH = ROOT_DIR / "site" / "data" / "skills-table.json"

if not SKILLS_TABLE_PATH.exists():
    print(f"Error: Canonical skills table not found at {SKILLS_TABLE_PATH}")
    sys.exit(1)

with open(SKILLS_TABLE_PATH, "r", encoding="utf-8") as f:
    SKILLS_TABLE = json.load(f)

CATEGORY_CANONICAL_MAP = {
    'combate': 'combat', 'combat': 'combat',
    'técnica': 'technical', 'tecnica': 'technical', 'technical': 'technical',
    'social': 'social',
    'otros': 'other', 'other': 'other',
    'psiónica': 'psionics', 'psionica': 'psionics', 'psionics': 'psionics'
}

def normalize_id(identifier):
    if not identifier: return ''
    return str(identifier).lower().strip().replace(' ', '-').replace('_', '-')

def normalize_cat(cat):
    if not cat: return 'other'
    t = str(cat).lower().strip()
    return CATEGORY_CANONICAL_MAP.get(t, t)

# Index skills table for ground truth classification
BROAD_SKILLS = {}
SPECIALTY_SKILLS = {}

for cat in SKILLS_TABLE.get('items', []):
    cat_id = normalize_cat(cat.get('id', cat.get('skill', '')))
    for broad in cat.get('items', []):
        bid = normalize_id(broad.get('id', broad.get('skill', '')))
        BROAD_SKILLS[bid] = {
            'id': bid,
            'name': broad.get('skill', ''),
            'category': cat_id,
            'cost': broad.get('cost', 3),
            'attribute': broad.get('attribute', 'STR')
        }
        for spec in broad.get('items', []):
            sid = normalize_id(spec.get('id', spec.get('skill', '')))
            SPECIALTY_SKILLS[sid] = {
                'id': sid,
                'name': spec.get('skill', ''),
                'parentBroad': bid,
                'category': cat_id,
                'cost': spec.get('cost', 3)
            }

PROFESSION_DATA = {
    'combat-spec': {
        'favoredCategories': ['combat'],
        'favoredBroad': ['modern-ranged-weapons', 'heavy-weapons', 'armor-operation', 'athletics'],
        'favoredSpecialty': []
    },
    'free-agent': {
        'favoredCategories': ['social', 'technical'],
        'favoredBroad': ['covert-ops', 'interaction', 'investigation', 'vehicle-operation'],
        'favoredSpecialty': []
    },
    'tech-spec': {
        'favoredCategories': ['technical'],
        'favoredBroad': ['computer-science', 'engineering', 'knowledge', 'system-operation', 'technical-science', 'demolitions', 'vehicle-operation'],
        'favoredSpecialty': []
    },
    'tech-op': {
        'favoredCategories': ['technical'],
        'favoredBroad': ['computer-science', 'engineering', 'knowledge', 'system-operation', 'technical-science', 'demolitions', 'vehicle-operation'],
        'favoredSpecialty': []
    },
    'mindwalker': {
        'favoredCategories': ['psionics'],
        'favoredBroad': ['telepathy', 'telekinesis', 'biokinesis', 'teleportation'],
        'favoredSpecialty': []
    }
}

SPECIES_FREE_BROAD_SLUGS = {
    'human': ['athletics', 'vehicle-operation', 'stamina', 'knowledge', 'awareness', 'interaction'],
    'fraal': ['awareness', 'resolve', 'vehicle-operation', 'knowledge', 'interaction', 'telepathy'],
    'mechalus': ['athletics', 'vehicle-operation', 'stamina', 'knowledge', 'awareness', 'computer-science'],
    'sesheyan': ['melee-combat', 'acrobatics', 'stamina', 'knowledge', 'awareness', 'interaction'],
    'tsa': ['athletics', 'covert-ops', 'stamina', 'knowledge', 'awareness', 'interaction'],
    'weren': ['athletics', 'melee-combat', 'stamina', 'knowledge', 'awareness', 'interaction']
}

def is_favored(skill_id, cat_id, parent_broad_id=None, profession='combat-spec'):
    prof = PROFESSION_DATA.get(profession, PROFESSION_DATA['combat-spec'])
    cat = normalize_cat(cat_id)
    ns = normalize_id(skill_id)
    np = normalize_id(parent_broad_id) if parent_broad_id else None
    
    if cat in prof['favoredCategories']: return True
    if ns in prof['favoredBroad']: return True
    if np and np in prof['favoredBroad']: return True
    return False

def get_adv_cost(skill_id, target_rank, profession='combat-spec'):
    ns = normalize_id(skill_id)
    if ns in BROAD_SKILLS:
        b = BROAD_SKILLS[ns]
        fav = is_favored(ns, b['category'], profession=profession)
        return max(1, b['cost'] - 1) if fav else b['cost']
    elif ns in SPECIALTY_SKILLS:
        s = SPECIALTY_SKILLS[ns]
        fav = is_favored(ns, s['category'], s['parentBroad'], profession=profession)
        base = max(1, s['cost'] - 1) if fav else s['cost']
        if target_rank >= 11: base += 6
        elif target_rank >= 9: base += 4
        elif target_rank >= 6: base += 2
        return base
    return 3

def validate_character_json(file_path, verbose=False, loose=False):
    path = Path(file_path)
    if not path.exists():
        return False, [f"File not found: {file_path}"], [], []
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return False, [f"JSON Parse Error: {e}"], [], []
    
    errors = []
    warnings = []
    info = []
    
    profession = data.get('profession', 'combat-spec')
    faction = data.get('faction', '')
    species = data.get('species', 'tsa')

    # 1. Build Points (BP) Calculation
    base_sp = 76 if (faction == 'rigunmor' and data.get('bonusPerkOrPointsChoice') == 'points') else 70
    
    creation_perks = data.get('perks', [])
    creation_flaws = data.get('flaws', [])
    
    # Identify free perks granted by species & faction
    FREE_PERK_MAP = {
        'fraal': ['innate psionics', 'psiónica innata'],
        'mechalus': ['cybernetic interface', 'interfaz cibernética'],
        'sesheyan': ['gliding flight', 'vuelo de planeo'],
        'tsa': ['scaly hide', 'piel escamosa'],
        'weren': ['natural weapons (claws)', 'armas naturales (garras)']
    }
    free_perk_names = [p.lower() for p in FREE_PERK_MAP.get(species, [])]
    if faction == 'hatire': free_perk_names.append('faith')
    if faction == 'nariac':
        free_perk_names.extend(['cybernetic interface', 'interfaz cibernética', 'free cyber gear ($5,000)'])
    if faction == 'rigunmor' and data.get('bonusPerkOrPointsChoice') == 'perk':
        free_perk_names.append('filthy rich')

    # Background free flaws (e.g. Borealis automatic Obsessed flaw)
    background_flaws = ['obsessed (borealin discovery)', 'obsessed'] if faction == 'borealis' else []

    chosen_perks = [p for p in creation_perks if (p if isinstance(p, str) else p.get('name', '')).lower() not in free_perk_names]
    chosen_flaws = [f for f in creation_flaws if (f if isinstance(f, str) else f.get('name', '')).lower() not in background_flaws]

    if len(chosen_perks) > 3:
        errors.append(f"Perks Limit Violation: Has {len(chosen_perks)} chosen creation perks (Max allowed is 3).")
    if len(chosen_flaws) > 3:
        errors.append(f"Flaws Limit Violation: Has {len(chosen_flaws)} chosen creation flaws (Max allowed is 3).")

    perk_sp_cost = 0
    for p in chosen_perks:
        if isinstance(p, dict):
            perk_sp_cost += p.get('cost', p.get('finalCost', p.get('level', 1) * 3))
        elif isinstance(p, str):
            perk_sp_cost += 3
            
    flaw_sp_bonus = 0
    for f in chosen_flaws:
        if isinstance(f, dict):
            flaw_sp_bonus += f.get('bonus', f.get('rawBonus', f.get('level', 1) * 3))
        elif isinstance(f, str):
            flaw_sp_bonus += 3
            
    total_sp_budget = base_sp
    creation_sp_spent = perk_sp_cost - flaw_sp_bonus
    broad_count = 0
    adv_skills = data.get('advancementSkills', {})
    skills = data.get('skills', {})
    
    species_free_broads = SPECIES_FREE_BROAD_SLUGS.get(species, ['athletics', 'awareness', 'stamina', 'interaction', 'knowledge', 'covert-ops'])
    
    for skill_name, item in skills.items():
        ns = normalize_id(skill_name)
        total_ranks = item.get('ranks', 0)
        if total_ranks <= 0: continue
        
        camp_ranks = adv_skills.get(skill_name, 0)
        creation_ranks = max(0, total_ranks - camp_ranks)
        
        is_broad = ns in BROAD_SKILLS
        is_specialty = ns in SPECIALTY_SKILLS
        
        if not is_broad and not is_specialty:
            warnings.append(f"Skill '{skill_name}' not found in canonical skills-table.json")
            continue
            
        is_free_broad = (ns in species_free_broads) or (faction == 'voidcorp' and ns == 'business')
        
        if total_ranks > 12:
            errors.append(f"Skill '{skill_name}' rank {total_ranks} exceeds absolute MAX rank cap of 12!")

        if is_broad:
            if not is_free_broad and creation_ranks > 0:
                fav = is_favored(ns, BROAD_SKILLS[ns]['category'], profession=profession)
                cost = max(1, BROAD_SKILLS[ns]['cost'] - 1) if fav else BROAD_SKILLS[ns]['cost']
                creation_sp_spent += cost
                broad_count += 1
                if verbose: info.append(f"Broad '{skill_name}': {cost} BP (favored={fav})")
        else: # Specialty skill
            parent_broad = SPECIALTY_SKILLS[ns]['parentBroad']
            parent_item = skills.get(parent_broad)
            if not parent_item or parent_item.get('ranks', 0) <= 0:
                errors.append(f"Specialty skill '{skill_name}' trained (rank {total_ranks}) but parent broad '{parent_broad}' is missing/untrained!")
                
            if not loose and creation_ranks > 3:
                errors.append(f"Specialty skill '{skill_name}' exceeds MAX 3 Creation Ranks! Found {creation_ranks} creation ranks.")
                
            if creation_ranks > 0:
                fav = is_favored(ns, SPECIALTY_SKILLS[ns]['category'], parent_broad, profession=profession)
                unit_cost = max(1, SPECIALTY_SKILLS[ns]['cost'] - 1) if fav else SPECIALTY_SKILLS[ns]['cost']
                sp_cost = unit_cost * creation_ranks
                creation_sp_spent += sp_cost
                if verbose: info.append(f"Specialty '{skill_name}': {sp_cost} BP ({creation_ranks}r @ {unit_cost} BP/r, favored={fav})")

    remaining_bp = total_sp_budget - creation_sp_spent
    is_finalized = data.get('isFinalized', True) or bool(adv_skills) or data.get('earnedAP', 0) > 0
    
    if not loose:
        if is_finalized and remaining_bp > 0:
            errors.append(f"Unspent Build Points (BP) Violation: Found {remaining_bp} unspent BP! Characters entering campaign mode must spend all BP.")
        elif creation_sp_spent > total_sp_budget:
            errors.append(f"Build Points Budget Exceeded: Spent {creation_sp_spent} BP out of {total_sp_budget} total budget ({total_sp_budget - creation_sp_spent} BP).")
        else:
            info.append(f"Creation Budget (BP): {creation_sp_spent} / {total_sp_budget} BP spent (0 remaining)")

        # 3. Broad Skill Count Check (Max 5)
        if broad_count > 5:
            errors.append(f"Broad Skill Cap Violation: Has {broad_count} broad skills at creation (Max allowed is 5).")
    else:
        info.append(f"Creation Budget (BP): {creation_sp_spent} BP estimated (strict limits disabled in loose mode)")

    # 4. Campaign AP Spent Check
    total_campaign_ap = 0
    for skill_name, camp_ranks in adv_skills.items():
        if camp_ranks <= 0: continue
        ns = normalize_id(skill_name)
        total_ranks = skills.get(skill_name, {}).get('ranks', 0)
        creation_ranks = max(0, total_ranks - camp_ranks)
        
        if ns in BROAD_SKILLS:
            total_campaign_ap += get_adv_cost(ns, 1, profession=profession)
        elif ns in SPECIALTY_SKILLS:
            for r in range(1, camp_ranks + 1):
                total_campaign_ap += get_adv_cost(ns, creation_ranks + r, profession=profession)
                
    for perk in data.get('advancementPerks', []):
        total_campaign_ap += perk.get('apCost', perk.get('cost', 0))
        
    for flaw in data.get('removedFlaws', []):
        total_campaign_ap += flaw.get('apCost', 0)
        
    earned_ap = data.get('earnedAP', 75)
    if is_finalized:
        if total_campaign_ap != earned_ap:
            if not loose:
                warnings.append(f"Campaign AP mismatch: Spent {total_campaign_ap} AP vs Earned {earned_ap} AP.")
            else:
                info.append(f"Total Campaign AP Value: {total_campaign_ap} AP (Strict AP parity disabled in loose mode).")
        else:
            info.append(f"Campaign Advancement: {total_campaign_ap} / {earned_ap} AP spent (Parity OK)")

    # 5. Ability Scores Bounds Check (Species Limits + Faction Adjustments)
    SPECIES_LIMITS = {
        'human': { 'STR': [4, 14], 'DEX': [4, 14], 'CON': [4, 14], 'INT': [4, 14], 'WIL': [4, 14], 'PER': [4, 14] },
        'fraal': { 'STR': [3, 12], 'DEX': [4, 14], 'CON': [3, 12], 'INT': [7, 17], 'WIL': [7, 17], 'PER': [5, 15] },
        'mechalus': { 'STR': [5, 15], 'DEX': [4, 14], 'CON': [5, 15], 'INT': [7, 17], 'WIL': [3, 12], 'PER': [3, 12] },
        'sesheyan': { 'STR': [3, 12], 'DEX': [5, 15], 'CON': [4, 14], 'INT': [3, 12], 'WIL': [5, 15], 'PER': [3, 12] },
        'tsa': { 'STR': [3, 12], 'DEX': [7, 17], 'CON': [3, 12], 'INT': [5, 15], 'WIL': [4, 14], 'PER': [5, 15] },
        'weren': { 'STR': [7, 17], 'DEX': [3, 12], 'CON': [7, 17], 'INT': [3, 12], 'WIL': [3, 12], 'PER': [3, 12] }
    }
    
    spec_limits = json.loads(json.dumps(SPECIES_LIMITS.get(species, SPECIES_LIMITS['human'])))
    if species == 'human':
        if faction == 'thuldan':
            spec_limits['STR'][1] = 15
            spec_limits['CON'][1] = 15
        elif faction == 'borealis':
            spec_limits['INT'][1] = 15
        elif faction == 'orion':
            spec_limits['PER'][1] = 15

    abilities = data.get('abilities', {})
    adv_abilities = data.get('advancementAbilities', {})
    
    for stat, (min_val, max_val) in spec_limits.items():
        base_val = abilities.get(stat, 10)
        bonus_val = 1 if (species == 'human' and ((faction == 'borealis' and stat == 'INT') or (faction == 'orion' and stat == 'PER'))) else 0
        adv_val = adv_abilities.get(stat, 0)
        total_val = base_val + bonus_val + adv_val
        
        if total_val < min_val:
            errors.append(f"Ability Score Violation ({stat}): Total score {total_val} is below species minimum of {min_val}.")
        elif total_val > max_val:
            errors.append(f"Ability Score Violation ({stat}): Total score {total_val} exceeds species maximum of {max_val}.")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings, info

def main():
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    loose = "--loose" in sys.argv
    args = [a for a in sys.argv[1:] if a not in ("-v", "--verbose", "--loose")]
    
    if len(args) < 1:
        target = ROOT_DIR / "premade_characters"
    else:
        target = Path(args[0])
        
    files = []
    if target.is_dir():
        files = list(target.glob("*.json"))
    elif target.is_file():
        files = [target]
    else:
        print(f"Path does not exist: {target}")
        sys.exit(1)
        
    print("==========================================================================")
    print("           CHARACTER BUILDER JSON RULEBOOK VALIDATOR REPORT               ")
    print("==========================================================================")
    
    passed_count = 0
    failed_count = 0
    
    for f in sorted(files):
        rel_path = f.relative_to(ROOT_DIR) if ROOT_DIR in f.parents else f
        valid, errors, warnings, info = validate_character_json(f, verbose=verbose, loose=loose)
        
        status = "✅ PASS" if valid else "❌ FAIL"
        print(f"\n[{status}] {rel_path}")
        
        for item in info:
            print(f"  ℹ️  {item}")
        for w in warnings:
            print(f"  ⚠️  WARNING: {w}")
        for e in errors:
            print(f"  🚨 ERROR: {e}")
            
        if valid: passed_count += 1
        else: failed_count += 1
        
    print("\n--------------------------------------------------------------------------")
    print(f"SUMMARY: Total Checked: {len(files)} | Passed: {passed_count} | Failed: {failed_count}")
    print("==========================================================================")
    
    if failed_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
