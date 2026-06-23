import re

with open('scratch/warships_layout.txt') as f:
    lines = [l.rstrip() for l in f.readlines()]

tables = {}
current_table = None

for i, line in enumerate(lines):
    if re.search(r'Table 5[-–]\d+[a-z]?(:| )', line) and not re.search(r'\.\s+\d+$', line) and not re.search(r'\. \. \. ', line):
        current_table = re.search(r'Table 5[-–]\d+[a-z]?[^\n]*', line).group(0).strip()
        tables[current_table] = []
        for j in range(i+1, min(i+100, len(lines))):
            s = lines[j].strip()
            if not s: continue
            if re.match(r'^\s*Table \d+-', lines[j]) or lines[j].startswith('\x0c') or s.startswith('Chapter') or s.startswith('CHAPTER'):
                break
            if re.search(r'Table 5[-–]\d+[a-z]?(:| )', lines[j]):
                break
            tables[current_table].append(s)

with open('scratch/markdown_tables.md', 'w') as f:
    for k, v in tables.items():
        if not v:
            continue
        
        table_title = k
        if 'Part 2' in k or 'Part 3' in k:
            table_title = ''
        elif table_title:
            f.write(f"### {table_title}\n\n")
            
        header_idx = 0
        for i, row in enumerate(v):
            if len(re.split(r'\s{2,}', row)) > 1:
                header_idx = i
                break
        
        headers = re.split(r'\s{2,}', v[header_idx])
        headers = [h.replace('hero', 'character').replace('Hero', 'Character') for h in headers]
        
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("|" + "|".join(["---"] * len(headers)) + "|\n")
        
        for row in v[header_idx+1:]:
            cols = re.split(r'\s{2,}', row)
            if len(cols) == 1:
                continue
            cols = [c.replace('hero', 'character').replace('Hero', 'Character') for c in cols]
            f.write("| " + " | ".join(cols) + " |\n")
        f.write("\n")
