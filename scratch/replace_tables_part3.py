import re

with open('site/content/warships/ship-construction.md', 'r') as f:
    content = f.read()

with open('scratch/markdown_tables.md', 'r') as f:
    tables_md = f.read()

tables = {}
parts = re.split(r'### (Table 5[-–]\d+[a-z]?[^\n]*)', tables_md)
for i in range(1, len(parts), 2):
    title = parts[i].strip()
    key = re.match(r'Table 5[-–]\d+[a-z]?', title).group(0).replace('–', '-')
    if key not in tables: tables[key] = ""
    tables[key] += f"### {title}\n" + parts[i+1].strip() + "\n\n"

patterns = [
    (r'Table 5-4: Engines.*?(?=will burn fuel two, three, and so on times)', tables['Table 5-4']),
    (r'Table 5-5: FTL Drives.*?(?=is devoted to the hyperdrive system)', tables['Table 5-5']),
    (r'Table 5-6: Support Systems.*?(?=begin decelerating at the same rate)', tables['Table 5-6']),
    (r'Table 5-8: Beam Weapons.*?(?=Laser \(PL 6\))', tables['Table 5-8']),
    (r'Table 5-9: Projectile Weapons.*?(?=Point Defense Gun \(PL 6\))', tables['Table 5-9']),
    (r'Table 5-18: Hit Locations and Zone Limits.*?(?=## Step 11: Hangars)', tables['Table 5-18']),
]

for pat, rep in patterns:
    if not re.search(pat, content, flags=re.DOTALL):
        print(f"Pattern not found: {pat[:30]}...")
    else:
        content = re.sub(pat, rep, content, count=1, flags=re.DOTALL)
        print(f"Replaced {pat[:30]}...")

with open('site/content/warships/ship-construction.md', 'w') as f:
    f.write(content)
