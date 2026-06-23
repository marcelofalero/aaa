import re

with open('scratch/warships_clean.txt', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('STEP 7: WEAPONS')
end = text.find('STEP 9: COMMAND AND')
clean_5 = text[start:end]

# Now, we manually strip out the raw tables
tables_to_strip = [
    ("Table 5-7:", "4                  3               5\n"),
    ("Table 5-8:", "PL 9     Null bore**                  Null       A            X          -          -          -          -          -          -\n"),
    ("Table 5-9:", "PL 8    Mass cannon              G          G            5          10\n"),
    ("Table 5-10:", "PL 8     Plasma                   D, X        1.0                 5\n"),
    ("Table 5-11:", "PL 9    Null bomb                  Null torpedo             Null bomb\n"),
    ("Table 5-12:", "Null torpedo                       M, X          100             100            $150 K        +1\n"),
    ("Table 5-13:", "PL 9   Defense Network               C           10           -                 1\n")
]

for t_start, t_end in tables_to_strip:
    idx_start = clean_5.find(t_start)
    if idx_start != -1:
        idx_end = clean_5.find(t_end, idx_start)
        if idx_end != -1:
            # We want to remove the table, but let's insert the markdown table!
            clean_5 = clean_5[:idx_start] + f"\n\n[INSERT {t_start.strip()}]\n\n" + clean_5[idx_end + len(t_end):]
        else:
            print(f"Could not find end for {t_start}")
    else:
        print(f"Could not find start for {t_start}")

with open('scratch/clean_5_stripped.txt', 'w', encoding='utf-8') as f:
    f.write(clean_5)
