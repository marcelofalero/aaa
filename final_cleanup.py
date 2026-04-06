import yaml

def final_cleanup():
    file_path = 'site/data_sources/armor.yaml'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # 1. Categories Cleanup
    for cat_id, cat in data['categories'].items():
        for grp_id, items in cat['groups'].items():
            new_items = []
            seen_names = set()
            for item in items:
                name = item['name']
                # Remove duplicates in same group
                if name in seen_names:
                    continue
                seen_names.add(name)
                
                # Cleanup Mass and Price
                item['mass'] = str(item.get('mass', '0')).replace(' kg', '').strip()
                item['cost'] = str(item.get('cost', '0')).replace(',', '').replace('$', '').strip()
                
                # Ensure all required fields exist to avoid empty columns
                if 'ap' not in item: item['ap'] = '-'
                if 'lhe' not in item: item['lhe'] = '-/-/-'
                if 'type' not in item: item['type'] = '-'
                if 'hide' not in item: item['hide'] = '-'
                
                new_items.append(item)
            cat['groups'][grp_id] = new_items

    # 2. Specifically remove the duplicate tail end
    # I'll manually check the powered category
    if 'powered' in data['categories']:
        p_groups = data['categories']['powered']['groups']
        for g_id in p_groups:
             # Remove items seen in other categories (like screens if they are duplicated)
             p_groups[g_id] = [i for i in p_groups[g_id] if i['name'] not in ["DEFLECTION SCREENS", "SCM-16 CAPACITOR SCREEN"]]

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, indent=2, sort_keys=False, allow_unicode=True)
    print("Armor database sanitized and standardized.")

if __name__ == '__main__':
    final_cleanup()
