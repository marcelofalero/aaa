import os
import re

with open('site/content/warships/ship-construction.md', 'r') as f:
    lines = f.readlines()

def get_section(start_idx, end_idx):
    # include start_idx to end_idx (exclusive)
    return "".join(lines[start_idx:end_idx]).strip() + "\n"

# We know the approximate line numbers:
idx_step2 = [i for i, l in enumerate(lines) if l.startswith('## Step 2: Armor')][0]
idx_step6 = [i for i, l in enumerate(lines) if l.startswith('## Step 6: Support Systems')][0]
idx_step7 = [i for i, l in enumerate(lines) if l.startswith('## Step 7: Weapons')][0]
idx_step9 = [i for i, l in enumerate(lines) if l.startswith('## Step 9: Command And')][0]
idx_step11 = [i for i, l in enumerate(lines) if l.startswith('## Step 11: Hangars And')][0]
idx_step13 = [i for i, l in enumerate(lines) if l.startswith('## Step 13: Adding It Up')][0]

sections = {
    "_index.md": {
        "fm": """+++
title = "Ship Construction"
description = "A step-by-step system for designing custom starships."
weight = 60
+++
""",
        "content": "".join(lines[6:idx_step2]).strip() + "\n" # Skip the original frontmatter which ends at line 5
    },
    "01-engineering.md": {
        "fm": """+++
title = "Armor & Engineering"
description = "Step 2 through Step 5 of Starship Construction."
weight = 10
+++
""",
        "content": get_section(idx_step2, idx_step6)
    },
    "02-systems-crew.md": {
        "fm": """+++
title = "Support Systems & Crew"
description = "Step 6 of Starship Construction."
weight = 20
+++
""",
        "content": get_section(idx_step6, idx_step7)
    },
    "03-weapons-defenses.md": {
        "fm": """+++
title = "Weapons & Defenses"
description = "Step 7 and Step 8 of Starship Construction."
weight = 30
+++
""",
        "content": get_section(idx_step7, idx_step9)
    },
    "04-command-sensors.md": {
        "fm": """+++
title = "Command & Sensors"
description = "Step 9 and Step 10 of Starship Construction."
weight = 40
+++
""",
        "content": get_section(idx_step9, idx_step11)
    },
    "05-hangars-misc.md": {
        "fm": """+++
title = "Hangars & Miscellaneous"
description = "Step 11 and Step 12 of Starship Construction."
weight = 50
+++
""",
        "content": get_section(idx_step11, idx_step13)
    },
    "06-finalizing.md": {
        "fm": """+++
title = "Finalizing the Design"
description = "Step 13 and Starship Construction Examples."
weight = 60
+++
""",
        "content": get_section(idx_step13, len(lines))
    }
}

os.makedirs('site/content/warships/ship-construction', exist_ok=True)

for fname, data in sections.items():
    with open(os.path.join('site/content/warships/ship-construction', fname), 'w') as f:
        f.write(data['fm'] + "\n" + data['content'])

print("Files generated successfully!")
