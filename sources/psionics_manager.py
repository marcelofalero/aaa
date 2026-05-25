import os
import sys
import re
import argparse
from pathlib import Path
from ruamel.yaml import YAML

def find_project_root():
    current = Path.cwd().resolve()
    for parent in [current] + list(current.parents):
        marker = parent / '.alternity_root'
        if marker.exists():
            return parent
    return Path.cwd().resolve()

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
    'Biokinesis': 'biokinesis',
    'ESP': 'esp',
    'Psychoportation': 'psychoportation',
    'Telekinesis': 'telekinesis',
    'Telepathy': 'telepathy'
}
REVERSE_MAPPING = {v: k for k, v in FOLDER_MAPPING.items()}

def clean_text(text):
    if text is None: return ""
    text = text.replace('\r\n', '\n').replace("''", "'")
    for pattern, replacement in REPLACEMENTS.items():
        text = re.sub(pattern, replacement, text)
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
        f.write(f"---\n{frontmatter}\n---\n\n{content.strip()}")

def cmd_push(args):
    yaml_engine = get_yaml_engine()
    with open(args.yaml, 'r', encoding='utf-8') as f:
        data = yaml_engine.load(f)
    if 'items' not in data: data['items'] = {}
    
    psionics_path = Path(args.psionics_dir)
    changes = 0
    
    for broad_folder in sorted(psionics_path.iterdir()):
        if not broad_folder.is_dir(): continue
        folder_name = broad_folder.name
        broad_key = REVERSE_MAPPING.get(folder_name, folder_name)
        
        if broad_key not in data['items']:
            data['items'][broad_key] = {
                'localized': [
                    {'en': {'name': folder_name, 'description': ''}},
                    {'es': {'name': '', 'description': ''}}
                ],
                'items': {}
            }
            print(f"[NEW BROAD] {broad_key}")
            changes += 1

        # Track active specialty stem names on disk
        active_specs = set()
        for p_file in sorted(broad_folder.glob("*.md")):
            name = p_file.stem
            if not name.startswith('_'):
                active_specs.add(name)

        # 1. Delete specialties in YAML that are missing from disk
        if 'items' not in data['items'][broad_key]:
            data['items'][broad_key]['items'] = {}
            
        yaml_specs = list(data['items'][broad_key]['items'].keys())
        for spec_key in yaml_specs:
            if spec_key not in active_specs:
                print(f"[DELETE SPEC] {broad_key}/{spec_key}")
                del data['items'][broad_key]['items'][spec_key]
                changes += 1

        # 2. Process all markdown files on disk
        for p_file in sorted(broad_folder.glob("*.md")):
            name = p_file.stem
            metadata, raw_desc = parse_file(p_file)
            
            if name.startswith('_'):
                target = data['items'][broad_key]
            else:
                # If it's a new specialty, initialize it in YAML first
                if name not in data['items'][broad_key]['items']:
                    new_spec = {
                        'attribute': metadata.get('attribute', data['items'][broad_key].get('attribute', 'WIL')),
                        'cost': int(metadata.get('cost', 3)),
                        'url': metadata.get('url', f"/psionics/{folder_name}/#{name}"),
                        'trained_only': bool(metadata.get('trained_only', False)),
                        'localized': [
                            {'en': {
                                'name': metadata.get('name', name.replace('-', ' ').title()),
                                'description': ''
                            }},
                            {'es': {
                                'name': '',
                                'description': ''
                            }}
                        ]
                    }
                    if 'rank_benefits' in metadata:
                        new_spec['rank_benefits'] = metadata['rank_benefits']
                    if 'extended_duration' in metadata:
                        new_spec['extended_duration'] = bool(metadata['extended_duration'])
                    if 'alien_only' in metadata:
                        new_spec['alien_only'] = bool(metadata['alien_only'])
                        
                    data['items'][broad_key]['items'][name] = new_spec
                    print(f"[NEW SPEC] {broad_key}/{name}")
                    changes += 1
                
                target = data['items'][broad_key]['items'][name]

            # Update Metadata (All keys except 'name' and 'localized')
            for k, val in metadata.items():
                if k in ['name', 'localized']: continue
                if k in target:
                    target_val = target[k]
                    if isinstance(target_val, int) and isinstance(val, str):
                        try: val = int(val)
                        except ValueError: pass
                    elif isinstance(target_val, str) and isinstance(val, int):
                        val = str(val)
                
                if target.get(k) != val:
                    print(f"[UPDATE META] {broad_key}{'' if name.startswith('_') else '/' + name} ({k}: {target.get(k)} -> {val})")
                    target[k] = val
                    changes += 1

            # Update Description and Name
            en_loc = next((loc['en'] for loc in target['localized'] if 'en' in loc), None)
            es_loc = next((loc['es'] for loc in target['localized'] if 'es' in loc), None)

            if en_loc:
                if 'name' in metadata and en_loc.get('name') != metadata['name']:
                    print(f"[UPDATE NAME] {broad_key}{'' if name.startswith('_') else '/' + name} ({en_loc.get('name')} -> {metadata['name']})")
                    en_loc['name'] = metadata['name']
                    if es_loc:
                        es_loc['name'] = ""
                    changes += 1

                if clean_text(en_loc.get('description')) != clean_text(raw_desc):
                    en_loc['description'] = raw_desc
                    if es_loc:
                        es_loc['description'] = "" # Clear to trigger translation
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
    psionics_path = Path(args.psionics_dir)
    for broad_folder in sorted(psionics_path.iterdir()):
        if not broad_folder.is_dir(): continue
        folder_name = broad_folder.name
        broad_key = REVERSE_MAPPING.get(folder_name, folder_name)
        if broad_key not in data['items']: continue
        for p_file in sorted(broad_folder.glob("*.md")):
            metadata, file_raw = parse_file(p_file)
            name = p_file.stem
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

            if 'name' in metadata and en_loc.get('name') != metadata['name']:
                print(f"[DIFF NAME] {broad_key}{'' if name.startswith('_') else '/' + name} ({en_loc.get('name')} -> {metadata['name']})")
                diff_found = True

            for k, v in metadata.items():
                if k != 'name':
                    target_val = target.get(k)
                    if isinstance(target_val, int) and isinstance(v, str):
                        try: v = int(v)
                        except ValueError: pass
                    if target_val != v:
                        print(f"[DIFF META] {broad_key}{'' if name.startswith('_') else '/' + name} ({k}: {target_val} -> {v})")
                        diff_found = True
            if diff_found and args.verbose:
                print(f"    YAML (Cleaned): {yaml_text[:80]}...")
                print(f"    FILE (Cleaned): {file_text[:80]}...")

