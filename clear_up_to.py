from ruamel.yaml import YAML

ryaml = YAML()
ryaml.preserve_quotes = True
ryaml.width = 1000
ryaml.indent(mapping=2, sequence=4, offset=2)

with open('sources/data_sources/skills.yaml', 'r', encoding='utf-8') as f:
    data = ryaml.load(f)

cleared_count = 0
found_medical_science = False

def clear_es_descriptions(node):
    global cleared_count
    global found_medical_science
    
    if found_medical_science:
        return
        
    if isinstance(node, dict):
        # We process 'localized' first for the current node
        if 'localized' in node:
            en_name = ''
            for loc in node['localized']:
                if 'en' in loc:
                    en_name = loc['en'].get('name', '')
            
            # clear the Spanish description
            for loc in node['localized']:
                if 'es' in loc:
                    if loc['es'].get('description'):
                        loc['es']['description'] = ''
                        cleared_count += 1
                        print(f"Cleared description for: {en_name}")
            
            if en_name == 'Medical Science':
                found_medical_science = True
                print("Found Medical Science. Stopping clearing.")
                return

        for k, v in node.items():
            if k != 'localized':
                clear_es_descriptions(v)
    elif isinstance(node, list):
        for item in node:
            clear_es_descriptions(item)

clear_es_descriptions(data)
print(f"Cleared {cleared_count} descriptions.")

with open('sources/data_sources/skills.yaml', 'w', encoding='utf-8') as f:
    ryaml.dump(data, f)
