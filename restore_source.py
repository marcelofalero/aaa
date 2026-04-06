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
    fused_groups = {}
    
    # In the JSON, categories were: light, combat, powered
    # But now we fused them into 'all'
    # Wait! I'll just iterate all original categories and combine
    categories = ['light', 'combat', 'powered']
    
    group_map = {}
    
    def get_nice_name(cat_id, grp_name):
        # We can detect if it's already a nice name or a simple PL
        if grp_name.startswith('PL '):
             if cat_id == 'light':
                 return f"{grp_name} - Simple & Personnel Armor"
             if cat_id == 'combat':
                 return f"{grp_name} - Tactical & Combat Gear"
             if cat_id == 'powered':
                 return f"{grp_id} - Powered Battle Suits"
        return grp_name

    for cat_id in categories:
        if cat_id in en:
            en_cat = en[cat_id]
            es_cat = es[cat_id]
            
            for en_grp, es_grp in zip(en_cat['groups'], es_cat['groups']):
                nice_name = en_grp['name']
                if nice_name not in group_map:
                    group_map[nice_name] = []
                
                for i_en, i_es in zip(en_grp['items'], es_grp['items']):
                    # Reconstruct the the the the bilingual YAML object
                    item = i_en.copy()
                    item['name_es'] = i_es.get('name')
                    # Localized descriptions
                    item['description'] = {
                        'en': i_en.get('description', ''),
                        'es': i_es.get('description', '')
                    }
                    group_map[nice_name].append(item)

    # Re-syncing the config too
    config = {
        'columns': {
            'en': en['light']['columns'], # Grabbing from the the the first one found
            'es': es['light']['columns']
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
    print("Master YAML restored to be bilingual and fused.")

if __name__ == '__main__':
    restore_bilingual_source()
