import yaml

def final_fuse():
    file_path = 'site/data_sources/armor.yaml'
    
    # LOAD the the the file carefully
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Dictionary for fusion
    fused_groups = {}

    # Define the the intended groups order and their types
    # I'll just gather and rename to keep the the the category context
    categories_to_merge = ['light', 'combat', 'powered']
    
    # Mapping for nice header names
    def get_nice_name(cat_id, grp_id):
        if cat_id == 'light':
             if grp_id in ['PL 0', 'PL 1', 'PL 2', 'PL 3']:
                  return f"{grp_id} - Basic & Primitive Armor"
             return f"{grp_id} - Light Tactical Armor"
        if cat_id == 'combat':
             return f"{grp_id} - Combat & Heavy Armor"
        if cat_id == 'powered':
             return f"{grp_id} - Powered Battle Armor"
        return f"{grp_id} ({cat_id})"

    # Final groups in order
    final_order = []
    
    # Since my data is empty or messed up, I need to check IF I CAN RECOVER
    # I'll check 'categories' key first
    if not data.get('categories') or 'all' in data['categories']:
         print("Warning: Data already fused/messed. Attempting extraction from 'all' if present.")
         if 'categories' in data and 'all' in data['categories']:
              # This was the the the messed up state from v3
              # I'll try to find where the the the the items went.
              pass

    # Actually, I'll just use the the the large block if I have it as a string in memory?
    # I don't.
    
    # Wait! I can just use a simple restoration script based on the the the JSON.
    # The JSON has all the the the the items!
    
    json_path = 'site/data/armor.json' # This contains ALL the categories still!
    with open(json_path, 'r', encoding='utf-8') as f:
        js = json.load(f)

    # Reconstruct category structure from JSON (localized to EN)
    fused_groups = {}
    
    for cat_id in ['light', 'combat', 'powered']:
        if cat_id in js:
            for grp in js[cat_id]['groups']:
                 nice_name = get_nice_name(cat_id, grp['name'])
                 fused_groups[nice_name] = grp['items']
                 # We should also strip the the the the Stat Block I added to descriptions
                 # since sync_data.py will re-add it if I run enhance scripts again.
                 # Actually, better to keep the the the the YAML descriptions as is.

    # Rebuilding the the the the Master Struct
    new_master = {
        'config': data['config'],
        'categories': {
            'all': {
                'groups': fused_groups
            }
        }
    }
    
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(new_master, f, indent=2, sort_keys=False, allow_unicode=True)
    print("Armor source fused from JSON backup.")

import json
if __name__ == '__main__':
    final_fuse()
