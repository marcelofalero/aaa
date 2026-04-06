import yaml

def fix_armor_types():
    file_path = 'site/data_sources/armor.yaml'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Categories that should NOT have 'G' types for standard armors
    # Only Power Armor category should have 'G'
    for cat_id in ['light', 'combat']:
        if cat_id in data['categories']:
            for group_name, items in data['categories'][cat_id]['groups'].items():
                for item in items:
                    # If it's a shield/helm, it remains '-'
                    if item.get('type') == 'G':
                         print(f"Fixing {item['name']}: G -> O")
                         item['type'] = 'O'
    
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, indent=2, sort_keys=False, allow_unicode=True)
    print("Armor types fixed.")

if __name__ == '__main__':
    fix_armor_types()
