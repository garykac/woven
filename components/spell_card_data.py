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
#     'starter': 'true' if this is a basic, starter spell

# Spell patterns are normalized:
#  * If spell has '@', then it should be in upper-left corner
#    * If not possible, then in top row as close as possible to upper-left corner
#      * If multiple options, then choose option with '.' in upper-left
#  * Else 'X' in upper-left corner. 
#  * Prefer wider spells over taller spells.

# Element properties
# ==================
#
# Air
#  * Opposed to Earth
#  * Properties: masculine, active, light (weight), bright, thin
#      movement, travel, flying, finding, teaching, imagination, sound
#  * Primary Ability: Physical movement
#  * Secondary Abilities:
#  * Tendrils: manipulate
#
# Fire
#  * Opposed to Water
#  * Properties: masculine, active, light (weight), bright, thin
#      movement, transformation, change, destruction, hot
#  * Primary Ability: Attack
#  * Secondary Abilities:
#  * Tendrils: quick, many, temporary, attack
#
# Earth
#  * Opposed to Air
#  * Properties: feminine, passive, heavy, dark, thick
#      stability, quiet, birth, fertility, strength, cool, solid
#  * Primary Ability: Defense, Stability
#  * Secondary Abilities:
#  * Tendrils: slow, safe, stable, anchored
#
# Water
#  * Opposed to Fire
#  * Properties: feminine, passive, heavy, dark, thick
#      motion, flowing, living, cleansing, psychic, scrying/mirrors, dreams, cool
#  * Primary Ability: Astral Movement
#  * Secondary Abilities:
#  * Tendrils: quick, few, stable

# Spell Fragments

## Neutral
# Creep [STARTER]
# Return [STARTER]

## Air
# Basic:
#  * Haste [STARTER]
#  * Haste through terrain - If in Plain, move through 6 adjacent Plains
# Terrain:
#  * Forest Run - If in or next to forest, pay cost to move into any space within or adjacent to that forest, crossing rivers if necessary
#  * When in forest, add TENDRIL to any 1- or 2-space forest
#  * When in forest, add TENDRIL to any forest
#  * Mountain Run - If in or next to mountain, pay cost to move into any space within or adjacent to that mountain
# Levitate
#  * Levitate - N charges. Spend a charge to ignore terrain restrictions (so movement cost is 0) when you move into (or are moved into) a location
#  * Fly
# Tendril Terrain:
#  * Select a TENDRIL (T) you control that is located in a plain (P); move T up to 7 spaces through neighboring plain locations
#  * Select a TENDRIL (T) you control that is located in a forest (F1); move T to any location in another forest (F2) such that size(F2) < size(F1)
#  * Select a TENDRIL (T) you control that is located in a forest (F); move T to any forest location
#  * Select a TENDRIL (T) you control that is located in mountain (M), move T to any other mountain location
# Misc:
#  * Push - When in adjacent space, move creature out and enter space (my choice where vs. your choice)
#  * Dodge - Charged. Move out of the way of an attack
#  * Shield Pierce - Causes 3 points of damage to any shield in targeted location

## Fire
# Attack:
#  * Fire Arrow [STARTER]
#  * Fire Ball - Attack all creatures in the target location for 2 damage.
#  * Fire Burst - Attack all creatures in all neighboring locations for 1 damage.
#  * Ricochet Blast - Attack all creatures in a single neighboring location for 2 damage
#  * Wall of Flame - Charged. 3 or more adjacent TENDRILS cause 1 damage
#  * Creatures in all TENDRILs you control take 1 damage
#  * Boost - Place CHARGE that can be used to increase a later attack by 1
# Terrain Attack:
#  * Volcanic Rift - When targeting a mountain location, all targeted creatures take 3 damage
#  * Forest Fire - When targeting a forest location, all creatures in that forest take 2 damage
# Tendril Movement:
#  * FIRE Move all TENDRILs you control 1 space
#  * Move TENDRILs you control a total of 5 spaces, split amongst any number of TENDRILs
#  * Move TENDRILs a total of 9 spaces, split amongst any number of TENDRILs
# Tendril Attack:
#  * Remove all TENDRILs from location (including this one)
#  * Remove - When in the same location as a TENDRIL controlled by another mage, remove any one of their TENDRILs
# Defense:
#  * FIRE Reflection - Charge protects against 1 damage and reflects 1 damage back to attacker

