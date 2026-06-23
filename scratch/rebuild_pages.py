import re
import os

with open('scratch/warships_clean.txt', 'r', encoding='utf-8') as f:
    clean_txt = f.read()

# Load Markdown tables
with open('scratch/markdown_tables.md', 'r', encoding='utf-8') as f:
    tables_md = f.read()

tables = {}
parts = re.split(r'### (Table 5[-–]\d+[a-z]?[^\n]*)', tables_md)
for i in range(1, len(parts), 2):
    title = parts[i].strip()
    key = re.match(r'Table 5[-–]\d+[a-z]?', title).group(0).replace('–', '-')
    if key == 'Table 5-10':
        if key not in tables:
            tables[key] = ""
        tables[key] += parts[i+1].strip() + "\n\n"
    else:
        tables[key] = f"### {title}\n" + parts[i+1].strip() + "\n\n"

# Table 5-7 manually added
tables['Table 5-7'] = """### Table 5-7: Hull Point Costs for Fixed Mounts and Turrets

| Standard | Fixed | Turret |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 3 |
| 3 | 2 | 4 |
| 4 | 3 | 5 |

"""

# Define boundaries in warships_clean.txt for each raw table
bounds = [
    ("Table 5-2: Armor", "d6-1        d6-1          d6-1         2.5%                   $100 K\n", "Table 5-2"),
    ("Table 5-3: Power Plants", "Anti-matter                  150           15           No         -          -\n", "Table 5-3"),
    ("Table 5-4: Engines", "PL 9   Quantum   A/Q           0             2.0        $2 M       $200 K     -         -\n", "Table 5-4"),
    ("Table 5-5: FTL Drives", "PL 9   Matter Transmission M          X           20         10%        $5 M\n", "Table 5-5"),
    ("Table 5-6: Support Systems", "Life support                   Any     Any           1          -          $2 M\n", "Table 5-6"),
    ("Table 5-7: Hull Point Costs for Fixed Mounts and Turrets", "4                  3               5\n", "Table 5-7"),
    ("Table 5-8: Beam Weapons", "Matter gun                 M            A          F          1          2          2          1          2          3\n", "Table 5-8"),
    ("Table 5-9: Projectile Weapons", "PL 8    Mass cannon              G          G            5          10\n", "Table 5-9"),
    ("Table 5-10: Missiles, Bombs, and Mines (Part 1)", "PL 8     Plasma                   D, X        1.0                 5\n", "Table 5-10"),
    ("Table 5-11: Area Effect Weapons", "PL 9    Null bomb                  Null torpedo             Null bomb\n", "Table 5-11"),
    ("Table 5-12: Torpedoes and Special Weapons", "Null torpedo                       M, X          100             100            $150 K        +1\n", "Table 5-12"),
    ("Table 5-13: Defensive Systems", "PL 9   Defense Network               C           10           -                 1\n", "Table 5-13"),
    ("Table 5-14: Command, Control, and Communication Systems", "PL 8   Ansible                         P/Q       5            2                 1\n", "Table 5-14"),
    ("Table 5-14a: Computers", "PL 8 Nav Control, Amazing                 5                 5\n", "Table 5-14a"),
    ("Table 5-15: Sensors", "Drive Detection Array                  0                 0                  1\n", "Table 5-15"),
    ("Table 5-16: Tracking Capability", "PL 9                  36\n", "Table 5-16"),
    ("Table 5-17: Hangars and Miscellaneous Installations", "Cargo handling                 Any    Any          Any          -\n", "Table 5-17"),
    ("Table 5-18: Hit Locations and Zone Limits", "Weapon                           8          4          2           1\n", "Table 5-18"),
]

for start_str, end_str, key in bounds:
    start_idx = clean_txt.find(start_str)
    if start_idx == -1:
        print(f"Could not find start for {key}")
        continue
    
    end_idx = clean_txt.find(end_str, start_idx)
    if end_idx == -1:
        print(f"Could not find end for {key}")
        continue
        
    end_idx += len(end_str)
    clean_txt = clean_txt[:start_idx] + tables[key] + "\n\n" + clean_txt[end_idx:]

with open('scratch/warships_clean_with_tables.txt', 'w', encoding='utf-8') as f:
    f.write(clean_txt)

print("Tables inserted into clean text!")
