import yaml
import os

def fix_all_headers():
    data_dir = 'site/data_sources/'
    files = [f for f in os.listdir(data_dir) if f.endswith('.yaml')]

    # Mapping for English headers
    header_map = {
        'Armadura': 'Armor',
        'Armor': 'Armor',
        'Masa': 'Mass',
        'Mass': 'Mass',
        'Pena.': 'Pen.',
        'Pen.': 'Pen.',
        'Ocult.': 'Hide',
        'Hide': 'Hide',
        'Disp.': 'Avail.',
        'Avail.': 'Avail.',
        'Coste ($)': 'Cost ($)',
        'Cost ($)': 'Cost ($)',
        'Descripción': 'Description',
        'Description': 'Description',
        'Tipo': 'Type',
        'Type': 'Type',
        'Equipo': 'Item',
        'Item': 'Item',
        'Nanocomp.': 'Nanocomp.',
        'Calidad': 'Quality',
        'Quality': 'Quality',
        'Ranuras': 'Slots',
        'Slots': 'Slots',
        'Tamaño': 'Size',
        'Size': 'Size',
        'Objeto': 'Item'
    }

    for filename in files:
        file_path = os.path.join(data_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
            except Exception as e:
                print(f"Skipping {filename}: {e}")
                continue

        if 'config' in data and 'columns' in data['config'] and 'en' in data['config']['columns']:
            changed = False
            for col in data['config']['columns']['en']:
                old_name = col.get('name')
                new_name = header_map.get(old_name)
                if new_name and old_name != new_name:
                    print(f"Fixing header in {filename}: {old_name} -> {new_name}")
                    col['name'] = new_name
                    changed = True
            
            if changed:
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, indent=2, sort_keys=False, allow_unicode=True)
                print(f"Updated {filename}")

if __name__ == '__main__':
    fix_all_headers()
