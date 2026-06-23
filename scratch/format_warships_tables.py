import re

print("Parsing warships_layout.txt...")
with open('scratch/warships_layout.txt') as f:
    lines = [l.rstrip() for l in f.readlines()]

parsed_tables = {}
current_table = None

for i, line in enumerate(lines):
    if re.search(r'Table 5[-–]\d+[a-z]?(:| )', line) and not re.search(r'\.\s+\d+$', line) and not re.search(r'\. \. \. ', line):
        current_table = re.search(r'Table 5[-–]\d+[a-z]?[^\n]*', line).group(0).strip()
        parsed_tables[current_table] = []
        for j in range(i+1, min(i+100, len(lines))):
            s = lines[j].strip()
            if not s: continue
            if re.match(r'^\s*Table \d+-', lines[j]) or lines[j].startswith('\x0c') or s.startswith('Chapter') or s.startswith('CHAPTER'):
                break
            if re.search(r'Table 5[-–]\d+[a-z]?(:| )', lines[j]):
                break
            parsed_tables[current_table].append(s)

tables = {}
for k, v in parsed_tables.items():
    if not v:
        continue
    
    table_title = k
    if 'Part 2' in k or 'Part 3' in k:
        table_title = ''
        
    key = re.match(r'Table 5[-–]\d+[a-z]?', k).group(0).replace('–', '-')
    
    if key == 'Table 5-1a' or key == 'Table 5-1b':
        key_main = 'Table 5-1'
        if key_main not in tables:
            tables[key_main] = ""
        tables[key_main] += f"### {k}\n\n"
    elif key == 'Table 5-10':
        if key not in tables:
            tables[key] = ""
        if table_title: tables[key] += f"### {table_title}\n\n"
    elif key == 'Table 5-14a':
        tables['Table 5-14a'] = f"### {table_title}\n\n"
    else:
        tables[key] = f"### {table_title}\n\n"
        
    header_idx = 0
    for i, row in enumerate(v):
        if len(re.split(r'\s{2,}', row)) > 1:
            header_idx = i
            break
            
    headers = re.split(r'\s{2,}', v[header_idx])
    headers = [h.replace('hero', 'character').replace('Hero', 'Character') for h in headers]
    
    t_str = "| " + " | ".join(headers) + " |\n"
    t_str += "|" + "|".join(["---"] * len(headers)) + "|\n"
    
    for row in v[header_idx+1:]:
        cols = re.split(r'\s{2,}', row)
        if len(cols) == 1:
            continue
        cols = [c.replace('hero', 'character').replace('Hero', 'Character') for c in cols]
        t_str += "| " + " | ".join(cols) + " |\n"
    
    if key == 'Table 5-1a' or key == 'Table 5-1b':
        tables['Table 5-1'] += t_str + "\n"
    else:
        tables[key] += t_str + "\n"

# Add Table 5-7 manually
tables['Table 5-7'] = """### Table 5-7: Hull Point Costs for Fixed Mounts and Turrets

| Standard | Fixed | Turret |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 3 |
| 3 | 2 | 4 |
| 4 | 3 | 5 |

"""

with open('site/content/warships/ship-construction.md', 'r') as f:
    content = f.read()

bounds = [
    ("Table 5-1a: Military Hulls", "$400 M $1000 M\n", "Table 5-1"),
    ("Table 5-2: Armor", "$250 K $500 K $500 K $1 M $2 M $4 M\n", "Table 5-2"),
    ("Table 5-3: Power Plants", "6.0\n\n$10 M\n\n$500 K\n\nNo\n\n-\n\n-\n", "Table 5-3"),
    ("Table 5-4: Engines", "2.0\n\n$2 M\n\n$200 K\n\n-\n\n-\n", "Table 5-4"),
    ("Table 5-5: FTL Drives", "X\n\n20\n\n10%\n\n$5 M\n", "Table 5-5"),
    ("Table 5-6: Support Systems", "1\n\n-\n\n$2 M\n", "Table 5-6"),
    ("Table 5–7: Hull Point Costs for Fixed Mounts and Turrets", "Standard Fixed Turret\n", "Table 5-7"),
    ("Table 5-8: Beam Weapons", "A\n\nF\n\nQ\n\n-\n\nA\n\nF\n\n1\n\n2\n\n2\n\n1\n\n2\n\n3\n", "Table 5-8"),
    ("Table 5-9: Projectile Weapons", "Q\n\nG\n\n5\n\n10\n", "Table 5-9"),
    ("Table 5-10: Missiles, Bombs, and Mines (Part 1)", "Plasma Missile Rack\n", "Table 5-10"),
    ("Table 5-11: Area Effect Weapons", "Null torpedo Null bomb\n", "Table 5-11"),
    ("Table 5-12: Torpedoes and Special Weapons", "$150 K +1\n", "Table 5-12"),
    ("Table 5-13: Defensive Systems", "Defense Network\n", "Table 5-13"),
    ("Table 5-14: Command, Control, and Communication Systems", "Ansible\n", "Table 5-14"),
    ("Table 5-14a: Computers", "Nav Control, Amazing\n", "Table 5-14a"),
    ("Table 5-15: Sensors", "Drive Detection Array\n", "Table 5-15"),
    ("Table 5-16: Tracking Capability", "PL\n", "Table 5-16"),
    ("Table 5-17: Hangars and Miscellaneous Installations", "$100 K $500 K\n", "Table 5-17"),
    ("Table 5-18: Hit Locations and Zone Limits", "## Step 11: Hangars and Small Craft", "Table 5-18"),
]

for start_str, end_str, key in reversed(bounds):
    start_idx = content.find(start_str)
    if start_idx == -1:
        print(f"Error: Could not find start for {key}")
        continue
    
    end_idx = content.find(end_str, start_idx)
    if end_idx == -1:
        print(f"Error: Could not find end for {key}")
        continue
        
    if "Step 11" in end_str:
        # Don't delete Step 11
        pass
    else:
        end_idx += len(end_str)
        
    if key not in tables:
        print(f"Error: Key {key} not found in tables!")
        continue
        
    content = content[:start_idx] + tables[key] + "\n\n" + content[end_idx:]

with open('site/content/warships/ship-construction.md', 'w') as f:
    f.write(content)
print("Replaced all tables!")
