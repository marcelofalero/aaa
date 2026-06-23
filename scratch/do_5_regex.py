import re

with open('scratch/warships_clean.txt', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('STEP 7: WEAPONS')
end = text.find('STEP 9: COMMAND AND')
clean_5 = text[start:end]

# We will use regex to find the tables. They all start with "Table 5-X:" and end right before a normal paragraph.
# Looking at the pdftotext output, the tables are characterized by lots of spaces.
# But it's easier to just specify a short unique substring near the end of each table.

tables_to_strip = [
    ("Table 5-7", "4                  3               5"),
    ("Table 5-8:", "Null bore**                  Null       A            X          -          -          -          -          -          -"),
    ("Table 5-9:", "Mass cannon              G          G            5          10"),
    ("Table 5-10", "D, X        1.0                 5"), # Part 1 and Part 2 are combined or separate
    ("Table 5-11:", "Null bomb                  Null torpedo             Null bomb"),
    ("Table 5-12:", "M, X          100             100            $150 K        +1"),
    ("Table 5-13:", "C           10           -                 1")
]

for t_start, t_end in tables_to_strip:
    idx_start = clean_5.find(t_start)
    if idx_start != -1:
        idx_end = clean_5.find(t_end, idx_start)
        if idx_end != -1:
            clean_5 = clean_5[:idx_start] + f"\n\n[INSERT {t_start.strip()}]\n\n" + clean_5[idx_end + len(t_end):]
        else:
            print(f"Could not find end for {t_start}")
    else:
        print(f"Could not find start for {t_start}")

with open('scratch/clean_5_stripped.txt', 'w', encoding='utf-8') as f:
    f.write(clean_5)
