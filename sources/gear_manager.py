import os
import sys
import re
import argparse
from pathlib import Path
from ruamel.yaml import YAML

# Terminology & Character Normalization mapping
REPLACEMENTS = {
    r'\bhero\b': 'character',
    r'\bHero\b': 'Character',
    r'\bheroes\b': 'characters',
    r'\bHeroes\b': 'Characters',
    r'[\u2018\u2019]': "'",
    r'[\u201C\u201D]': '"',
    r'\u2013': '-',
    r'\u2014': '--',
}

# Folder and broad key mapping
FOLDER_MAPPING = {
    'pl-7-survival-gear': 'stardrive'
}
REVERSE_MAPPING = {v: k for k, v in FOLDER_MAPPING.items()}

def clean_text(text):
    if text is None: return ""
    # 1. Standardize line endings and quotes
    text = text.replace('\r\n', '\n').replace("''", "'")
    # 2. Apply terminology and smart quote replacements
    for pattern, replacement in REPLACEMENTS.items():
        text = re.sub(pattern, replacement, text)
    # 3. Aggressive whitespace cleanup for comparison
    lines = [line.strip() for line in text.split('\n')]
    text = ' '.join([l for l in lines if l])
    return ' '.join(text.split()) # Normalize internal spaces

def get_yaml_engine():
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    return yaml

def parse_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            yaml = get_yaml_engine()
            metadata = yaml.load(parts[1]) or {}
            return metadata, parts[2].strip()
    return {}, content.strip()

def save_file_with_frontmatter(path, metadata, content, overwrite):
    if path.exists() and not overwrite: return
    yaml = get_yaml_engine()
    from io import StringIO
    stream = StringIO()
    yaml.dump(metadata, stream)
    frontmatter = stream.getvalue().strip()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"---\n{frontmatter}\n---\n\n{content.strip()}\n")

def cmd_push(args):
    yaml_engine = get_yaml_engine()
    with open(args.yaml, 'r', encoding='utf-8') as f:
        data = yaml_engine.load(f)
    if 'items' not in data: data['items'] = {}
    
    gear_path = Path(args.gear_dir)
    changes = 0
    
    for broad_folder in sorted(gear_path.iterdir()):
        if not broad_folder.is_dir(): continue
        folder_name = broad_folder.name
        broad_key = REVERSE_MAPPING.get(folder_name, folder_name)
        
        for gear_file in sorted(broad_folder.glob("*.md")):
            name = gear_file.stem
            metadata, raw_desc = parse_file(gear_file)
            
            if name.startswith('_'):
                if broad_key not in data['items']: continue
                target = data['items'][broad_key]
            else:
                if broad_key not in data['items'] or 'items' not in data['items'][broad_key]: continue
                if name not in data['items'][broad_key]['items']: continue
                target = data['items'][broad_key]['items'][name]

            # Update Metadata
            for k in metadata:
                if k == 'name': continue
                val = metadata[k]
                if isinstance(val, int) and k in ['pl', 'cost']:
                    val = str(val)
                if target.get(k) != val:
                    print(f"[UPDATE META] {broad_key}{'' if name.startswith('_') else '/' + name} ({k}: {target.get(k)} -> {val})")
                    target[k] = val
                    changes += 1

            # Update Description
            en_loc = next((loc['en'] for loc in target['localized'] if 'en' in loc), None)
            es_loc = next((loc['es'] for loc in target['localized'] if 'es' in loc), None)

            if en_loc and clean_text(en_loc.get('description')) != clean_text(raw_desc):
                en_loc['description'] = raw_desc
                if es_loc:
                    es_loc['description'] = "" # Clear translation to trigger re-translation
                changes += 1
                print(f"[UPDATE DESC] {broad_key}{'' if name.startswith('_') else '/' + name}")

    if changes == 0:
        print("No changes needed. YAML is in sync.")
        return

    if args.commit:
        with open(args.yaml, 'w', encoding='utf-8') as f:
            yaml_engine.dump(data, f)
        print(f"\nCommitted {changes} changes.")
    else:
        print(f"\nDry run: {changes} changes pending. Use --commit to apply.")

