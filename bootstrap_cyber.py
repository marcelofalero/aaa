import json
import yaml
import os

def bootstrap_cybernetics():
    with open('site/data/cybernetics.json', 'r') as f:
        base = json.load(f)
    
    # Load expansion (if any)
    exp_file = 'site/data/cybernetics_expansion.yaml'
    exp_items = []
    if os.path.exists(exp_file):
        with open(exp_file, 'r') as f:
            exp_data = yaml.safe_load(f)
            exp_items = exp_data.get('items', [])

    # Master structure
    master = {
        "config": {
            "columns": {
                "en": [
                    {"name": "Gear", "key": "name"},
                    {"name": "Nanocomp.", "key": "nanocomp"},
                    {"name": "Mass", "key": "mass"},
                    {"name": "Size", "key": "size"},
                    {"name": "Cost", "key": "cost"},
                    {"name": "Description", "key": "description", "hidden": True}
                ],
                "es": [
                    {"name": "Equipo", "key": "name"},
                    {"name": "Nanocomp.", "key": "nanocomp"},
                    {"name": "Masa", "key": "mass"},
                    {"name": "Tamaño", "key": "size"},
                    {"name": "Coste", "key": "cost"},
                    {"name": "Descripción", "key": "description", "hidden": True}
                ]
            }
        },
        "categories": {
            "gear": {
                "groups": {
                    "Progress Level 6": [],
                    "Progress Level 7": [],
                    "Expansion": []
                }
            }
        }
    }

    # Populate from base JSON
    # Map groups
    for group in base['gear']['groups']:
        g_name = group['name']
        if g_name not in master['categories']['gear']['groups']:
             master['categories']['gear']['groups'][g_name] = []
        
        for item in group['items']:
            # Try to get localized description
            # Actually, I'll just keep them as is for now
            master['categories']['gear']['groups'][g_name].append({
                "name": item.get('name'),
                "nanocomp": item.get('nanocomp', '-'),
                "mass": item.get('mass', '-'),
                "size": item.get('size', '-'),
                "cost": item.get('cost', '-'),
                "description": {"en": item.get('description', ''), "es": ""}
            })

    # Add expansion items to "Expansion" group
    seen = {i['name'] for g in master['categories']['gear']['groups'].values() for i in g}
    for item in exp_items:
        if item['name'] not in seen:
            master['categories']['gear']['groups']['Expansion'].append({
                "name": item['name'],
                "nanocomp": item.get('nanocomp', 'Yes'),
                "mass": item.get('mass', '-'),
                "size": item.get('size', '1'),
                "cost": item.get('cost', '-'),
                "description": {"en": item.get('description', ''), "es": ""}
            })
            seen.add(item['name'])

    with open('site/data/cybernetics.yaml', 'w') as f:
        yaml.dump(master, f, indent=2, sort_keys=False)
    print("Bootstrapped cybernetics.yaml")

if __name__ == '__main__':
    bootstrap_cybernetics()
