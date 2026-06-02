#!/usr/bin/env python3
"""
Unified Data Manager — YAML ↔ Markdown review for all data domains.

Usage:
    data-manager <domain> pull [--overwrite]
    data-manager <domain> push [--commit]
    data-manager <domain> diff [-v]

Domains: skill, psionics, gear, armor, weapons, goods, services, computers, cybernetics
"""

import os
import re
import argparse
from dataclasses import dataclass, field
from pathlib import Path
from io import StringIO
from typing import Optional

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString


# ---------------------------------------------------------------------------
# Project root detection
# ---------------------------------------------------------------------------

def find_project_root():
    """Walk up from cwd until we find the .project_root marker file."""
    current = Path.cwd().resolve()
    for parent in [current] + list(current.parents):
        if (parent / '.project_root').exists():
            return parent
    return Path.cwd().resolve()


# ---------------------------------------------------------------------------
# Terminology & character normalization
# ---------------------------------------------------------------------------

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


def clean_text(text):
    """Normalize text for comparison (ignoring whitespace and smart quotes)."""
    if text is None:
        return ""
    text = text.replace('\r\n', '\n').replace("''", "'")
    for pattern, replacement in REPLACEMENTS.items():
        text = re.sub(pattern, replacement, text)
    lines = [line.strip() for line in text.split('\n')]
    text = ' '.join([l for l in lines if l])
    return ' '.join(text.split())


# ---------------------------------------------------------------------------
# YAML helpers
# ---------------------------------------------------------------------------

def get_yaml_engine():
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    return yaml


