import os
import re

base_dir = 'site/content/warships/ship-construction'

# 1. Read _index.md
with open(os.path.join(base_dir, '_index.md'), 'r') as f:
    lines = f.readlines()

idx_step1 = [i for i, l in enumerate(lines) if l.startswith('## Step 1: Class And Hull')][0]

index_content = "".join(lines[:idx_step1]).strip() + "\n"
step1_content = "".join(lines[idx_step1:]).strip() + "\n"

step1_fm = """+++
title = "Class & Hull"
description = "Step 1 of Starship Construction."
weight = 10
+++
"""

# write _index.md
with open(os.path.join(base_dir, '_index.md'), 'w') as f:
    f.write(index_content)

# write 01-class-hull.md
with open(os.path.join(base_dir, '01-class-hull.md'), 'w') as f:
    f.write(step1_fm + "\n" + step1_content)

# 2. Rename existing files and update weight
rename_map = {
    '01-armor.md': ('02-armor.md', 20),
    '02-engineering.md': ('03-engineering.md', 30),
    '03-systems-crew.md': ('04-systems-crew.md', 40),
    '04-weapons-defenses.md': ('05-weapons-defenses.md', 50),
    '05-command-sensors.md': ('06-command-sensors.md', 60),
    '06-hangars-misc.md': ('07-hangars-misc.md', 70),
    '07-finalizing.md': ('08-finalizing.md', 80)
}

# sort keys in reverse order to avoid overwriting existing files before they are moved
for old_name in sorted(rename_map.keys(), reverse=True):
    new_name, new_weight = rename_map[old_name]
    old_path = os.path.join(base_dir, old_name)
    new_path = os.path.join(base_dir, new_name)
    
    with open(old_path, 'r') as f:
        content = f.read()
        
    content = re.sub(r'weight = \d+', f'weight = {new_weight}', content)
    
    with open(new_path, 'w') as f:
        f.write(content)
        
    os.remove(old_path)
    
print("Refactored Step 1 into its own file!")
