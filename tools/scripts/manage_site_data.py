import os
import json
import yaml
import re
from collections import defaultdict

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

AVAIL_MAP = {
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
    """
    Applies terminology mapping to text while protecting Markdown links and Hugo shortcodes.
    """
    if not text or not isinstance(text, str): return text
    
    placeholders = []
    def store_block(match):
        placeholders.append(match.group(0))
        return f"@BLOCK_PLACEHOLDER_{len(placeholders)-1}@"
    
    # Protect Markdown URLs and Hugo shortcodes
    block_pattern = r'(\]\s*\([\s\S]*?\)|{{<[\s\S]*?>}})'
    text_with_placeholders = re.sub(block_pattern, store_block, text, flags=re.DOTALL)
    
    # Sort terms by length descending to avoid partial matches
    sorted_terms = sorted(mapping.keys(), key=len, reverse=True)
    for en in sorted_terms:
        es = mapping[en]
        is_short = len(en) <= 3
        flags = 0 if is_short else re.IGNORECASE
        
        # Word boundary check for alphanumeric terms
        if re.match(r'^\w', en):
            pattern = f"\\b{re.escape(en)}\\b"
        else:
            pattern = re.escape(en)
            
        text_with_placeholders = re.sub(pattern, es, text_with_placeholders, flags=flags)
    
    # Restore protected blocks
    def restore_block(match):
        idx = int(match.group(1))
        return placeholders[idx]
    
    return re.sub(r'@BLOCK_PLACEHOLDER_(\d+)@', restore_block, text_with_placeholders)

def get_localized(node, lang):
    """Extracts the language-specific block from the 'localized' list."""
    if not isinstance(node, dict) or 'localized' not in node:
        return {}
    for item in node['localized']:
        if lang in item:
            return item[lang]
    return {}

def translate_field_robust(node, field, lang, mapping):
    """Robustly extracts and translates a field with fallbacks."""
    if not isinstance(node, dict): return ""
    
    # 1. Get explicit localized value
    loc = get_localized(node, lang)
    val = loc.get(field)
    if val: return val
    
    # 2. Fallback for Spanish: Try English localized block then root
    if lang == 'es':
        en_loc = get_localized(node, 'en')
        en_val = en_loc.get(field)
        if en_val:
            # Special case for names/short fields: check direct mapping first
            if field in ['name', 'skill', 'power', 'perk', 'flaw', 'title']:
                if en_val in mapping: return mapping[en_val]
            return apply_mapping(en_val, mapping)
            
        es_root = node.get(f"{field}_es") or node.get(f"{field}_override")
        if es_root: return es_root
        
        en_root = node.get(field)
        if en_root:
            if field in ['name', 'skill', 'power', 'perk', 'flaw', 'title']:
                if en_root in mapping: return mapping[en_root]
            return apply_mapping(en_root, mapping)
    else:
        # Fallback for English: Try root field
        return node.get(field, "")
        
    return ""

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

def transform_gear_category(cat_node, mapping, lang):
    """Flattens gear categories for Hugo shortcodes."""
    if not isinstance(cat_node, dict): return cat_node
    result = cat_node.copy()
    
    # 1. Flatten config if it only has default
    if "config" in result and isinstance(result["config"], dict):
        
        if "default" in result["config"] and len(result["config"]) == 1:
            result["config"] = result["config"]["default"]
            
    # 2. Transform items map-of-maps into a list of groups
    if "items" in result and isinstance(result["items"], dict):
        new_groups = []
        sorted_keys = sorted(result["items"].keys())
        for group_id in sorted_keys:
            group = result["items"][group_id]
            if isinstance(group, dict) and "items" in group:
                group_name = group.get("name") or group_id.replace("-", " ").title()
                
                items_list = []
                sorted_item_keys = sorted(group["items"].keys())
                for item_id in sorted_item_keys:
                    item = group["items"][item_id]
                    if isinstance(item, dict):
                        # Ensure item has id and name
                        item["id"] = item_id
                        if "name" not in item:
                            item["name"] = item_id.replace("-", " ").title()
                        
                        items_list.append(item)
                
                new_groups.append({
                    "id": group_id,
                    "name": group_name,
                    "items": items_list
                })
        result["items"] = new_groups
    return result

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
    gear_sources = ["armor", "computers", "cybernetics", "goods_and_services", "survival_gear", "weapons"]
    for base_name in gear_sources:
        yaml_path = os.path.join(DATA_SOURCES_DIR, f"{base_name}.yaml")
        if not os.path.exists(yaml_path): continue
        print(f"Processing {base_name}...")
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        
        for lang in ["en", "es"]:
            # Process the entire structure recursively first (localization and terminology)
            processed = apply_rules_to_node(data, mapping, lang)
            
            # Post-process for structural requirements (Hugo templates)
            final_data = {}
            if "search_config" in processed:
                final_data["search_config"] = processed["search_config"]
            
            if "items" in processed or "config" in processed:
                final_data.update(transform_gear_category(processed, mapping, lang))
            else:
                # Handle multiple categories (e.g., weapons.yaml has melee, ranged, etc.)
                for key, value in processed.items():
                    if isinstance(value, dict) and ("items" in value or "config" in value):
                        final_data[key] = transform_gear_category(value, mapping, lang)
                    elif key != "search_config":
                        final_data[key] = value
            
            suffix = ".es.json" if lang == "es" else ".json"
            with open(os.path.join(SITE_DATA_DIR, base_name + suffix), "w", encoding="utf-8") as f:
                
                json.dump(final_data, f, indent=4, ensure_ascii=False)

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
    """Recursively applies terminology mapping and localization rules to a node."""
    if isinstance(node, dict):
        new_node = {}
        # 1. Handle all fields using robust translation
        for k, v in node.items():
            if k == 'localized':
                continue
            if k.endswith('_es'): continue
            
            if k == 'url' or k == 'skill_url':
                title = translate_field_robust(node, 'name', lang, mapping) or translate_field_robust(node, 'skill', lang, mapping) or translate_field_robust(node, 'title', lang, mapping)
                new_node[k] = localize_url(v, lang, title)
            elif isinstance(v, str):
                new_node[k] = translate_field_robust(node, k, lang, mapping)
            elif isinstance(v, dict):
                # If it's a map (like 'items' or 'config'), process values recursively
                new_node[k] = {ik: apply_rules_to_node(iv, mapping, lang) if isinstance(iv, (dict, list)) else iv 
                               for ik, iv in v.items() if ik != 'localized' and not ik.endswith('_es')}
            elif isinstance(v, list):
                new_node[k] = [apply_rules_to_node(item, mapping, lang) if isinstance(item, (dict, list)) else item for item in v]
            else:
                new_node[k] = v
        return new_node
    elif isinstance(node, list):
        return [apply_rules_to_node(item, mapping, lang) for item in node]
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
            d_title = translate_field_robust(d, 'name', lang, mapping) or translate_field_robust(d, 'discipline', lang, mapping)
            d_attr = translate_field(d.get('attribute', 'WIL'), None, mapping, lang)
            d_url = localize_url(d.get('url', ''), lang, d_title)
            
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
                p_title = translate_field_robust(p, 'name', lang, mapping) or translate_field_robust(p, 'power', lang, mapping)
                p_attr = translate_field(p.get('attribute', d_attr), None, mapping, lang)
                p_url = localize_url(p.get('url', ''), lang, p_title)
                p_desc = translate_field_robust(p, 'description', lang, mapping)
                
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
            
            # Generate the Markdown file for the Hugo site content
            slug = (d.get('id') or d_title.lower()).lower()
            out_dir = f'site/content/psionics/{slug}'
            os.makedirs(out_dir, exist_ok=True)
            
            suffix = '.es.md' if lang == 'es' else '.md'
            d_desc = translate_field_robust(d, 'description', lang, mapping)
            d_clean_desc = d_desc.replace('\n', ' ').replace('"', '\\"') if d_desc else ""
            if len(d_clean_desc) > 150:
                d_clean_desc = d_clean_desc[:147] + "..."
                
            weights = {'biokinesis': 1, 'esp': 2, 'psychoportation': 3, 'telekinesis': 4, 'telepathy': 5}
            weight = weights.get(slug, 1)
            
            with open(os.path.join(out_dir, '_index' + suffix), 'w', encoding='utf-8') as f:
                f.write('+++\n')
                f.write(f'title = "{d_title}"\n')
                f.write(f'description = "{d_clean_desc}"\n')
                f.write(f'weight = {weight}\n')
                f.write(f'attribute = "{d_attr}"\n')
                f.write('category = "Psionics"\n')
                f.write(f'untrained = {"true" if not d.get("trained_only", False) else "false"}\n')
                f.write('type = "skill"\n')
                f.write('layout = "list"\n')
                f.write('+++\n\n')
                f.write(f'{d_desc}\n\n')
                f.write('---\n\n')
                
                for p in to_list(d.get('items', [])):
                    p_title = translate_field_robust(p, 'name', lang, mapping) or translate_field_robust(p, 'power', lang, mapping)
                    p_attr = translate_field(p.get('attribute', d_attr), None, mapping, lang)
                    p_cost = p.get('cost', 5)
                    p_untrained = 'yes' if not p.get('trained_only', False) else 'no'
                    p_desc = translate_field_robust(p, 'description', lang, mapping)
                    f.write(f'## {p_title}\n')
                    # Build the specialty shortcode correctly
                    shortcode = f'{{{{< specialty attr=\"{p_attr}\" untrained=\"{p_untrained}\" cost=\"{p_cost}\"'
                    if p.get('extended_duration', False):
                        shortcode += ' extended=\"true\"'
                    shortcode += ' >}}\n\n'
                    f.write(shortcode)
                    f.write(f'{p_desc}\n\n')
                    f.write('---\n\n')
            
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
            title = translate_field_robust(item, 'name', lang, mapping) or item.get('id', 'unknown')
            slug = slugify(item.get('id') or title)
            url = f"/perks_flaws/perks/{slug}/"
            if lang == 'es': url = f"/es{url}"
            
            desc = translate_field_robust(item, 'description', lang, mapping) or ""
            
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
            title = translate_field_robust(item, 'name', lang, mapping) or item.get('id', 'unknown')
            slug = slugify(item.get('id') or title)
            url = f"/perks_flaws/flaws/{slug}/"
            if lang == 'es': url = f"/es{url}"
            
            desc = translate_field_robust(item, 'description', lang, mapping) or ""
            
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
            title = translate_field_robust(item, 'name', lang, mapping) or translate_field_robust(item, 'background', lang, mapping)
            slug = slugify(item.get('id') or title)
            url = f"/backgrounds/{slug}/"
            if lang == 'es': url = f"/es{url}"

            # Full description for Markdown content
            full_description = translate_field_robust(item, 'description', lang, mapping) or ""

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
                val = translate_field_robust(item, field, lang, mapping) or ""
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
            
            footnote = translate_field_robust(item, 'footnote', lang, mapping)
            if footnote:
                content += f'---\n\n{footnote}\n'
            
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
            title = translate_field_robust(broad, 'name', lang, mapping) or translate_field_robust(broad, 'skill', lang, mapping)
            attr = broad.get('attribute', 'N/A')
            cat = broad.get('category', 'N/A')
            desc = translate_field_robust(broad, 'description', lang, mapping)
            
            suffix = '.es.md' if lang == 'es' else '.md'
            with open(os.path.join(out_dir, '_index' + suffix), 'w', encoding='utf-8') as f:
                f.write(f'+++\ntitle = "{title}"\nattribute = "{attr}"\ncategory = "{cat}"\ntype = "skill"\nlayout = "list"\n+++\n\n{desc}\n\n')
                for spec in to_list(broad.get('items', [])):
                    s_title = translate_field_robust(spec, 'name', lang, mapping)
                    s_attr = spec.get('attribute', attr)
                    s_cost = spec.get('cost', 'N/A')
                    s_untrained = 'yes' if not spec.get('trained_only', False) else 'no'
                    s_desc = translate_field_robust(spec, 'description', lang, mapping)
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
            
            title = translate_field_robust(b, 'name', lang, mapping) or translate_field_robust(b, 'skill', lang, mapping)
            desc = translate_field_robust(b, 'description', lang, mapping)
            
            broad_entry = {
                "skill": title,
                "attribute": translate_field(b['attribute'], None, mapping, lang),
                "url": localize_url(b.get('url') or b.get('skill_url'), lang, title),
                "cost": b.get('cost', 0),
                "type": "Broad"
            }
            specs = []
            for s in to_list(b.get('items', [])):
                s_title = translate_field_robust(s, 'name', lang, mapping)
                specs.append({
                    "skill": s_title,
                    "attribute": translate_field(s.get('attribute', b.get('attribute', 'N/A')), None, mapping, lang),
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
