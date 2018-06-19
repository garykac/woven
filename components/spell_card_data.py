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

spell_card_revision = 1

spell_card_data = [

	#  _____         _           _    ___   
	# |   | |___ _ _| |_ ___ ___| |  |_  |  
	# | | | | -_| | |  _|  _| .'| |   _| |_ 
	# |_|___|___|___|_| |_| |__,|_|  |_____|
	#

	# +---+
	# | X |  Level 0
	# +---+
	[	[	"X",
		],
		[
			["Creep",
				{'element': 'none', 'category': 'tendril', 'id': 1, 'starter': 'true'},
				["Move a TENDRIL you control one space in any direction."] ],
		],
	],

	#  _____         _           _    ___ 
	# |   | |___ _ _| |_ ___ ___| |  |_  |
	# | | | | -_| | |  _|  _| .'| |  |  _|
	# |_|___|___|___|_| |_| |__,|_|  |___|
	#

	# +-----+
	# | X X |  Level 1
	# +-----+

	# +-----+
	# | X . |  Level 1
	# | . X |
	# +-----+

	# +-------+
	# | X . X |  Level 1
	# +-------+

	# +-------+
	# | X . . |  Level 1
	# | . . X |
	# +-------+
	[	[	"X . .",
			". . X",
		],
		[
			["Return",
				{'element': 'none', 'category': 'astral', 'id': 2, 'starter': 'true'},
				["When in the Astral Plane, return to the Physical Realm at a TENDRIL you control or at your home location."] ],
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

	# +-------+
	# | X X . |  Level 2
	# | . . X |
	# +-------+

	# +-----+
	# | X X |  Level 2
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
				{'element': 'air', 'category': 'move', 'id': 3, 'starter': 'true'},
				["Gain 3 MP to use at any time during this turn:", "* 1MP - Move into Plains", "* 2MP - Move into Forest", "* 3MP - Move into Mountain"] ],
			["Protection",
				{'element': 'earth', 'category': 'defend', 'id': 4, 'starter': 'true'},
				["Place a charge on this spell.", "-", "This shield absorbs all damage from attacks.", "-", "Remove CHARGE when it takes 1 or more damage from a single attack."] ],
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
				{'element': 'fire', 'category': 'attack', 'id': 5, 'starter': 'true'},
				["Attack for 1 damage at a TENDRIL you control."] ],
			["Teleport Away",
				{'element': 'water', 'category': 'astral', 'id': 6, 'starter': 'true'},
				["Move yourself to the Astral Plane."] ],
		],
	],

	# +-------+
	# | @ . X |  Level 1
	# +-------+

	# +-------+
	# | @ . . |  Level 1
	# | . . X |
	# +-------+

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
			["Shield Boost",
				{'element': 'earth', 'category': 'defend', 'id': 37},
				["Place a CHARGE on this spell.", "-", "Spend this CHARGE to boost the defense power of any spell by 1."] ],
		],
	],

	# +---------+
	# | @ . . X |  Level 2
	# +---------+
	[	[	"@ . . X",
		],
		[
			["Fire Boost",
				{'element': 'fire', 'category': 'attack', 'id': 27},
				["Place a CHARGE on this spell.", "-", "Spend this CHARGE to boost the attack power of any spell by 1."] ],
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
			["Plains Walker",
				{'element': 'air', 'category': 'terrain,move', 'id': 7},
				["Move through up to 6 contiguous Plains locations."] ],
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
			["Split",
				{'element': 'earth', 'category': 'tendril', 'id': 8},
				["Place a new TENDRIL in the same location where you already control a TENDRIL."] ],
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
			["Levitate",
				{'element': 'air', 'category': 'move', 'id': 9},
				["Place a CHARGE on this spell.", "-", "Spend CHARGE to ignore terrain cost and effects when you move into (or are forced into) a location."] ],
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
			["Fire Ball",
				{'element': 'fire', 'category': 'attack', 'id': 22},
				["Attack for 2 damage at a TENDRIL you control."] ],
			["Double Shield",
				{'element': 'earth', 'category': 'defend', 'id': 36},
				["Place a CHARGE on this spell.", "-", "When CHARGED, this shield absorbs all damage from attacks.", "-", "Remove CHARGE when it takes 2 or more damage from a single attack."] ],
		],
	],

	# +-------+                     +-----+     +-------+
	# | @ X X |  Level 2 - Built on | @ X | and | @ . X |
	# +-------+                     +-----+     +-------+
	[	[	"@ X X",
		],
		[
			["Reactive Shield",
				{'element': 'earth', 'category': 'defend', 'id': 38},
				["Place a CHARGE on this spell.", "-", "When in the same location as a TENDRIL controlled by another mage, this shield absorbs all damage from attacks.", "-", "Remove CHARGE when it takes 3 or more damage from a single attack."] ],
		],
	],

	# +---------+                     +-----+     +-------+
	# | X @ . X |  Level 3 - Built on | @ X | and | @ . X |
	# +---------+                     +-----+     +-------+
	[	[	"X @ . X",
		],
		[
			["Fly",
				{'element': 'air', 'category': 'move', 'id': 10},
				["Ignore terrain cost and effects when moving into 4 locations this turn."] ],
			["Anchor Shield",
				{'element': 'earth', 'category': 'move,defend', 'id': 39},
				["Place a CHARGE on this spell.", "-", "When CHARGEd, this shield absorbs all damage from attacks and prevents you from being involuntary moved out of your location.", "-", "Remove CHARGE when it takes 1 or more damage from a single attack."] ],
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
			["Forest Run",
				{'element': 'air', 'category': 'terrain,move', 'id': 11},
				["If in or next to a Forest location, pay terrain cost to move into any location within or adjacent to that Forest, bypassing any obstacles."] ],
			["Recovery Shield",
				{'element': 'water', 'category': 'defend,tapestry', 'id': 57},
				["Place a CHARGE on this spell.", "-", "When CHARGEd, this shield absorbs all damage from attacks.", "-", "Remove CHARGE and 2 THREADs from your TAPESTRY when it takes 1 or more damage from a single attack."] ],
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
			["Resist Shield",
				{'element': 'earth', 'category': 'defend,tendril', 'id': 40},
				["Place a CHARGE on this spell.", "-", "When CHARGEd, this shield absorbs all damage from attacks and prevents others from placing new TENDRILs on your location.", "-", "Remove CHARGE when it takes 1 or more damage from a single attack."] ],
			["Water Moccasins",
				{'element': 'water', 'category': 'move,terrain', 'id': 54},
				["Place a CHARGE on this spell.", "-", "This charge can be spent at any time to cross a river or move into a water location."] ],
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
			["Mountain Climb",
				{'element': 'air', 'category': 'terrain,move', 'id': 12},
				["If in or next to a Mountain location, pay terrain cost to move into any location within or adjacent to that Mountain Range, bypassing any obstacles."] ],
			["Mountain Ranger",
				{'element': 'earth', 'category': 'terrain,move', 'id': 44},
				["If in a Mountain location, add a TENDRIL to a location in any Mountain range."] ],
			["River Run",
				{'element': 'water', 'category': 'move,terrain', 'id': 55},
				["If next to a river or water location, pay terrain cost to move into any other space adjacent to that river or water location.", "-", "Restrictions:", "* Rivers: Without passing a bridge", "* Water: Crossing 4 water locations max."] ],
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
			["Mountain Reach",
				{'element': 'earth', 'category': 'terrain,move', 'id': 45},
				["If in or adjacent to a Mountain location, add a TENDRIL to any location in a 1- or 2-size Mountain range."] ],
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
			["Fire Reign",
				{'element': 'fire', 'category': 'attack', 'id': 26},
				["Attack for 1 damage at every TENDRIL you control."] ],
			["Reverse Tendril",
				{'element': 'water', 'category': 'tendril', 'id': 52},
				["When in the same location as an opponent's TENDRIL, add a TENDRIL at the opponent's location."] ],
		],
	],

	# +---------+                     +-----+     +---------+
	# | @ X . X |  Level 3 - Built on | @ X | and | @ . . X |
	# +---------+                     +-----+     +---------+

	# +-----------+                     +-----+     +---------+
	# | X @ . . X |  Level 3 - Built on | @ X | and | @ . . X |
	# +-----------+                     +-----+     +---------+

	# +---------+                     +-----+     +---------+
	# | @ . . X |  Level 3 - Built on | @ X | and | @ . . X |
	# | X . . . |                     +-----+     +---------+
	# +---------+

	# +---------+                     +-----+     +---------+
	# | @ X . . |  Level 3 - Built on | @ X | and | @ . . . |
	# | . . . X |                     +-----+     | . . . X |
	# +---------+                                 +---------+
	[	[	"@ X . .",
			". . . X",
		],
		[
			["Rest",
				{'element': 'water', 'category': 'tapestry', 'id': 58},
				["Move 2 THREADs on your TAPESTRY to empty positions."] ],
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
			["Recover",
				{'element': 'water', 'category': 'tapestry', 'id': 59},
				["Remove a THREAD from your TAPESTRY and place it back in your MANA POOL."] ],
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
			["Forest Bind",
				{'element': 'air', 'category': 'tendril,terrain', 'id': 14},
				["When in a Forest location, add a TENDRIL to any location in Forest that is smaller in size than the one you occupy."] ],
			["Fire Burst",
				{'element': 'fire', 'category': 'tendril,terrain', 'id': 23},
				["Attack for 1 damage in all locations adjacent to a TENDRIL you control."] ],
			["Selective Prune",
				{'element': 'earth', 'category': 'tendril,attack', 'id': 41},
				["Remove all TENDRILs (except the one used for this spell) from a location where you control a TENDRIL."] ],
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
			["Plains Link",
				{'element': 'air', 'category': 'tendril,terrain', 'id': 15},
				["Move a TENDRIL you control that is in a Plains location up to 7 spaces through connecting Plains locations."] ],
			["Water Skip",
				{'element': 'water', 'category': 'tendril,terrain', 'id': 60},
				["Move a TENDRIL you control that is adjacent to a river or water location into any other space adjacent to that river or water location.", "-", "Restrictions:", "* Rivers: Without passing a bridge", "* Water: Crossing 4 water locations max."] ],
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
			["Forest Link Minor",
				{'element': 'air', 'category': 'tendril,terrain', 'id': 16},
				["Move a TENDRIL you control that is in a Forest location to another location in any Forest of size 1 or 2."] ],
			["Ricochet Blast",
				{'element': 'fire', 'category': 'tendril,terrain', 'id': 24},
				["Attack for 2 damage in single location adjacent to a TENDRIL you control."] ],
			["Water Hop",
				{'element': 'water', 'category': 'tendril,terrain', 'id': 61},
				["When next to a river or Water location, add a TENDRIL to any location adjacent to that water.", "-", "Restrictions:", "* Rivers: Without passing a bridge", "* Water: Crossing 3 water locations max."] ],
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
			["Forest Link",
				{'element': 'air', 'category': 'tendril,terrain', 'id': 17},
				["Move a TENDRIL you control that is in a Forest location to another location in any Forest that is smaller then the Forest with the TENDRIL."] ],
			["Prune Neighbor",
				{'element': 'earth', 'category': 'tendril,attack', 'id': 42},
				["Remove all TENDRILs from a location adjacent to where you control a TENDRIL."] ],
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
			["Forest Fire",
				{'element': 'fire', 'category': 'attack,terrain', 'id': 29},
				["Attack for 2 all locations in a Forest with a TENDRIL you control."] ],
			["Water Jump",
				{'element': 'water', 'category': 'tendril,terrain', 'id': 62},
				["When next to a river or Water location, add a TENDRIL to any location adjacent to that water.", "-", "Restrictions:", "* Rivers: Passing at most 1 bridge", "* Water: Crossing 5 water locations max."] ],
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
			["Mountain Link",
				{'element': 'air', 'category': 'tendril,terrain', 'id': 18},
				["Move a TENDRIL you control that is in a Mountain location to any other Mountain location."] ],
			["Boulder Tumble",
				{'element': 'fire', 'category': 'attack,terrain', 'id': 28},
				["Attack for 3 all neighboring locations to a TENDRIL you control that is in a Mountain location."] ],
			["Duplicate",
				{'element': 'water', 'category': 'tendril', 'id': 53},
				["When in the same location as an opponent's TENDRIL, add a TENDRIL at any location where that opponent controls a TENDRIL."] ],
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
			["Whirlwind",
				{'element': 'air', 'category': 'tendril', 'id': 13},
				["Place CHARGE on this spell.", "-", "While CHARGEd, all TENDRILs you control are obstacles that other mages may not move into or pass through."] ],
			["Delete All",
				{'element': 'earth', 'category': 'tendril,attack', 'id': 43},
				["When in a location with a TENDRIL controlled by another mage, remove all of that mage's TENDRILs.", "-", "If multiple mages, choose one."] ],
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
			["Prune",
				{'element': 'fire', 'category': 'attack', 'id': 33},
				["Remove all TENDRILs from a location where you control a TENDRIL.", "-", "Yes, that includes the TENDRIL used to cast this spell."] ],
			["Exchange Tendril",
				{'element': 'water', 'category': 'tendril', 'id': 51},
				["Exchange locations with a TENDRIL you control."] ],
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
			["Wall of Flame",
				{'element': 'fire', 'category': 'attack', 'id': 25},
				["Place CHARGE on this spell.", "-", "While CHARGEd, all groups of 3 adjacent TENDRILs you control are on fire and cause 1 damage.", "-", "CHARGE is lost immediately when you do not have 3 adjacent TENDRILs."] ],
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
			["Scatter",
				{'element': 'fire', 'category': 'tendril', 'id': 30},
				["Move all TENDRILs you control 1 space."] ],
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
			["Scatter Far",
				{'element': 'fire', 'category': 'tendril', 'id': 32},
				["Move any 2 TENDRILs you control a total of 9 spaces."] ],
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
			["Distraction",
				{'element': 'fire', 'category': 'tendril', 'id': 34},
				["When in the same location as a TENDRIL controlled by another mage, remove any one of their TENDRILs."] ],
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
			["Scatter Wide",
				{'element': 'fire', 'category': 'tendril', 'id': 31},
				["Move TENDRILs you control a total of 5 spaces, split amongst any number of TENDRILs."] ],
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
			["Teleport Other",
				{'element': 'water', 'category': 'astral', 'id': 49},
				["Move a mage in the same location as a TENDRIL you control to the Astral Plane."] ],
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
			["Return Other",
				{'element': 'water', 'category': 'astral', 'id': 50},
				["Move a mage in the Astral Plane to any TENDRIL you control."] ],
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
			["Blur",
				{'element': 'air', 'category': 'defend', 'id': 19},
				["Place a CHARGE on this spell.", "-", "Spend a CHARGE at any time to move into a neighboring location ignoring terrain cost."] ],
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
			["Push",
				{'element': 'air', 'category': 'attack', 'id': 20},
				["Move into an adjacent location and push out all current occupants of that location into neighboring locations.", "-", "Former occupants get to choose where they move."] ],
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
			["Stone Cage",
				{'element': 'earth', 'category': 'attack', 'id': 47},
				["PLace a CHARGE on this spell.", "-", "While CHARGEd, there is a barrier at a TENDRIL you control that traps the occupants of that location and prevents them from moving out.", "-", "CHARGE is lost if the TENDRIL moves or if the barrier takes 1 damage."] ],
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
			["Reflection Shield",
				{'element': 'fire', 'category': 'defend,attack', 'id': 35},
				["Place 1 charge on this spell.", "-", "Spend a charge at any time to protect against 1 or more points of damage and reflect 1 point of damage back at the attacker."] ],
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
			["Trap",
				{'element': 'earth', 'category': 'attack', 'id': 48},
				["Place 1 charge on this spell.", "-", "When an opponent's TENDRIL moves into your location, that opponent takes 1 damage and this CHARGE is removed."] ],
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
			["Flood",
				{'element': 'water', 'category': 'terrain', 'id': 56},
				["Place CHARGE on this spell.", "-", "While CHARGEd, all groups of 2 or more adjacent TENDRILs you control change all Plains locations to Water up to 3 spaces away from the TENDRILs.", "-", "CHARGE is lost immediately when you do not have 2 adjacent TENDRILs."] ],
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
			["Shield Pierce",
				{'element': 'air', 'category': 'attack', 'id': 21},
				["Cause 3 points of damage to all shields at a TENDRIL you control."] ],
			["Growth",
				{'element': 'earth', 'category': 'terrain', 'id': 46},
				["Place CHARGE on this spell.", "-", "While CHARGEd, all groups of 2 or more adjacent TENDRILs you control change all neighboring locations to Forest.", "-", "CHARGE is lost immediately when you do not have 2 adjacent TENDRILs."] ],
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
