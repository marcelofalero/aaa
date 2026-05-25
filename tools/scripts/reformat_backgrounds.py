#!/usr/bin/env python3
import sys
import re
from pathlib import Path
from ruamel.yaml import YAML

def format_string(val):
    if not isinstance(val, str):
        return val
    
    if '<br>' in val or '<br/>' in val or '<br />' in val:
        parts = re.split(r'\s*<br\s*/?>\s*', val)
        is_list = all(p.startswith('[') or p.startswith('**') or p.startswith('-') for p in parts if p.strip())
        if is_list:
            return '\n'.join(f"- {p.strip()}" for p in parts if p.strip())
        else:
            return '\n\n'.join(p.strip() for p in parts if p.strip())
    
    return val

def process_node(node):
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, str):
                node[k] = format_string(v)
            else:
                process_node(v)
    elif isinstance(node, list):
        for i in range(len(node)):
            if isinstance(node[i], str):
                node[i] = format_string(node[i])
            else:
                process_node(node[i])

def main():
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096  # Avoid wrapping lines
    
    filepath = Path(__file__).parent.parent / 'data_sources' / 'backgrounds.yaml'
    if not filepath.exists():
        print(f"File not found: {filepath}")
        sys.exit(1)
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.load(f)
        
    process_node(data)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)
        
    print(f"Successfully Reformatted: {filepath}")

if __name__ == '__main__':
    main()
