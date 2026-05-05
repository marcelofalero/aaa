import yaml, json, os

SKILLS_YAML = 'sources/data_sources/skills.yaml'
OUTPUT_JSON = 'site/data/skills.json'

def get_en_name(node, default='Unknown'):
    for loc in node.get('localized', []):
        if 'en' in loc:
            return loc['en'].get('name', default)
    return node.get('skill', node.get('name', default))

def generate_legacy_json():
    if not os.path.exists(SKILLS_YAML):
        print(f"Error: {SKILLS_YAML} not found.")
        return

    with open(SKILLS_YAML, 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    
    items_raw = data.get('items', {})
    
    # If items is a dict (acrobatics: {...}), convert it to a sorted list of dicts
    if isinstance(items_raw, dict):
        items = []
        for k, v in items_raw.items():
            if isinstance(v, dict):
                item = v.copy()
                item['id'] = k
                items.append(item)
        # Sort for consistency
        items.sort(key=lambda x: get_en_name(x))
    else:
        items = items_raw

    legacy_items = []
    
    for broad in items:
        # Add Broad Skill
        name = get_en_name(broad)
        url = broad.get('url', broad.get('skill_url', ''))
        legacy_items.append({
            "skill": name,
            "skill_url": url
        })
        
        # Add Specialty Skills
        specs_raw = broad.get('items', {})
        if isinstance(specs_raw, dict):
            specs = []
            for k, v in specs_raw.items():
                if isinstance(v, dict):
                    s = v.copy()
                    s['id'] = k
                    specs.append(s)
            specs.sort(key=lambda x: get_en_name(x))
        else:
            specs = specs_raw
            
        for spec in specs:
            s_name = get_en_name(spec)
            s_url = spec.get('url', spec.get('skill_url', ''))
            if not s_url and url:
                # Fallback anchor generation
                anchor = s_name.lower().replace(' ', '-').replace('\'', '').replace('(', '').replace(')', '')
                s_url = f"{url}#{anchor}"
            
            legacy_items.append({
                "skill": s_name,
                "skill_url": s_url
            })

    # Wrap in the "groups" structure expected by build_sheet.py
    output = {
        "search_config": {
            "display_name": "SKILLS",
            "base_url": "/skills/",
            "section": "skills"
        },
        "groups": [
            {
                "items": legacy_items
            }
        ]
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully recreated {OUTPUT_JSON} with {len(legacy_items)} entries.")

if __name__ == "__main__":
    generate_legacy_json()
