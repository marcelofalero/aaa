import yaml
import os
import sys

def validate_localized(localized, path):
    if not isinstance(localized, list):
        print(f"ERROR: {path} -> 'localized' must be a list")
        return False
    
    valid = True
    for i, entry in enumerate(localized):
        if not isinstance(entry, dict):
            print(f"ERROR: {path} -> 'localized[{i}]' must be a dictionary")
            valid = False
            continue
        
        for lang in ['en', 'es']:
            if lang in entry:
                if not isinstance(entry[lang], dict):
                    print(f"ERROR: {path} -> 'localized[{i}][{lang}]' must be a dictionary")
                    valid = False
                elif 'name' not in entry[lang] and entry[lang] != {}:
                    # name is generally required unless it's an empty override
                    print(f"WARNING: {path} -> 'localized[{i}][{lang}]' is missing 'name'")
    return valid

def validate_config(config, path):
    if not isinstance(config, dict):
        print(f"ERROR: {path} -> 'config' must be a dictionary")
        return False
    
    if 'default' not in config:
        print(f"ERROR: {path} -> 'config' missing 'default'")
        return False
    
    default = config['default']
    if 'columns' not in default:
        print(f"ERROR: {path} -> 'config.default' missing 'columns'")
        return False
    
    columns = default['columns']
    valid = True
    for lang in ['en', 'es']:
        if lang not in columns:
            print(f"ERROR: {path} -> 'config.default.columns' missing '{lang}'")
            valid = False
            continue
        
        if not isinstance(columns[lang], list):
            print(f"ERROR: {path} -> 'config.default.columns.{lang}' must be a list")
            valid = False
            continue
            
        for i, col in enumerate(columns[lang]):
            if not isinstance(col, dict):
                print(f"ERROR: {path} -> 'config.default.columns.{lang}[{i}]' must be a dictionary")
                valid = False
                continue
            if 'name' not in col or 'key' not in col:
                print(f"ERROR: {path} -> 'config.default.columns.{lang}[{i}]' must have 'name' and 'key'")
                valid = False
                
    return valid

def validate_items(items, path):
    if not isinstance(items, dict):
        print(f"ERROR: {path} -> 'items' must be a dictionary")
        return False
    
    valid = True
    for item_id, item_data in items.items():
        if not isinstance(item_data, dict):
            print(f"ERROR: {path}.{item_id} -> item data must be a dictionary")
            valid = False
            continue
        
        # Check for optional metadata fields (commonly found in skills and psionics)
        if 'url' in item_data:
            if not isinstance(item_data['url'], str):
                print(f"ERROR: {path}.{item_id} -> 'url' must be a string")
                valid = False
            elif not item_data['url'].startswith('/'):
                print(f"WARNING: {path}.{item_id} -> 'url' ({item_data['url']}) should usually start with '/'")

        if 'rank_benefits' in item_data:
            # Optional list of benefits for skills/psionics
            if not isinstance(item_data['rank_benefits'], list):
                print(f"ERROR: {path}.{item_id} -> 'rank_benefits' must be a list")
                valid = False
            else:
                for i, benefit in enumerate(item_data['rank_benefits']):
                    if not isinstance(benefit, dict):
                        print(f"ERROR: {path}.{item_id} -> 'rank_benefits[{i}]' must be a dictionary")
                        valid = False
                        continue
                    if 'rank' not in benefit:
                        print(f"ERROR: {path}.{item_id} -> 'rank_benefits[{i}]' missing 'rank'")
                        valid = False
                    elif not isinstance(benefit['rank'], int):
                        print(f"ERROR: {path}.{item_id} -> 'rank_benefits[{i}].rank' must be an integer")
                        valid = False

        # Common physical item properties (optional, varied by file)
        for field in ['cost', 'mass', 'pl', 'avail']:
            if field in item_data and not isinstance(item_data[field], (str, int, float)):
                 print(f"ERROR: {path}.{item_id} -> '{field}' must be a simple value (string/number)")
                 valid = False

        # Check for localized (Recommended for all items/categories)
        if 'localized' in item_data:
            if not validate_localized(item_data['localized'], f"{path}.{item_id}"):
                valid = False
        elif 'items' not in item_data: # If it's a leaf item, it SHOULD have localized
             print(f"WARNING: {path}.{item_id} -> Leaf item is missing 'localized' data")
        
        # If it has nested items, it's a category or broad skill
        if 'items' in item_data:
            if not validate_items(item_data['items'], f"{path}.{item_id}"):
                valid = False
                
    return valid

def validate_section(data, path):
    valid = True
    if 'config' in data:
        if not validate_config(data['config'], path):
            valid = False
    
    if 'items' in data:
        if not validate_items(data['items'], path):
            valid = False
    else:
        print(f"ERROR: {path} missing 'items'")
        valid = False
        
    return valid

def validate_file(file_path):
    print(f"Validating {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"ERROR: Failed to parse YAML: {e}")
        return False

    if not data:
        print(f"WARNING: {file_path} is empty")
        return True

    valid = True
    
    # Check if it's a multi-section file or a single-section file
    # skills.yaml has 'items' at top level
    # weapons.yaml has 'melee', 'ranged' which contain 'items'
    
    if 'items' in data or 'config' in data:
        # Single section style
        if not validate_section(data, file_path):
            valid = False
    else:
        # Multi-section style or unknown
        # We look for keys that look like sections (have 'items' or are listed in the logic)
        sections_found = 0
        for key, value in data.items():
            if isinstance(value, dict) and 'items' in value:
                if not validate_section(value, f"{file_path} -> {key}"):
                    valid = False
                sections_found += 1
        
        if sections_found == 0:
            print(f"ERROR: {file_path} -> No valid sections with 'items' found at top level")
            valid = False
            
    return valid

def main():
    data_dir = 'data_sources'
    if not os.path.exists(data_dir):
        # try relative to script
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data_sources')
    
    if not os.path.exists(data_dir):
        print(f"ERROR: Could not find data_sources directory")
        sys.exit(1)

    files = [f for f in os.listdir(data_dir) if f.endswith('.yaml')]
    all_valid = True
    for file in sorted(files):
        if not validate_file(os.path.join(data_dir, file)):
            all_valid = False
            print(f"FAILED: {file}")
        else:
            print(f"PASSED: {file}")
        print("-" * 40)

    if all_valid:
        print("All data sources validated successfully.")
        sys.exit(0)
    else:
        print("Validation errors found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
