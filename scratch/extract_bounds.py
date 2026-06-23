with open('scratch/warships_clean.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find all occurrences of "Table 5-"
matches = re.finditer(r'Table 5-\d+[a-z]?:.*?\n', text)
for m in matches:
    title = m.group(0).strip()
    print(f"TITLE: {title}")
    
    # print the next 20 lines to find a suitable end bound
    snippet = text[m.end():m.end()+1500]
    lines = snippet.split('\n')
    for i, line in enumerate(lines[:30]):
        if line.strip():
            print(f"{i}: {line}")
    print("-------")