## Earth
# Protection:
#  * Protection [STARTER]
#  * EARTH Shield - deflects up to 2 damage with 1 charge, remove if it takes 2 or more damage in a single attack
#  * EARTH Reactive Shield - Charge that activates a 2 defense shield when the caster is the same location as an opponent's TENDRIL
#  * EARTH Shield Boost - Charge that can be used to temporarily boost a shield by 2 points. Boost takes damage before the shield.
#  * Shield Block - Charge on shield, while active no one else can enter or move tendril into your location
#  * Anchor - Resist attempt to move out of location (+ shield?)
# Tendril:
#  * Split
#  * When in mountain, add TENDRIL to any 1- or 2-space mountain
#  * When in mountain, add TENDRIL to any mountain
# Terrain:
#  * Growth - All fields within 5 spaces of target are forest for the remainder of this turn.
# Tendril attack:
#  * Remove all opponent TENDRILs from location
#  * Remove all TENDRILs from neighboring location
#  * Delete All - When in the same location as a TENDRIL controlled by another mage, remove all of their TENDRILs from the map.
# Misc:
#  * Stone cage - Trap creatures at location - until 2 pts of damage done to location
#  * Trap - Charge that automatically activates when targeted to cause 1 damage to target owner

## Water
# Astral Movement:
#  * Teleport Away [STARTER]
#  * Teleport: Move target creature into Astral Plane
#  * Teleport: Move creature in Astral plane to tendril
# Tendril:
#  * Reverse Tendril - Exchange locations between the caster and a TENDRIL controlled by the caster.
#  * Reverse target - follow a TENDRIL back to its caster's location and add a TENDRIL there
#  * Copy - When in the same location as a TENDRIL controlled by another mage, make a duplicate copy of any one of their TENDRILs
# Terrain Movement:
#  * Water Moccasins - Charge that can be spent to cross river or move into 1 water space.
#  * River Run - If next to river/lake, pay cost to move into any space adjacent to that river/lake without passing a bridge
# Terrain:
#  * Flood - All fields within 5 spaces of target are water for the remainder of this turn.
# Defense:
#  * WATER Recovery - Deflects 1 damage. caster may recover up to 2 THREADs from their TAPESTRY when this shield defends against an attack
# Tapestry:
#  * WATER: Move 2 THREADs in TAPESTRY to new locations
#  * WATER: Remove a THREAD from TAPESTRY
# Tendril Terrain:
#  * When next to a river or lake, add a TENDRIL to any space adjacent to that river/lake as long as it doesn't require passing a bridge
#  * When next to a river or lake, add a TENDRIL to any space adjacent to that river/lake passing at most 1 bridge
#  * Move a TENDRIL you control that is adjacent to a River


