import re

with open('scratch/warships_clean.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Build 06: Command and Control
start_6 = text.find('STEP 9: COMMAND AND')
end_6 = text.find('STEP 10: SENSORS')
clean_6 = text[start_6:end_6]

tables_to_remove_6 = [
    ("Table 5-14: Command, Control, and Communication Systems", "bridge won’t completely incapacitate the ship."),
    ("Table 5-14a: Computers", "Cost: The cost for one unit of this system, or per hull point of a system based on a percentage of the hull.")
]

for t_start, t_end in tables_to_remove_6:
    s_idx = clean_6.find(t_start)
    if s_idx == -1: print(f"Failed 6 start: {t_start}"); continue
    e_idx = clean_6.find(t_end, s_idx)
    if e_idx == -1: print(f"Failed 6 end: {t_end}"); continue
    e_idx += len(t_end)
    clean_6 = clean_6[:s_idx] + clean_6[e_idx:]

with open('scratch/markdown_tables.md', 'r') as f:
    tables_md = f.read()

tables = {}
parts = re.split(r'### (Table 5[-–]\d+[a-z]?[^\n]*)', tables_md)
for i in range(1, len(parts), 2):
    title = parts[i].strip()
    key = re.match(r'Table 5[-–]\d+[a-z]?', title).group(0).replace('–', '-')
    tables[key] = f"### {title}\n" + parts[i+1].strip() + "\n\n"

clean_6 += "\n\n"
for k in ['Table 5-14', 'Table 5-14a']:
    if k in tables:
        clean_6 += tables[k] + "\n\n"

frontmatter_6 = """+++
title = "Command & Control"
description = "Step 9 of Starship Construction."
weight = 60
+++

"""
final_6 = frontmatter_6 + clean_6.replace('STEP 9: COMMAND AND', '## Step 9: Command and Control').replace('CONTROL\n\n', '').replace('--- PAGE BREAK ---', '')
final_6 = re.sub(r'\n{3,}', '\n\n', final_6)

with open('site/content/warships/ship-construction/06-command-control-comm.md', 'w', encoding='utf-8') as f:
    f.write(final_6)
print("Done building 06!")

# Build 07: Sensors
start_7 = end_6
end_7 = text.find('STEP 11: HANGARS AND')
clean_7 = text[start_7:end_7]

tables_to_remove_7 = [
    ("Table 5-15: Sensors", "Targeting: Attack penalties for firing on a target using this sensor information."),
    ("Table 5-16: Tracking Capability", "PL 8")
]

for t_start, t_end in tables_to_remove_7:
    s_idx = clean_7.find(t_start)
    if s_idx == -1: print(f"Failed 7 start: {t_start}"); continue
    e_idx = clean_7.find(t_end, s_idx)
    if e_idx == -1: print(f"Failed 7 end: {t_end}"); continue
    e_idx += len(t_end)
    clean_7 = clean_7[:s_idx] + clean_7[e_idx:]

clean_7 += "\n\n"
for k in ['Table 5-15', 'Table 5-16']:
    if k in tables:
        clean_7 += tables[k] + "\n\n"

frontmatter_7 = """+++
title = "Sensors"
description = "Step 10 of Starship Construction."
weight = 70
+++

"""
final_7 = frontmatter_7 + clean_7.replace('STEP 10: SENSORS', '## Step 10: Sensors').replace('--- PAGE BREAK ---', '')
final_7 = re.sub(r'\n{3,}', '\n\n', final_7)

with open('site/content/warships/ship-construction/07-sensors.md', 'w', encoding='utf-8') as f:
    f.write(final_7)
print("Done building 07!")
