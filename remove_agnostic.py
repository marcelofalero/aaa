import yaml

def remove_agnostic_cerametal():
    file_path = 'site/data_sources/armor.yaml'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Search and remove "Cerametal armor" (lowercase name) but keep "ACN 4..."
    found = False
    for cat_id, cat in data['categories'].items():
        for grp_id, items in cat['groups'].items():
            new_items = []
            for item in items:
                if item['name'] == "Cerametal armor":
                     print(f"Removing agnostic armor: {item['name']}")
                     found = True
                     continue
                new_items.append(item)
            cat['groups'][grp_id] = new_items

    if found:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, indent=2, sort_keys=False, allow_unicode=True)
        print("Agnostic Cerametal armor removed.")
    else:
        print("Agnostic Cerametal armor not found in a way that matches exactly.")

if __name__ == '__main__':
    remove_agnostic_cerametal()
