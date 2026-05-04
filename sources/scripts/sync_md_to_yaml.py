import sys
import re
from ruamel.yaml import YAML

# Initialize YAML parser
yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 4096

def update_yaml_from_markdown():
    # 1. Load the Markdown content
    try:
        with open('sources/processed-skills.md', 'r', encoding='utf-8') as f:
            md_content = f.read()
    except Exception as e:
        print(f"Error reading Markdown: {e}")
        return

    # 2. Load the YAML data
    yaml_path = 'sources/data_sources/skills.yaml'
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            full_data = yaml.load(f)
    except Exception as e:
        print(f"Error reading YAML: {e}")
        return

    # Work with the 'items' dict if it exists
    data = full_data.get('items', full_data)

    # 3. Parse Markdown by skill blocks
    skill_blocks = re.split(r'\n(?=# [^#\n]+ \(Broad Skill\))', '\n' + md_content)
    
    # Define which skills are fully reviewed and ready for sync
    approved_skills = [
        'Acrobatics', 'Administration', 'Animal Handling', 'Armor Operation',
        'Athletics', 'Awareness', 'Business', 'Computer Science', 
        'Covert Ops', 'Creativity', 'Culture', 'Deception'
    ]

    for block in skill_blocks:
        block = block.strip()
        if not block: continue
        
        # Extract Broad Skill Name
        match = re.search(r'^# ([^(\n]+) \(Broad Skill\)', block)
        if not match: continue
        
        broad_name = match.group(1).strip()
        if broad_name not in approved_skills:
            print(f"Skipping '{broad_name}' (not in approved sync list).")
            continue

        # Find the key in YAML that matches this name
        broad_key = None
        for k, v in data.items():
            en_loc = next((loc['en'] for loc in v.get('localized', []) if 'en' in loc), None)
            if en_loc and en_loc.get('name') == broad_name:
                broad_key = k
                break
        
        if not broad_key:
            print(f"Warning: Broad Skill '{broad_name}' not found in YAML keys. Skipping.")
            continue

        print(f"Syncing '{broad_name}'...")

        # Extract Broad Skill Description
        broad_parts = re.split(r'\n(?=## [^#\n]+ \(Specialty\))', block)
        broad_desc_raw = broad_parts[0].replace(f"# {broad_name} (Broad Skill)", "").strip()
        
        for loc in data[broad_key].get('localized', []):
            if 'en' in loc:
                loc['en']['description'] = broad_desc_raw
                break

        # 4. Parse Specialties
        specialty_blocks = broad_parts[1:]
        
        # Restructure skills with significantly changed specialty lists
        if broad_key in ['creativity', 'deception']:
            new_items = {}
            for spec_block in specialty_blocks:
                spec_block = spec_block.strip()
                spec_match = re.search(r'^## ([^(\n]+) \(Specialty\)', spec_block)
                if not spec_match: continue
                
                spec_name = spec_match.group(1).strip()
                spec_key = spec_name.lower().replace(' (', '-').replace(')', '').replace(' ', '-')
                spec_desc = spec_block.replace(f"## {spec_name} (Specialty)", "").strip()
                
                # Extract Rank Benefits titles for the rank_benefits list
                rb = []
                # Look for patterns like "⊗ **Rank 3 [Artistic Flourish]:**" or "⊗ **Rank 3:**"
                rb_matches = re.findall(r'[⊗▶] \*\*Rank (\d+)(?: \[([^\]]+)\])?:\*\*', spec_desc)
                for rank_val, title in rb_matches:
                    rb.append({'rank': int(rank_val), 'title': title if title else "Benefit"})

                # Also check Gamble specific "Pro Advantage" which isn't always in a [Title]
                if "Pro Advantage" in spec_desc:
                    pro_matches = re.findall(r'\*\*Rank (\d+) \(-(\d)\)\*\*', spec_desc)
                    for r, val in pro_matches:
                        rb.append({'rank': int(r), 'title': 'Pro Advantage'})

                new_items[spec_key] = {
                    'attribute': data[broad_key]['attribute'], # Default to broad skill attribute
                    'cost': 3, # Default cost
                    'url': f'/skills/{broad_key}#{spec_key}',
                    'localized': [
                        {'en': {'name': spec_name, 'description': spec_desc}},
                        {'es': {'name': spec_name, 'description': ''}}
                    ],
                    'trained_only': False
                }
                if rb:
                    # Remove duplicates and sort
                    unique_rb = []
                    seen = set()
                    for item in rb:
                        tup = (item['rank'], item['title'])
                        if tup not in seen:
                            unique_rb.append(item)
                            seen.add(tup)
                    new_items[spec_key]['rank_benefits'] = sorted(unique_rb, key=lambda x: x['rank'])
            
            data[broad_key]['items'] = new_items
            print(f"  Restructured specialties for '{broad_name}'.")

        else:
            # Standard specialty update
            for spec_block in specialty_blocks:
                spec_block = spec_block.strip()
                spec_match = re.search(r'^## ([^(\n]+) \(Specialty\)', spec_block)
                if not spec_match: continue
                
                spec_name = spec_match.group(1).strip()
                spec_desc_raw = spec_block.replace(f"## {spec_name} (Specialty)", "").strip()
                
                # Clean up legacy YAML trigger sections if they still exist in MD
                spec_desc_raw = re.sub(r'\n+### YAML Rank Benefits \(Mechanical Triggers\).*$', '', spec_desc_raw, flags=re.DOTALL).strip()

                items = data[broad_key].get('items', {})
                spec_key = None
                for k, v in items.items():
                    en_loc = next((loc['en'] for loc in v.get('localized', []) if 'en' in loc), None)
                    if en_loc and en_loc.get('name') == spec_name:
                        spec_key = k
                        break
                
                if spec_key:
                    for loc in items[spec_key].get('localized', []):
                        if 'en' in loc:
                            loc['en']['description'] = spec_desc_raw
                            break
                    
                    # Update rank_benefits list based on new markers in description
                    rb = []
                    rb_matches = re.findall(r'[⊗▶] \*\*Rank (\d+)(?: \[([^\]]+)\])?:\*\*', spec_desc_raw)
                    for rank_val, title in rb_matches:
                        rb.append({'rank': int(rank_val), 'title': title if title else "Benefit"})
                    
                    if rb:
                        unique_rb = []
                        seen = set()
                        for item in rb:
                            tup = (item['rank'], item['title'])
                            if tup not in seen:
                                unique_rb.append(item)
                                seen.add(tup)
                        items[spec_key]['rank_benefits'] = sorted(unique_rb, key=lambda x: x['rank'])
                else:
                    print(f"  Warning: Specialty '{spec_name}' not found under '{broad_name}' in YAML.")

    # 5. Save the updated YAML
    try:
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(full_data, f)
        print("Successfully updated YAML from Markdown using automated script.")
    except Exception as e:
        print(f"Error writing YAML: {e}")

if __name__ == "__main__":
    update_yaml_from_markdown()
