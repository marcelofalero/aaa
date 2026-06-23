import re

with open('scratch/warships_clean.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# We know that all raw tables start with "Table 5-X:"
# And we can see that in pdftotext -layout, the raw tables are basically lines with multiple spaces.
# Let's just find the start of each table.

def remove_table(text, start_str, end_str):
    start = text.find(start_str)
    if start == -1: return text
    end = text.find(end_str, start)
    if end == -1: return text
    
    # We want to remove everything from start up to and including end_str
    # BUT we might have missed some trailing table lines if end_str was in the middle of a paragraph.
    return text[:start] + "\n[TABLE_PLACEHOLDER_" + start_str.split(':')[0] + "]\n" + text[end + len(end_str):]

# Manual bounds for the 18 tables. I will use unique strings.
bounds = [
    ("Table 5-1a: Military Hulls\n", "$10000 M\n"),
    ("Table 5-1b: Civilian Hulls\n", "$400 M\n"),
    ("Table 5-2: Armor\n", "2d4+3       2d4+4          2d4+3        20%                    $4 M\n"),
    ("Table 5-3: Power Plants\n", "G          6.0      $10 M    $500 K        20         No           -         -\n"),
    ("Table 5-4: Engines\n", "Cost/Hull: The cost per hull point assigned to this engine; cumulative with the base cost.\n"),
    ("Table 5-5: FTL Drives\n", "Tech: The technology required to build this drive system.\n"),
    ("Table 5-6: Support Systems\n", "Cost: The system cost, or the cost per hull point for a system requiring some percentage of the hull.\n"),
    ("Table 5-7: Hull Point Costs for Fixed Mounts and Turrets\n", "4                  3               5\n"),
    ("Table 5-8: Beam Weapons\n", "PL 9     Null bore**                  Null       A            X          -          -          -          -          -          -\n"),
    ("Table 5-9: Projectile Weapons\n", "PL 8    Mass cannon              G          G            5          10\n"),
    ("Table 5-10: Missiles, Bombs, and Mines (Part 1)\n", "PL 8     Plasma                   D, X        1.0                 5\n"),
    ("Table 5-10: Missiles, Bombs, and Mines (Part 2)\n", "PL 8     Plasma                   D, X        1.0                 5\n"), # Wait, part 2 might not exist
    ("Table 5-11: Area Effect Weapons\n", "PL 9    Null bomb                  Null torpedo             Null bomb\n"),
    ("Table 5-12: Torpedoes and Special Weapons\n", "Null torpedo                       M, X          100             100            $150 K        +1\n"),
    ("Table 5-13: Defensive Systems\n", "PL 9   Defense Network               C           10           -                 1\n"),
    ("Table 5-14: Command, Control, and Communication Systems\n", "PL 8   Ansible                         P/Q       5            2                 1\n"),
    ("Table 5-14a: Computers\n", "PL 8 Nav Control, Amazing                 5                 5\n"),
    ("Table 5-15: Sensors\n", "Drive Detection Array                  0                 0                  1\n"),
    ("Table 5-16: Tracking Capability\n", "PL 9                  36\n"),
    ("Table 5-17: Hangars and Miscellaneous Installations\n", "Cargo handling                 Any    Any          Any          -\n"),
    ("Table 5-18: Hit Locations and Zone Limits\n", "Weapon                           8          4          2           1\n"),
]

for start_str, end_str in bounds:
    text = remove_table(text, start_str, end_str)

with open('scratch/warships_no_tables.txt', 'w', encoding='utf-8') as f:
    f.write(text)
