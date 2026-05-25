import yaml
import os
import sys
import re
import argparse
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString, FoldedScalarString

# Initialize ruamel.yaml for formatting checks
yaml_ruamel = YAML()
yaml_ruamel.preserve_quotes = True

def get_file_type(data, file_path):
    # Determine if it's skill-based or item-based
    if 'skills' in file_path.lower() or 'psionics' in file_path.lower():
        return 'skill'
    
    def check_for_skills(items):
        for item in items.values():
            if not isinstance(item, dict): continue
            if 'rank_benefits' in item or 'attribute' in item:
                return True
            if 'items' in item:
                return check_for_skills(item['items'])
        return False

    if isinstance(data, dict) and 'items' in data:
        if check_for_skills(data['items']):
            return 'skill'
    
    return 'item'

def validate_localized(localized, path, errors):
    if not isinstance(localized, list):
        errors.append(f"{path} -> 'localized' must be a list")
        return
    
    found_langs = set()
    for i, entry in enumerate(localized):
        if not isinstance(entry, dict):
            errors.append(f"{path} -> 'localized[{i}]' must be a dictionary")
            continue
        
        for lang in ['en', 'es']:
            if lang in entry:
                found_langs.add(lang)
                if not isinstance(entry[lang], dict):
                    errors.append(f"{path} -> 'localized[{i}][{lang}]' must be a dictionary")

    for lang in ['en', 'es']:
        if lang not in found_langs:
            errors.append(f"{path} -> missing '{lang}' translation in 'localized' list")

def validate_item_schema(item_data, path, file_type, errors):
    if not isinstance(item_data, dict): return

    # Check for optional metadata fields
    if 'url' in item_data:
        if not isinstance(item_data['url'], str):
            errors.append(f"{path} -> 'url' must be a string")
        elif not item_data['url'].startswith('/'):
            errors.append(f"{path} -> 'url' ({item_data['url']}) should start with '/'")

    if file_type == 'skill' or 'rank_benefits' in item_data:
        if 'rank_benefits' in item_data:
            if not isinstance(item_data['rank_benefits'], list):
                errors.append(f"{path} -> 'rank_benefits' must be a list")
            else:
                for i, benefit in enumerate(item_data['rank_benefits']):
                    if not isinstance(benefit, dict):
                        errors.append(f"{path} -> 'rank_benefits[{i}]' must be a dictionary")
                        continue
                    if 'rank' not in benefit:
                        errors.append(f"{path} -> 'rank_benefits[{i}]' missing 'rank'")
                    elif not isinstance(benefit['rank'], int):
                        errors.append(f"{path} -> 'rank_benefits[{i}].rank' must be an integer")

    # Common physical item properties for item-based
    if file_type == 'item':
        for field in ['cost', 'mass', 'pl', 'avail']:
            if field in item_data and not isinstance(item_data[field], (str, int, float)):
                 errors.append(f"{path} -> '{field}' must be a simple value (string/number)")

    # Check for localized
    if 'localized' in item_data:
        validate_localized(item_data['localized'], path, errors)
    elif 'items' not in item_data:
        errors.append(f"{path} -> Leaf item is missing 'localized' data")

    # Recurse
    if 'items' in item_data:
        for sub_id, sub_data in item_data['items'].items():
            validate_item_schema(sub_data, f"{path}.{sub_id}", file_type, errors)

def check_formatting(file_path, data, errors):
    # 1. Check raw file for whitespace and tabs
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        if line.endswith(' \n') or line.endswith('\t\n'):
            errors.append(f"Line {i+1}: Trailing whitespace detected")
        if '\t' in line:
            errors.append(f"Line {i+1}: Tab character detected (use spaces)")

    # 2. Check for long strings and their formatting style
    def walk_style(node, path=""):
        if isinstance(node, dict):
            for k, v in node.items():
                walk_style(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk_style(v, f"{path}[{i}]")
        elif isinstance(node, str):
            if len(node) > 80:
                # Check if it's a LiteralScalarString (|) or FoldedScalarString (>)
                if not isinstance(node, (LiteralScalarString, FoldedScalarString)):
                    errors.append(f"Formatting: Value at '{path}' is long ({len(node)} chars) but not in block scalar format (|- or >)")

    walk_style(data)

def generate_changes_report(old_data, new_data):
    report = []
    
    def compare_nodes(v1, v2, path=""):
        if type(v1) != type(v2) and not (isinstance(v1, str) and isinstance(v2, str)):
            report.append(f"CHANGED (type): {path} ({type(v1).__name__} -> {type(v2).__name__})")
            return

        if isinstance(v1, dict):
            keys1, keys2 = set(v1.keys()), set(v2.keys())
            for k in keys2 - keys1: report.append(f"ADDED: {path}.{k}")
            for k in keys1 - keys2: report.append(f"REMOVED: {path}.{k}")
            for k in keys1 & keys2: compare_nodes(v1[k], v2[k], f"{path}.{k}")
        elif isinstance(v1, list):
            if len(v1) != len(v2):
                report.append(f"CHANGED (length): {path} ({len(v1)} -> {len(v2)})")
            else:
                for i in range(len(v1)):
                    compare_nodes(v1[i], v2[i], f"{path}[{i}]")
        else:
            if v1 != v2:
                report.append(f"CHANGED: {path}")
                    
    compare_nodes(old_data, new_data)
    return report

def lint_file(file_path, reference_path=None):
    errors = []
    print(f"Linting {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml_ruamel.load(f)
    except Exception as e:
        print(f"ERROR: Failed to parse YAML: {e}")
        return False

    if not data:
        print("WARNING: File is empty")
        return True

    file_type = get_file_type(data, file_path)
    print(f"Detected type: {file_type}")

    # Schema Validation
    if isinstance(data, dict):
        if 'items' in data:
            for item_id, item_data in data['items'].items():
                validate_item_schema(item_data, f"items.{item_id}", file_type, errors)
        else:
            for sect_id, sect_data in data.items():
                if isinstance(sect_data, dict) and 'items' in sect_data:
                    for item_id, item_data in sect_data['items'].items():
                        validate_item_schema(item_data, f"{sect_id}.items.{item_id}", file_type, errors)

    # Formatting Validation
    check_formatting(file_path, data, errors)

    if errors:
        for err in errors:
            print(f"  [X] {err}")
    else:
        print("  [OK] No issues found.")

    # Changes Report
    if reference_path and os.path.exists(reference_path):
        print(f"Generating changes report against {reference_path}...")
        try:
            with open(reference_path, 'r', encoding='utf-8') as f:
                old_data = yaml_ruamel.load(f)
            changes = generate_changes_report(old_data, data)
            if changes:
                for change in sorted(list(set(changes))):
                    print(f"  [CHANGE] {change}")
            else:
                print("  [CHANGE] No changes detected.")
        except Exception as e:
            print(f"ERROR: Failed to load reference file: {e}")

    # Return True if no errors (ignoring formatting warnings for now if desired, 
    # but here we consider everything an error)
    return len(errors) == 0

def main():
    parser = argparse.ArgumentParser(description="Linter for YAML data sources")
    parser.add_argument("files", nargs="+", help="Files to lint")
    parser.add_argument("--ref", help="Reference file for changes report")
    
    args = parser.parse_args()
    
    all_passed = True
    for file in args.files:
        if not lint_file(file, args.ref if len(args.files) == 1 else None):
            all_passed = False
        print("-" * 40)
        
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
