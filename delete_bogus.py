with open('fix_weapons_temp.md', 'r') as f:
    lines = f.readlines()

out = []
skip = False
for line in lines:
    if line.startswith('| changes or maneuvers for 1d4 hours. |'):
        skip = True
    elif line.startswith('| 6x | 4 Mpp | If the target is too big'):
        skip = True
    elif line.startswith('| If the ship changes its course or speed'):
        skip = True
        
    if not skip:
        out.append(line)
        
    if skip:
        if line.startswith('| likely to hit a target that’s trying not to be hit. |'):
            skip = False
        elif line.startswith('| beam that scored a Good hit when it initially captured the | target vessel. |'):
            skip = False
        # The last block goes to the end of the file, so it stays skip=True

with open('site/content/warships/ship-construction/weapons-defenses.md', 'w') as f:
    f.writelines(out)