if __name__ == "__main__":
    root_dir = find_project_root()
    default_yaml = str(root_dir / "sources/data_sources/psionics.yaml")
    default_psionics_dir = str(root_dir / "sources/psionics")

    parser = argparse.ArgumentParser(description="Alternity Psionics Manager")
    subparsers = parser.add_subparsers(dest="command")
    
    p_push = subparsers.add_parser("push", help="Push files TO YAML")
    p_push.add_argument("--yaml", default=default_yaml)
    p_push.add_argument("--psionics-dir", default=default_psionics_dir)
    p_push.add_argument("--commit", action="store_true")
    
    p_pull = subparsers.add_parser("pull", help="Pull YAML TO files")
    p_pull.add_argument("--yaml", default=default_yaml)
    p_pull.add_argument("--output", default=default_psionics_dir)
    p_pull.add_argument("--overwrite", action="store_true")
    
    p_diff = subparsers.add_parser("diff", help="Compare files with YAML")
    p_diff.add_argument("--yaml", default=default_yaml)
    p_diff.add_argument("--psionics-dir", default=default_psionics_dir)
    p_diff.add_argument("-v", "--verbose", action="store_true")
    
    args = parser.parse_args()
    if args.command == "push": cmd_push(args)
    elif args.command == "pull": cmd_pull(args)
    elif args.command == "diff": cmd_diff(args)
    else: parser.print_help()
