with open('scratch/warships_clean.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_line = 0
end_line = 0
for i, line in enumerate(lines):
    if 'STEP 7: WEAPONS' in line:
        start_line = i
    if 'STEP 9: COMMAND AND' in line:
        end_line = i
        break

# The tables are in these line ranges in warships_clean.txt:
# Table 5-8: 7066
# Table 5-9: 7332
# Table 5-10: 7583, 7679, 7772
# Table 5-11: 7996
# Table 5-12: 8329
# Table 5-13: 8543

# I'll find the start of each table inside my slice.
slice_lines = lines[start_line:end_line]

def find_line(text_snippet, start_idx=0):
    for i in range(start_idx, len(slice_lines)):
        if text_snippet in slice_lines[i]:
            return i
    return -1

t8_start = find_line("Table 5-8: Beam Weapons")
t8_end = find_line("Cost: The cost of the weapon.", t8_start) + 1

t9_start = find_line("Table 5-9: Projectile Weapons", t8_end)
t9_end = find_line("Cost: The cost of the weapon.", t9_start) + 1

t10_start = find_line("Table 5-10: Missiles, Bombs, and Mines (Part 1)", t9_end)
t10_end = find_line("Cost: The cost of the weapon.", t10_start) + 1 # wait, it might be in Part 3!
if t10_end <= t10_start + 10:
    # Missiles has 3 parts. Let's find Part 3
    t10_p3 = find_line("Table 5-10: Missiles, Bombs, and Mines (Part 3)", t10_start)
    t10_end = find_line("Cost: The cost of the weapon.", t10_p3) + 1

t11_start = find_line("Table 5-11: Area Effect Weapons", t10_end)
t11_end = find_line("Type: The weapon’s category (beam weapon, projectile weapon, or warhead for a missile, bomb, or mine).", t11_start) + 1

t12_start = find_line("Table 5-12: Torpedoes and Special Weapons", t11_end)
t12_end = find_line("Hull: The number of hull points required for the installation of this weapon system.", t12_start) + 1

t13_start = find_line("Table 5-13: Defensive Systems", t12_end)
t13_end = find_line("total, so a ship of 240 hull points would require 12 hull points for a damage control system.", t13_start) + 1

ranges = [(t8_start, t8_end), (t9_start, t9_end), (t10_start, t10_end), (t11_start, t11_end), (t12_start, t12_end), (t13_start, t13_end)]

out_lines = []
i = 0
while i < len(slice_lines):
    skip = False
    for r_s, r_e in ranges:
        if r_s <= i < r_e:
            skip = True
            break
        # Also let's insert a placeholder right where the table used to be
        if i == r_e:
            out_lines.append(f"\n\n[INSERT TABLE HERE]\n\n")
    if not skip:
        out_lines.append(slice_lines[i])
    i += 1

with open('scratch/clean_5_sliced.txt', 'w', encoding='utf-8') as f:
    f.writelines(out_lines)

print("Ranges found:", ranges)
