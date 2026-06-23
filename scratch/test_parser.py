import re

def parse_tables(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    tables = {}
    current_table = None
    table_lines = []
    
    for line in lines:
        if 'Table 5-' in line and not '. . .' in line:
            if current_table:
                tables[current_table] = table_lines
            m = re.search(r'(Table 5-[0-9a-z]+[^\n]+)', line)
            if m:
                current_table = m.group(1).strip()
                table_lines = []
        elif current_table:
            table_lines.append(line.rstrip())
            
    if current_table:
        tables[current_table] = table_lines
        
    for k, v in list(tables.items())[:3]:
        print(f"--- {k} ---")
        for r in v[:12]:
            print(re.split(r'\s{2,}', r.strip()))
            
parse_tables('scratch/warships_layout.txt')
