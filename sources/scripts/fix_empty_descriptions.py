import yaml
from ruamel.yaml import YAML
import os

def fix_skills():
    yaml_path = 'sources/data_sources/skills.yaml'
    backup_dir = 'sources/skills_backup/'
    
    ryaml = YAML()
    ryaml.preserve_quotes = True
    ryaml.indent(mapping=2, sequence=4, offset=2)
    ryaml.width = 4096 # Avoid wrapping
    
    with open(yaml_path, 'r') as f:
        data = ryaml.load(f)
    
    # List of skills to fix (Broad, Specialty, BackupPath)
    to_fix = [
        ('athletics', 'climb', 'athletics/climb.md'),
        ('athletics', 'jump', 'athletics/jump.md'),
        ('athletics', 'swim', 'athletics/swim.md'),
        ('athletics', 'throw', 'athletics/throw.md'),
        ('culture', 'etiquette', 'culture/etiquette.md'),
        ('entertainment', 'musical-instrument', 'entertainment/musical-instrument.md'),
        ('survival', 'survival-training', 'survival/survival-training.md'),
        ('technical-science', 'jury-rig', 'technical-science/jury-rig.md'),
    ]
    
    for broad, spec, path in to_fix:
        full_path = os.path.join(backup_dir, path)
        if not os.path.exists(full_path):
            print(f"Backup not found: {full_path}")
            continue
            
        with open(full_path, 'r') as f:
            content = f.read()
            # Extract content after frontmatter
            if '---' in content:
                parts = content.split('---')
                if len(parts) >= 3:
                    desc = parts[2].strip()
                else:
                    desc = parts[-1].strip()
            else:
                desc = content.strip()
        
        if broad in data['items'] and spec in data['items'][broad].get('items', {}):
            idata = data['items'][broad]['items'][spec]
            for loc in idata.get('localized', []):
                if 'en' in loc:
                    loc['en']['description'] = desc
                    print(f"Fixed: {broad} -> {spec}")

    # Remove duplicate jury-rig if it exists
    if 'technical-science' in data['items']:
        items = data['items']['technical-science']['items']
        if 'jury-rig' in items and 'juryrig' in items:
            # Transfer desc if needed
            if not items['jury-rig']['localized'][0]['en']['description'] and items['juryrig']['localized'][0]['en']['description']:
                 items['jury-rig']['localized'][0]['en']['description'] = items['juryrig']['localized'][0]['en']['description']
            del items['juryrig']
            print("Removed duplicate juryrig")

    with open(yaml_path, 'w') as f:
        ryaml.dump(data, f)

if __name__ == '__main__':
    fix_skills()
