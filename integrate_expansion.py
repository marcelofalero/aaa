import yaml
import os
import json

def merge_yaml_list(base_file, expansion_file, category_path):
    """
    Merges items from expansion_file into a specific category in base_file.
    category_path: e.g. ['categories', 'light', 'groups', 'PL 7']
    """
    with open(base_file, 'r', encoding='utf-8') as f:
        base = yaml.safe_load(f)
    with open(expansion_file, 'r', encoding='utf-8') as f:
        exp = yaml.safe_load(f)
    
    # Navigate to the target group
    target = base
    for key in category_path[:-1]:
        target = target[key]
    
    group_key = category_path[-1]
    if group_key not in target:
        target[group_key] = []
    
    seen_names = {item['name'] for item in target[group_key]}
    
    new_count = 0
    for item in exp.get('items', []):
        if item['name'] not in seen_names:
            target[group_key].append(item)
            seen_names.add(item['name'])
            new_count += 1
            
    with open(base_file, 'w', encoding='utf-8') as f:
        yaml.dump(base, f, indent=2, sort_keys=False, allow_unicode=True)
    
    print(f"Merged {new_count} items into {base_file} -> {category_path}")

def integrate_armor():
    # Armor expansion items are usually PL 7
    merge_yaml_list('site/data/armor.yaml', 'site/data/armor_expansion_expansion.yaml', ['categories', 'powered', 'groups', 'PL 7'])

def integrate_weapons():
    # I'll create weapons.yaml first from weapons.json
    base_json = 'site/data/weapons.json'
    with open(base_json, 'r', encoding='utf-8') as f:
        weapons_data = json.load(f)
    
    # Weapons expansion
    with open('site/data/weapons_expansion_expansion.yaml', 'r', encoding='utf-8') as f:
        exp = yaml.safe_load(f)
        
    # Simplify: Just append all expansion weapons to a new "Expansion" category or similar
    # Actually, weapons.json has nested categories: melee, ranged, etc.
    # I'll just merge them into 'ranged' for now or detect based on the name if possible.
    # For now, to fulfill the request quickly, I'll just ensure they are in the JSON.
    
    # Better: I'll create a dedicated weapons_expansion.json as the user asked for "create any missing category"
    pass

if __name__ == '__main__':
    integrate_armor()
    # For other categories, I'll create new YAML files and sync them
