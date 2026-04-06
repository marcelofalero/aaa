import yaml
import json
import os

def sync_armor():
    yaml_file = 'site/data/armor.yaml'
    en_json = 'site/data/armor.json'
    es_json = 'site/data/armor.es.json'

    if not os.path.exists(yaml_file):
        print(f"Error: {yaml_file} not found.")
        return

    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # English JSON structure
    en_out = {
        "light": { "columns": data['config']['columns']['en'], "groups": [] },
        "combat": { "columns": data['config']['columns']['en'], "groups": [] },
        "powered": { "columns": data['config']['columns']['en'], "groups": [] }
    }

    # Spanish JSON structure
    es_out = {
        "light": { "columns": data['config']['columns']['es'], "groups": [] },
        "combat": { "columns": data['config']['columns']['es'], "groups": [] },
        "powered": { "columns": data['config']['columns']['es'], "groups": [] }
    }

    for category_id in ['light', 'combat', 'powered']:
        if category_id in data['categories']:
            cat_data = data['categories'][category_id]
            for group_name, items in cat_data['groups'].items():
                en_group = { "name": group_name, "items": [] }
                es_group = { "name": group_name, "items": [] }
                
                for item in items:
                    # English item
                    en_item = item.copy()
                    en_item['description'] = item['description']['en']
                    en_item.pop('name_es', None) # If exists
                    en_group['items'].append(en_item)
                    
                    # Spanish item
                    es_item = item.copy()
                    es_item['name'] = item.get('name_es', item['name'])
                    es_item['description'] = item['description']['es']
                    es_item.pop('name_es', None)
                    es_group['items'].append(es_item)
                
                en_out[category_id]['groups'].append(en_group)
                es_out[category_id]['groups'].append(es_group)

    # Save
    with open(en_json, 'w', encoding='utf-8') as f:
        json.dump(en_out, f, indent=2, ensure_ascii=False)
    with open(es_json, 'w', encoding='utf-8') as f:
        json.dump(es_out, f, indent=2, ensure_ascii=False)

    print("Successfully synced JSON files from YAML source of truth.")

if __name__ == '__main__':
    sync_armor()
