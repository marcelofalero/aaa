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
    
    if key not in tables:
        tables[key] = ""
    tables[key] += f"### {title}\n" + parts[i+1].strip() + "\n\n"

bounds = [
    ("Table 5-4: Engines", "* Acceleration on PL 6 game scale; see Chapter 2.\n", "Table 5-4"),
    ("Table 5-5: FTL Drives", "* The jump drive takes 10 percent", "Table 5-5"),
    ("Table 5-6: Support Systems", "* These support systems provide enough facilities", "Table 5-6"),
    ("Table 5-8: Beam Weapons", "** Note that hydrogen bores, fusion bores", "Table 5-8"),
    ("Table 5-9: Projectile Weapons", "* Unlike most projectile weapons", "Table 5-9"),
    ("Table 5-18: Hit Locations and Zone Limits", "## Step 11: Hangars and Small Craft\n", "Table 5-18"),
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
        
    if key not in tables:
        print(f"Error: Key {key} not found in tables!")
        continue
        
    content = content[:start_idx] + tables[key] + "\n\n" + content[end_idx:]

with open('site/content/warships/ship-construction.md', 'w') as f:
    f.write(content)
print("Replaced remaining tables!")
