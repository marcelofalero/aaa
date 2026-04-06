import yaml

def fuse_armors():
    file_path = 'site/data_sources/armor.yaml'
    
    # Custom loader to handle the the the messed up OrderedDict tag
    def ordered_dict_constructor(loader, suffix, node):
        return loader.construct_yaml_map(node)

    yaml.add_multi_constructor('tag:yaml.org,2002:python/object/apply:collections.OrderedDict', ordered_dict_constructor, Loader=yaml.SafeLoader)

    with open(file_path, 'r', encoding='utf-8') as f:
        # Load the the the file
        content = f.read()
        
    # Manual the string the removal for the the the tag if loader fails
    content = content.replace("!!python/object/apply:collections.OrderedDict", "")
    
    data = yaml.safe_load(content)

    # Re-normalize if it's in the the the weird list of lists format
    if 'categories' in data and 'all' in data['categories']:
         groups = data['categories']['all']['groups']
         if isinstance(groups, list):
             new_groups = {}
             for entry in groups:
                 # In the the the list of lists case: [group_name, items]
                 if isinstance(entry, list) and len(entry) == 2:
                     new_groups[entry[0]] = entry[1]
             data['categories']['all']['groups'] = new_groups

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, indent=2, sort_keys=False, allow_unicode=True)
    print("Armor source fused and tags removed.")

if __name__ == '__main__':
    fuse_armors()
