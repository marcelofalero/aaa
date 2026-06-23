import re

with open('scratch/warships_layout.txt') as f:
    lines = [l.rstrip() for l in f.readlines()]

tables = {}
current_table = None

for i, line in enumerate(lines):
    if re.match(r'^\s*Table 5-\d+[a-z]?:\s+([^\.]+)$', line):
        current_table = line.strip()
        tables[current_table] = []
        # get next 30 lines
        for j in range(i+1, min(i+40, len(lines))):
            s = lines[j].strip()
            if not s: continue
            if re.match(r'^\s*Table \d+-', lines[j]) or lines[j].startswith('\x0c') or s.startswith('Chapter') or s.startswith('CHAPTER'):
                break
            tables[current_table].append(s)

for k, v in list(tables.items())[:3]:
    print(k)
    for row in v:
        print("  ", re.split(r'\s{2,}', row))