## Unused
# Add damage marker to opponent's Tapestry
# Leech - When in same location as an opponent, take mana from opponent and add to your Tapestry
# * Astral Prison - stuck in prison until 2 pts damage done to it
# * Move opponent's target up to 3 spaces when on their space
# * Select a TENDRIL (T) you control that is located in a plain (P); move T to another plain location within 4 spaces of P
# * Select a TENDRIL (T) you control that is located in a forest (F); move T to any other location in F
# * Select a TENDRIL (T) you control that is located in mountain (M), move T to any other location in M
# * When next to a river or lake, add a TENDRIL to any space adjacent to that river/lake passing at most 2 bridges
# * When in forest, add TENDRIL to any 1-space forest
# * When in forest, add TENDRIL to any forest 4 or less in size
# * Effects that trigger when player is targeted by another player.
# * Shield trigger an effect when attacked
# * Trap triggered when visited/targeted
# * Gain extra cubes permanently - can only be cast once
# * Gain extra colorless (temporary) cubes - these cubes can only be used once. return when removed from matrix

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
		[	["Creep",
				{'element': 'none', 'starter': 'true'},
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
		[	["Return",
				{'element': 'none', 'starter': 'true'},
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
		[	["Haste",
				{'element': 'air', 'starter': 'true'},
				["Gain 3 MP to use this turn"] ],
			["Protection",
				{'element': 'earth', 'starter': 'true'},
				["Place 1 charge on this spell.", "Spend a charge at any time to protect against 1 or more points of damage."] ],
		],
	],

	# +-----+
	# | @ . |  Level 1
	# | . X |
	# +-----+
	[	[	"@ .",
			". X",
		],
		[	["Fire Burst",
				{'element': 'fire', 'starter': 'true'},
				["Attack all creatures at a TENDRIL you control for 1pt damage."] ],
			["Teleport Away",
				{'element': 'water', 'starter': 'true'},
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

	# +---------+
	# | @ . . X |  Level 2
	# +---------+

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

	# +-----+                     +-----+
	# | @ X |  Level 2 - Built on | @ X |
	# | X . |                     +-----+
	# +-----+
	[	[	"@ X",
			"X .",
		],
		[	["Split",
				{'element': 'earth'},
				["Place a new TENDRIL in the same location where you already control a TENDRIL."] ],
		],
	],

	# +-------+                     +-----+     +-----+
	# | . @ X |  Level 2 - Built on | @ X | and | @ . | 
	# | X . . |                     +-----+     | . X |
	# +-------+                                 +-----+

	# +-----+                     +-----+     +-----+
	# | @ . |  Level 2 - Built on | @ X | and | @ . |
	# | X X |                     +-----+     | . X |
	# +-----+                                 +-----+

	# +-------+                     +-----+     +-------+
	# | @ X X |  Level 2 - Built on | @ X | and | @ . X |
	# +-------+                     +-----+     +-------+

	# +---------+                     +-----+     +-------+
	# | X @ . X |  Level 3 - Built on | @ X | and | @ . X |
	# +---------+                     +-----+     +-------+

	# +-------+                     +-----+     +-------+
	# | @ . X |  Level 2 - Built on | @ X | and | @ . X |
	# | X . . |                     +-----+     +-------+
	# +-------+

	# +-------+                     +-----+     +-------+
	# | @ X . |  Level 2 - Built on | @ X | and | @ . . |
	# | . . X |                     +-----+     | . . X |
	# +-------+                                 +-------+

	# +-------+                     +-----+     +-------+
	# | @ . . |  Level 2 - Built on | @ X | and | @ . . |
	# | X . X |                     +-----+     | . . X |
	# +-------+                                 +-------+

	# +---------+                     +-----+     +-------+
	# | X @ . . |  Level 3 - Built on | @ X | and | @ . . |
	# | . . . X |                     +-----+     | . . X |
	# +---------+                                 +-------+

	# +-------+                     +-----+     +-------+
	# | X . . |  Level 3 - Built on | @ X | and | @ . . |
	# | @ . . |                     +-----+     | . . X |
	# | . . X |                                 +-------+
	# +-------+

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

	# +---------+                     +-----+     +---------+
	# | @ . . . |  Level 3 - Built on | @ X | and | @ . . . |
	# | X . . X |                     +-----+     | . . . X |
	# +---------+                                 +---------+

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

	# +-------+                     +-----+
	# | X . . |  Level 3 - Built on | @ . |
	# | . @ . |                     | . X |
	# | . . X |                     +-----+
	# +-------+

	# +-------+                     +-----+     +-------+
	# | @ . X |  Level 2 - Built on | @ . | and | @ . X |
	# | . X . |                     | . X |     +-------+
	# +-------+                     +-----+

	# +---------+                     +-----+     +-------+
	# | . @ . X |  Level 3 - Built on | @ . | and | @ . X |
	# | X . . . |                     | . X |     +-------+
	# +---------+                     +-----+

	# +-------+                     +-----+     +-------+
	# | @ . . |  Level 2 - Built on | @ . | and | @ . . |
	# | . X X |                     | . X |     | . . X |
	# +-------+                     +-----+     +-------+

	# +---------+                     +-----+     +-------+
	# | . @ . . |  Level 3 - Built on | @ . | and | @ . . |
	# | X . . X |                     | . X |     | . . X |
	# +---------+                     +-----+     +-------+

	# +---------+                     +-----+     +-------+
	# | X . . . |  Level 3 - Built on | @ . | and | @ . . |
	# | . @ . . |                     | . X |     | . . X |
	# | . . . X |                     +-----+     +-------+
	# +---------+

	# +-------+                     +-----+     +-------+
	# | . @ . |  Level 3 - Built on | @ . | and | @ . . |
	# | X . . |                     | . X |     | . . X |
	# | . . X |                     +-----+     +-------+
	# +-------+

	# +-------+                     +-----+     +-------+
	# | @ . . |  Level 3 - Built on | @ . | and | @ . . |
	# | . X . |                     | . X |     | . . . |
	# | . . X |                     +-----+     | . . X |
	# +-------+                                 +-------+

	# +---------+                     +-----+     +---------+
	# | @ . . X |  Level 3 - Built on | @ . | and | @ . . X |
	# | . X . . |                     | . X |     +---------+
	# +---------+                     +-----+

	# +-----------+                     +-----+     +---------+
	# | . @ . . X |  Level 3 - Built on | @ . | and | @ . . X |
	# | X . . . . |                     | . X |     +---------+
	# +-----------+                     +-----+

	# +---------+                     +-----+     +---------+
	# | @ . . . |  Level 3 - Built on | @ . | and | @ . . . |
	# | . X . X |                     | . X |     | . . . X |
	# +---------+                     +-----+     +---------+
	# + 3 variants
	
	# +---------+                     +-----+     +---------=
	# | @ . . . |  Level 3 - Build on | @ . | and | @ . . . |
	# | . X . . |                     | . X |     | . . . . |
	# | . . . X |                     +-----+     | . . . X |
	# +---------+                                 +---------+
	# + 3 variants

	# +-----------+                     +-------+
	# | X . @ . X |  Level 3 - Built on | @ . X |
	# +-----------+                     +-------+

	# +-------+                     +-------+
	# | @ . X |  Level 3 - Build on | @ . X |
	# | . . . |                     +-------+
	# | X . . |
	# +-------+

	# +-------+                     +-------+     +-------+
	# | @ . X |  Level 2 - Built on | @ . X | and | @ . . |
	# | . . X |                     +-------+     | . . X |
	# +-------+                                   +-------+

	# +-------+                     +-------+     +-------+
	# | @ . X |  Level 2 - Built on | @ . X | and | @ . . |
	# | . . . |                     +-------+     | . . X |
	# | . X . |                                   +-------+
	# +-------+

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

	# +-------+                     +-----+
	# | @ . @ |  Level 2 - Built on | @ . |
	# | . X . |                     | . X |
	# +-------+                     +-----+

	# +-----------+                     +-------+
	# | @ . . . . |  Level 3 - Built on | @ . . |
	# | . . X . . |                     | . . X |
	# | . . . . @ |                     +-------+
	# +-----------+

	#  _____ _                   _       _    ___      _      ___ 
	# |   __| |___ _____ ___ ___| |_ ___| |  |_  |   _| |_   |_  |
	# |   __| | -_|     | -_|   |  _| .'| |  |  _|  |_   _|  |  _|
	# |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |___|    |_|    |___|
	#

	# +-----+                     +-----+
	# | @ X |  Level 3 - Built on | @ X |
	# | X @ |                     +-----+
	# +-----+

	# +-------+                     +-----+
	# | . @ . |  Level 3 - Built on | @ . |
	# | X . X |                     | . X |
	# | . @ . |                     +-----+
	# +-------+

]
