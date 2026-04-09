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

CATEGORY_MAP = {
    'Combat': 'Combate',
    'Technical': 'Técnica',
    'Social': 'Social',
    'Other': 'Otros'
}

def load_mapping():
    mapping = {}
    if not os.path.exists(MAPPING_MD): return mapping
    with open(MAPPING_MD, 'r', encoding='utf-8') as f:
        content = f.read()
    # Simple table parser for terminology mapping
    matches = re.findall(r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|', content)
    for en, es in matches:
        en_clean = en.strip().strip('*').strip('_')
        es_clean = es.strip().strip('*').strip('_')
        if en_clean and es_clean and en_clean not in ['English', ':---', '...']:
            mapping[en_clean] = es_clean
    return mapping

def apply_mapping(text, mapping):
    if not text or not isinstance(text, str): return text
    # Soft mapping using terminology rules
    sorted_en_terms = sorted(mapping.keys(), key=len, reverse=True)
    for en in sorted_en_terms:
        pattern = r'\b' + re.escape(en) + r'\b' if re.match(r'^\w', en) else re.escape(en)
        text = re.sub(pattern, mapping[en], text, flags=re.IGNORECASE)
    return text

def translate_field(en_val, es_override, mapping, lang):
    if lang == 'en': return en_val
    # Strong mapping: prioritize terminal mapping rules over YAML overrides
    if en_val in mapping:
        return mapping[en_val]
    # Soft fallback: use override or apply general mapping rules
    return es_override if es_override else apply_mapping(en_val, mapping)

def slugify(text):
    if not text: return ""
    text = text.lower()
    # Handle common Spanish accents to avoid problematic slugs
    replacements = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ñ': 'n'}
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Replace non-lowercase letters/numbers with -
    text = re.sub(r'[^a-z0-9]', '-', text)
    # Remove consecutive -
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def localize_url(url, lang, localized_title=None):
    if not url: return url
    if lang == 'es':
        # Handle the path
        if url.startswith('/') and not url.startswith('/es/'):
            url = '/es' + url
        # Handle the anchor if we have a localized title (matches Hugo header anchors)
        if '#' in url and localized_title:
            path_part = url.split('#')[0]
            url = f"{path_part}#{slugify(localized_title)}"
    return url

def rebuild_all():
    mapping = load_mapping()
    print(f'Applying {len(mapping)} terminology rules...')
    os.makedirs(SITE_DATA_DIR, exist_ok=True)
    
    skills_yaml = os.path.join(DATA_SOURCES_DIR, 'skills.yaml')
    if os.path.exists(skills_yaml):
        print('Processing Skills...')
        with open(skills_yaml, 'r', encoding='utf-8') as f:
            skills_data = yaml.load(f, Loader=yaml.FullLoader)
        process_skills(skills_data, mapping)
    
    # Generic gear data (Armor, weapons, etc)
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
        # Special case: translation dictionary
        if 'en' in node and 'es' in node and len(node) == 2:
             val = node.get(lang, node.get('en', ''))
             return apply_mapping(val, mapping) if lang == 'es' else val
        
        # Pre-translate name/skill if possible for URL localization
        loc_title = None
        if lang == 'es':
            if 'name' in node: loc_title = translate_field(node['name'], node.get('name_es'), mapping, 'es')
            elif 'skill' in node: loc_title = translate_field(node['skill'], node.get('skill_es'), mapping, 'es')

        for k, v in node.items():
            if k in ['name_es', 'skill_es', 'description_es']: continue
            # Translate keys like 'name'
            if k == 'name':
                new_node[k] = loc_title if lang == 'es' else v
            elif k == 'skill':
                new_node[k] = loc_title if lang == 'es' else v
            elif k == 'attribute':
                new_node[k] = translate_field(v, None, mapping, lang)
            elif k.endswith('url'):
                new_node[k] = localize_url(v, lang, loc_title)
            else:
                new_val = apply_rules_to_node(v, mapping, lang)
                if isinstance(new_val, str) and lang == 'es' and k not in ['type', 'category']:
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
        
        for lang in ['en', 'es']:
            title = translate_field(broad['skill'], broad.get('skill_es'), mapping, lang)
            attr = translate_field(broad['attribute'], None, mapping, lang)
            cat_en = broad.get('category', 'Other')
            cat = cat_en if lang == 'en' else CATEGORY_MAP.get(cat_en, apply_mapping(cat_en, mapping))
            desc = broad.get('description', '') if lang == 'en' else apply_mapping(broad.get('description_es', broad.get('description', '')), mapping)
            
            suffix = '.es.md' if lang == 'es' else '.md'
            with open(os.path.join(out_dir, '_index' + suffix), 'w', encoding='utf-8') as f:
                f.write(f'+++\ntitle = "{title}"\nattribute = "{attr}"\ncategory = "{cat}"\ntype = "skill"\nlayout = "list"\n+++\n\n{desc}\n\n')
                for spec in broad.get('specialties', []):
                    s_title = translate_field(spec['skill'], spec.get('skill_es'), mapping, lang)
                    s_attr = translate_field(spec['attribute'], None, mapping, lang)
                    s_desc = spec.get('description', '') if lang == 'en' else apply_mapping(spec.get('description_es', spec.get('description', '')), mapping)
                    f.write(f'## {s_title}\n### ({s_attr})\n\n{s_desc}\n\n---\n\n')

    def build_nested_skills_table(lang):
        fields = [
            {"key": "skill", "name": "Skill" if lang == 'en' else "Habilidad", "link": True},
            {"key": "attribute", "name": "Attr." if lang == 'en' else "Atrib."},
            {"key": "cost", "name": "Cost" if lang == 'en' else "Costo"}
        ]
        categories = defaultdict(list)
        for b in skills_list:
            cat_en = b.get('category', 'Other')
            cat = cat_en if lang == 'en' else CATEGORY_MAP.get(cat_en, apply_mapping(cat_en, mapping))
            
            b_title = translate_field(b['skill'], b.get('skill_es'), mapping, lang)
            broad_entry = {
                "skill": b_title,
                "attribute": translate_field(b['attribute'], None, mapping, lang),
                "skill_url": localize_url(b['skill_url'], lang, b_title),
                "cost": b.get('cost', 0),
                "type": "Broad"
            }
            specs = []
            for s in b.get('specialties', []):
                s_title = translate_field(s['skill'], s.get('skill_es'), mapping, lang)
                specs.append({
                    "skill": s_title,
                    "attribute": translate_field(s['attribute'], None, mapping, lang),
                    "skill_url": localize_url(s['skill_url'], lang, s_title),
                    "cost": s.get('cost', 0),
                    "type": "Specialty"
                })
            if specs: broad_entry["children"] = specs
            categories[cat].append(broad_entry)
            
        data = []
        for cat in sorted(categories.keys()):
            data.append({"skill": cat, "type": "Category", "children": categories[cat]})
        return {"fields": fields, "data": data}

    with open(os.path.join(SITE_DATA_DIR, 'skills-table.json'), 'w', encoding='utf-8') as f:
        json.dump(build_nested_skills_table('en'), f, indent=4, ensure_ascii=False)
    with open(os.path.join(SITE_DATA_DIR, 'skills-table.es.json'), 'w', encoding='utf-8') as f:
        json.dump(build_nested_skills_table('es'), f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    rebuild_all()
