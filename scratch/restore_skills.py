import os
import re
import yaml
from pathlib import Path

# Custom YAML dumper
class FoldedDumper(yaml.SafeDumper):
    pass

def folded_str_representer(dumper, data):
    if len(str(data).splitlines()) > 1:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

FoldedDumper.add_representer(str, folded_str_representer)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')

ATTRIBUTES = ["str", "dex", "con", "int", "wil", "per", "cha", "fue", "des", "con", "int", "vol", "per", "car", "agu", "fir"]

def extract_skill_data(filepath):
    """Parses a markdown file."""
    if not os.path.exists(filepath):
        return None, []
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = re.split(r'---\s*\n|\+\+\+\s*\n', content, maxsplit=2)
    frontmatter = parts[1] if len(parts) > 1 else ""
    body = parts[2] if len(parts) > 2 else content
    
    title_match = re.search(r'title\s*=\s*["\']([^"\']+)["\']', frontmatter)
    title = title_match.group(1) if title_match else ""
    attr_match = re.search(r'attribute\s*=\s*["\']([^"\']+)["\']', frontmatter)
    attr = attr_match.group(1) if attr_match else ""
    cat_match = re.search(r'category\s*=\s*["\']([^"\']+)["\']', frontmatter)
    category = cat_match.group(1) if cat_match else ""
    
    blocks = re.split(r'\n## ', body)
    broad_desc_raw = blocks[0]
    
    broad_lines = broad_desc_raw.splitlines()
    clean_broad_lines = []
    found_content = False
    for line in broad_lines:
        if not found_content:
            if line.startswith('#') or line.startswith('###') or line.strip().startswith('*') or line.strip() == "":
                continue
            else:
                found_content = True
        clean_broad_lines.append(line)
    broad_desc = "\n".join(clean_broad_lines).strip()
    broad_desc = re.split(r'# Specialty Skills|# Especialidades', broad_desc, flags=re.I)[0].strip()
    
    specialties = []
    for section in blocks[1:]:
        lines = section.splitlines()
        if not lines: continue
        raw_header = lines[0].strip()
        clean_header = re.sub(r'\s*\[[^\]]+\]|\s*\([^)]+\)', '', raw_header).strip()
        
        if slugify(clean_header) in ATTRIBUTES:
            continue
            
        eng_name_match = re.search(r'^### \(([^)]+)\)', "\n".join(lines[1:]), re.MULTILINE)
        eng_name = eng_name_match.group(1) if (eng_name_match and slugify(eng_name_match.group(1)) not in ATTRIBUTES) else clean_header
        
        start_idx = 1
        sub_attr = attr
        for i, line in enumerate(lines[1:], 1):
            if line.startswith('###'):
                m = re.match(r'### \(([^)]+)\)', line)
                if m and len(m.group(1)) <= 4:
                     sub_attr = m.group(1).strip()
                start_idx = i + 1
            elif line.strip().startswith('*') or line.strip() == "":
                start_idx = i + 1
            else:
                break
        
        spec_desc = "\n".join(lines[start_idx:]).strip()
        spec_desc = re.sub(r'(\n|^)---+\s*$', '', spec_desc).strip()
        
        specialties.append({
            "slug": slugify(eng_name),
            "name": clean_header, 
            "desc": spec_desc, 
            "eng_name": eng_name,
            "attribute": sub_attr
        })
    
    return {"name": title, "desc": broad_desc, "attribute": attr, "category": category}, specialties

def main():
    root_dir = "/home/dimble/projects/aaa"
    yaml_path = os.path.join(root_dir, "sources/data_sources/skills.yaml")
    skills_dir = os.path.join(root_dir, "site/content/skills")
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        skills_data = yaml.safe_load(f)
    
    new_items_block = {}
    
    # Sort folders to maintain consistent processing
    for folder in sorted(os.listdir(skills_dir)):
        folder_path = os.path.join(skills_dir, folder)
        if not os.path.isdir(folder_path): continue
        
        en_file = os.path.join(folder_path, "_index.md")
        es_file = os.path.join(folder_path, "_index.es.md")
        
        en_broad, en_specs = extract_skill_data(en_file)
        es_broad, es_specs = extract_skill_data(es_file)
        
        if not en_broad: continue
        
        yaml_id = folder
        # Preserve original costs if possible
        old_broad = skills_data['items'].get(yaml_id, {})
        old_cost = old_broad.get('cost', 6)
        old_category = old_broad.get('category', en_broad['category'])
        
        print(f"Restoring Broad Skill: {yaml_id}")
        
        new_broad = {
            "attribute": en_broad['attribute'],
            "cost": old_cost,
            "category": old_category,
            "url": f"/skills/{yaml_id}",
            "localized": [
                {"en": {"name": en_broad['name'], "description": en_broad['desc']}},
                {"es": {"name": es_broad['name'] if es_broad else en_broad['name'], 
                        "description": es_broad['desc'] if es_broad else en_broad['desc']}}
            ],
            "items": {}
        }
        
        for idx, spec_info in enumerate(en_specs):
            spec_slug = spec_info['slug']
            # Special slug fixes
            if spec_slug == "specialty-skills": continue # Noise
            if spec_slug == "xenomedicine": spec_slug = "xenomedicine-specific"
            if spec_slug == "powered": spec_slug = "powered-weapons"
            
            old_item = old_broad.get('items', {}).get(spec_slug, {})
            item_cost = old_item.get('cost', 3)
            
            es_match = es_specs[idx] if idx < len(es_specs) else None
            
            new_broad['items'][spec_slug] = {
                "attribute": spec_info['attribute'],
                "cost": item_cost,
                "url": f"/skills/{yaml_id}#{spec_slug}",
                "localized": [
                    {"en": {"name": spec_info['name'], "description": spec_info['desc']}},
                    {"es": {"name": es_match['name'] if es_match else spec_info['name'], 
                            "description": es_match['desc'] if es_match else spec_info['desc']}}
                ]
            }
            print(f"  Restored Spec: {spec_slug}")

        new_items_block[yaml_id] = new_broad

    skills_data['items'] = new_items_block
    
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(skills_data, f, Dumper=FoldedDumper, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    main()
