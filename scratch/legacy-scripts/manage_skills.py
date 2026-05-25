import yaml, os, re, sys

# Custom representer for block scalar (|) strings to ensure clean YAML
def str_presenter(dumper, data):
    if len(data) > 60 or '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)

SKILLS_YAML = 'sources/data_sources/skills.yaml'
MAPPING_MD = 'site/content/notes/terminology-mapping.md'

def load_mapping():
    mapping = {}
    if not os.path.exists(MAPPING_MD): return mapping
    with open(MAPPING_MD, 'r', encoding='utf-8') as f:
        content = f.read()
    # Match | English | Spanish | rows efficiently
    matches = re.findall(r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|', content)
    for en, es in matches:
        en_clean = en.strip().strip('*').strip('_')
        es_clean = es.strip().strip('*').strip('_')
        # Skip headers, separators, and placeholders
        if en_clean and es_clean and en_clean != 'English' and en_clean != ':---' and en_clean != '...':
            mapping[en_clean] = es_clean
    return mapping

def apply_mapping(text, mapping):
    if not text: return ''
    # Sort terms by length (descending) to prevent sub-string collision (e.g., 'Skill' vs 'Skill Points')
    sorted_en_terms = sorted(mapping.keys(), key=len, reverse=True)
    
    # We replace terms while respecting word boundaries to preserve grammar and links
    for en in sorted_en_terms:
        es = mapping[en]
        pattern = r'\b' + re.escape(en) + r'\b'
        text = re.sub(pattern, es, text, flags=re.IGNORECASE)
    return text

def rebuild():
    print(f'Loading {SKILLS_YAML}...')
    with open(SKILLS_YAML, 'r', encoding='utf-8') as f:
        skills = yaml.load(f, Loader=yaml.FullLoader)
    
    mapping = load_mapping()
    print(f'Loaded {len(mapping)} terminology rules from {MAPPING_MD}.')
    
    for broad in skills:
        url = broad.get('skill_url', '')
        if not url: continue
        slug = url.strip('/').split('/')[1]
        out_dir = f'site/content/skills/{slug}'
        os.makedirs(out_dir, exist_ok=True)
        
        # --- Generate English Page ---
        en_path = os.path.join(out_dir, '_index.md')
        with open(en_path, 'w', encoding='utf-8') as f:
            f.write('+++\n')
            f.write(f'title = \"{broad["skill"]}\"\n')
            f.write(f'attribute = \"{broad["attribute"]}\"\n')
            f.write(f'category = \"{broad["category"]}\"\n')
            f.write('+++\n\n')
            f.write(broad.get('description', '') + '\n\n')
            
            for spec in broad.get('specialties', []):
                attr_part = f' ({spec["attribute"]})' if spec.get('attribute') else ''
                f.write(f'## {spec["skill"]}{attr_part}\n\n')
                f.write(spec.get('description', '') + '\n\n')
                f.write('---\n\n')
        
        # --- Generate Spanish Page ---
        es_path = os.path.join(out_dir, '_index.es.md')
        
        # Translate and Enforce Metadata Rules
        title_es = broad.get('skill_es', apply_mapping(broad['skill'], mapping))
        attr_es = apply_mapping(broad['attribute'], mapping)
        cat_es = broad.get('category_es', apply_mapping(broad['category'], mapping))
        
        with open(es_path, 'w', encoding='utf-8') as f:
            f.write('+++\n')
            f.write(f'title = \"{title_es}\"\n')
            f.write(f'attribute = \"{attr_es}\"\n')
            f.write(f'category = \"{cat_es}\"\n')
            f.write('+++\n\n')
            
            # Prioritize existing Spanish description but enforce rules
            # Fallback to translated English if no Spanish description exists
            desc_es = broad.get('description_es', '')
            if not desc_es:
                desc_es = apply_mapping(broad.get('description', ''), mapping)
            else:
                desc_es = apply_mapping(desc_es, mapping)
                
            f.write(desc_es + '\n\n')
            
            for spec in broad.get('specialties', []):
                spec_title_es = spec.get('skill_es', apply_mapping(spec['skill'], mapping))
                spec_attr_es = apply_mapping(spec['attribute'], mapping)
                f.write(f'## {spec_title_es} ({spec_attr_es})\n\n')
                
                spec_desc_es = spec.get('description_es', '')
                if not spec_desc_es:
                    spec_desc_es = apply_mapping(spec.get('description', ''), mapping)
                else:
                    spec_desc_es = apply_mapping(spec_desc_es, mapping)
                    
                f.write(spec_desc_es + '\n\n')
                f.write('---\n\n')

    print(f'Sync Complete. Regenerated {len(skills)} skills across both languages.')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: manage_skills.py [rebuild]')
    elif sys.argv[1] == 'rebuild':
        rebuild()
    else:
        print(f'Unknown command: {sys.argv[1]}')
