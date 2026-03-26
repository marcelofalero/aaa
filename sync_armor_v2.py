import yaml
import json
import os

def sync_armor():
    yaml_file = 'site/data_sources/armor.yaml'
    en_json = 'site/data/armor.json'
    es_json = 'site/data/armor.es.json'

    if not os.path.exists(yaml_file):
        print(f"Error: {yaml_file} not found.")
        return

    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Prepare English and Spanish versions
    results = {
        'en': { 'columns': data['config']['columns']['en'], 'groups': [] },
        'es': { 'columns': data['config']['columns']['es'], 'groups': [] }
    }

    # Process "all" category (the current one)
    cat_data = data['categories']['all']
    # Use items() to maintain order if it's an OrderedDict, or just iterate groups.
    # Actually yaml.safe_load might not preserve order if it's old python, but let's assume it does.
    for group_name, items in cat_data['groups'].items():
        en_group = { "name": group_name, "items": [] }
        es_group = { "name": group_name, "items": [] }
        
        for item in items:
            # EN item
            en_item = item.copy()
            if isinstance(item.get('description'), dict):
                en_item['description'] = item['description'].get('en', '')
            
            en_item.pop('description_es', None) # cleanup if exists
            en_item.pop('name_es', None)
            en_group['items'].append(en_item)
            
            # ES item
            es_item = item.copy()
            es_item['name'] = item.get('name_es', item['name'])
            if isinstance(item.get('description'), dict):
                es_item['description'] = item['description'].get('es', '')
            
            es_item.pop('name_es', None)
            es_item.pop('description_es', None)
            es_group['items'].append(es_item)
        
        results['en']['groups'].append(en_group)
        results['es']['groups'].append(es_group)

    # Save
    with open(en_json, 'w', encoding='utf-8') as f:
        json.dump({'all': results['en']}, f, indent=2, ensure_ascii=False)
    with open(es_json, 'w', encoding='utf-8') as f:
        json.dump({'all': results['es']}, f, indent=2, ensure_ascii=False)

    print("Armor data successfully synced to JSON files!")

if __name__ == '__main__':
    sync_armor()
