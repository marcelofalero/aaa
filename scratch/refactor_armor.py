import os
import re

base_dir = 'site/content/warships/ship-construction'

# 1. Read 01-engineering.md
with open(os.path.join(base_dir, '01-engineering.md'), 'r') as f:
    lines = f.readlines()

idx_step3 = [i for i, l in enumerate(lines) if l.startswith('## Step 3: Power Plant')][0]

armor_content = "".join(lines[6:idx_step3]).strip() + "\n"
eng_content = "".join(lines[idx_step3:]).strip() + "\n"

armor_fm = """+++
title = "Armor"
description = "Step 2 of Starship Construction."
weight = 10
+++
"""

eng_fm = """+++
title = "Engineering"
description = "Step 3 through Step 5 of Starship Construction."
weight = 20
+++
"""

# write 01-armor.md
with open(os.path.join(base_dir, '01-armor.md'), 'w') as f:
    f.write(armor_fm + "\n" + armor_content)

# write 02-engineering.md
with open(os.path.join(base_dir, '02-engineering.md'), 'w') as f:
    f.write(eng_fm + "\n" + eng_content)

# 2. Rename existing files and update weight
rename_map = {
    '02-systems-crew.md': ('03-systems-crew.md', 30),
    '03-weapons-defenses.md': ('04-weapons-defenses.md', 40),
    '04-command-sensors.md': ('05-command-sensors.md', 50),
    '05-hangars-misc.md': ('06-hangars-misc.md', 60),
    '06-finalizing.md': ('07-finalizing.md', 70)
}

for old_name, (new_name, new_weight) in rename_map.items():
    old_path = os.path.join(base_dir, old_name)
    new_path = os.path.join(base_dir, new_name)
    
    with open(old_path, 'r') as f:
        content = f.read()
        
    content = re.sub(r'weight = \d+', f'weight = {new_weight}', content)
    
    with open(new_path, 'w') as f:
        f.write(content)
        
    os.remove(old_path)
    
os.remove(os.path.join(base_dir, '01-engineering.md'))

print("Refactored armor into its own file!")
