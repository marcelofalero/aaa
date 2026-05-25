import yaml
import re

def audit():
    # Load mapping
    expected_skills = {}
    with open('sources/psionic-skill/definitive_mapping.txt', 'r') as f:
        content = f.read()
        # Find numeric mappings like 30:Dimension Walk
        matches = re.finditer(r'(\d+):([A-Za-z ]+)', content)
        for m in matches:
            idx = int(m.group(1))
            name = m.group(2).strip().lower().replace(' ', '-')
            expected_skills[name] = m.group(2).strip()

    # Load YAML
    with open('sources/data_sources/psionics.yaml', 'r') as f:
        data = yaml.safe_load(f)
    
    disciplines = data.get('items', {})
    actual_skills = set()
    report = []
    
    for disc_name, disc_data in disciplines.items():
        skills = disc_data.get('items', {})
        for skill_id, skill_data in skills.items():
            actual_skills.add(skill_id.lower())
            loc = skill_data.get('localized', [])
            en = {}
            es = {}
            for item in loc:
                if 'en' in item: en = item['en']
                if 'es' in item: es = item['es']
            
            en_desc = en.get('description', '')
            es_desc = es.get('description', '')
            
            fidelity = "Detailed" if len(en_desc) > 300 else "Short"
            has_rank_ben = "Rank Benefits" in en_desc or "improved" in en_desc.lower()
            
            report.append({
                "id": skill_id,
                "fidelity": fidelity,
                "en_len": len(en_desc),
                "es_len": len(es_desc),
                "rank_ben": has_rank_ben
            })
            
    print(f"{'Skill ID':<25} | {'Fidelity':<10} | {'EN Len':<6} | {'ES Len':<6} | {'Rank Ben'}")
    print("-" * 65)
    for r in report:
        print(f"{r['id']:<25} | {r['fidelity']:<10} | {r['en_len']:<6} | {r['es_len']:<6} | {r['rank_ben']}")

    print("\nMissing Skills:")
    for skill_id, skill_name in expected_skills.items():
        if skill_id not in actual_skills:
            # Check for slight variations
            if any(skill_id in s or s in skill_id for s in actual_skills):
                continue
            print(f"- {skill_name} ({skill_id})")

if __name__ == "__main__":
    audit()
