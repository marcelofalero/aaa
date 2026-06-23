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
    (r'Table 5-8: Beam Weapons.*?(?=Beams Beam weapons direct some form of energy)', tables['Table 5-8']),
    (r'Table 5-18: Hit Locations and Zone Limits.*?(?=## Step 11: Hangars And)', tables['Table 5-18']),
]

for pat, rep in patterns:
    if not re.search(pat, content, flags=re.DOTALL):
        print(f"Pattern not found: {pat[:30]}...")
    else:
        content = re.sub(pat, rep, content, count=1, flags=re.DOTALL)
        print(f"Replaced {pat[:30]}...")

with open('site/content/warships/ship-construction.md', 'w') as f:
    f.write(content)
