import yaml, os, re, sys, json, copy
from collections import defaultdict

# Custom representer for block scalar (|) strings to ensure clean YAML output
def str_presenter(dumper, data):
    if len(data) > 60 or '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)

def to_list(data):
    """Converts a Map-based collection to a List, injecting keys as IDs."""
    if isinstance(data, dict):
        res = []
        for k, v in data.items():
            if isinstance(v, dict):
                item = v.copy()
                if 'id' not in item:
                    item['id'] = k
                res.append(item)
            else:
                res.append({'id': k, 'name': v})
        return res
    return data

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

AVAIL_MAPS = {
    'en': {
        'Any': 'Any',
        'Com': 'Common',
        'Con': 'Controlled',
        'Mil': 'Military',
        'Res': 'Restricted',
        'Availability: Any': 'Availability: Any',
        'Availability: Common': 'Availability: Common',
        'Availability: Controlled': 'Availability: Controlled',
        'Availability: Military': 'Availability: Military',
        'Availability: Restricted': 'Availability: Restricted'
    },
    'es': {
        'Any': 'Cualquiera',
        'Com': 'Común',
        'Con': 'Controlada',
        'Mil': 'Militar',
        'Res': 'Restringida',
        'Availability: Any': 'Disponibilidad: Cualquiera',
        'Availability: Common': 'Disponibilidad: Común',
        'Availability: Controlled': 'Disponibilidad: Controlada',
        'Availability: Military': 'Disponibilidad: Militar',
        'Availability: Restricted': 'Disponibilidad: Restringida'
    }
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
    
    # Identify blocks to skip: Markdown links [text](url) and Hugo shortcodes {{< ... >}}
    # We replace them with placeholders, apply mapping, and then restore them.
    placeholders = []
    
    def store_block(match):
        placeholders.append(match.group(0))
        return f"__BLOCK_PLACEHOLDER_{len(placeholders)-1}__"
    
    # Combined pattern for Markdown links and Hugo shortcodes
    # Handles multiline links: [text]\s*({{< relref ... >}}) or [text]\s*(URL)
    block_pattern = r'(\[[\s\S]*?\]\s*\([\s\S]*?\)|{{<[\s\S]*?>}})'
    text_with_placeholders = re.sub(block_pattern, store_block, text, flags=re.DOTALL)
    
    # Soft mapping using terminology rules
    sorted_en_terms = sorted(mapping.keys(), key=len, reverse=True)
    for en in sorted_en_terms:
        # Avoid clobbering common Spanish words like 'con' or 'mil' with short game terms like 'CON' (attribute)
        is_short = len(en) <= 3
        flags = 0 if is_short else re.IGNORECASE
        
        # Use a regex that respects word boundaries for alphanumeric terms
        if re.match(r'^\w', en):
            pattern = f"\\b{re.escape(en)}\\b"
        else:
            pattern = re.escape(en)
        
        text_with_placeholders = re.sub(pattern, mapping[en], text_with_placeholders, flags=flags)
    
    # Restore blocks
    def restore_block(match):
        idx = int(match.group(1))
        return placeholders[idx]
    
    final_text = re.sub(r'__BLOCK_PLACEHOLDER_(\d+)__', restore_block, text_with_placeholders)
    return final_text

def get_localized(node, lang):
    """Extracts the language-specific block from the 'localized' list."""
    if not isinstance(node, dict) or 'localized' not in node:
        return {}
    for item in node['localized']:
        if lang in item:
            return item[lang]
    return {}

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
            skills_raw = yaml.load(f, Loader=yaml.FullLoader)
        process_skills(to_list(skills_raw.get('items', [])), mapping)
    
    psionics_yaml = os.path.join(DATA_SOURCES_DIR, 'psionics.yaml')
    if os.path.exists(psionics_yaml):
        print('Processing Psionics...')
        with open(psionics_yaml, 'r', encoding='utf-8') as f:
            psionics_raw = yaml.load(f, Loader=yaml.FullLoader)
        process_psionics(to_list(psionics_raw.get('items', [])), mapping)
    
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

    # Perks & Flaws
    perks_yaml = os.path.join(DATA_SOURCES_DIR, 'perks.yaml')
    flaws_yaml = os.path.join(DATA_SOURCES_DIR, 'flaws.yaml')
    if os.path.exists(perks_yaml) and os.path.exists(flaws_yaml):
        print('Processing Perks & Flaws...')
        with open(perks_yaml, 'r', encoding='utf-8') as f:
            perks_raw = yaml.load(f, Loader=yaml.FullLoader)
        with open(flaws_yaml, 'r', encoding='utf-8') as f:
            flaws_raw = yaml.load(f, Loader=yaml.FullLoader)
        process_perks_flaws(to_list(perks_raw.get('items', [])), to_list(flaws_raw.get('items', [])), mapping)

    # Backgrounds
    backgrounds_yaml = os.path.join(DATA_SOURCES_DIR, 'backgrounds.yaml')
    if os.path.exists(backgrounds_yaml):
        print('Processing Backgrounds...')
        with open(backgrounds_yaml, 'r', encoding='utf-8') as f:
            backgrounds_raw = yaml.load(f, Loader=yaml.FullLoader)
        process_backgrounds(to_list(backgrounds_raw.get('items', [])), mapping)

def apply_rules_to_node(node, mapping, lang='en'):
    if isinstance(node, dict):
        new_node = {}
        
        # Get localized data if present
        loc_data = get_localized(node, lang)
        
        # 1. First, handle core identity fields (name, skill, etc., and ID)
        for k in ['id', 'name', 'skill', 'discipline', 'title']:
            # Try explicit localization in the same-lang block
            lo_val = loc_data.get(k)
            if not lo_val and lang == 'es':
                # Fallback to general mapping/translation of the English root value
                en_val = node.get(k)
                if en_val:
                    lo_val = translate_field(en_val, node.get(f"{k}_es"), mapping, 'es')
            
            # If we found a value (either explicit or translated fallback), use it
            if lo_val:
                new_node[k] = lo_val
            elif k in node:
                # Keep original English if no localization found
                new_node[k] = node[k]

        # 2. Process all other attributes
        for k, v in node.items():
            if k in ['localized', 'id', 'name', 'skill', 'discipline', 'title'] or k.endswith('_es'):
                continue
            
            if k in ['items', 'config'] and isinstance(v, dict):
                # Optimize for Humans (YAML Map) -> Optimize for Machines (JSON List)
                # Create a simplified index structure for the list page
                index_data = {
                    'config': {
                        'columns': {
                            'en': [
                                {'name': 'Background', 'key': 'name', 'link': True},
                                {'name': 'Description', 'key': 'summary'}
                            ],
                            'es': [
                                {'name': 'Trasfondo', 'key': 'name', 'link': True},
                                {'name': 'Descripción', 'key': 'summary'}
                            ]
                        }
                    },
                    'items': []
                }
                item_list = []
                for item_id, item_data in v.items():
                    # Ensure it's a dict
                    if not isinstance(item_data, dict):
                        item_data = {'name': item_data}
                    
                    # Inject Key as ID (item_id)
                    item_data = item_data.copy()
                    # For config, we use 'id' or 'name' if not present
                    if 'id' not in item_data:
                        item_data['id'] = item_id
                    
                    item_list.append(apply_rules_to_node(item_data, mapping, lang))
                new_node[k] = item_list
            elif k == 'avail':
                # Use language-aware availability map
                new_node[k] = AVAIL_MAPS[lang].get(v, translate_field(v, None, mapping, lang))
            elif k != 'id':
                new_node[k] = apply_rules_to_node(v, mapping, lang)
            else:
                new_node[k] = v

        # loc_title for URL mapping (slugging)
        loc_title = new_node.get('name') or new_node.get('skill') or new_node.get('title')
        if not loc_title:
             loc_title = node.get('name') or node.get('skill') or node.get('discipline')

        # Fix URL and link logic
        for k, v in list(new_node.items()):
            if k.endswith('url') and isinstance(v, str):
                loc_url = localize_url(v, lang, loc_title)
                new_node[k] = loc_url

        # Merge in description and other non-field localized strings
        for k, v in loc_data.items():
            if k in ['name', 'skill', 'discipline', 'title', 'id']: continue
            processed_v = v
            if isinstance(v, str) and lang == 'es':
                processed_v = apply_mapping(v, mapping)
            new_node[k] = processed_v

        return new_node
    elif isinstance(node, list):
        return [apply_rules_to_node(item, mapping, lang) for item in node]
    else:
        return node

def process_psionics(psionics_list, mapping):
    for lang in ['en', 'es']:
        fields = [
            {"key": "skill", "name": "Discipline/Power" if lang == 'en' else "Disciplina/Poder", "link": True},
            {"key": "attribute", "name": "Attr." if lang == 'en' else "Atrib."},
            {"key": "cost", "name": "Cost" if lang == 'en' else "Costo"}
        ]
        
        discipline_entries = []
        search_groups = {}
        
        for d in psionics_list:
            loc_d = get_localized(d, lang)
            d_title = loc_d.get('name') or loc_d.get('discipline') or translate_field(d.get('discipline', ''), None, mapping, lang)
            d_attr = translate_field(d['attribute'], None, mapping, lang)
            d_url = localize_url(d['url'], lang, d_title)
            
            broad_entry = {
                "skill": d_title,
                "attribute": d_attr,
                "url": d_url,
                "cost": d.get('cost', 6),
                "type": "Broad",
                "css_class": "trained-only" if d.get('trained_only', False) else ""
            }
            
            powers = []
            powers_search = []
            for p in to_list(d.get('items', [])):
                loc_p = get_localized(p, lang)
                p_title = loc_p.get('name') or translate_field(p.get('name', ''), None, mapping, lang)
                p_attr = translate_field(p['attribute'], None, mapping, lang)
                p_url = localize_url(p['url'], lang, p_title)
                
                # Extract description from localized block
                p_desc = loc_p.get('description')
                if not p_desc:
                    # Legacy support
                    p_desc = p.get('description', {}).get(lang, p.get('description', {}).get('en', ''))
                
                if lang == 'es':
                    p_desc = apply_mapping(p_desc, mapping)
                
                power_entry = {
                    "skill": p_title,
                    "attribute": p_attr,
                    "url": p_url,
                    "cost": p.get('cost', 5),
                    "type": "Specialty",
                    "css_class": "trained-only" if p.get('trained_only', False) else "",
                    "description": p_desc
                }
                powers.append(power_entry)
                
                # For search index
                powers_search.append({
                    "name": p_title,
                    "attribute": p_attr,
                    "skill_url": p_url,
                    "description": p_desc
                })
            
            if powers: broad_entry["items"] = powers
            discipline_entries.append(broad_entry)
            search_groups[d_title] = powers_search
            
        # Nested Table Data
        table_data = {
            "fields": fields,
            "items": [{"skill": "PSIONICS" if lang == 'en' else "PSIÓNICA", "type": "Category", "items": discipline_entries}]
        }
        
        suffix = '.es.json' if lang == 'es' else '.json'
        with open(os.path.join(SITE_DATA_DIR, 'psionics-table' + suffix), 'w', encoding='utf-8') as f:
            json.dump(table_data, f, indent=4, ensure_ascii=False)
            
        # Search Index Data
        search_data = {
            "search_config": {
                "display_name": "PSIONICS" if lang == 'en' else "PSIÓNICA",
                "base_url": "/core-mechanics/psionics/",
                "section": "psionics"
            },
            "groups": search_groups
        }
        with open(os.path.join(SITE_DATA_DIR, 'psionics' + suffix), 'w', encoding='utf-8') as f:
            json.dump(search_data, f, indent=4, ensure_ascii=False)

def process_perks_flaws(perks_list, flaws_list, mapping):
    for lang in ['en', 'es']:
        processed_perks = []
        processed_flaws = []
        
        perk_columns = [
            {"name": "Perk" if lang == "en" else "Ventaja", "key": "name", "link": True},
            {"name": "Cost" if lang == "en" else "Costo", "key": "cost"},
            {"name": "Ability" if lang == "en" else "Capacidad", "key": "ability"},
            {"name": "Type" if lang == "en" else "Tipo", "key": "type"},
            {"name": "Description" if lang == "en" else "Descripción", "key": "description", "hidden": True}
        ]
        
        flaw_columns = [
            {"name": "Flaw" if lang == "en" else "Defecto", "key": "name", "link": True},
            {"name": "Bonus Points" if lang == "en" else "Puntos de bonificación", "key": "bonus_points"},
            {"name": "Ability" if lang == "en" else "Capacidad", "key": "ability"},
            {"name": "Description" if lang == "en" else "Descripción", "key": "description", "hidden": True}
        ]

        for item in perks_list:
            loc = get_localized(item, lang)
            title = loc.get('name') or item.get('id', 'unknown')
            slug = slugify(item.get('id') or title)
            url = f"/perks_flaws/perks/{slug}/"
            if lang == 'es': url = f"/es{url}"
            
            desc = loc.get('description') or ""
            if lang == 'es': desc = apply_mapping(desc, mapping)
            
            processed_perks.append({
                "name": title,
                "cost": item.get('cost'),
                "ability": translate_field(item.get('ability', '—'), None, mapping, lang),
                "type": translate_field(item.get('type', '—'), None, mapping, lang),
                "description": desc,
                "url": url
            })
            
            out_dir = f'site/content/perks_flaws/perks/{slug}'
            os.makedirs(out_dir, exist_ok=True)
            suffix = '.es.md' if lang == 'es' else '.md'
            with open(os.path.join(out_dir, '_index' + suffix), 'w', encoding='utf-8') as f:
                f.write(f'+++\ntitle = "{title}"\ncost = "{item.get("cost")}"\nability = "{item.get("ability")}"\ntype = "perk"\nlayout = "list"\nomit_automatic_list = true\n+++\n\n{desc}\n')

        for item in flaws_list:
            loc = get_localized(item, lang)
            title = loc.get('name') or item.get('id', 'unknown')
            slug = slugify(item.get('id') or title)
            url = f"/perks_flaws/flaws/{slug}/"
            if lang == 'es': url = f"/es{url}"
            
            desc = loc.get('description') or ""
            if lang == 'es': desc = apply_mapping(desc, mapping)
            
            processed_flaws.append({
                "name": title,
                "bonus_points": item.get('bonus_points'),
                "ability": translate_field(item.get('ability', '—'), None, mapping, lang),
                "description": desc,
                "url": url
            })
            
            out_dir = f'site/content/perks_flaws/flaws/{slug}'
            os.makedirs(out_dir, exist_ok=True)
            suffix = '.es.md' if lang == 'es' else '.md'
            with open(os.path.join(out_dir, '_index' + suffix), 'w', encoding='utf-8') as f:
                f.write(f'+++\ntitle = "{title}"\nbonus_points = "{item.get("bonus_points")}"\nability = "{item.get("ability")}"\ntype = "flaw"\nlayout = "list"\nomit_automatic_list = true\n+++\n\n{desc}\n')

        combined = {
            "search_config": {
                "display_name": "PERKS & FLAWS" if lang == 'en' else "VENTAJAS Y DEFECTOS",
                "base_url": "/perks_flaws/",
                "section": "rules"
            },
            "perks": {
                "config": { "columns": perk_columns },
                "items": [{"name": "Perks" if lang == 'en' else "Ventajas", "items": processed_perks}]
            },
            "flaws": {
                "config": { "columns": flaw_columns },
                "items": [{"name": "Flaws" if lang == 'en' else "Defectos", "items": processed_flaws}]
            }
        }
        
        json_suffix = '.es.json' if lang == 'es' else '.json'
        with open(os.path.join(SITE_DATA_DIR, 'perks_and_flaws' + json_suffix), 'w', encoding='utf-8') as f:
            json.dump(combined, f, indent=4, ensure_ascii=False)

def process_backgrounds(backgrounds_list, mapping):
    for lang in ['en', 'es']:
        processed_items = []
        columns = [
            {"name": "Background" if lang == "en" else "Antecedente", "key": "name", "link": True},
            {"name": "Summary" if lang == "en" else "Resumen", "key": "summary"},
            {"name": "Favored Broad Skill" if lang == "en" else "Habilidad Amplia", "key": "favored_broad_skill"},
            {"name": "Favored Specialty Skills" if lang == "en" else "Especialidades", "key": "favored_specialty_skills"},
            {"name": "Favored Perks" if lang == "en" else "Ventajas", "key": "favored_perks"},
            {"name": "Flaw" if lang == "en" else "Defecto", "key": "flaw"}
        ]

        for item in backgrounds_list:
            loc = get_localized(item, lang)
            title = loc.get('name') or item.get('id', 'unknown')
            slug = slugify(item.get('id') or title)
            url = f"/backgrounds/{slug}/"
            if lang == 'es': url = f"/es{url}"

            # Full description for Markdown content
            full_description = loc.get('description', "")
            if lang == 'es':
                full_description = apply_mapping(full_description, mapping)

            # Extract summary for table column (first sentence)
            summary = full_description.split('.')[0].strip()
            if summary and not summary.endswith('.'):
                summary += '.'

            # Process all fields
            processed_item = {
                "name": title,
                "summary": summary,
                "favored_broad_skill": translate_field(item.get('favored_broad_skill', ''), None, mapping, lang),
                "url": url,
                "skill_url": url # Backward compatibility for some layouts
            }

            # Map remaining visible fields
            for field in ['favored_specialty_skills', 'favored_perks', 'flaw', 'equipment', 'special_ability', 'tendencies']:
                val = loc.get(field, "")
                if lang == 'es':
                    val = apply_mapping(val, mapping)
                processed_item[field] = val
            
            processed_items.append(processed_item)

            # Generate Markdown
            out_dir = f'site/content/backgrounds/{slug}'
            os.makedirs(out_dir, exist_ok=True)
            suffix = '.es.md' if lang == 'es' else '.md'
            
            content = f'+++\ntitle = "{title}"\ntype = "background"\nlayout = "background"\n+++\n\n'
            content += f'{full_description}\n\n'
            
            # Use specific headers matching the existing structure
            headers = {
                "favored_broad_skill": "Favored Broad Skill" if lang == "en" else "Paquete de Habilidades",
                "favored_specialty_skills": "Favored Specialty Skills" if lang == "en" else "Habilidades de Especialidad Favorecidas",
                "favored_perks": "Favored Perks" if lang == "en" else "Ventajas Favorecidas",
                "flaw": "Automatic Flaw" if lang == "en" else "Defecto Automático",
                "equipment": "Starting Equipment" if lang == "en" else "Equipo Inicial",
                "special_ability": "Special Ability" if lang == "en" else "Capacidad Especial",
                "tendencies": "Tendencies (Pick 2)" if lang == "en" else "Tendencias (Elige 2)"
            }

            content += f'## {headers["favored_broad_skill"]}:\n* {processed_item["favored_broad_skill"] or ("None." if lang == "en" else "Ninguna.")}\n\n'
            
            skills_val = processed_item["favored_specialty_skills"]
            if '<br>' in skills_val:
                skills_val = "\n".join([f"* {s.strip()}" for s in skills_val.split('<br>')])
            
            content += f'## {headers["favored_specialty_skills"]}:\n{skills_val}\n\n'
            content += f'## {headers["favored_perks"]}:\n* {processed_item["favored_perks"]}\n\n'
            content += f'## {headers["flaw"]}:\n* {processed_item["flaw"]}\n\n'
            content += f'## {headers["equipment"]}:\n{processed_item["equipment"]}\n\n'
            content += f'## {headers["special_ability"]}:\n{processed_item["special_ability"]}\n\n'
            
            if processed_item.get("tendencies"):
                tend_val = processed_item["tendencies"]
                if '<br>' in tend_val:
                    tend_val = "\n".join([f"* {s.strip()}" for s in tend_val.split('<br>')])
                content += f'## {headers["tendencies"]}:\n{tend_val}\n\n'
            
            if loc.get('footnote'):
                content += f'---\n\n{loc["footnote"]}\n'
            
            with open(os.path.join(out_dir, '_index' + suffix), 'w', encoding='utf-8') as f:
                f.write(content)

        # Build final JSON with minimalist columns
        minimal_columns = [
            {"key": "name", "name": "Background" if lang == 'en' else "Procedencia", "link": True},
            {"key": "summary", "name": "Description" if lang == 'en' else "Descripción"}
        ]
        
        combined = {
            "search_config": {
                "display_name": "BACKGROUNDS" if lang == 'en' else "PROCEDENCIA",
                "base_url": "/backgrounds/",
                "section": "rules"
            },
            "columns": minimal_columns,
            "all": {
                "items": [{"name": "Backgrounds" if lang == "en" else "Antecedentes", "items": processed_items}]
            }
        }
        
        json_suffix = '.es.json' if lang == 'es' else '.json'
        with open(os.path.join(SITE_DATA_DIR, 'backgrounds' + json_suffix), 'w', encoding='utf-8') as f:
            json.dump(combined, f, indent=4, ensure_ascii=False)

def process_skills(skills_list, mapping):
    for broad in skills_list:
        url = broad.get('url') or broad.get('skill_url', '')
        if not url: continue
        slug = url.strip('/').split('/')[-1]
        out_dir = f'site/content/skills/{slug}'
        os.makedirs(out_dir, exist_ok=True)
        
        for lang in ['en', 'es']:
            loc_broad = get_localized(broad, lang)
            title = loc_broad.get('name') or loc_broad.get('skill') or translate_field(broad.get('skill', ''), broad.get('skill_es'), mapping, lang)
            attr = translate_field(broad['attribute'], None, mapping, lang)
            cat_en = broad.get('category', 'Other')
            cat = cat_en if lang == 'en' else CATEGORY_MAP.get(cat_en, apply_mapping(cat_en, mapping))
            
            desc = loc_broad.get('description')
            if not desc:
                # Legacy support
                desc = broad.get('description', '') if lang == 'en' else apply_mapping(broad.get('description_es', broad.get('description', '')), mapping)
            elif lang == 'es':
                desc = apply_mapping(desc, mapping)
            
            suffix = '.es.md' if lang == 'es' else '.md'
            with open(os.path.join(out_dir, '_index' + suffix), 'w', encoding='utf-8') as f:
                f.write(f'+++\ntitle = "{title}"\nattribute = "{attr}"\ncategory = "{cat}"\ntype = "skill"\nlayout = "list"\n+++\n\n{desc}\n\n')
                for spec in to_list(broad.get('items', [])):
                    loc_spec = get_localized(spec, lang)
                    s_title = loc_spec.get('name') or loc_spec.get('skill') or translate_field(spec.get('skill', ''), spec.get('skill_es'), mapping, lang)
                    s_attr = translate_field(spec['attribute'], None, mapping, lang)
                    
                    s_desc = loc_spec.get('description')
                    if not s_desc:
                        # Legacy support
                        s_desc = spec.get('description', '') if lang == 'en' else apply_mapping(spec.get('description_es', spec.get('description', '')), mapping)
                    elif lang == 'es':
                        s_desc = apply_mapping(s_desc, mapping)
                        
                    s_untrained = "no" if spec.get('trained_only', False) else "yes"
                    s_cost = spec.get('cost', 5)
                    f.write(f'## {s_title}\n{{{{< specialty attr="{s_attr}" untrained="{s_untrained}" cost="{s_cost}" >}}}}\n\n{s_desc}\n\n---\n\n')

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
            
            loc_b = get_localized(b, lang)
            b_title = loc_b.get('name') or loc_b.get('skill') or translate_field(b.get('skill', ''), b.get('skill_es'), mapping, lang)
            
            broad_entry = {
                "skill": b_title,
                "attribute": translate_field(b['attribute'], None, mapping, lang),
                "url": localize_url(b.get('url') or b.get('skill_url'), lang, b_title),
                "cost": b.get('cost', 0),
                "type": "Broad"
            }
            specs = []
            for s in to_list(b.get('items', [])):
                loc_s = get_localized(s, lang)
                s_title = loc_s.get('name') or loc_s.get('skill') or translate_field(s.get('skill', ''), s.get('skill_es'), mapping, lang)
                specs.append({
                    "skill": s_title,
                    "attribute": translate_field(s['attribute'], None, mapping, lang),
                    "url": localize_url(s.get('url') or s.get('skill_url'), lang, s_title),
                    "cost": s.get('cost', 0),
                    "type": "Specialty",
                    "css_class": "trained-only" if s.get('trained_only', False) else ""
                })
            if specs: broad_entry["items"] = specs
            categories[cat].append(broad_entry)
            
        items = []
        for cat in sorted(categories.keys()):
            items.append({"skill": cat, "type": "Category", "items": categories[cat]})
        return {"fields": fields, "items": items}

    with open(os.path.join(SITE_DATA_DIR, 'skills-table.json'), 'w', encoding='utf-8') as f:
        json.dump(build_nested_skills_table('en'), f, indent=4, ensure_ascii=False)
    with open(os.path.join(SITE_DATA_DIR, 'skills-table.es.json'), 'w', encoding='utf-8') as f:
        json.dump(build_nested_skills_table('es'), f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    rebuild_all()
