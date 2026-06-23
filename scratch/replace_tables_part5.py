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

# Replace Table 5-8
start_idx = content.find("Table 5-8: Beam Weapons Weapon Tech Hull")
if start_idx == -1: start_idx = content.find("Table 5-8: Beam Weapons")
end_idx = content.find("‘A’ stands for autofire.", start_idx)
if start_idx != -1 and end_idx != -1:
    end_idx += len("‘A’ stands for autofire.")
    content = content[:start_idx] + tables['Table 5-8'] + "\n\n" + content[end_idx:]
    print("Replaced Table 5-8")
else:
    print("Could not find Table 5-8 bounds")

# Replace Table 5-18
start_idx = content.find("Table 5-18: Hit Locations and Zone Limits")
end_idx = content.find("Step 2: Armor", start_idx)
if start_idx != -1 and end_idx != -1:
    # We want to keep "Step 2: Armor"
    content = content[:start_idx] + tables['Table 5-18'] + "\n\n" + content[end_idx:]
    print("Replaced Table 5-18")
else:
    print("Could not find Table 5-18 bounds")

with open('site/content/warships/ship-construction.md', 'w') as f:
    f.write(content)
