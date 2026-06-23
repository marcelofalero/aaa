import re

with open('scratch/warships_clean.txt', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('STEP 7: WEAPONS')
end = text.find('STEP 9: COMMAND AND')
clean_5 = text[start:end]

# Instead of using line slicing which was buggy, I will use regex to find and remove the raw tables.
# I already found the exact string bounds in find_ends_manual.py!

tables_to_remove = [
    # Table 5-8
    ("Table 5-8: Beam Weapons", "Fusion Bore**          F      60"),
    # Table 5-9
    ("Table 5-9: Projectile Weapons", "burst fire; and ‘A’ stands for autofire."),
    # Table 5-10
    ("Table 5-10: Missiles, Bombs, and Mines (Part 1)", "magazine to the rail and then firing it off, but a simple rack"),
    # Table 5-11
    ("Table 5-11: Area Effect Weapons", "Weapons marked SA are strategic arms and generally can’t be used with the direct approval of a national command authority."),
    # Table 5-12
    ("Table 5-12: Torpedoes and Special Weapons", "‘F’ stands for single-shot."),
    # Table 5-13
    ("Table 5-13: Defensive Systems", "total, so a ship of 240 hull points would require 12 hull points for a damage control system.")
]

for t_start, t_end in tables_to_remove:
    s_idx = clean_5.find(t_start)
    if s_idx == -1:
        print(f"Failed to find start: {t_start[:20]}")
        continue
    e_idx = clean_5.find(t_end, s_idx)
    if e_idx == -1:
        print(f"Failed to find end: {t_end[:20]}")
        continue
    
    e_idx += len(t_end)
    clean_5 = clean_5[:s_idx] + clean_5[e_idx:]

# Load tables
with open('scratch/markdown_tables.md', 'r') as f:
    tables_md = f.read()

# Split tables_md into individual tables
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

# Add Table 5-7 manually
tables['Table 5-7'] = """### Table 5-7: Hull Point Costs for Fixed Mounts and Turrets

| Standard | Fixed | Turret |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 3 |
| 3 | 2 | 4 |
| 4 | 3 | 5 |

"""

# Append tables at the end
clean_5 += "\n\n"
for k in ['Table 5-7', 'Table 5-8', 'Table 5-9', 'Table 5-10', 'Table 5-11', 'Table 5-12', 'Table 5-13']:
    clean_5 += tables[k] + "\n\n"

# Add Hugo frontmatter
frontmatter = """+++
title = "Weapons & Defenses"
description = "Step 7 and Step 8 of Starship Construction."
weight = 50
+++

"""

final_text = frontmatter + clean_5.replace('STEP 7: WEAPONS', '## Step 7: Weapons').replace('STEP 8: DEFENSES', '## Step 8: Defenses').replace('--- PAGE BREAK ---', '')

# Remove extra newlines
final_text = re.sub(r'\n{3,}', '\n\n', final_text)

with open('site/content/warships/ship-construction/05-weapons-defenses.md', 'w', encoding='utf-8') as f:
    f.write(final_text)

print("Done building 05!")
