import os
import re
import yaml

def extract_phb_stats():
    phb_path = "/home/dimble/projects/aaa/sources/chapters/chapter_14_psionics.md"
    with open(phb_path, 'r') as f:
        content = f.read()
    
    # Match | Skill Name | Cost |
    # | *Bioweapon* | 3 |
    matches = re.findall(r'\| (?:[*])?([^*|]+)(?:[*])? \| (\d+) \|', content)
    return {name.strip(): int(cost) for name, cost in matches}

def main():
    phb_stats = extract_phb_stats()
    
    yaml_path = "/home/dimble/projects/aaa/sources/data_sources/psionics.yaml"
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    
    diffs = []
    
    for disc_name, disc_data in data.get('items', {}).items():
        items = disc_data.get('items', {})
        for item_id, item_data in items.items():
            en_name = None
            for loc in item_data.get('localized', []):
                if 'en' in loc: en_name = loc['en']['name']
            
            cost = item_data.get('cost')
            attr = item_data.get('attribute')
            
            if en_name in phb_stats:
                phb_cost = phb_stats[en_name]
                if cost != phb_cost:
                    diffs.append(f"Skill: {en_name} | PHB Cost: {phb_cost} | YAML Cost: {cost}")
            else:
                diffs.append(f"Skill: {en_name} | Not in PHB (Mindwalking specific? or name mismatch)")

    print("\n".join(diffs))

if __name__ == "__main__":
    main()
