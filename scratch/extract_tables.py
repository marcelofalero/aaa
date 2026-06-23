import re

with open('scratch/warships_layout.txt', 'r') as f:
    lines = f.readlines()

table_lines = []

for i, line in enumerate(lines):
    if line.strip().startswith('Table 5-'):
        table_lines.append('\n' + '='*80 + '\n')
        for j in range(i, min(i+40, len(lines))):
            table_lines.append(lines[j].rstrip())

with open('scratch/tables_extracted.txt', 'w') as f:
    f.write('\n'.join(table_lines))
