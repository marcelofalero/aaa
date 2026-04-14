import os
import re
import yaml

# Custom YAML dumper for better formatting of multi-line strings
class FoldedDumper(yaml.SafeDumper):
    pass

def folded_str_representer(dumper, data):
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

FoldedDumper.add_representer(str, folded_str_representer)

# Manual overrides for Spanish matching where the name differs significantly
ES_MAPPING = {
    "Bio-armor": "Bioarmadura",
    "Bioweapon": "Bioarma",
    "Clamber": "Trepado",
    "Control Metabolism": "Control del Metabolismo",
    "Heal": "Sanar",
    "Intangibility": "Intangibilidad",
    "Morph": "Metamorfosis",
    "Rejuvenate": "Rejuvenecer",
    "Shatter": "Destrozar",
    "Transfer Damage": "Transferir Daño",
    "Medical Knowledge": "Conocimiento Médico", # Example
    "Street knowledge": "Conocimiento Callejero" # Example
}

def extract_descriptions(filepath):
    """Extracts content from markdown, mapping by header OR subheader name."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by ## headers
    sections = re.split(r'\n## ', content)
    data = {}
    
    for section in sections[1:]: # Skip frontmatter
        lines = section.splitlines()
        if not lines:
            continue
        
        main_header = lines[0].strip()
        
        # Look for English name in ### (Name)
        eng_name = main_header
        for line in lines[1:]:
            m = re.match(r'^### \(([^)]+)\)', line)
            if m:
                eng_name = m.group(1).strip()
                break
        
        # Find description start
        start_idx = 1
        for i, line in enumerate(lines[1:], 1):
            if line.startswith('###') or line.strip().startswith('*'):
                start_idx = i + 1
            elif line.strip() == "":
                continue
            else:
                break
        
        description = "\n".join(lines[start_idx:]).strip()
        
        # Store by both names for matching
        data[main_header] = {"name": main_header, "desc": description}
        if eng_name != main_header:
            data[eng_name] = {"name": main_header, "desc": description}
    
    return data

def main():
    root_dir = "/home/dimble/projects/aaa"
    yaml_path = os.path.join(root_dir, "sources/data_sources/psionics.yaml")
    site_content_dir = os.path.join(root_dir, "site/content/psionics")
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        psionics_data = yaml.safe_load(f)
    
    disciplines = ["biokinesis", "esp", "telepathy", "telekinesis", "psychoportation"]
    
    for disc in disciplines:
        en_path = os.path.join(site_content_dir, disc, "_index.md")
        es_path = os.path.join(site_content_dir, disc, "_index.es.md")
        
        en_descriptions = extract_descriptions(en_path) if os.path.exists(en_path) else {}
        es_descriptions = extract_descriptions(es_path) if os.path.exists(es_path) else {}
        
        yaml_disc_key = None
        for k in psionics_data['items']:
            if k.lower() == disc.lower():
                yaml_disc_key = k
                break
        
        if not yaml_disc_key:
            continue
            
        items = psionics_data['items'][yaml_disc_key].get('items', {})
        for item_id, item_data in items.items():
            en_name = None
            es_name = None
            
            for loc in item_data.get('localized', []):
                if 'en' in loc: en_name = loc['en']['name']
                if 'es' in loc: es_name = loc['es']['name']
            
            # Match EN
            if en_name in en_descriptions:
                desc = en_descriptions[en_name]['desc']
                new_name = en_descriptions[en_name]['name']
                for loc in item_data['localized']:
                    if 'en' in loc:
                        loc['en']['description'] = desc
                        loc['en']['name'] = new_name

            # Match ES
            # Try manual mapping first
            mapped_es_name = ES_MAPPING.get(en_name)
            match_key = mapped_es_name if mapped_es_name in es_descriptions else (es_name if es_name in es_descriptions else (en_name if en_name in es_descriptions else None))
            
            if match_key:
                desc = es_descriptions[match_key]['desc']
                new_name = es_descriptions[match_key]['name']
                for loc in item_data['localized']:
                    if 'es' in loc:
                        loc['es']['description'] = desc
                        loc['es']['name'] = new_name
                        print(f"  Restored ES for {en_name}: {new_name}")

    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(psionics_data, f, Dumper=FoldedDumper, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    main()
