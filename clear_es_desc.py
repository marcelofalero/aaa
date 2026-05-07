from ruamel.yaml import YAML

ryaml = YAML()
ryaml.preserve_quotes = True
ryaml.width = 1000
ryaml.indent(mapping=2, sequence=4, offset=2)

with open('sources/data_sources/skills.yaml', 'r', encoding='utf-8') as f:
    data = ryaml.load(f)

def clear_es(node):
    if isinstance(node, dict):
        if 'localized' in node:
            en_name = ''
            for loc in node['localized']:
                if 'en' in loc:
                    en_name = loc['en'].get('name', '')
            if en_name in ['Administration', 'Bureaucracy', 'Management', 'Zero-g Training']:
                for loc in node['localized']:
                    if 'es' in loc:
                        loc['es']['description'] = ''
                        print(f"Cleared {en_name}")
        for k, v in node.items():
            if k != 'localized':
                clear_es(v)
    elif isinstance(node, list):
        for item in node:
            clear_es(item)

clear_es(data)
with open('sources/data_sources/skills.yaml', 'w', encoding='utf-8') as f:
    ryaml.dump(data, f)
