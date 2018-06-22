# Spell fragment card data

# Text -> ASCII Art: http://patorjk.com/software/taag/#p=display&f=Rectangles&t=Monster

# Data Format:
#   spell_card_data:
#     List of <pattern-info>
#
#   <pattern-info>:
#     <pattern>, List of <card>s that use pattern
#
#   <card>:
#     <title>, <attributes>, List of <description> strings
#
#   <attribute>:
#     'element': 'air', 'fire', 'earth', 'water' or 'none'
#     'category': <string> to group spells by general category
#     'starter': 'true' if this is a basic, starter spell

# Spell patterns are normalized:
#  * If spell has '@', then it should be in upper-left corner
#    * If not possible, then in top row as close as possible to upper-left corner
#      * If multiple options, then choose option with '.' in upper-left
#  * Else 'X' in upper-left corner. 
#  * Prefer wider spells over taller spells.

# Next id = 88

spell_card_revision = 2

spell_card_categories = [
	'attack-mage',
	'attack-tendril',
	'attack-charge',

	'create-tendril',

	'defend-mage',
	'defend-tendril',
	'defend-charge',

	'move-mage',
	'move-tendril',

	'move-other-mage',
	'move-other-tendril',

	'astral',
	'tapestry',
	'terrain',
]

spell_card_data = [

	#  _____         _           _    ___   
	# |   | |___ _ _| |_ ___ ___| |  |_  |  
	# | | | | -_| | |  _|  _| .'| |   _| |_ 
	# |_|___|___|___|_| |_| |__,|_|  |_____|
	#

	# +---+
	# | X |  Level 0 - Castable on all starting cards.
	# +---+
	[	[	"X",
		],
		[
		],
	],

	#  _____         _           _    ___ 
	# |   | |___ _ _| |_ ___ ___| |  |_  |
	# | | | | -_| | |  _|  _| .'| |  |  _|
	# |_|___|___|___|_| |_| |__,|_|  |___|
	#

	# +-----+
	# | X X |  Level 1 - Castable on all starting cards.
	# +-----+

	# +-----+
	# | X . |  Level 1 - Castable on all starting cards.
	# | . X |
	# +-----+

	# +-------+                                                   xx  xx
	# | X . X |  Level 1 - Castable on all starting cards except xx    xx
	# +-------+

	# +-------+                                                   x    x
	# | X . . |  Level 1 - Castable on all starting cards except xxx  xxx
	# | . . X |
	# +-------+
	[	[	"X . .",
			". . X",
		],
		[
		],
	],

	# +-------+
	# | X . . |  Level 2
	# | . . . |
	# | . . X |
	# +-------+

	# +---------+
	# | X . . X |  Level 2
	# +---------+

	# +---------+
	# | X . . . |  Level 2
	# | . . . X |
	# +---------+

	# +---------+
	# | X . . . |  Level 2
	# | . . . . |
	# | . . . X |
	# +---------+

	#  _____         _           _    ___ 
	# |   | |___ _ _| |_ ___ ___| |  |_  |
	# | | | | -_| | |  _|  _| .'| |  |_  |
	# |_|___|___|___|_| |_| |__,|_|  |___|
	#

	# +-------+
	# | X X X |  Level 2
	# +-------+

	# +-------+                                                   x    x
	# | X X . |  Level 2 - Castable on all starting cards except xxx  xxx
	# | . . X |
	# +-------+

	# +-----+
	# | X X |  Level 2 - Castable on all starting cards.
	# | . X |
	# +-----+

	# +-------+
	# | X . X |  Level 2
	# | . X . |
	# +-------+

	# +-------+
	# | X . . |  Level 3
	# | . X . |
	# | . . X |
	# +-------+

	#  _____ _                   _       _    ___        _      ___   
	# |   __| |___ _____ ___ ___| |_ ___| |  |_  |     _| |_   |_  |  
	# |   __| | -_|     | -_|   |  _| .'| |   _| |_   |_   _|   _| |_ 
	# |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |_____|    |_|    |_____|
	#

	# +-----+
	# | @ X |  Level 1
	# +-----+
	[	[	"@ X",
		],
		[
			["Haste",
				{'element': 'air', 'category': 'move-mage', 'id': 3},
				["Move 2 spaces, ignoring terrain cost."] ],
			["Protection",
				{'element': 'earth', 'category': 'defend-mage', 'id': 4},
				["Place a CHARGE on this spell.", "-", "Defend 1: This shield absorbs all damage from attacks.", "-", "Remove CHARGE when it takes 1 or more damage from a single attack."] ],
		],
	],

	# +-----+
	# | @ . |  Level 1
	# | . X |
	# +-----+
	[	[	"@ .",
			". X",
		],
		[
			["Fire Arrow",
				{'element': 'fire', 'category': 'attack-mage', 'id': 5},
				["Attack 1 at a TENDRIL you control.", "-", "Consume that TENDRIL."] ],
			["Creep",
				{'element': 'water', 'category': 'create-tendril,move-tendril', 'id': 73},
				["Place a TENDRIL.", "-", "Move a TENDRIL 3 spaces."] ],
		],
	],

	# +-------+
	# | @ . X |  Level 1
	# +-------+
	[	[	"@ .",
			". X",
		],
		[
			["Quick Drop",
				{'element': 'air', 'category': 'move-mage,create-tendril', 'id': 66},
				["Move 4 spaces, ignoring terrain cost.", "You may place a TENDRIL in your final location."] ],
			["Recovery Shield",
				{'element': 'earth', 'category': 'defend-mage,tapestry', 'id': 82},
				["Place a CHARGE on this spell.", "-", "Defend 1: This shield absorbs all damage from attacks.", "-", "Remove CHARGE and recover 2 mana from your TAPESTRY when it takes 1 or more damage from a single attack."] ],
		],
	],

	# +-------+
	# | @ . . |  Level 1
	# | . . X |
	# +-------+
	[	[	"@ . .",
			". . X",
		],
		[
			["Ricochet Blast",
				{'element': 'fire', 'category': 'attack-mage', 'id': 24},
				["Attack 1 at location adjacent to a TENDRIL you control.", "-", "Consume that TENDRIL."] ],
		],
	],

	# +-------+
	# | @ . . |  Level 2
	# | . . . |
	# | . . X |
	# +-------+
	[	[	"@ . .",
			". . .",
			". . X",
		],
		[
			["Tendril Shield",
				{'element': 'earth', 'category': 'defend-mage,defend-tendril', 'id': 83},
				["Place a CHARGE on this spell.", "-", "Defend 1.", "-", "You may choose to remove this CHARGE to prevent a TENDRIL you control from being removed."] ],
		],
	],

	# +---------+
	# | @ . . X |  Level 2
	# +---------+
	[	[	"@ . . X",
		],
		[
			["Teleport",
				{'element': 'water', 'category': 'move-mage', 'id': 78},
				["Teleport to a location with a TENDRIL you control.", "-", "Consume that TENDRIL."] ],
		],
	],

	# +---------+
	# | @ . . . |  Level 2
	# | . . . X |
	# +---------+

	# +---------+
	# | @ . . . |  Level 2
	# | . . . . |
	# | . . . X |
	# +---------+

	#  _____ _                   _       _    ___        _      ___ 
	# |   __| |___ _____ ___ ___| |_ ___| |  |_  |     _| |_   |_  |
	# |   __| | -_|     | -_|   |  _| .'| |   _| |_   |_   _|  |  _|
	# |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |_____|    |_|    |___|
	#

	# +-------+                     +-----+
	# | X @ X |  Level 2 - Built on | @ X |
	# +-------+                     +-----+
	[	[	"X @ X",
		],
		[
		],
	],

	# +-----+                     +-----+
	# | @ X |  Level 2 - Built on | @ X |
	# | X . |                     +-----+
	# +-----+
	[	[	"@ X",
			"X .",
		],
		[
			["Double Shield",
				{'element': 'earth', 'category': 'defend-mage', 'id': 36},
				["Place a CHARGE on this spell.", "-", "Defend 2."] ],
		],
	],

	# +-------+                     +-----+     +-----+
	# | . @ X |  Level 2 - Built on | @ X | and | @ . | 
	# | X . . |                     +-----+     | . X |
	# +-------+                                 +-----+
	[	[	". @ X",
			"X . .",
		],
		[
		],
	],

	# +-----+                     +-----+     +-----+
	# | @ . |  Level 2 - Built on | @ X | and | @ . |
	# | X X |                     +-----+     | . X |
	# +-----+                                 +-----+
	[	[	"@ .",
			"X X",
		],
		[
			["Rock Back",
				{'element': 'earth', 'category': 'defend-mage,attack-mage', 'id': 88},
				["Place a CHARGE on this spell.", "-", "When CHARGEd, you take 1/2 damage (rounded down) from attacks.", "-", "Full attack damage is reflected back at your attacker."] ],
		],
	],

	# +-------+                     +-----+     +-------+
	# | @ X X |  Level 2 - Built on | @ X | and | @ . X |
	# +-------+                     +-----+     +-------+
	[	[	"@ X X",
		],
		[
			["Push",
				{'element': 'air', 'category': 'move-mage,move-other-mage', 'id': 70},
				["Push mage out of an adjacent location and then move into that location."] ],
		],
	],

	# +---------+                     +-----+     +-------+
	# | X @ . X |  Level 3 - Built on | @ X | and | @ . X |
	# +---------+                     +-----+     +-------+
	[	[	"X @ . X",
		],
		[
			["Plains Walker",
				{'element': 'air', 'category': 'move-mage,terrain', 'id': 7},
				["Move through up to 6 contiguous Plains locations."] ],
			["Meteor Shower",
				{'element': 'earth', 'category': 'attack-charge', 'id': 84},
				["Remove all CHARGEs from all mages at a TENDRIL you control."] ],
		],
	],

	# +-------+                     +-----+     +-------+
	# | @ . X |  Level 2 - Built on | @ X | and | @ . X |
	# | X . . |                     +-----+     +-------+
	# +-------+
	[	[	"@ . X",
			"X . .",
		],
		[
			["Water Moccasins",
				{'element': 'air', 'category': 'move-mage,terrain', 'id': 54},
				["Place a CHARGE on this spell.", "-", "When CHARGEd, you may move into or across Water locations.", "-", "When CHARGEd and you are in a location adjacent to a River, you may place a TENDRIL in your location."] ],
		],
	],


	# +-------+                     +-----+     +-------+
	# | @ X . |  Level 2 - Built on | @ X | and | @ . . |
	# | . . X |                     +-----+     | . . X |
	# +-------+                                 +-------+
	[	[	"@ X .",
			". . X",
		],
		[
			["Run and Toss",
				{'element': 'air', 'category': 'move-mage,create-tendril,move-tendril', 'id': 67},
				["Move 2, place TENDRIL, then move that TENDRIL 3 spaces."] ],
			["Nudge",
				{'element': 'earth', 'category': 'defend-mage,move-other-tendril', 'id': 85},
				["Place a CHARGE on this spell.", "-", "Defend 1.", "-", "When CHARGEd and another mage's TENDRIL is in the same location or adjacent to one of your TENDRILs, you may move their TENDRIL 1 space."] ],
		],
	],

	# +-------+                     +-----+     +-------+
	# | @ . . |  Level 2 - Built on | @ X | and | @ . . |
	# | X . X |                     +-----+     | . . X |
	# +-------+                                 +-------+
	[	[	"@ . .",
			"X . X",
		],
		[
			["Creepy Shield",
				{'element': 'earth', 'category': 'defend-mage,move-tendril', 'id': 86},
				["Place a CHARGE on this spell.", "-", "Defend 1.", "-", "When CHARGEd, you may move a TENDRIL you control 1 space."] ],
		],
	],

	# +---------+                     +-----+     +-------+
	# | X @ . . |  Level 3 - Built on | @ X | and | @ . . |
	# | . . . X |                     +-----+     | . . X |
	# +---------+                                 +-------+
	[	[	"X @ . .",
			". . . X",
		],
		[
			["Sneaky Stab",
				{'element': 'fire', 'category': 'attack-mage,move-mage', 'id': 64},
				["Attack 1 at an adjacent location to a TENDRIL you control and then move into that location."] ],
		],
	],

	# +-------+                     +-----+     +-------+
	# | X . . |  Level 3 - Built on | @ X | and | @ . . |
	# | @ . . |                     +-----+     | . . X |
	# | . . X |                                 +-------+
	# +-------+
	[	[	"X . .",
			"@ . .",
			". . X",
		],
		[
			["Barrier",
				{'element': 'earth', 'category': 'defend-mage,terrain', 'id': 87},
				["Place a CHARGE on this spell.", "-", "Defend 1.", "-", "When CHARGEd, all your TENDRILs are obstacles that other mages may not move into."] ],
		],
	],

	# +---------+                     +-----+     +---------+
	# | @ X . X |  Level 3 - Built on | @ X | and | @ . . X |
	# +---------+                     +-----+     +---------+
	[	[	"@ X . X",
		],
		[
			["Double Attack",
				{'element': 'air', 'category': 'attack-charge', 'id': 71},
				["A mage at a TENDRIL you control must remove 2 of their CHARGEs."] ],
		],
	],

	# +-----------+                     +-----+     +---------+
	# | X @ . . X |  Level 3 - Built on | @ X | and | @ . . X |
	# +-----------+                     +-----+     +---------+

	# +---------+                     +-----+     +---------+
	# | @ . . X |  Level 3 - Built on | @ X | and | @ . . X |
	# | X . . . |                     +-----+     +---------+
	# +---------+
	[	[	"@ . . X",
			"X . . .",
		],
		[
			["Remove Shield",
				{'element': 'air', 'category': 'attack-charge', 'id': 72},
				["If in a location with a TENDRIL controlled by another mage, you may remove a CHARGE from one of their spells."] ],
		],
	],

	# +---------+                     +-----+     +---------+
	# | @ X . . |  Level 3 - Built on | @ X | and | @ . . . |
	# | . . . X |                     +-----+     | . . . X |
	# +---------+                                 +---------+
	[	[	"@ X . .",
			". . . X",
		],
		[
			["Snapback",
				{'element': 'water', 'category': 'defend-mage,move-tendril', 'id': 79},
				["Place a CHARGE on this spell.", "-", "When CHARGEd, you may sacrifice a TENDRIL to Defend 1.", "-", "Place sacrificed TENDRIL at the location of the mage who attacked you."] ],
		],
	],

	# +---------+                     +-----+     +---------+
	# | @ . . . |  Level 3 - Built on | @ X | and | @ . . . |
	# | X . . X |                     +-----+     | . . . X |
	# +---------+                                 +---------+
	[	[	"@ . . .",
			"X . . X",
		],
		[
			["Deflect",
				{'element': 'water', 'category': 'defend-mage,attack-mage,attack-tendril', 'id': 80},
				["Place a CHARGE on this spell.", "-", "You may remove this CHARGE when attacked to deflect the attack to an adjacent location.", "-", "Attack 1 and remove all TENDRILs from that location."] ],
		],
	],

	# +-----------+                     +-----+     +---------+
	# | X @ . . . |  Level 3 - Built on | @ X | and | @ . . . |
	# | . . . . X |                     +-----+     | . . . X |
	# +-----------+                                 +---------+

	# +---------+                     +-----+     +---------+
	# | X . . . |  Level 3 - Built on | @ X | and | @ . . . |
	# | @ . . . |                     +-----+     | . . . X |
	# | . . . X |                                 +---------+
	# +---------+

	# +-------+                     +-----+
	# | . @ . |  Level 2 - Built on | @ . |
	# | X . X |                     | . X |
	# +-------+                     +-----+
	[
		[	". @ .",
			"X . X",
		],
		[
			["Fire Burst",
				{'element': 'fire', 'category': 'attack-mage', 'id': 23},
				["Attack for 1 damage in all locations adjacent to a TENDRIL you control.", "-", "Consume that TENDRIL."] ],
		],
	],

	# +-------+                     +-----+
	# | X . . |  Level 3 - Built on | @ . |
	# | . @ . |                     | . X |
	# | . . X |                     +-----+
	# +-------+
	[
		[	"X . .",
			". @ .",
			". . X",
		],
		[
			["Spread",
				{'element': 'water', 'category': 'create-tendril,move-tendril', 'id': 75},
				["Place a TENDRIL.", "-", "Move all TENDRILs 1 space."] ],
		],
	],

	# +-------+                     +-----+     +-------+
	# | @ . X |  Level 2 - Built on | @ . | and | @ . X |
	# | . X . |                     | . X |     +-------+
	# +-------+                     +-----+
	[
		[	"@ . X",
			". X .",
		],
		[
			["Whiplash",
				{'element': 'water', 'category': 'defend-mage', 'id': 76},
				["Place a CHARGE on this spell.", "-", "When CHARGEd, you may sacrifice a TENDRIL to Defend 1."] ],
		],
	],

	# +---------+                     +-----+     +-------+
	# | . @ . X |  Level 3 - Built on | @ . | and | @ . X |
	# | X . . . |                     | . X |     +-------+
	# +---------+                     +-----+
	[
		[	". @ . X",
			"X . . .",
		],
		[
			["Hands of Flame",
				{'element': 'fire', 'category': 'move-mage,attack-mage', 'id': 63},
				["Move 1 and then Attack 1 at a location adjacent to your new location."] ],
			["Tendril Coil",
				{'element': 'water', 'category': 'defend-mage', 'id': 81},
				["Place a CHARGE on this spell.", "-", "When CHARGEd and you are at a location with a TENDRIL you control, that TENDRIL acts as a shield to Defend 2."] ],
		],
	],

	# +-------+                     +-----+     +-------+
	# | @ . . |  Level 2 - Built on | @ . | and | @ . . |
	# | . X X |                     | . X |     | . . X |
	# +-------+                     +-----+     +-------+
	[
		[	"@ . .",
			". X X",
		],
		[
		],
	],

	# +---------+                     +-----+     +-------+
	# | . @ . . |  Level 3 - Built on | @ . | and | @ . . |
	# | X . . X |                     | . X |     | . . X |
	# +---------+                     +-----+     +-------+
	[
		[	". @ . .",
			"X . . X",
		],
		[
			["Burst",
				{'element': 'water', 'category': 'create-tendril,move-tendril', 'id': 74},
				["Place 3 TENDRILs.", "-", "Move all TENDRILs 2 spaces."] ],
		],
	],

	# +---------+                     +-----+     +-------+
	# | X . . . |  Level 3 - Built on | @ . | and | @ . . |
	# | . @ . . |                     | . X |     | . . X |
	# | . . . X |                     +-----+     +-------+
	# +---------+
	[	[	"X . . .",
			". @ . .",
			". . . X",
		],
		[
			["Delete All",
				{'element': 'fire', 'category': 'attack-tendril', 'id': 43},
				["Remove all TENDRILs from your location."] ],
		],
	],

	# +-------+                     +-----+     +-------+
	# | . @ . |  Level 3 - Built on | @ . | and | @ . . |
	# | X . . |                     | . X |     | . . X |
	# | . . X |                     +-----+     +-------+
	# +-------+
	[	[	". @ .",
			"X . .",
			". . X",
		],
		[
			["Fire Ball",
				{'element': 'fire', 'category': 'attack-mage', 'id': 22},
				["Attack for 2 damage at a TENDRIL you control.", "-", "Consume that TENDRIL."] ],
		],
	],

	# +-------+                     +-----+     +-------+
	# | @ . . |  Level 3 - Built on | @ . | and | @ . . |
	# | . X . |                     | . X |     | . . . |
	# | . . X |                     +-----+     | . . X |
	# +-------+                                 +-------+
	[	[	"@ . .",
			". X .",
			". . X",
		],
		[
			["Fire Reign",
				{'element': 'fire', 'category': 'attack-mage', 'id': 26},
				["Attack for 1 damage at every TENDRIL you control.", "-", "Consume all of your TENDRILs except one."] ],
		],
	],

	# +---------+                     +-----+     +---------+
	# | @ . . X |  Level 3 - Built on | @ . | and | @ . . X |
	# | . X . . |                     | . X |     +---------+
	# +---------+                     +-----+
	[	[	"@ . . X",
			". X . .",
		],
		[
			["Erase",
				{'element': 'fire', 'category': 'move-tendril,attack-tendril', 'id': 65},
				["Move a TENDRIL you control 3 spaces, removing all other TENDRILs from its starting location and all locations it moves into.", "-", "Consume the TENDRIL you moved for this spell."] ],
		],
	],

	# +-----------+                     +-----+     +---------+
	# | . @ . . X |  Level 3 - Built on | @ . | and | @ . . X |
	# | X . . . . |                     | . X |     +---------+
	# +-----------+                     +-----+
	[	[	". @ . . X",
			"X . . . .",
		],
		[
		],
	],

	# +---------+                     +-----+     +---------+
	# | @ . . . |  Level 3 - Built on | @ . | and | @ . . . |
	# | . X . X |                     | . X |     | . . . X |
	# +---------+                     +-----+     +---------+
	[	[	"@ . . .",
			". X . X",
		],
		[
			["Diasporate",
				{'element': 'water', 'category': 'create-tendril,move-tendril', 'id': 77},
				["Place 4 TENDRILs in neighboring locations.", "-", "Move all TENDRILs 2 spaces."] ],
		],
	],

	# +---------+                     +-----+     +---------+
	# | . X . . |  Level 3 - Built on | @ . | and | @ . . . |
	# | @ . . . |                     | . X |     | . . . X |
	# | . . . X |                     +-----+     +---------+
	# +---------+

	# +-----------+                     +-----+     +---------+
	# | . @ . . . |  Level 3 - Built on | @ . | and | @ . . . |
	# | X . . . X |                     | . X |     | . . . X |
	# +-----------+                     +-----+     +---------+

	# +-----------+                     +-----+     +---------+
	# | X . . . . |  Level 3 - Built on | @ . | and | @ . . . |
	# | . @ . . . |                     | . X |     | . . . X |
	# | . . . . X |                     +-----+     +---------+
	# +-----------+
	
	# +---------+                     +-----+     +---------=
	# | @ . . . |  Level 3 - Build on | @ . | and | @ . . . |
	# | . X . . |                     | . X |     | . . . . |
	# | . . . X |                     +-----+     | . . . X |
	# +---------+                                 +---------+
	# + 3 variants

	# +-----------+                     +-------+
	# | X . @ . X |  Level 3 - Built on | @ . X |
	# +-----------+                     +-------+
	[	[	"X . @ . X",
		],
		[
		],
	],

	# +-------+                     +-------+
	# | @ . X |  Level 3 - Build on | @ . X |
	# | . . . |                     +-------+
	# | X . . |
	# +-------+

	# +-------+                     +-------+     +-------+
	# | @ . X |  Level 2 - Built on | @ . X | and | @ . . |
	# | . . X |                     +-------+     | . . X |
	# +-------+                                   +-------+
	[	[	"@ . X",
			". . X",
		],
		[
			["Follow",
				{'element': 'air', 'category': 'move-mage,create-tendril', 'id': 69},
				["Move 3. If in a location with a TENDRIL controlled by another mage, place a TENDRIL at that mage's location and remove their TENDRIL in your location."] ],
		],
	],

	# +-------+                     +-------+     +-------+
	# | @ . X |  Level 2 - Built on | @ . X | and | @ . . |
	# | . . . |                     +-------+     | . . X |
	# | . X . |                                   +-------+
	# +-------+
	[	[	"@ . X",
			". . .",
			". X .",
		],
		[
		],
	],

	# +-----------+                     +-------+     +-------+
	# | X . @ . . |  Level 3 - Built on | @ . X | and | @ . . |
	# | . . . . X |                     +-------+     | . . X |
	# +-----------+                                   +-------+

	# +---------+                     +-------+     +-------+
	# | . @ . X |  Level 2 - Built on | @ . X | and | @ . . |
	# | . . . . |                     +-------+     | . . X |
	# | X . . . |                                   +-------+
	# +---------+

	# +---------+                     +-------+     +---------+
	# | @ . X X |  Level 3 - Built on | @ . X | and | @ . . X |
	# +---------+                     +-------+     +---------+
	# + 3 variants

	# +---------+                     +-------+     +---------+
	# | @ . X . |  Level 3 - Built on | @ . X | and | @ . . . |
	# | . . . X |                     +-------+     | . . . X |
	# +---------+                                   +---------+
	# + 3 variants

	# +-----------+                     +-------+     +-----------+
	# | @ . X . . |  Level 3 - Built on | @ . X | and | @ . . . . |
	# | . . . . X |                     +-------+     | . . . . X |
	# +-----------+                                   +-----------+
	# + 3 variants

	# +-------+                     +-------+
	# | . @ . |  Level 3 - Built on | @ . . |
	# | . . . |                     | . . X |
	# | X . X |                     +-------+
	# +-------+

	# +---------+                     +-------+
	# | . @ . . |  Level 3 - Built on | @ . . |
	# | . . . X |                     | . . X |
	# | X . . . |                     +-------+
	# +---------+

	# +-----------+                     +-------+
	# | . . @ . . |  Level 3 - Built on | @ . . |
	# | X . . . X |                     | . . X |
	# +-----------+                     +-------+

	# +-----------+                     +-------+
	# | X . . . . |  Level 3 - Built on | @ . . |
	# | . . @ . . |                     | . . X |
	# | . . . . X |                     +-------+
	# +-----------+

	# +---------+                     +-------+
	# | . . . X |  Level 3 - Built on | @ . . |
	# | . @ . . |                     | . . X |
	# | . . . . |                     +-------+
	# | X . . . |
	# +---------+

	# +---------+                     +-------+     +---------+
	# | @ . . X |  Level 3 - Built on | @ . . | and | @ . . X |
	# | . . X . |                     | . . X |     +---------+
	# +---------+                     +-------+
	# + 3 variants

	# +---------+                     +-------+     +---------+
	# | @ . . . |  Level 3 - Built on | @ . . | and | @ . . . |
	# | . . X X |                     | . . X |     | . . . X |
	# +---------+                     +-------+     +---------+
	# + 3 variants

	# +---------+                     +-------+     +---------+
	# | @ . . . |  Level 3 - Built on | @ . . | and | @ . . . |
	# | . . X . |                     | . . X |     | . . . . |
	# | . . . X |                     +-------+     | . . . X |
	# +---------+                                   +---------+
	# + 3 variants

	# +-----------+                     +-------+     +-----------+
	# | @ . . . X |  Level 3 - Built on | @ . . | and | @ . . . X |
	# | . . X . . |                     | . . X |     +-----------+
	# +-----------+                     +-------+
	# + 3 variants

	# +-----------+                     +-------+     +-----------+
	# | @ . . . . |  Level 3 - Built on | @ . . | and | @ . . . . |
	# | . . X . X |                     | . . X |     | . . . . X |
	# +-----------+                     +-------+     +-----------+
	# + 3 variants

	# +-----------+                     +-------+     +-----------+
	# | @ . . . . |  Level 3 - Built on | @ . . | and | @ . . . . |
	# | . . X . . |                     | . . X |     | . . . . . |
	# | . . . . X |                     +-------+     | . . . . X |
	# +-----------+                                   +-----------+
	# + 3 variants

	#  _____ _                   _       _    ___        _      ___ 
	# |   __| |___ _____ ___ ___| |_ ___| |  |_  |     _| |_   |_  |
	# |   __| | -_|     | -_|   |  _| .'| |   _| |_   |_   _|  |_  |
	# |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |_____|    |_|    |___|
	#

	# +-------+                     +-----+     +-------+
	# | @ . X |  Level 4 - Built on | @ . | and | @ . X |
	# | . X . |                     | . X |     +-------+
	# | X . . |                     +-----+
	# +-------+

	# +-------+                     +-----+     +-------+
	# | @ X . |  Level 4 - Build on | @ X | and | @ . . |
	# | X . . |                     +-----+     | . . . |
	# | . . X |                                 | . . X |
	# +-------+                                 +-------+

	# +-------+                     +-------+     +-------+
	# | @ . X |  Level 4 - Build on | @ . X | and | @ . . |
	# | . . . |                     +-------+     | . . . |
	# | X . X |                                   | . . X |
	# +-------+                                   +-------+

	#  _____ _                   _       _    ___      _      ___   
	# |   __| |___ _____ ___ ___| |_ ___| |  |_  |   _| |_   |_  |  
	# |   __| | -_|     | -_|   |  _| .'| |  |  _|  |_   _|   _| |_ 
	# |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |___|    |_|    |_____|
	#

	# +-------+                     +-----+
	# | @ X @ |  Level 2 - Built on | @ X |
	# +-------+                     +-----+

	# +-----+                     +-----+
	# | @ X |  Level 2 - Built on | @ X |
	# | . @ |                     +-----+
	# +-----+

	# +-------+                     +-----+     +-------+
	# | @ @ X |  Level 2 - Built on | @ X | and | @ . X |
	# +-------+                     +-----+     +-------+

	# +-------+                     +-----+
	# | @ . . |  Level 3 - Built on | @ . |
	# | . X . |                     | . X |
	# | . . @ |                     +-----+
	# +-------+
	[
		[	"@ . .",
			". X .",
			". . @",
		],
		[
		],
	],

	# +-------+                     +-----+
	# | @ . @ |  Level 2 - Built on | @ . |
	# | . X . |                     | . X |
	# +-------+                     +-----+
	[
		[	"@ . @",
			". X .",
		],
		[
		],
	],

	# +-----------+                     +-------+
	# | @ . . . . |  Level 3 - Built on | @ . . |
	# | . . X . . |                     | . . X |
	# | . . . . @ |                     +-------+
	# +-----------+
	[
		[	"@ . . . .",
			". . X . .",
			". . . . @",
		],
		[
		],
	],

	#  _____ _                   _       _    ___      _      ___ 
	# |   __| |___ _____ ___ ___| |_ ___| |  |_  |   _| |_   |_  |
	# |   __| | -_|     | -_|   |  _| .'| |  |  _|  |_   _|  |  _|
	# |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |___|    |_|    |___|
	#

	# +-----+                     +-----+
	# | @ X |  Level 3 - Built on | @ X |
	# | X @ |                     +-----+
	# +-----+
	[
		[	"@ X",
		 	"X @",
		],
		[
		],
	],

	# +-------+                     +-----+
	# | @ X . |  Level 3 - Built on | @ X |
	# | . @ X |                     +-----+
	# +-------+
	[
		[	"@ X .",
		 	". @ X",
		],
		[
		],
	],

	# +-------+                     +-----+
	# | X . . |  Level 4 - Built on | @ X |
	# | @ . . |                     +-----+
	# | . @ X |
	# +-------+

	# +---------+                     +-----+
	# | X @ . . |  Level 3 - Built on | @ X |
	# | . . @ X |                     +-----+
	# +---------+
	[
		[	"X @ . .",
		 	". . @ X",
		],
		[
		],
	],

	# +-------+                     +-----+
	# | @ . . |  Level 3 - Built on | @ X |
	# | X @ X |                     +-----+
	# +-------+

	# +-------+                     +-----+
	# | . @ . |  Level 4 - Built on | @ . |
	# | X . X |                     | . X |
	# | . @ . |                     +-----+
	# +-------+
	[
		[	". @ .",
		 	"X . X",
			". @ .",
		],
		[
		],
	],

	# +---------+                     +-----+
	# | . @ @ . |  Level 4 - Built on | @ . |
	# | X . . X |                     | . X |
	# +---------+                     +-----+

	# +---------+                     +-----+
	# | X . . . |  Level 4 - Built on | @ . |
	# | . @ @ . |                     | . X |
	# | . . . X |                     +-----+
	# +---------+

]

