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
        pattern = r'\b' + re.escape(en) + r'\b' if re.match(r'^\w', en) else re.escape(en)
        text = re.sub(pattern, mapping[en], text, flags=re.IGNORECASE)
    return text

def rebuild_all():
    mapping = load_mapping()
    print(f'Applying {len(mapping)} terminology rules to ABSOLUTELY EVERYTHING...')
    os.makedirs(SITE_DATA_DIR, exist_ok=True)
    
    skills_yaml = os.path.join(DATA_SOURCES_DIR, 'skills.yaml')
    if os.path.exists(skills_yaml):
        print('Processing Skills...')
        with open(skills_yaml, 'r', encoding='utf-8') as f:
            skills_data = yaml.load(f, Loader=yaml.FullLoader)
        process_skills(skills_data, mapping)
    
    gear_sources = ['armor', 'computers', 'cybernetics', 'survival_gear', 'weapons']
    for base_name in gear_sources:
        yaml_path = os.path.join(DATA_SOURCES_DIR, f'{base_name}.yaml')
        if not os.path.exists(yaml_path): continue
        print(f'Processing {base_name}...')
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        for lang in ['en', 'es']:
            processed = apply_rules_to_node(data, mapping, lang)
            suffix = '.es.json' if lang == 'es' else '.json'
            with open(os.path.join(SITE_DATA_DIR, base_name + suffix), 'w', encoding='utf-8') as f:
                json.dump(processed, f, indent=4, ensure_ascii=False)

