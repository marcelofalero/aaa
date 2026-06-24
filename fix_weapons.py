import re

with open('site/content/warships/ship-construction/weapons-defenses.md', 'r') as f:
    text = f.read()

# Fix 1: Stray Page Numbers
text = text.replace("74   The plasma cannon", "The plasma cannon")
text = text.replace("76   The point defense gun", "The point defense gun")
text = text.replace("86   The mass converter", "The mass converter")

# Fix 2: Cloaking Unit
bad_cloak = """The cloaking unit imposes a +4 step penalty to enemy sensor

### Command Systems

90   checks and missile attack rolls. Obviously, the cloaking unit

can’t be used in conjunction with a jammer or chaff bloom, since those devices would give away the ship’s position."""
good_cloak = "The cloaking unit imposes a +4 step penalty to enemy sensor checks and missile attack rolls. Obviously, the cloaking unit can’t be used in conjunction with a jammer or chaff bloom, since those devices would give away the ship’s position."
text = text.replace(bad_cloak, good_cloak)

# Fix 3: Launch Systems Intro
bad_launch_intro = """If you don’t want to go to the trouble of customizing your ship’s ordnance, check out the standard launch systems described later in this section.

78   Launch Systems

### Weapon

or cell system can torch off a number of missiles at the same time. Bomb Rack (PL 6): As you might expect, this launch system is designed to carry bombs. Its capacity can’t be expanded, but a ship could buy and mount multiple bomb racks."""
good_launch_intro = """If you don’t want to go to the trouble of customizing your ship’s ordnance, check out the standard launch systems described later in this section.

Most launch systems cannot be reloaded in space. Reloading them requires a base or tender and prevents the ship from making changes or maneuvers for 1d4 hours. Bomb bays and missile tubes are an exception to this rule; they can be reloaded in space, as long as the ship is carrying extra ordnance in an internal magazine.

Finally, every launch system possesses a basic rate of fire, which indicates how many weapons it can fire, drop, or dispense in a single round. A missile tube must cycle through the process of bringing the next missile from the magazine to the rail and then firing it off, but a simple rack or cell system can torch off a number of missiles at the same time.

### Bomb Rack (PL 6)
As you might expect, this launch system is designed to carry bombs. Its capacity can’t be expanded, but a ship could buy and mount multiple bomb racks."""
text = text.replace(bad_launch_intro, good_launch_intro)

# Fix 4: Launch Systems Formatting
bad_launch_fmt = """Bomb Bay (PL 6): The bomb bay has a capacity of 40 light, 20 medium, or 10 heavy bombs. Its capacity can be expanded by 4 points (4 light, 2 medium, or 1 heavy bomb) for each additional hull point assigned to the system beyond the 10 hull points normally required. Minelayer (PL 6): This system consists of two or more mine rails, low-powered magnetic accelerators designed to deploy a pattern of mines into one hex adjacent to the launching ship in a single phase.

Unlike other launched weapons, at least ten mines (a single mine pattern) must be deployed to be effective. Since the minelayer also includes machinery for deploying the mines, it has half the capacity of other launch systems of a similar size. Missile Rack (PL 6): This is a system that can hold eight light missiles, four medium missiles, or two heavy missiles.

Its capacity can’t be increased, but it’s easy enough to buy

multiple missile racks. Missile Tube (PL 6): This is an internal missile storage and launch facility. Its basic capacity is twelve, and it can fire one missile per round.

While its rate of fire is inferior to the missile rack, the missile tube enjoys one advantage; it can be reloaded in space. Ordnance Cell Array (PL 7): This system is similar to the vertical launch cells of today’s naval vessels. Each missile is pre-loaded into a single cell or canister; the array consists of dozens of these canisters.

Bombs, mines, and missiles of various sizes and warheads can be carried as the shipbuilder sees fit, offering a great deal of tactical flexibility."""
good_launch_fmt = """### Bomb Bay (PL 6)
The bomb bay has a capacity of 40 light, 20 medium, or 10 heavy bombs. Its capacity can be expanded by 4 points (4 light, 2 medium, or 1 heavy bomb) for each additional hull point assigned to the system beyond the 10 hull points normally required.

### Minelayer (PL 6)
This system consists of two or more mine rails, low-powered magnetic accelerators designed to deploy a pattern of mines into one hex adjacent to the launching ship in a single phase. Unlike other launched weapons, at least ten mines (a single mine pattern) must be deployed to be effective. Since the minelayer also includes machinery for deploying the mines, it has half the capacity of other launch systems of a similar size.

### Missile Rack (PL 6)
This is a system that can hold eight light missiles, four medium missiles, or two heavy missiles. Its capacity can’t be increased, but it’s easy enough to buy multiple missile racks.

### Missile Tube (PL 6)
This is an internal missile storage and launch facility. Its basic capacity is twelve, and it can fire one missile per round. While its rate of fire is inferior to the missile rack, the missile tube enjoys one advantage; it can be reloaded in space.

### Ordnance Cell Array (PL 7)
This system is similar to the vertical launch cells of today’s naval vessels. Each missile is pre-loaded into a single cell or canister; the array consists of dozens of these canisters. Bombs, mines, and missiles of various sizes and warheads can be carried as the shipbuilder sees fit, offering a great deal of tactical flexibility."""
text = text.replace(bad_launch_fmt, good_launch_fmt)

# Fix 5: Tractor Beam Table
bad_tractor = """Multiple tractor beams can “combine” to capture larger vessels. If the tractor beam can affect the target, the firing ship can apply an acceleration of 0.25 Mpp per phase to the target vessel. If the firing ship has enough tractor beams to affect the target multiple times, this acceleration capacity increases as shown below:

### Weapon

For example, a destroyer mounts three tractor beams, so it can affect a target of up to 150 hull points."""
good_tractor = """Multiple tractor beams can “combine” to capture larger vessels. If the tractor beam can affect the target, the firing ship can apply an acceleration of 0.25 Mpp per phase to the target vessel. If the firing ship has enough tractor beams to affect the target multiple times, this acceleration capacity increases as shown below:

| Tractor Overage | Target Acceleration |
| --- | --- |
| 1x | 0.25 Mpp |
| 2x | 0.5 Mpp |
| 3x | 1 Mpp |
| 4x | 2 Mpp |
| 5x | 3 Mpp |
| 6x | 4 Mpp |
| 7x | 5 Mpp |
| 8x | 6 Mpp |
| 9x | 7 Mpp |
| 10x | 8 Mpp |

For example, a destroyer mounts three tractor beams, so it can affect a target of up to 150 hull points."""
text = text.replace(bad_tractor, good_tractor)

# Fix 6: Remove Bogus Tables from End
with open('fix_weapons_temp.md', 'w') as f:
    f.write(text)