def parse_file(path):
    """Read a Markdown file with YAML frontmatter. Returns (metadata_dict, body_text)."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            yaml = get_yaml_engine()
            metadata = yaml.load(parts[1]) or {}
            return metadata, parts[2].strip()
    return {}, content.strip()


def save_file_with_frontmatter(path, metadata, content, overwrite, trailing_newline=False):
    """Write a Markdown file with YAML frontmatter. Skips if file exists and not overwrite."""
    if path.exists() and not overwrite:
        return
    yaml = get_yaml_engine()
    stream = StringIO()
    yaml.dump(metadata, stream)
    frontmatter = stream.getvalue().strip()
    newline = '\n' if trailing_newline else ''
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"---\n{frontmatter}\n---\n\n{content.strip()}{newline}")


# ---------------------------------------------------------------------------
# Domain configuration
# ---------------------------------------------------------------------------

@dataclass
class DomainConfig:
    """Configuration for a single data domain."""
    # Identity
    name: str                     # e.g. "skill", "psionics", "gear"
    label_broad: str              # e.g. "skill", "discipline", "category"
    label_item: str               # e.g. "specialty", "power", "item"

    # Paths
    yaml_path: str                # Default path to YAML data source
    review_dir: str               # Default review directory

    # Folder name mapping (broad_key → folder_name)
    # Empty dict = direct mapping (folder_name == broad_key)
    folder_mapping: dict = field(default_factory=dict)

    # Metadata handling
    # None = accept all keys except internal ones ('name', 'localized')
    # list = whitelist of keys to sync
    metadata_keys: Optional[list] = None

    # Type coercions for metadata values: {key: callable}
    # e.g. {'cost': int, 'pl': str}
    type_coercions: dict = field(default_factory=dict)

    # Auto-create/delete items on push (psionics creates/deletes powers)
    auto_create: bool = False
    auto_delete: bool = False

    # Write trailing newline (gear uses this)
    trailing_newline: bool = False

    # Extra nesting level for top-level type grouping (e.g. weapons: melee, ranged)
    # When set, iterates over these keys instead of root 'items'
    type_keys: Optional[list] = None

    # Root-level broad items (e.g. goods_and_services with categories at root)
    # Category keys are looked up via category_map when iterating disk
    root_level_broad: bool = False
    skip_keys: list = field(default_factory=list)  # Top-level keys to skip
    include_categories: Optional[list] = None  # If set, only these top-level categories
    category_map: dict = field(default_factory=dict)  # {folder_name: category_key}


# ---------------------------------------------------------------------------
# Reverse mapping helper
# ---------------------------------------------------------------------------

def _reverse_mapping(config):
    """Build folder_name → broad_key mapping from config.folder_mapping (or identity)."""
    if config.folder_mapping:
        return {v: k for k, v in config.folder_mapping.items()}
    return {}


def _broad_key(config, folder_name):
    """Convert folder name to YAML broad key using reverse mapping or identity."""
    rev = _reverse_mapping(config)
    return rev.get(folder_name, folder_name)


def _folder_name(config, broad_key):
    """Convert YAML broad key to folder name using mapping or identity."""
    return config.folder_mapping.get(broad_key, broad_key)


# ---------------------------------------------------------------------------
# Folder iteration helpers (handles type_keys nesting like weapons)
# ---------------------------------------------------------------------------

def _iter_broad_folders(config, review_path, data):
    """Yield (broad_key, broad_folder_path, parent_dict) for each broad item folder on disk.

    parent_dict is the dict that contains this broad item in the YAML data
    (e.g. data['items'] for standard, data[type_key]['items'] for type_key domains,
     data[category_key]['items'] for root_level_broad domains).
    """
    if config.root_level_broad:
        for broad_folder in sorted(review_path.iterdir()):
            if not broad_folder.is_dir() or broad_folder.name.startswith('.'):
                continue
            bk = broad_folder.name  # folder name IS the broad key
            category_key = config.category_map.get(bk, bk)
            if category_key not in data or category_key in config.skip_keys:
                continue
            if config.include_categories is not None and category_key not in config.include_categories:
                continue
            parent_dict = data[category_key].setdefault('items', {})
            yield bk, broad_folder, parent_dict
    elif config.type_keys:
        for type_folder in sorted(review_path.iterdir()):
            if not type_folder.is_dir() or type_folder.name.startswith('.'):
                continue
            type_key = type_folder.name
            if type_key not in data:
                data[type_key] = {}
            parent = data[type_key].setdefault('items', {})
            for pl_folder in sorted(type_folder.iterdir()):
                if not pl_folder.is_dir() or pl_folder.name.startswith('.'):
                    continue
                broad_key = _broad_key(config, pl_folder.name)
                yield broad_key, pl_folder, parent
    else:
        parent = data.setdefault('items', {})
        for broad_folder in sorted(review_path.iterdir()):
            if not broad_folder.is_dir() or broad_folder.name.startswith('.'):
                continue
            broad_key = _broad_key(config, broad_folder.name)
            yield broad_key, broad_folder, parent


# ---------------------------------------------------------------------------
# Pull: YAML → Markdown
# ---------------------------------------------------------------------------

def cmd_pull(config, args):
    """Generate Markdown review files from YAML data source."""
    yaml_engine = get_yaml_engine()
    with open(args.yaml, 'r', encoding='utf-8') as f:
        data = yaml_engine.load(f)

    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)

    # Build list of (broad_key, broad_val, broad_folder) from YAML, handling type_keys or root_level_broad
    pull_entries = []
    if config.root_level_broad:
        for category_key in data:
            if category_key in config.skip_keys:
                continue
            if config.include_categories is not None and category_key not in config.include_categories:
                continue
            for bk, bv in data[category_key].get('items', {}).items():
                pull_entries.append((bk, bv, output_path / bk))
    elif config.type_keys:
        for type_key in config.type_keys:
            type_data = data.get(type_key, {})
            for bk, bv in type_data.get('items', {}).items():
                folder = _folder_name(config, bk)
                pull_entries.append((bk, bv, output_path / type_key / folder))
    else:
        for bk, bv in data.get('items', {}).items():
            folder = _folder_name(config, bk)
            pull_entries.append((bk, bv, output_path / folder))

    for broad_key, broad_val, broad_folder in pull_entries:
        broad_folder.mkdir(parents=True, exist_ok=True)
        try:
            # Broad item (e.g. broad skill, discipline, PL category)
            meta = {k: v for k, v in broad_val.items() if k not in ['items', 'localized']}
            en_loc = next((loc['en'] for loc in broad_val['localized'] if 'en' in loc), {})
            meta['name'] = en_loc.get('name', broad_key)
            desc = en_loc.get('description', '')
            save_file_with_frontmatter(
                broad_folder / f"_{broad_folder.name}.md", meta, desc, args.overwrite,
                trailing_newline=config.trailing_newline,
            )

            # Sub-items (specialties, powers, gear/armor/weapon items)
            for item_key, item_val in broad_val.get('items', {}).items():
                s_meta = {k: v for k, v in item_val.items() if k not in ['localized']}
                s_en_loc = next((loc['en'] for loc in item_val['localized'] if 'en' in loc), {})
                s_meta['name'] = s_en_loc.get('name', item_key)
                s_desc = s_en_loc.get('description', '')
                save_file_with_frontmatter(
                    broad_folder / f"{item_key}.md", s_meta, s_desc, args.overwrite,
                    trailing_newline=config.trailing_newline,
                )
        except (KeyError, StopIteration):
            pass


# ---------------------------------------------------------------------------
# Push: Markdown → YAML
# ---------------------------------------------------------------------------

def cmd_push(config, args):
    """Apply Markdown review edits back to YAML data source. Clears Spanish to trigger re-translation."""
    yaml_engine = get_yaml_engine()
    with open(args.yaml, 'r', encoding='utf-8') as f:
        data = yaml_engine.load(f)

    review_path = Path(args.dir)
    changes = 0

    for broad_key, broad_folder, parent_dict in _iter_broad_folders(config, review_path, data):
        # Auto-create broad item if it doesn't exist
        if broad_key not in parent_dict:
            if config.auto_create:
                parent_dict[broad_key] = {
                    'localized': [
                        {'en': {'name': broad_folder.name, 'description': ''}},
                        {'es': {'name': '', 'description': ''}},
                    ],
                    'items': {},
                }
                print(f"[NEW BROAD] {broad_key}")
                changes += 1
            else:
                continue

        # Track active item names on disk (for auto-delete)
        if config.auto_delete:
            active_items = set()
            for md_file in sorted(broad_folder.glob("*.md")):
                if not md_file.stem.startswith('_'):
                    active_items.add(md_file.stem)

            # Delete YAML items that no longer exist on disk
            yaml_items = list(parent_dict[broad_key].get('items', {}).keys())
            for item_key in yaml_items:
                if item_key not in active_items:
                    print(f"[DELETE {config.label_item.upper()}] {broad_key}/{item_key}")
                    del parent_dict[broad_key]['items'][item_key]
                    changes += 1

        # Process all markdown files
        for md_file in sorted(broad_folder.glob("*.md")):
            name = md_file.stem
            metadata, raw_desc = parse_file(md_file)

            if name.startswith('_'):
                target = parent_dict[broad_key]
            else:
                # Auto-create new item if needed and configured
                if name not in parent_dict[broad_key].get('items', {}):
                    if config.auto_create:
                        # Build sensible defaults
                        new_item = {
                            'attribute': metadata.get('attribute', parent_dict[broad_key].get('attribute', 'WIL')),
                            'cost': int(metadata.get('cost', 3)),
                            'url': metadata.get('url', f"/{config.name}/{broad_folder.name}/#{name}"),
                            'trained_only': bool(metadata.get('trained_only', False)),
                            'localized': [
                                {'en': {'name': metadata.get('name', name.replace('-', ' ').title()), 'description': ''}},
                                {'es': {'name': '', 'description': ''}},
                            ],
                        }
                        # Copy over any extras from metadata
                        for extra_key in ['rank_benefits', 'extended_duration', 'alien_only']:
                            if extra_key in metadata:
                                new_item[extra_key] = metadata[extra_key]
                        parent_dict[broad_key]['items'][name] = new_item
                        print(f"[NEW {config.label_item.upper()}] {broad_key}/{name}")
                        changes += 1
                    else:
                        continue

                # Ensure 'items' dict exists
                if 'items' not in parent_dict[broad_key]:
                    parent_dict[broad_key]['items'] = {}
                target = parent_dict[broad_key]['items'][name]

            # --- Update metadata ---
            if config.metadata_keys is not None:
                # Whitelist approach
                for k in config.metadata_keys:
                    if k in metadata and target.get(k) != metadata[k]:
                        print(f"[UPDATE META] {broad_key}{'' if name.startswith('_') else '/' + name} ({k}: {target.get(k)} -> {metadata[k]})")
                        target[k] = metadata[k]
                        changes += 1
            else:
                # Accept all metadata keys except the reserved ones
                for k, val in metadata.items():
                    if k in ('name', 'localized'):
                        continue

                    # Apply type coercion
                    if k in config.type_coercions:
                        try:
                            val = config.type_coercions[k](val)
                        except (ValueError, TypeError):
                            pass
                    # Also coerce to match target type if needed
                    elif k in target:
                        target_val = target[k]
                        if isinstance(target_val, int) and isinstance(val, str):
                            try:
                                val = int(val)
                            except ValueError:
                                pass
                        elif isinstance(target_val, str) and isinstance(val, int):
                            val = str(val)

                    if target.get(k) != val:
                        print(f"[UPDATE META] {broad_key}{'' if name.startswith('_') else '/' + name} ({k}: {target.get(k)} -> {val})")
                        target[k] = val
                        changes += 1

            # --- Update localized name & description ---
            en_loc = next((loc['en'] for loc in target['localized'] if 'en' in loc), None)
            es_loc = next((loc['es'] for loc in target['localized'] if 'es' in loc), None)

            if en_loc:
                # Name
                if 'name' in metadata and en_loc.get('name') != metadata['name']:
                    print(f"[UPDATE NAME] {broad_key}{'' if name.startswith('_') else '/' + name} ({en_loc.get('name')} -> {metadata['name']})")
                    en_loc['name'] = metadata['name']
                    if es_loc:
                        es_loc['name'] = ""
                    changes += 1

                # Description
                if clean_text(en_loc.get('description')) != clean_text(raw_desc):
                    en_loc['description'] = LiteralScalarString(raw_desc) if '\n' in raw_desc else raw_desc
                    if es_loc:
                        es_loc['description'] = ""
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


# ---------------------------------------------------------------------------
# Diff: compare Markdown with YAML
# ---------------------------------------------------------------------------

def cmd_diff(config, args):
    """Show differences between Markdown review files and YAML data source."""
    yaml_engine = get_yaml_engine()
    with open(args.yaml, 'r', encoding='utf-8') as f:
        data = yaml_engine.load(f)

    review_path = Path(args.dir)

    for broad_key, broad_folder, parent_dict in _iter_broad_folders(config, review_path, data):
        if broad_key not in parent_dict:
            continue

        for md_file in sorted(broad_folder.glob("*.md")):
            metadata, file_raw = parse_file(md_file)
            name = md_file.stem

            if name.startswith('_'):
                target = parent_dict[broad_key]
            else:
                if 'items' not in parent_dict[broad_key] or name not in parent_dict[broad_key]['items']:
                    continue
                target = parent_dict[broad_key]['items'][name]

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
                if k == 'name':
                    continue
                target_val = target.get(k)
                # Apply same type coercion logic as push for accurate comparison
                if isinstance(target_val, int) and isinstance(v, str):
                    try:
                        v = int(v)
                    except ValueError:
                        pass
                if target_val != v:
                    print(f"[DIFF META] {broad_key}{'' if name.startswith('_') else '/' + name} ({k}: {target_val} -> {v})")
                    diff_found = True

            if diff_found and args.verbose:
                print(f"    YAML (Cleaned): {yaml_text[:80]}...")
                print(f"    FILE (Cleaned): {file_text[:80]}...")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_cli(configs):
    """Build argument parser with nested subcommands for each domain."""
    parser = argparse.ArgumentParser(description="Unified Data Manager — YAML ↔ Markdown review")
    subparsers = parser.add_subparsers(dest="domain", help="Data domain to manage")

    for domain_name, cfg in configs.items():
        domain_parser = subparsers.add_parser(domain_name, help=f"Manage {domain_name} data")
        domain_sub = domain_parser.add_subparsers(dest="command", help=f"{domain_name} command")

        # pull: YAML → Markdown
        p_pull = domain_sub.add_parser("pull", help=f"Pull YAML to Markdown review files ({cfg.label_broad}s → {cfg.review_dir})")
        p_pull.add_argument("--yaml", default=cfg.yaml_path, help=f"Path to {domain_name} YAML (default: {cfg.yaml_path})")
        p_pull.add_argument("--output", default=cfg.review_dir, help=f"Output directory for review files (default: {cfg.review_dir})")
        p_pull.add_argument("--overwrite", action="store_true", help="Overwrite existing review files")

        # push: Markdown → YAML
        p_push = domain_sub.add_parser("push", help=f"Push Markdown edits back to YAML")
        p_push.add_argument("--yaml", default=cfg.yaml_path, help=f"Path to {domain_name} YAML (default: {cfg.yaml_path})")
        p_push.add_argument("--dir", default=cfg.review_dir, help=f"Review directory to push from (default: {cfg.review_dir})")
        p_push.add_argument("--commit", action="store_true", help="Actually write changes (dry-run without this flag)")

        # diff: compare
        p_diff = domain_sub.add_parser("diff", help=f"Compare Markdown review files with YAML")
        p_diff.add_argument("--yaml", default=cfg.yaml_path, help=f"Path to {domain_name} YAML (default: {cfg.yaml_path})")
        p_diff.add_argument("--dir", default=cfg.review_dir, help=f"Review directory to compare (default: {cfg.review_dir})")
        p_diff.add_argument("-v", "--verbose", action="store_true", help="Show cleaned text preview for content diffs")

    return parser


def main():
    root_dir = find_project_root()

    # ---- Domain configurations ----
    DOMAINS = {
        'skill': DomainConfig(
            name='skill',
            label_broad='skill',
            label_item='specialty',
            yaml_path=str(root_dir / 'sources/data_sources/skills.yaml'),
            review_dir=str(root_dir / 'sources/skills'),
            folder_mapping={},
            metadata_keys=['attribute', 'cost', 'url', 'category', 'trained_only', 'untrained', 'rank_benefits'],
            auto_delete=True,
        ),

        'psionics': DomainConfig(
            name='psionics',
            label_broad='discipline',
            label_item='power',
            yaml_path=str(root_dir / 'sources/data_sources/psionics.yaml'),
            review_dir=str(root_dir / 'sources/psionics'),
            folder_mapping={
                'Biokinesis': 'biokinesis',
                'ESP': 'esp',
                'Psychoportation': 'psychoportation',
                'Telekinesis': 'telekinesis',
                'Telepathy': 'telepathy',
            },
            metadata_keys=None,
            auto_create=True,
            auto_delete=True,
            type_coercions={'cost': int},
        ),

        'gear': DomainConfig(
            name='gear',
            label_broad='gear category',
            label_item='item',
            yaml_path=str(root_dir / 'sources/data_sources/survival_gear.yaml'),
            review_dir=str(root_dir / 'sources/survival-gear'),
            folder_mapping={
                'pl-7-survival-gear': 'stardrive',
            },
            metadata_keys=None,
            type_coercions={'pl': str, 'cost': str},
            trailing_newline=True,
        ),

        'armor': DomainConfig(
            name='armor',
            label_broad='PL category',
            label_item='armor',
            yaml_path=str(root_dir / 'sources/data_sources/armor.yaml'),
            review_dir=str(root_dir / 'sources/armor'),
            folder_mapping={},
            metadata_keys=None,
            trailing_newline=True,
        ),

        'weapons': DomainConfig(
            name='weapons',
            label_broad='PL category',
            label_item='weapon',
            yaml_path=str(root_dir / 'sources/data_sources/weapons.yaml'),
            review_dir=str(root_dir / 'sources/weapons'),
            folder_mapping={},
            type_keys=['melee', 'ranged'],
            metadata_keys=None,
            trailing_newline=True,
        ),

        'goods': DomainConfig(
            name='goods',
            label_broad='goods category',
            label_item='item',
            yaml_path=str(root_dir / 'sources/data_sources/goods_and_services.yaml'),
            review_dir=str(root_dir / 'sources/goods'),
            root_level_broad=True,
            skip_keys=['search_config', 'services'],
            category_map={
                'medical-gear': 'medical_gear',
                'clothing-and-accessories': 'clothing_and_accessories',
                'professional-equipment': 'tools_and_electronics',
                'communications': 'communications',
                'sensors': 'sensors',
                'survival-and-miscellaneous-gear': 'general_gear',
            },
            metadata_keys=None,
            type_coercions={'pl': str, 'cost': str, 'mass': str},
            trailing_newline=True,
        ),

        'services': DomainConfig(
            name='services',
            label_broad='service category',
            label_item='service',
            yaml_path=str(root_dir / 'sources/data_sources/goods_and_services.yaml'),
            review_dir=str(root_dir / 'sources/services'),
            root_level_broad=True,
            skip_keys=['search_config'],
            include_categories=['services'],
            category_map={'services': 'services'},
            metadata_keys=None,
            type_coercions={'pl': str, 'cost': str, 'mass': str},
            trailing_newline=True,
        ),

        'computers': DomainConfig(
            name='computers',
            label_broad='computer category',
            label_item='computer component',
            yaml_path=str(root_dir / 'sources/data_sources/computers.yaml'),
            review_dir=str(root_dir / 'sources/computers'),
            metadata_keys=None,
            type_coercions={'pl': str, 'cost': str, 'mass': str},
            trailing_newline=True,
        ),

        'cybernetics': DomainConfig(
            name='cybernetics',
            label_broad='PL level',
            label_item='cybernetic',
            yaml_path=str(root_dir / 'sources/data_sources/cybernetics.yaml'),
            review_dir=str(root_dir / 'sources/cybernetics'),
            metadata_keys=None,
            type_coercions={'pl': str, 'cost': str, 'mass': str},
            trailing_newline=True,
        ),
    }

    parser = build_cli(DOMAINS)
    args = parser.parse_args()

    if not args.domain:
        parser.print_help()
        return

    config = DOMAINS[args.domain]

    if args.command == 'pull':
        cmd_pull(config, args)
    elif args.command == 'push':
        cmd_push(config, args)
    elif args.command == 'diff':
        cmd_diff(config, args)
    else:
        # Show domain-specific help
        parser.parse_args([args.domain, '--help'])


if __name__ == '__main__':
    main()
