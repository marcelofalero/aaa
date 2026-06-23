with open('scratch/eng_clean.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "Table 5-" in line:
        print(f"Line {i}: {line.strip()}")