def cmd_pull(args):
    yaml_engine = get_yaml_engine()
    with open(args.yaml, 'r', encoding='utf-8') as f:
        data = yaml_engine.load(f)
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    for broad_key, broad_val in data.get('items', {}).items():
        folder_name = FOLDER_MAPPING.get(broad_key, broad_key)
        broad_folder = output_path / folder_name
        broad_folder.mkdir(exist_ok=True)
        try:
            meta = {k: v for k, v in broad_val.items() if k not in ['items', 'localized']}
            en_loc = next((loc['en'] for loc in broad_val['localized'] if 'en' in loc), {})
            meta['name'] = en_loc.get('name', broad_key)
            desc = en_loc.get('description', '')
            save_file_with_frontmatter(broad_folder / f"_{folder_name}.md", meta, desc, args.overwrite)
            for spec_key, spec_val in broad_val.get('items', {}).items():
                s_meta = {k: v for k, v in spec_val.items() if k not in ['localized']}
                s_en_loc = next((loc['en'] for loc in spec_val['localized'] if 'en' in loc), {})
                s_meta['name'] = s_en_loc.get('name', spec_key)
                s_desc = s_en_loc.get('description', '')
                save_file_with_frontmatter(broad_folder / f"{spec_key}.md", s_meta, s_desc, args.overwrite)
        except (KeyError, StopIteration): pass

def cmd_diff(args):
    yaml_engine = get_yaml_engine()
    with open(args.yaml, 'r', encoding='utf-8') as f:
        data = yaml_engine.load(f)
    gear_path = Path(args.gear_dir)
    for broad_folder in sorted(gear_path.iterdir()):
        if not broad_folder.is_dir(): continue
        folder_name = broad_folder.name
        broad_key = REVERSE_MAPPING.get(folder_name, folder_name)
        if broad_key not in data['items']: continue
        for gear_file in sorted(broad_folder.glob("*.md")):
            metadata, file_raw = parse_file(gear_file)
            name = gear_file.stem
            if name.startswith('_'): target = data['items'][broad_key]
            else:
                if 'items' not in data['items'][broad_key] or name not in data['items'][broad_key]['items']: continue
                target = data['items'][broad_key]['items'][name]
            
            en_loc = next((loc['en'] for loc in target['localized'] if 'en' in loc), {})
            yaml_text = clean_text(en_loc.get('description', ''))
            file_text = clean_text(file_raw)
            
            diff_found = False
            if file_text != yaml_text:
                print(f"[DIFF CONTENT] {broad_key}{'' if name.startswith('_') else '/' + name}")
                diff_found = True
            for k, v in metadata.items():
                if k != 'name':
                    target_val = target.get(k)
                    if isinstance(target_val, int) and isinstance(v, str):
                        target_val = str(target_val)
                    if target_val != v:
                        print(f"[DIFF META] {broad_key}{'' if name.startswith('_') else '/' + name} ({k}: {target_val} -> {v})")
                        diff_found = True
            if diff_found and args.verbose:
                print(f"    YAML (Cleaned): {yaml_text[:80]}...")
                print(f"    FILE (Cleaned): {file_text[:80]}...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Alternity Gear Manager")
    subparsers = parser.add_subparsers(dest="command")
    p_push = subparsers.add_parser("push", help="Push files TO YAML")
    p_push.add_argument("--yaml", default="sources/data_sources/survival_gear.yaml")
    p_push.add_argument("--gear-dir", default="sources/survival-gear")
    p_push.add_argument("--commit", action="store_true")
    p_pull = subparsers.add_parser("pull", help="Pull YAML TO files")
    p_pull.add_argument("--yaml", default="sources/data_sources/survival_gear.yaml")
    p_pull.add_argument("--output", default="sources/survival-gear")
    p_pull.add_argument("--overwrite", action="store_true")
    p_diff = subparsers.add_parser("diff", help="Compare files with YAML")
    p_diff.add_argument("--yaml", default="sources/data_sources/survival_gear.yaml")
    p_diff.add_argument("--gear-dir", default="sources/survival-gear")
    p_diff.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    if args.command == "push": cmd_push(args)
    elif args.command == "pull": cmd_pull(args)
    elif args.command == "diff": cmd_diff(args)
    else: parser.print_help()
