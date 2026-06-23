import re

with open('scratch/warships_clean.txt', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('STEP 7: WEAPONS')
end = text.find('STEP 9: COMMAND AND')
clean_5 = text[start:end]

tables_to_strip = [
    ("Table 5-7", r"4\s+3\s+5"),
    ("Table 5-8:", r"Null bore\*\*\s+Null\s+A\s+X\s+-\s+-\s+-\s+-\s+-\s+-"),
    ("Table 5-9:", r"Mass cannon\s+G\s+G\s+5\s+10"),
    ("Table 5-10", r"D,\s+X\s+1\.0\s+5"), 
    ("Table 5-11:", r"Null bomb\s+Null torpedo\s+Null bomb"),
    ("Table 5-12:", r"M,\s+X\s+100\s+100\s+\$150 K\s+\+1"),
    ("Table 5-13:", r"C\s+10\s+-\s+1")
]

for t_start, t_end_regex in tables_to_strip:
    idx_start = clean_5.find(t_start)
    if idx_start != -1:
        match = re.search(t_end_regex, clean_5[idx_start:])
        if match:
            idx_end = idx_start + match.end()
            clean_5 = clean_5[:idx_start] + f"\n\n[INSERT {t_start.strip()}]\n\n" + clean_5[idx_end:]
        else:
            print(f"Could not find end for {t_start}")
    else:
        print(f"Could not find start for {t_start}")

with open('scratch/clean_5_stripped.txt', 'w', encoding='utf-8') as f:
    f.write(clean_5)
