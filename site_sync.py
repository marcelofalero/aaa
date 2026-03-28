import yaml
import os
import json

SOURCE_DIR = 'site/data_sources'
DATA_DIR = 'site/data'

def sync_data(file_base):
    """
    Syncs a YAML source of truth to English and Spanish JSON files.
    """
    yaml_file = os.path.join(SOURCE_DIR, f'{file_base}.yaml')
    json_en = os.path.join(DATA_DIR, f'{file_base}.json')
    json_es = os.path.join(DATA_DIR, f'{file_base}.es.json')
    
    if not os.path.exists(yaml_file):
        print(f"Skipping {file_base}, source not found.")
        return

    with open(yaml_file, 'r', encoding='utf-8') as f:
        master = yaml.safe_load(f)

    # Version check / Basic structure
    if 'categories' not in master:
        print(f"Invalid YAML structure in {yaml_file}")
        return

    # English and Spanish data containers
    data_en = {}
    data_es = {}

    for cat_id, cat_data in master.get('categories', {}).items():
        cat_en = {
            "columns": master['config']['columns']['en'],
            "groups": []
        }
        cat_es = {
            "columns": master['config']['columns']['es'],
            "groups": []
        }

        for grp_name, items in cat_data.get('groups', {}).items():
            grp_en = {"name": grp_name, "items": []}
            grp_es = {"name": grp_name, "items": []}

            for item in items:
                # English item
                i_en = item.copy()
                if isinstance(item.get('description'), dict):
                    i_en['description'] = item['description'].get('en', '')
                
                # Spanish item
                i_es = item.copy()
                if 'name_es' in i_es:
                    i_es['name'] = i_es['name_es']
                if isinstance(item.get('description'), dict):
                    i_es['description'] = item['description'].get('es', '')
                
                # Cleanup internal fields from the JSON output
                for k in ['name_es']:
                    if k in i_en: del i_en[k]
                    if k in i_es: del i_es[k]

                grp_en['items'].append(i_en)
                grp_es['items'].append(i_es)

            cat_en['groups'].append(grp_en)
            cat_es['groups'].append(grp_es)

        data_en[cat_id] = cat_en
        data_es[cat_id] = cat_es

    with open(json_en, 'w', encoding='utf-8') as f:
        json.dump(data_en, f, indent=2, ensure_ascii=False)
    with open(json_es, 'w', encoding='utf-8') as f:
        json.dump(data_es, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully synced: {file_base}")

if __name__ == '__main__':
    # Ensure source directory exists
    if not os.path.exists(SOURCE_DIR):
        os.makedirs(SOURCE_DIR)
        
    categories = ['armor', 'computers', 'cybernetics']
    for cat in categories:
        sync_data(cat)
