with open('scratch/warships_clean.txt', 'r', encoding='utf-8') as f:
    clean_txt = f.read()

def get_end(start_str):
    idx = clean_txt.find(start_str)
    if idx == -1:
        print(f"NOT FOUND: {start_str}")
        return
    snippet = clean_txt[idx:idx+2500]
    lines = snippet.split('\n')
    for i, line in enumerate(lines):
        if line.strip() == "": continue
        print(f"{i}: {line}")
    print("\n")

get_end("Table 5-3: Power Plants\n")
get_end("Table 5-4: Engines\n")
get_end("Table 5-5: FTL Drives\n")
get_end("Table 5-6: Support Systems\n")
get_end("Table 5-8: Beam Weapons\n")
get_end("Table 5-9: Projectile Weapons\n")
get_end("Table 5-10: Missiles, Bombs, and Mines (Part 1)\n")
get_end("Table 5-11: Area Effect Weapons\n")
get_end("Table 5-12: Torpedoes and Special Weapons\n")
get_end("Table 5-13: Defensive Systems\n")
get_end("Table 5-14: Command, Control, and Communication Systems\n")
get_end("Table 5-14a: Computers\n")
get_end("Table 5-15: Sensors\n")
get_end("Table 5-16: Tracking Capability\n")
get_end("Table 5-17: Hangars and Miscellaneous Installations\n")
get_end("Table 5-18: Hit Locations and Zone Limits\n")
