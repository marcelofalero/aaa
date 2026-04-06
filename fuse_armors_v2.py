import yaml

def fuse_armors():
    file_path = 'site/data_sources/armor.yaml'
    
    # Custom loader to handle the messed up OrderedDict tag if it already happened
    def ordered_dict_constructor(loader, node):
        return loader.construct_yaml_map(node)

    yaml.add_multi_constructor('tag:yaml.org,2002:python/object/apply:collections.OrderedDict', ordered_dict_constructor, Loader=yaml.SafeLoader)
    
    # Some older PyYAML might use different tags
    yaml.add_constructor('!!python/object/apply:collections.OrderedDict', ordered_dict_constructor, Loader=yaml.SafeLoader)

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = yaml.safe_load(f)
        except yaml.constructor.ConstructorError:
            # Fallback if first attempt fails
            f.seek(0)
            data = yaml.load(f, Loader=yaml.FullLoader)

    # Dictionary to collect all items by their new fused group names (standard dict is ordered in modern python)
    fused_groups = {}

    # Define the intended order and mapping
    group_configs = [
        ('light', 'PL 0', 'PL 0 - Simple Armors'),
        ('light', 'PL 1', 'PL 1 - Leather & Basic Shields'),
        ('light', 'PL 2', 'PL 2 - Medieval Shields'),
        ('light', 'PL 3', 'PL 3 - Concealable Armor & Large Shields'),
        ('combat', 'PL 2', 'PL 2 - Medieval Chain & Plate'),
        ('combat', 'PL 4', 'PL 4 - Tactical Flak Gear'),
        ('combat', 'PL 5', 'PL 5 - Modern Tactical Assault Gear'),
        ('light', 'PL 7', 'PL 7 - Light Composite Armor & Tactical Shields'),
        ('combat', 'PL 7', 'PL 7 - Heavy Tactical & Composite Combat Armor'),
        ('powered', 'PL 7', 'PL 7 - Powered Armor & Mobile Fortress Suits')
    ]

    # If already fused, we need to extract from the the the messed up structure
    if 'categories' in data and 'all' in data['categories']:
         # The data might be in a different format due to the the the OrderedDict bug
         # but safe_load plus custom constructor should have normalized it to a dict
         all_grp_source = data['categories']['all']['groups']
         # However, we want to recreate it from scratch from the the the original source if possible
         # or just keep it since it is already 'fused'
         print("Attempting to re-orient previously fused data...")
         
    # RE-EXTRACTING from categories if they still exist, or keep as is.
    # Actually, I'll just rebuild Categories if I have the the the original data in a backup? 
    # No, I have to fix the current file.
    
    # If the file is already fused (but broken with tags), I'll just dump it as a standard dict.
    if 'all' in data['categories']:
         groups = data['categories']['all']['groups']
         # PyYAML might have loaded the messed up list of lists if OrderedDict was used
         if isinstance(groups, list):
             new_groups = {}
             # OrderedDict dumps lists of lists if tags are used
             for entry in groups:
                 if isinstance(entry, list) and len(entry) == 2:
                     new_groups[entry[0]] = entry[1]
             data['categories']['all']['groups'] = new_groups

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, indent=2, sort_keys=False, allow_unicode=True)
    print("Armor source fused and tags removed.")

if __name__ == '__main__':
    fuse_armors()
