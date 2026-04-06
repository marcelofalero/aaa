import yaml
from collections import OrderedDict

def fuse_armors():
    file_path = 'site/data_sources/armor.yaml'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Dictionary to collect all items by their new fused group names
    fused_groups = OrderedDict()

    # Mapping of old groups to descriptive names to avoid collision and keep them separate
    group_mapping = {
        'light': {
            'PL 0': 'PL 0 - Simple Armors',
            'PL 1': 'PL 1 - Leather & Basic Shields',
            'PL 2': 'PL 2 - Medieval Shields',
            'PL 3': 'PL 3 - Concealable Armor & Large Shields',
            'PL 7': 'PL 7 - Light Composite Armor & Tactical Shields',
        },
        'combat': {
            'PL 2': 'PL 2 - Medieval Chain & Plate',
            'PL 4': 'PL 4 - Tactical Flak Gear',
            'PL 5': 'PL 5 - Modern Assault Gear',
            'PL 7': 'PL 7 - Heavy Tactical & Composite Combat Armor',
        },
        'powered': {
            'PL 7': 'PL 7 - Powered Armor & Mobile Fortress Suits',
        }
    }

    # Iterate through categories and merge them into a single list of groups
    for cat_name, mapping in group_mapping.items():
        if cat_name in data['categories']:
            groups = data['categories'][cat_name]['groups']
            for old_grp, new_grp in mapping.items():
                if old_grp in groups:
                     if new_grp not in fused_groups:
                         fused_groups[new_grp] = []
                     fused_groups[new_grp].extend(groups[old_grp])

    # Replace categories with a single 'all' category
    data['categories'] = {
        'all': {
            'groups': fused_groups
        }
    }

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, indent=2, sort_keys=False, allow_unicode=True)
    print("Armor source fused into a single 'all' category.")

if __name__ == '__main__':
    fuse_armors()