_unused_ = [

	# Create Tendril
			["Split",
				{'element': 'earth', 'category': 'tendril', 'id': 8},
				["Place a new TENDRIL in the same location where you already control a TENDRIL."] ],
			["Reverse Tendril",
				{'element': 'water', 'category': 'tendril', 'id': 52},
				["When in the same location as an opponent's TENDRIL, add a TENDRIL at the opponent's location."] ],
			["Forest Bind",
				{'element': 'air', 'category': 'tendril,terrain', 'id': 14},
				["When in a Forest location, add a TENDRIL to any location in Forest that is smaller in size than the one you occupy."] ],
			["Water Hop",
				{'element': 'water', 'category': 'tendril,terrain', 'id': 61},
				["When next to a river or Water location, add a TENDRIL to any location adjacent to that water.", "-", "Restrictions:", "* Rivers: Without passing a bridge", "* Water: Crossing 3 water locations max."] ],
			["Water Jump",
				{'element': 'water', 'category': 'tendril,terrain', 'id': 62},
				["When next to a river or Water location, add a TENDRIL to any location adjacent to that water.", "-", "Restrictions:", "* Rivers: Passing at most 1 bridge", "* Water: Crossing 5 water locations max."] ],
			["Duplicate",
				{'element': 'water', 'category': 'tendril', 'id': 53},
				["When in the same location as an opponent's TENDRIL, add a TENDRIL at any location where that opponent controls a TENDRIL."] ],

	# Move Tendril
			["Creep",
				{'element': 'none', 'category': 'tendril', 'id': 1},
				["Move a TENDRIL you control one space in any direction."] ],
			["Plains Link",
				{'element': 'air', 'category': 'tendril,terrain', 'id': 15},
				["Move a TENDRIL you control that is in a Plains location up to 7 spaces through connecting Plains locations."] ],
			["Water Skip",
				{'element': 'water', 'category': 'tendril,terrain', 'id': 60},
				["Move a TENDRIL you control that is adjacent to a river or water location into any other space adjacent to that river or water location.", "-", "Restrictions:", "* Rivers: Without passing a bridge", "* Water: Crossing 4 water locations max."] ],
			["Forest Link Minor",
				{'element': 'air', 'category': 'tendril,terrain', 'id': 16},
				["Move a TENDRIL you control that is in a Forest location to another location in any Forest of size 1 or 2."] ],
			["Forest Link",
				{'element': 'air', 'category': 'tendril,terrain', 'id': 17},
				["Move a TENDRIL you control that is in a Forest location to another location in any Forest that is smaller then the Forest with the TENDRIL."] ],
			["Mountain Link",
				{'element': 'air', 'category': 'tendril,terrain', 'id': 18},
				["Move a TENDRIL you control that is in a Mountain location to any other Mountain location."] ],
			["Exchange Tendril",
				{'element': 'water', 'category': 'tendril', 'id': 51},
				["Exchange locations with a TENDRIL you control."] ],
			["Scatter",
				{'element': 'fire', 'category': 'tendril', 'id': 30},
				["Move all TENDRILs you control 1 space."] ],
			["Scatter Far",
				{'element': 'fire', 'category': 'tendril', 'id': 32},
				["Move any 2 TENDRILs you control a total of 9 spaces."] ],
			["Scatter Wide",
				{'element': 'fire', 'category': 'tendril', 'id': 31},
				["Move TENDRILs you control a total of 5 spaces, split amongst any number of TENDRILs."] ],

	# Attack Tendril
			["Selective Prune",
				{'element': 'earth', 'category': 'tendril,attack', 'id': 41},
				["Remove all TENDRILs (except the one used for this spell) from a location where you control a TENDRIL."] ],
			["Prune Neighbor",
				{'element': 'earth', 'category': 'tendril,attack', 'id': 42},
				["Remove all TENDRILs from a location adjacent to where you control a TENDRIL."] ],
			["Whirlwind",
				{'element': 'air', 'category': 'tendril', 'id': 13},
				["Place CHARGE on this spell.", "-", "While CHARGEd, all TENDRILs you control are obstacles that other mages may not move into or pass through."] ],
			["Delete All 2",
				{'element': 'earth', 'category': 'tendril,attack', 'id': 43},
				["When in a location with a TENDRIL controlled by another mage, remove all of that mage's TENDRILs.", "-", "If multiple mages, choose one."] ],
			["Distraction",
				{'element': 'fire', 'category': 'tendril', 'id': 34},
				["When in the same location as a TENDRIL controlled by another mage, remove any one of their TENDRILs."] ],

	# Astral
			["Return",
				{'element': 'none', 'category': 'astral', 'id': 2},
				["When in the Astral Plane, return to the Physical Realm at a TENDRIL you control or at your home location."] ],
			["Teleport Away",
				{'element': 'water', 'category': 'astral', 'id': 6},
				["Move yourself to the Astral Plane."] ],
			["Teleport Other",
				{'element': 'water', 'category': 'astral', 'id': 49},
				["Move a mage in the same location as a TENDRIL you control to the Astral Plane."] ],
			["Return Other",
				{'element': 'water', 'category': 'astral', 'id': 50},
				["Move a mage in the Astral Plane to any TENDRIL you control."] ],

	# Move
			["Levitate",
				{'element': 'air', 'category': 'move', 'id': 9},
				["Place a CHARGE on this spell.", "-", "Spend CHARGE to ignore terrain cost and effects when you move into (or are forced into) a location."] ],
			["Fly",
				{'element': 'air', 'category': 'move', 'id': 10},
				["Ignore terrain cost and effects when moving into 4 locations this turn."] ],
			["Forest Run",
				{'element': 'air', 'category': 'terrain,move', 'id': 11},
				["If in or next to a Forest location, pay terrain cost to move into any location within or adjacent to that Forest, bypassing any obstacles."] ],
			["Mountain Climb",
				{'element': 'air', 'category': 'terrain,move', 'id': 12},
				["If in or next to a Mountain location, pay terrain cost to move into any location within or adjacent to that Mountain Range, bypassing any obstacles."] ],
			["Mountain Ranger",
				{'element': 'earth', 'category': 'terrain,move', 'id': 44},
				["If in a Mountain location, add a TENDRIL to a location in any Mountain range."] ],
			["River Run",
				{'element': 'water', 'category': 'move,terrain', 'id': 55},
				["If next to a river or water location, pay terrain cost to move into any other space adjacent to that river or water location.", "-", "Restrictions:", "* Rivers: Without passing a bridge", "* Water: Crossing 4 water locations max."] ],
			["Mountain Reach",
				{'element': 'earth', 'category': 'terrain,move', 'id': 45},
				["If in or adjacent to a Mountain location, add a TENDRIL to any location in a 1- or 2-size Mountain range."] ],

	# Protection
			["Shield Boost",
				{'element': 'earth', 'category': 'defend', 'id': 37},
				["Place a CHARGE on this spell.", "-", "Spend this CHARGE to boost the defense power of any spell by 1."] ],
			["Reactive Shield",
				{'element': 'earth', 'category': 'defend', 'id': 38},
				["Place a CHARGE on this spell.", "-", "When in the same location as a TENDRIL controlled by another mage, this shield absorbs all damage from attacks.", "-", "Remove CHARGE when it takes 3 or more damage from a single attack."] ],
			["Recovery Shield",
				{'element': 'water', 'category': 'defend,tapestry', 'id': 57},
				["Place a CHARGE on this spell.", "-", "When CHARGEd, this shield absorbs all damage from attacks.", "-", "Remove CHARGE and 2 THREADs from your TAPESTRY when it takes 1 or more damage from a single attack."] ],
			["Resist Shield",
				{'element': 'earth', 'category': 'defend,tendril', 'id': 40},
				["Place a CHARGE on this spell.", "-", "When CHARGEd, this shield absorbs all damage from attacks and prevents others from placing new TENDRILs on your location.", "-", "Remove CHARGE when it takes 1 or more damage from a single attack."] ],
			["Anchor Shield",
				{'element': 'earth', 'category': 'move,defend', 'id': 39},
				["Place a CHARGE on this spell.", "-", "When CHARGEd, this shield absorbs all damage from attacks and prevents you from being involuntary moved out of your location.", "-", "Remove CHARGE when it takes 1 or more damage from a single attack."] ],
			["Blur",
				{'element': 'air', 'category': 'defend', 'id': 19},
				["Place a CHARGE on this spell.", "-", "Spend a CHARGE at any time to move into a neighboring location ignoring terrain cost."] ],
			["Reflection Shield",
				{'element': 'fire', 'category': 'defend,attack', 'id': 35},
				["Place 1 charge on this spell.", "-", "Spend a charge at any time to protect against 1 or more points of damage and reflect 1 point of damage back at the attacker."] ],

	# Attack
			["Fire Boost",
				{'element': 'fire', 'category': 'attack', 'id': 27},
				["Place a CHARGE on this spell.", "-", "Spend this CHARGE to boost the attack power of any spell by 1."] ],
			["Forest Fire",
				{'element': 'fire', 'category': 'attack,terrain', 'id': 29},
				["Attack for 2 all locations in a Forest with a TENDRIL you control."] ],
			["Boulder Tumble",
				{'element': 'fire', 'category': 'attack,terrain', 'id': 28},
				["Attack for 3 all neighboring locations to a TENDRIL you control that is in a Mountain location."] ],
			["Prune",
				{'element': 'fire', 'category': 'attack,tendril', 'id': 33},
				["Remove all TENDRILs from a location where you control a TENDRIL.", "-", "Yes, that includes the TENDRIL used to cast this spell."] ],
			["Wall of Flame",
				{'element': 'fire', 'category': 'attack', 'id': 25},
				["Place CHARGE on this spell.", "-", "While CHARGEd, all groups of 3 adjacent TENDRILs you control are on fire and cause 1 damage.", "-", "CHARGE is lost immediately when you do not have 3 adjacent TENDRILs."] ],
			["Shield Pierce",
				{'element': 'air', 'category': 'attack', 'id': 21},
				["Cause 3 points of damage to all shields at a TENDRIL you control."] ],

	# Tapestry
			["Rest",
				{'element': 'water', 'category': 'tapestry', 'id': 58},
				["Move 2 THREADs on your TAPESTRY to empty positions."] ],
			["Recover",
				{'element': 'water', 'category': 'tapestry', 'id': 59},
				["Remove a THREAD from your TAPESTRY and place it back in your MANA POOL."] ],
			["Push",
				{'element': 'air', 'category': 'attack', 'id': 20},
				["Move into an adjacent location and push out all current occupants of that location into neighboring locations.", "-", "Former occupants get to choose where they move."] ],
			["Stone Cage",
				{'element': 'earth', 'category': 'attack', 'id': 47},
				["PLace a CHARGE on this spell.", "-", "While CHARGEd, there is a barrier at a TENDRIL you control that traps the occupants of that location and prevents them from moving out.", "-", "CHARGE is lost if the TENDRIL moves or if the barrier takes 1 damage."] ],
			["Trap",
				{'element': 'earth', 'category': 'attack', 'id': 48},
				["Place 1 charge on this spell.", "-", "When an opponent's TENDRIL moves into your location, that opponent takes 1 damage and this CHARGE is removed."] ],

	# Terrain
			["Flood",
				{'element': 'water', 'category': 'terrain', 'id': 56},
				["Place CHARGE on this spell.", "-", "While CHARGEd, all groups of 2 or more adjacent TENDRILs you control change all Plains locations to Water up to 3 spaces away from the TENDRILs.", "-", "CHARGE is lost immediately when you do not have 2 adjacent TENDRILs."] ],
			["Growth",
				{'element': 'earth', 'category': 'terrain', 'id': 46},
				["Place CHARGE on this spell.", "-", "While CHARGEd, all groups of 2 or more adjacent TENDRILs you control change all neighboring locations to Forest.", "-", "CHARGE is lost immediately when you do not have 2 adjacent TENDRILs."] ],
]
