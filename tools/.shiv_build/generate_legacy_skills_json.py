import os
import json
import yaml
from pathlib import Path
from ruamel.yaml import YAML

def find_project_root():
    current = Path.cwd().resolve()
    for parent in [current] + list(current.parents):
        if (parent / '.project_root').exists():
            return parent
    return Path.cwd().resolve()

os.chdir(find_project_root())

ryaml = YAML()
SKILLS_YAML = 'sources/data_sources/skills.yaml'
OUTPUT_JSON = 'site/data/skills.json'

def main():
    if not os.path.exists(SKILLS_YAML):
        print(f"Error: {SKILLS_YAML} not found.")
        return

    with open(SKILLS_YAML, 'r', encoding='utf-8') as f:
        data = ryaml.load(f)

    skills_map = {}
    items = data.get('items', {})
    
    # Process broad skills and specialties
    for broad_key, broad_val in items.items():
        # Broad skill entry
        skills_map[broad_key] = broad_val.get('url', f"/skills/{broad_key}")
        
        # Specialties
        specs = broad_val.get('items', {})
        for spec_key, spec_val in specs.items():
            skills_map[spec_key] = spec_val.get('url', f"/skills/{broad_key}#{spec_key}")

    print(f"Successfully reconstructed {OUTPUT_JSON} with {len(skills_map)} entries.")
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(skills_map, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
