import json
from pathlib import Path
from ruamel.yaml import YAML

def compare_costs(yaml_path, json_table_path):
    # 1. Load JSON Table Data
    with open(json_table_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # Map normalized URLs to expected costs
    expected_costs = {}
    
    def normalize_url(url):
        if not url:
            return ""
        # Normalize trailing slash and fragment
        url = url.strip().lower()
        if not url.startswith('/'):
            url = '/' + url
        return url

    # Parse nested JSON categories/broads/specialties
    for category in json_data.get('items', []):
        for broad in category.get('items', []):
            b_url = normalize_url(broad.get('url'))
            if b_url:
                expected_costs[b_url] = broad.get('cost')
            
            for spec in broad.get('items', []):
                s_url = normalize_url(spec.get('url'))
                if s_url:
                    expected_costs[s_url] = spec.get('cost')

    # 2. Load YAML Data
    yaml = YAML()
    with open(yaml_path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.load(f)

    mismatches = []
    
    for broad_key, broad_val in yaml_data.get('items', {}).items():
        # Check Broad
        b_url = normalize_url(broad_val.get('url'))
        b_cost = broad_val.get('cost')
        if b_url in expected_costs:
            if expected_costs[b_url] != b_cost:
                mismatches.append(f"[BROAD] {broad_key}: YAML={b_cost} vs Table={expected_costs[b_url]} (URL: {b_url})")
        
        # Check Specialties
        for spec_key, spec_val in broad_val.get('items', {}).items():
            s_url = normalize_url(spec_val.get('url'))
            s_cost = spec_val.get('cost')
            if s_url in expected_costs:
                if expected_costs[s_url] != s_cost:
                    mismatches.append(f"[SPEC] {broad_key}/{spec_key}: YAML={s_cost} vs Table={expected_costs[s_url]} (URL: {s_url})")

    if not mismatches:
        print("All skill costs match the defined costs in skills-table.json!")
    else:
        print(f"Found {len(mismatches)} cost mismatches:")
        for m in mismatches:
            print(m)

if __name__ == "__main__":
    compare_costs('sources/data_sources/skills.yaml', 'site/data/skills-table.json')
