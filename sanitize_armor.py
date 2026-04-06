import yaml
import re

def sanitize_armor():
    file_path = 'site/data_sources/armor.yaml'
    survival_path = 'site/data_sources/survival_gear.yaml'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # 1. Identify items to remove or move
    survival_names = [
        "TerrainMaster 5§ Portable Cabin",
        "Gliese 300 habitat dome",
        "ARMADILLO MPT Two-MAN TENT",
        "Unner 60 CLIMATE SuIT",
        "VacMaster 77 Vacuum Mask",
        "Explorer D9 Armored E-Suit"
    ]
    
    delete_names = [
        "Calefir Family Corporation",
        "Rockets",
        "Ptokh K'se", # I'll re-add it correctly if it's broken
        "CERAMETAL ARMOR" # This variant is bad
    ]

    survival_items = []
    
    for cat_id in list(data['categories'].keys()):
        cat = data['categories'][cat_id]
        for grp_id in list(cat['groups'].keys()):
            items = cat['groups'][grp_id]
            new_items = []
            for item in items:
                name = item.get('name', '')
                
                # Check for bad price concatenation like 2500035000
                cost = str(item.get('cost', ''))
                if len(cost) > 8: # Arbitrary threshold for concatenated prices
                    # Try to take the first 5 digits or something reasonable
                    match = re.match(r'(\d{4,6})', cost)
                    if match:
                        print(f"Fixing cost for {name}: {cost} -> {match.group(1)}")
                        item['cost'] = match.group(1)

                if name in survival_names:
                    survival_items.append(item)
                elif name in delete_names:
                    print(f"Deleting non-armor item: {name}")
                else:
                    # Specific fixes from the image
                    if name == "Paladin":
                         item['cost'] = "25000"
                    
                    new_items.append(item)
            
            cat['groups'][grp_id] = new_items

    # Save Survival Gear
    # Simple structure for survival gear
    survival_data = {
        "config": data['config'], # Reuse columns
        "categories": {
            "survival": {
                "groups": {
                    "PL 7 Survival Gear": survival_items
                }
            }
        }
    }
    
    with open(survival_path, 'w', encoding='utf-8') as f:
        yaml.dump(survival_data, f, indent=2, sort_keys=False, allow_unicode=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, indent=2, sort_keys=False, allow_unicode=True)
    
    print("Armor sanitized. Survival gear moved to separate file.")

if __name__ == '__main__':
    sanitize_armor()
