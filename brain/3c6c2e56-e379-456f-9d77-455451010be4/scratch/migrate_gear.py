import json, yaml, os, re

def str_presenter(dumper, data):
    if len(data) > 60 or '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', '-', text)
    return re.sub(r'-+', '-', text).strip('-')

# Weapons migration
with open('site/data/weapons.json', 'r', encoding='utf-8') as f:
    en_data = json.load(f)
with open('site/data/weapons.es.json', 'r', encoding='utf-8') as f:
    es_data = json.load(f)

final_yaml = {'search_config': en_data['search_config']}
categories = ['melee', 'ranged', 'heavy', 'ammunition', 'accessories']

for cat in categories:
    if cat not in en_data: continue
    
    cat_en = en_data[cat]
    cat_es = es_data.get(cat, {})
    
    cat_node = {
        'config': {
            'default': {
                'columns': {
                    'en': cat_en['columns'],
                    'es': cat_es.get('columns', cat_en['columns'])
                }
            }
        },
        'items': {}
    }
    
    for i, group_en in enumerate(cat_en.get('groups', [])):
        group_es = cat_es.get('groups', [{}])[i] if i < len(cat_es.get('groups', [])) else {}
        group_id = slugify(group_en['name'])
        group_node = {
            'localized': [
                {'en': {'name': group_en['name']}},
                {'es': {'name': group_es.get('name', group_en['name'])}}
            ],
            'items': {}
        }
        for j, item_en in enumerate(group_en.get('items', [])):
            item_es = group_es.get('items', [{}])[j] if j < len(group_es.get('items', [])) else {}
            item_id = slugify(item_en['name'])
            node = {}
            for k, v in item_en.items():
                if k not in ['name', 'description']: node[k] = v
            node['localized'] = [
                {'en': {'name': item_en['name'], 'description': item_en.get('description', '')}},
                {'es': {'name': item_es.get('name', item_en['name']), 'description': item_es.get('description', item_en.get('description', ''))}}
            ]
            group_node['items'][item_id] = node
        cat_node['items'][group_id] = group_node
    final_yaml[cat] = cat_node

with open('sources/data_sources/weapons.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(final_yaml, f, sort_keys=False, allow_unicode=True, width=80)

# Goods and Services migration
with open('site/data/goods_and_services.json', 'r', encoding='utf-8') as f:
    gs_en = json.load(f)
with open('site/data/goods_and_services.es.json', 'r', encoding='utf-8') as f:
    gs_es = json.load(f)

final_gs = {'search_config': gs_en['search_config']}
gs_categories = ['medical_gear', 'clothing_and_accessories', 'tools_and_electronics', 'communications', 'sensors', 'general_gear', 'services']

for cat in gs_categories:
    if cat not in gs_en: continue
    
    cat_en = gs_en[cat]
    cat_es = gs_es.get(cat, {})
    
    cat_node = {
        'config': {
            'default': {
                'columns': {
                    'en': cat_en['columns'],
                    'es': cat_es.get('columns', cat_en['columns'])
                }
            }
        },
        'items': {}
    }
    
    for i, group_en in enumerate(cat_en.get('groups', [])):
        group_es = cat_es.get('groups', [{}])[i] if i < len(cat_es.get('groups', [])) else {}
        group_id = slugify(group_en['name'])
        group_node = {
            'localized': [
                {'en': {'name': group_en['name']}},
                {'es': {'name': group_es.get('name', group_en['name'])}}
            ],
            'items': {}
        }
        for j, item_en in enumerate(group_en.get('items', [])):
            item_es = group_es.get('items', [{}])[j] if j < len(group_es.get('items', [])) else {}
            item_id = slugify(item_en['name'])
            node = {}
            for k, v in item_en.items():
                if k not in ['name', 'description']: node[k] = v
            node['localized'] = [
                {'en': {'name': item_en['name'], 'description': item_en.get('description', '')}},
                {'es': {'name': item_es.get('name', item_en['name']), 'description': item_es.get('description', item_en.get('description', ''))}}
            ]
            group_node['items'][item_id] = node
        cat_node['items'][group_id] = group_node
    final_gs[cat] = cat_node

with open('sources/data_sources/goods_and_services.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(final_gs, f, sort_keys=False, allow_unicode=True, width=80)
