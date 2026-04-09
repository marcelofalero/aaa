import yaml, os, re, sys, json, copy
from collections import defaultdict

# Custom representer for block scalar (|) strings to ensure clean YAML output
def str_presenter(dumper, data):
    if len(data) > 60 or '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)

DATA_SOURCES_DIR = 'sources/data_sources'
SITE_DATA_DIR = 'site/data'
SKILLS_CONTENT_DIR = 'site/content/skills'
MAPPING_MD = 'site/content/notes/terminology-mapping.md'

def load_mapping():
    mapping = {}
    if not os.path.exists(MAPPING_MD): return mapping
    with open(MAPPING_MD, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|', content)
    for en, es in matches:
        en_clean = en.strip().strip('*').strip('_')
        es_clean = es.strip().strip('*').strip('_')
        if en_clean and es_clean and en_clean not in ['English', ':---', '...']:
            mapping[en_clean] = es_clean
    return mapping

def apply_mapping(text, mapping):
    if not text or not isinstance(text, str): return text
    sorted_en_terms = sorted(mapping.keys(), key=len, reverse=True)
    for en in sorted_en_terms:
        # Use word boundaries if it's a word, else just replace
        pattern = r'\b' + re.escape(en) + r'\b' if re.match(r'^\w', en) else re.escape(en)
        text = re.sub(pattern, mapping[en], text, flags=re.IGNORECASE)
    return text

def is_untrained_forbidden(description):
    if not description: return False
    forbidden_phrases = [
        "skill can't be used untrained",
        "skill can’t be used untrained",
        "habilidad no se puede usar sin entrenamiento",
        "can't be used untrained"
    ]
    desc_lower = description.lower()
    return any(phrase in desc_lower for phrase in forbidden_phrases)

def rebuild_all():
    mapping = load_mapping()
    print(f'Applying {len(mapping)} terminology rules to ABSOLUTELY EVERYTHING...')
    
    os.makedirs(SITE_DATA_DIR, exist_ok=True)
    
    # 1. Handle Skills (Pages + JSON)
    skills_yaml = os.path.join(DATA_SOURCES_DIR, 'skills.yaml')
    if os.path.exists(skills_yaml):
        print('Processing Skills...')
        with open(skills_yaml, 'r', encoding='utf-8') as f:
            skills_data = yaml.load(f, Loader=yaml.FullLoader)
        process_skills(skills_data, mapping)
    
    # 2. Handle Equipment (Armor, Computers, etc.)
    gear_sources = ['armor', 'computers', 'cybernetics', 'survival_gear', 'weapons']
    for base_name in gear_sources:
        yaml_path = os.path.join(DATA_SOURCES_DIR, f'{base_name}.yaml')
        if not os.path.exists(yaml_path): continue
        print(f'Processing {base_name}...')
        
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        
        # English JSON
        en_json = apply_rules_to_node(data, mapping, lang='en')
        out_en = os.path.join(SITE_DATA_DIR, f'{base_name}.json')
        with open(out_en, 'w', encoding='utf-8') as f:
            json.dump(en_json, f, indent=4, ensure_ascii=False)
            
        # Spanish JSON
        es_json = apply_rules_to_node(data, mapping, lang='es')
        es_filename = f'{base_name}.es.json'
        out_es = os.path.join(SITE_DATA_DIR, es_filename)
        with open(out_es, 'w', encoding='utf-8') as f:
            json.dump(es_json, f, indent=4, ensure_ascii=False)

def apply_rules_to_node(node, mapping, lang='en'):
    if isinstance(node, dict):
        new_node = {}
        # Special handling for EN/ES nested objects
        if 'en' in node and 'es' in node and len(node) == 2:
             val = node.get(lang, node.get('en', ''))
             return apply_mapping(val, mapping) if lang == 'es' else val
        
        # Handle localized name fields
        if lang == 'es' and 'name_es' in node:
            new_node['name'] = apply_mapping(node['name_es'], mapping)
        
        for k, v in node.items():
            if k in ['name_es', 'skill_es', 'description_es']: continue
            if k == 'name' and lang == 'es' and 'name_es' in node: continue
            
            new_val = apply_rules_to_node(v, mapping, lang)
            if isinstance(new_val, str) and lang == 'es':
                new_val = apply_mapping(new_val, mapping)
            new_node[k] = new_val
        return new_node
    elif isinstance(node, list):
        return [apply_rules_to_node(item, mapping, lang) for item in node]
    else:
        return node

def process_skills(skills_list, mapping):
    # 1. Rebuild Hugo Pages
    for broad in skills_list:
        url = broad.get('skill_url', '')
        if not url: continue
        slug = url.strip('/').split('/')[-1] # Fix: get the actual slug, usually after /skills/
        out_dir = f'site/content/skills/{slug}'
        os.makedirs(out_dir, exist_ok=True)
        
        # EN Page
        with open(os.path.join(out_dir, '_index.md'), 'w', encoding='utf-8') as f:
            f.write(f'+++\ntitle = "{broad["skill"]}"\nattribute = "{broad["attribute"]}"\ncategory = "{broad["category"]}"\ntype = "skill"\nlayout = "list"\n+++\n\n')
            f.write(broad.get('description', '') + '\n\n')
            for spec in broad.get('specialties', []):
                attr = f'### ({spec["attribute"]})' if spec.get('attribute') else ''
                f.write(f'## {spec["skill"]}\n{attr}\n\n{spec.get("description", "")}\n\n---\n\n')
        
        # ES Page
        title_es = broad.get('skill_es', apply_mapping(broad['skill'], mapping))
        attr_es = apply_mapping(broad['attribute'], mapping)
        cat_es = apply_mapping(broad['category'], mapping)
        desc_es = apply_mapping(broad.get('description_es', broad.get('description', '')), mapping)
        
        with open(os.path.join(out_dir, '_index.es.md'), 'w', encoding='utf-8') as f:
            f.write(f'+++\ntitle = "{title_es}"\nattribute = "{attr_es}"\ncategory = "{cat_es}"\ntype = "skill"\nlayout = "list"\n+++\n\n')
            f.write(desc_es + '\n\n')
            for spec in broad.get('specialties', []):
                s_title_es = spec.get('skill_es', apply_mapping(spec['skill'], mapping))
                s_attr_es = apply_mapping(spec['attribute'], mapping)
                s_desc_es = apply_mapping(spec.get('description_es', spec.get('description', '')), mapping)
                attr_header = f'### ({s_attr_es})' if s_attr_es else ''
                f.write(f'## {s_title_es}\n{attr_header}\n\n{s_desc_es}\n\n---\n\n')

    # 2. Rebuild site/data/skills.json and skills.es.json
    def build_json(lang):
        groups_dict = defaultdict(list)
        for b in skills_list:
            # Metadata for Broad Skill
            name = b['skill'] if lang == 'en' else b.get('skill_es', apply_mapping(b['skill'], mapping))
            cat = b['category'] if lang == 'en' else b.get('category_es', apply_mapping(b['category'], mapping))
            attr = b['attribute'] if lang == 'en' else apply_mapping(b['attribute'], mapping)
            
            broad_entry = {
                "skill": name,
                "attribute": attr,
                "skill_url": b['skill_url'],
                "cost": b.get('cost', 0),
                "type": "Broad",
                "tier": b.get('tier', 1),
                "pr": b.get('pr', ''),
                "untrained": not is_untrained_forbidden(b.get('description', ''))
            }
            
            # Specialties
            specs = []
            for s in b.get('specialties', []):
                s_name = s['skill'] if lang == 'en' else s.get('skill_es', apply_mapping(s['skill'], mapping))
                s_attr = s['attribute'] if lang == 'en' else apply_mapping(s['attribute'], mapping)
                specs.append({
                    "skill": s_name,
                    "attribute": s_attr,
                    "skill_url": s['skill_url'],
                    "cost": s.get('cost', 0),
                    "type": "Specialty",
                    "tier": s.get('tier', 1 + (1 if s.get('cost', 0) >= 3 else 0)), # Tier heuristic
                    "pr": s.get('pr', ''),
                    "untrained": not is_untrained_forbidden(s.get('description', ''))
                })
            
            if specs:
                broad_entry["specialties"] = specs
            
            groups_dict[cat].append(broad_entry)
            
        return {"groups": [{"name": cat, "items": items} for cat, items in groups_dict.items()]}

    with open(os.path.join(SITE_DATA_DIR, 'skills.json'), 'w', encoding='utf-8') as f:
        json.dump(build_json('en'), f, indent=4, ensure_ascii=False)
    with open(os.path.join(SITE_DATA_DIR, 'skills.es.json'), 'w', encoding='utf-8') as f:
        json.dump(build_json('es'), f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    rebuild_all()
    print('ABSOLUTELY EVERYTHING synchronised and rule-enforced.')
