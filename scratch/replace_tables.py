import re

with open('site/content/warships/ship-construction.md', 'r') as f:
    content = f.read()

# Load generated tables
with open('scratch/markdown_tables.md', 'r') as f:
    tables_md = f.read()

# Split tables_md into individual tables
tables = {}
parts = re.split(r'### (Table 5[-–]\d+[a-z]?[^\n]*)', tables_md)
for i in range(1, len(parts), 2):
    title = parts[i].strip()
    key = re.match(r'Table 5[-–]\d+[a-z]?', title).group(0).replace('–', '-')
    
    if key == 'Table 5-1a' or key == 'Table 5-1b':
        key_main = 'Table 5-1'
        if key_main not in tables:
            tables[key_main] = ""
        tables[key_main] += f"### {title}\n" + parts[i+1].strip() + "\n\n"
    elif key == 'Table 5-10':
        if key not in tables:
            tables[key] = ""
        tables[key] += parts[i+1].strip() + "\n\n"
    else:
        tables[key] = f"### {title}\n" + parts[i+1].strip() + "\n\n"

# Add Table 5-7 manually
tables['Table 5-7'] = """### Table 5-7: Hull Point Costs for Fixed Mounts and Turrets

| Standard | Fixed | Turret |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 3 |
| 3 | 2 | 4 |
| 4 | 3 | 5 |

"""

# Define the boundaries in ship-construction.md manually to be 100% safe
# Format: (start_string, end_string, table_key)
# Notice we just search for the first occurrence of end_string AFTER start_string
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
    ("Table 5-17: Hangars and Miscellaneous Installations", "System\n", "Table 5-17"),
    ("Table 5-18: Hit Locations and Zone Limits", "## Step 11: Hangars and Small Craft\n", "Table 5-18"),
]

for start_str, end_str, key in reversed(bounds):
    start_idx = content.find(start_str)
    if start_idx == -1:
        print(f"Could not find start for {key}")
        continue
    
    end_idx = content.find(end_str, start_idx)
    if end_idx == -1:
        print(f"Could not find end for {key}")
        continue
        
    # We replace up to the BEGINNING of end_str IF it's a heading we want to keep
    if "Step 11" in end_str:
        pass
    else:
        end_idx += len(end_str)
    
    # Check if table exists
    if key not in tables:
        print(f"Key {key} not found in tables!")
        continue
        
    content = content[:start_idx] + tables[key] + "\n\n" + content[end_idx:]

with open('site/content/warships/ship-construction.md', 'w') as f:
    f.write(content)
print("Replaced all tables!")
