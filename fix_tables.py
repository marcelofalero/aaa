import re

def parse_bogus_tables(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    left = []
    right = []
    
    in_bogus = False
    
    for line in lines:
        if line.startswith('| changes or maneuvers for 1d4 hours. |') or line.startswith('| 6x | 4 Mpp | If the target is too big to affect'):
            in_bogus = True
        elif line.startswith('| If the ship changes its course or speed after deploying |'):
            in_bogus = True
            
        if in_bogus:
            # Check if this is a real table header or divider
            if "---|---" in line or line.startswith("### Table"):
                in_bogus = False
                continue
                
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                left.append(parts[1])
                # Special case: some tables only have 1 data column after being mangled, some have 2
                if len(parts) >= 4 and parts[2] != '':
                    right.append(parts[2])
                elif len(parts) >= 4 and len(parts) > 3:
                    right.append(parts[-2]) # get the last real column
                elif len(parts) == 3:
                     # there is no right column
                     pass

    print("LEFT:")
    print(" ".join(left).replace("- ", ""))
    print("\nRIGHT:")
    print(" ".join(right).replace("- ", ""))

parse_bogus_tables('site/content/warships/ship-construction/weapons-defenses.md')