def apply_rules_to_node(node, mapping, lang='en'):
    if isinstance(node, dict):
        new_node = {}
        if 'en' in node and 'es' in node and len(node) == 2:
             val = node.get(lang, node.get('en', ''))
             return apply_mapping(val, mapping) if lang == 'es' else val
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
    for broad in skills_list:
        url = broad.get('skill_url', '')
        if not url: continue
        slug = url.strip('/').split('/')[-1]
        out_dir = f'site/content/skills/{slug}'
        os.makedirs(out_dir, exist_ok=True)
        # Markdown Page Generation
        for lang in ['en', 'es']:
            title = broad['skill'] if lang == 'en' else broad.get('skill_es', apply_mapping(broad['skill'], mapping))
            attr = broad['attribute'] if lang == 'en' else apply_mapping(broad['attribute'], mapping)
            cat = broad.get('category', 'Other') if lang == 'en' else broad.get('category_es', apply_mapping(broad.get('category', 'Other'), mapping))
            desc = broad.get('description', '') if lang == 'en' else apply_mapping(broad.get('description_es', broad.get('description', '')), mapping)
            suffix = '.es.md' if lang == 'es' else '.md'
            with open(os.path.join(out_dir, '_index' + suffix), 'w', encoding='utf-8') as f:
                f.write(f'+++\ntitle = "{title}"\nattribute = "{attr}"\ncategory = "{cat}"\ntype = "skill"\nlayout = "list"\n+++\n\n{desc}\n\n')
                for spec in broad.get('specialties', []):
                    s_title = spec['skill'] if lang == 'en' else spec.get('skill_es', apply_mapping(spec['skill'], mapping))
                    s_attr = spec['attribute'] if lang == 'en' else apply_mapping(spec['attribute'], mapping)
                    s_desc = spec.get('description', '') if lang == 'en' else apply_mapping(spec.get('description_es', spec.get('description', '')), mapping)
                    f.write(f'## {s_title}\n### ({s_attr})\n\n{s_desc}\n\n---\n\n')

    # FLAT structure for legacy interactive table
    def build_flat_json(lang):
        groups_dict = defaultdict(list)
        for b in skills_list:
            b_name = b['skill'] if lang == 'en' else b.get('skill_es', apply_mapping(b['skill'], mapping))
            cat = b.get('category', 'Other') if lang == 'en' else b.get('category_es', apply_mapping(b.get('category', 'Other'), mapping))
            attr = b['attribute'] if lang == 'en' else apply_mapping(b['attribute'], mapping)
            groups_dict[cat].append({"skill": b_name, "attribute": attr, "skill_url": b['skill_url'], "cost": b.get('cost', 0), "type": "Broad"})
            for s in b.get('specialties', []):
                s_name = s['skill'] if lang == 'en' else s.get('skill_es', apply_mapping(s['skill'], mapping))
                s_attr = s['attribute'] if lang == 'en' else apply_mapping(s['attribute'], mapping)
                groups_dict[cat].append({"skill": s_name, "attribute": s_attr, "skill_url": s['skill_url'], "cost": s.get('cost', 0), "type": "Specialty"})
        cols = [{"key": "skill", "name": "Skill" if lang == "en" else "Habilidad", "link": True}, {"key": "attribute", "name": "Attr." if lang == "en" else "Atrib."}, {"key": "cost", "name": "Cost" if lang == "en" else "Costo"}]
        return {"columns": cols, "groups": [{"name": cat, "items": items} for cat, items in groups_dict.items()]}

    # NEW NESTED structure with fields (skills-table.json)
    def build_nested_skills_table(lang):
        fields = [
            {"key": "skill", "name": "Skill" if lang == 'en' else "Habilidad", "link": True},
            {"key": "attribute", "name": "Attr." if lang == 'en' else "Atrib."},
            {"key": "cost", "name": "Cost" if lang == 'en' else "Costo"}
        ]
        # Group by category (Tier 1)
        categories = defaultdict(list)
        for b in skills_list:
            cat = b.get('category', 'Other') if lang == 'en' else b.get('category_es', apply_mapping(b.get('category', 'Other'), mapping))
            
            # Tier 2 (Broad)
            broad_entry = {
                "skill": b['skill'] if lang == 'en' else b.get('skill_es', apply_mapping(b['skill'], mapping)),
                "attribute": b['attribute'] if lang == 'en' else apply_mapping(b['attribute'], mapping),
                "skill_url": b['skill_url'],
                "cost": b.get('cost', 0),
                "type": "Broad"
            }
            
            # Tier 3 (Specialties)
            specs = []
            for s in b.get('specialties', []):
                specs.append({
                    "skill": s['skill'] if lang == 'en' else s.get('skill_es', apply_mapping(s['skill'], mapping)),
                    "attribute": s['attribute'] if lang == 'en' else apply_mapping(s['attribute'], mapping),
                    "skill_url": s['skill_url'],
                    "cost": s.get('cost', 0),
                    "type": "Specialty"
                })
            if specs: broad_entry["children"] = specs # Using generic 'children' key
            categories[cat].append(broad_entry)
            
        data = []
        for cat, items in categories.items():
            data.append({
                "skill": cat, # Category name acts as the 'skill' name in the top level
                "type": "Category",
                "children": items
            })
            
        return {"fields": fields, "data": data}

    with open(os.path.join(SITE_DATA_DIR, 'skills.json'), 'w', encoding='utf-8') as f:
        json.dump(build_flat_json('en'), f, indent=4, ensure_ascii=False)
    with open(os.path.join(SITE_DATA_DIR, 'skills.es.json'), 'w', encoding='utf-8') as f:
        json.dump(build_flat_json('es'), f, indent=4, ensure_ascii=False)
        
    # Generate skills-table.json (EN and ES versions for now, or just one if agnostic)
    with open(os.path.join(SITE_DATA_DIR, 'skills-table.json'), 'w', encoding='utf-8') as f:
        json.dump(build_nested_skills_table('en'), f, indent=4, ensure_ascii=False)
    with open(os.path.join(SITE_DATA_DIR, 'skills-table.es.json'), 'w', encoding='utf-8') as f:
        json.dump(build_nested_skills_table('es'), f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    rebuild_all()
    print('Final Data Sync complete.')
