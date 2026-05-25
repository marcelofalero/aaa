import os
import sys
import re
import argparse
import difflib
import time
import shutil
from io import StringIO
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

def clean_string(s):
    if not isinstance(s, str):
        return s
    
    # 1. Trim trailing whitespace from each line
    lines = [line.rstrip() for line in s.splitlines()]
    
    # 2. Collapse multiple blank lines (max 1 blank line allowed)
    cleaned_lines = []
    last_was_blank = False
    
    for line in lines:
        is_blank = not line.strip()
        if is_blank:
            if not last_was_blank:
                cleaned_lines.append("")
                last_was_blank = True
        else:
            cleaned_lines.append(line)
            last_was_blank = False
            
    # 3. Join back and trim leading/trailing empty lines
    result = "\n".join(cleaned_lines).strip("\n")
    
    return result

def walk_and_format(node):
    """Recursively walk the data structure and apply formatting to strings."""
    changed = False
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, str):
                cleaned = clean_string(v)
                # Check if it should be a block scalar
                is_block = len(cleaned) > 80 or '\n' in cleaned
                
                # Check if style actually needs changing or content changed
                # ruamel's LiteralScalarString doesn't easily compare with standard str for type
                current_is_block = isinstance(v, LiteralScalarString)
                
                if cleaned != v or is_block != current_is_block:
                    if is_block:
                        node[k] = LiteralScalarString(cleaned)
                    else:
                        node[k] = cleaned
                    changed = True
            else:
                if walk_and_format(v):
                    changed = True
    elif isinstance(node, list):
        for i in range(len(node)):
            v = node[i]
            if isinstance(v, str):
                cleaned = clean_string(v)
                is_block = len(cleaned) > 80 or '\n' in cleaned
                current_is_block = isinstance(v, LiteralScalarString)
                
                if cleaned != v or is_block != current_is_block:
                    if is_block:
                        node[i] = LiteralScalarString(cleaned)
                    else:
                        node[i] = cleaned
                    changed = True
            else:
                if walk_and_format(v):
                    changed = True
    return changed

def clear_comments(node):
    """Recursively clear comments and extra vertical whitespace."""
    if hasattr(node, 'ca'):
        node.ca.items.clear()
    if isinstance(node, dict):
        for k, v in node.items():
            clear_comments(v)
    elif isinstance(node, list):
        for item in node:
            clear_comments(item)

def process_file(file_path, dry_run=False):
    print(f"Processing {file_path}...")
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.allow_unicode = True
    yaml.width = 1000
    yaml.indent(mapping=2, sequence=4, offset=2)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
            f.seek(0)
            data = yaml.load(f)
            
        if data is None:
            print(f"  [!] File is empty: {file_path}")
            return

        # Clear vertical space/comments and format strings
        clear_comments(data)
        walk_and_format(data)
        
        # Dump to string to compare
        output = StringIO()
        yaml.dump(data, output)
        new_content = output.getvalue()
        
        if original_content != new_content:
            if dry_run:
                print(f"  [DRY RUN] Changes detected in {file_path}:")
                diff = difflib.unified_diff(
                    original_content.splitlines(keepends=True),
                    new_content.splitlines(keepends=True),
                    fromfile='original',
                    tofile='formatted'
                )
                sys.stdout.writelines(diff)
            else:
                # Create backup with microepoch
                microepoch = int(time.time() * 1000000)
                backup_path = f"{file_path}.{microepoch}.bak"
                shutil.copy2(file_path, backup_path)
                print(f"  [BACKUP] Created backup: {backup_path}")

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  [OK] Successfully formatted.")
        else:
            print(f"  [OK] No changes needed.")
            
    except Exception as e:
        print(f"  [ERROR] Failed to process {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Formatter for YAML data sources")
    parser.add_argument("files", nargs="+", help="Files to format (can be paths or just filenames like 'skills')")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without applying them")
    
    args = parser.parse_args()
    
    data_dir = 'data_sources'
    
    for file_input in args.files:
        target_path = file_input
        
        # Convenience: check for file in data_sources if not found directly
        if not os.path.exists(target_path):
            potential_paths = [
                os.path.join(data_dir, file_input),
                os.path.join(data_dir, f"{file_input}.yaml"),
                f"{file_input}.yaml"
            ]
            for p in potential_paths:
                if os.path.exists(p):
                    target_path = p
                    break
        
        if os.path.exists(target_path) and os.path.isfile(target_path):
            process_file(target_path, dry_run=args.dry_run)
        else:
            print(f"File not found or is not a file: {file_input}")

if __name__ == "__main__":
    main()
