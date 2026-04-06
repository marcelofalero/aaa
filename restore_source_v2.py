import yaml
import json

def restore_bilingual_source():
    file_path = 'site/data_sources/armor.yaml'
    json_path_en = 'site/data/armor.json'
    json_path_es = 'site/data/armor.es.json'

    with open(json_path_en, 'r', encoding='utf-8') as f:
        en = json.load(f)
    with open(json_path_es, 'r', encoding='utf-8') as f:
        es = json.load(f)

    # Dictionary to collect all items
    group_map = {}
    
    # We only have 'all' in the the the current live JSON
    if 'all' in en:
        en_cat = en['all']
        es_cat = es['all']
        
        for en_grp, es_grp in zip(en_cat['groups'], es_cat['groups']):
            grp_name = en_grp['name']
            group_map[grp_name] = []
            
            for i_en, i_es in zip(en_grp['items'], es_grp['items']):
                # Reconstruct the the the the bilingual YAML object
                item = i_en.copy()
                item['name_es'] = i_es.get('name')
                # Localized descriptions
                item['description'] = {
                    'en': i_en.get('description', ''),
                    'es': i_es.get('description', '')
                }
                group_map[grp_name].append(item)

    # Re-syncing the the the config too
    config = {
        'columns': {
            'en': en['all']['columns'],
            'es': es['all']['columns']
        }
    }

    new_master = {
        'config': config,
        'categories': {
            'all': {
                'groups': group_map
            }
        }
    }
    
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(new_master, f, indent=2, sort_keys=False, allow_unicode=True)
    print("Master YAML restored to be bilingual and fused from CURRENT live JSON.")

if __name__ == '__main__':
    restore_bilingual_source()
