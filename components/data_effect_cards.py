# Effect (Combat/Event) card data

# Data Format:
#   [ <die-rolls>, <event> ]
#
# die-rolls:
#   [ <d4>, <d6>, <d8> ]
#   Negative values = Trigger event
#
# event:
#   [ <fire>, <air>, <water>, <earth> ]
#
# fire:
#   [ <line>+ ]
#
# Similar for <air>, <water> and <earth>

effect_card_revision = 1

PLUS_2 = ["+2"]
PLUS_3 = ["+3"]

RECOVER_1_THREAD = ["Recover 1 Thead", "from Tapestry"]
RECOVER_2_THREADS = ["Recover 2 Theads", "from Tapestry"]

effect_card_data = [
	[[ 1,  1,  1],[
		["Spell also affects", "all neighboring locations"],
		["Move 1 before", "spells take effect"],
		RECOVER_2_THREADS,
		PLUS_3,
	]],
	[[ 2,  1,  2],[
		PLUS_2,
		["Move 2 after spell", "effects complete"],
		["+2 OR -4 to", "opponent's roll"],
		["Recover 4 mana", "from Spent Pool"],
	]],
	[[ 3,  1,  3],[
		["Spell also affects", "a single neighboring location"],
		PLUS_3,
		["Exchange position", "with a Tendril before spell"],
		["+2 OR reflect", "attack back"],
	]],
	[[-4,  1,  4],[
		["Remove all Tendrils", "from neighboring locations"],
		["Move 3 after spell", "effects complete"],
		RECOVER_1_THREAD,
		PLUS_2,
	]],
	[[ 4,  1, -5],[
		PLUS_3,
		["Move 3 after spell", "effects complete"],
		["Recover 3 Theads", "from Tapestry"],
		["Recover 3 mana", "from Spent Pool"],
	]],
	[[ 3,  1,  6],[
		["Spell also affects", "2 neighboring locations"],
		PLUS_3,
		["+2 OR place tendril", "at attacker"],
		["Recover 3 mana", "from Spent Pool"],
	]],
	[[ 2,  1, -7],[
		["Spell also affects", "all neighboring locations"],
		["Move 1 before", "spells take effect"],
		RECOVER_2_THREADS,
		PLUS_3,
	]],
	[[ 1,  1,  8],[
		PLUS_2,
		["Move 2 after spell", "effects complete"],
		["+2 OR -4 to", "opponent's roll"],
		["Recover 4 mana", "from Spent Pool"],
	]],

	[[ 1,  2,  1],[
		["Spell also affects", "a single neighboring location"],
		PLUS_3,
		["Exchange position", "with a Tendril before spell"],
		["+2 OR reflect", "attack back"],
	]],
	[[ 1,  2,  2],[
		["Remove all Tendrils", "from neighboring locations"],
		["Move 3 after spell", "effects complete"],
		RECOVER_1_THREAD,
		PLUS_2,
	]],
	[[ 3,  2,  3],[
		PLUS_3,
		["Move 3 after spell", "effects complete"],
		["Recover 3 Theads", "from Tapestry"],
		["Recover 3 mana", "from Spent Pool"],
	]],
	[[ 3,  2,  4],[
		["Spell also affects", "2 neighboring locations"],
		PLUS_3,
		["+2 OR place tendril", "at attacker"],
		["Recover 3 mana", "from Spent Pool"],
	]],
	[[ 2,  2,  5],[
		["Spell also affects", "all neighboring locations"],
		["Move 1 before", "spells take effect"],
		RECOVER_2_THREADS,
		PLUS_3,
	]],
	[[ 2,  2, -6],[
		PLUS_2,
		["Move 2 after spell", "effects complete"],
		["+2 OR -4 to", "opponent's roll"],
		["Recover 4 mana", "from Spent Pool"],
	]],
	[[-4,  2,  7],[
		["Spell also affects", "a single neighboring location"],
		PLUS_3,
		["Exchange position", "with a Tendril before spell"],
		["+2 OR reflect", "attack back"],
	]],
	[[ 4,  2, -8],[
		["Remove all Tendrils", "from neighboring locations"],
		["Move 3 after spell", "effects complete"],
		RECOVER_1_THREAD,
		PLUS_2,
	]],

	[[ 3,  3,  1],[
		PLUS_3,
		["Move 3 after spell", "effects complete"],
		["Recover 3 Theads", "from Tapestry"],
		["Recover 3 mana", "from Spent Pool"],
	]],
	[[-3,  3,  2],[
		["Spell also affects", "2 neighboring locations"],
		PLUS_3,
		["+2 OR place tendril", "at attacker"],
		["Recover 3 mana", "from Spent Pool"],
	]],
	[[ 1,  3,  3],[
		["Spell also affects", "all neighboring locations"],
		["Move 1 before", "spells take effect"],
		RECOVER_2_THREADS,
		PLUS_3,
	]],
	[[ 1,  3,  4],[
		PLUS_2,
		["Move 2 after spell", "effects complete"],
		["+2 OR -4 to", "opponent's roll"],
		["Recover 4 mana", "from Spent Pool"],
	]],
	[[ 4,  3,  5],[
		["Spell also affects", "a single neighboring location"],
		PLUS_3,
		["Exchange position", "with a Tendril before spell"],
		["+2 OR reflect", "attack back"],
	]],
	[[ 4,  3,  6],[
		["Remove all Tendrils", "from neighboring locations"],
		["Move 3 after spell", "effects complete"],
		RECOVER_1_THREAD,
		PLUS_2,
	]],
	[[ 2,  3, -7],[
		PLUS_3,
		["Move 3 after spell", "effects complete"],
		["Recover 3 Theads", "from Tapestry"],
		["Recover 3 mana", "from Spent Pool"],
	]],
	[[ 2,  3,  8],[
		["Spell also affects", "2 neighboring locations"],
		PLUS_3,
		["+2 OR place tendril", "at attacker"],
		["Recover 3 mana", "from Spent Pool"],
	]],

	[[ 2,  4,  1],[
		["Spell also affects", "all neighboring locations"],
		["Move 1 before", "spells take effect"],
		RECOVER_2_THREADS,
		PLUS_3,
	]],
	[[ 4,  4,  2],[
		PLUS_2,
		["Move 2 after spell", "effects complete"],
		["+2 OR -4 to", "opponent's roll"],
		["Recover 4 mana", "from Spent Pool"],
	]],
	[[ 2, -4,  3],[
		["Spell also affects", "a single neighboring location"],
		PLUS_3,
		["Exchange position", "with a Tendril before spell"],
		["+2 OR reflect", "attack back"],
	]],
	[[-4,  4,  4],[
		["Remove all Tendrils", "from neighboring locations"],
		["Move 3 after spell", "effects complete"],
		RECOVER_1_THREAD,
		PLUS_2,
	]],
	[[ 1, -4,  5],[
		PLUS_3,
		["Move 3 after spell", "effects complete"],
		["Recover 3 Theads", "from Tapestry"],
		["Recover 3 mana", "from Spent Pool"],
	]],
	[[ 3,  4,  6],[
		["Spell also affects", "2 neighboring locations"],
		PLUS_3,
		["+2 OR place tendril", "at attacker"],
		["Recover 3 mana", "from Spent Pool"],
	]],
	[[ 1,  4,  7],[
		["Spell also affects", "all neighboring locations"],
		["Move 1 before", "spells take effect"],
		RECOVER_2_THREADS,
		PLUS_3,
	]],
	[[ 3,  4, -8],[
		PLUS_2,
		["Move 2 after spell", "effects complete"],
		["+2 OR -4 to", "opponent's roll"],
		["Recover 4 mana", "from Spent Pool"],
	]],

	[[-4,  5,  1],[
		["Spell also affects", "a single neighboring location"],
		PLUS_3,
		["Exchange position", "with a Tendril before spell"],
		["+2 OR reflect", "attack back"],
	]],
	[[ 2, -5,  2],[
		["Remove all Tendrils", "from neighboring locations"],
		["Move 3 after spell", "effects complete"],
		RECOVER_1_THREAD,
		PLUS_2,
	]],
	[[ 4, -5,  3],[
		PLUS_3,
		["Move 3 after spell", "effects complete"],
		["Recover 3 Theads", "from Tapestry"],
		["Recover 3 mana", "from Spent Pool"],
	]],
	[[ 2,  5,  4],[
		["Spell also affects", "2 neighboring locations"],
		PLUS_3,
		["+2 OR place tendril", "at attacker"],
		["Recover 3 mana", "from Spent Pool"],
	]],
	[[-3,  5,  5],[
		["Spell also affects", "all neighboring locations"],
		["Move 1 before", "spells take effect"],
		RECOVER_2_THREADS,
		PLUS_3,
	]],
	[[ 1,  5, -6],[
		PLUS_2,
		["Move 2 after spell", "effects complete"],
		["+2 OR -4 to", "opponent's roll"],
		["Recover 4 mana", "from Spent Pool"],
	]],
	[[ 3, -5,  7],[
		["Spell also affects", "a single neighboring location"],
		PLUS_3,
		["Exchange position", "with a Tendril before spell"],
		["+2 OR reflect", "attack back"],
	]],
	[[ 1,  5,  8],[
		["Remove all Tendrils", "from neighboring locations"],
		["Move 3 after spell", "effects complete"],
		RECOVER_1_THREAD,
		PLUS_2,
	]],

	[[-4,  6,  1],[
		PLUS_3,
		["Move 3 after spell", "effects complete"],
		["Recover 3 Theads", "from Tapestry"],
		["Recover 3 mana", "from Spent Pool"],
	]],
	[[ 3, -6,  2],[
		["Spell also affects", "2 neighboring locations"],
		PLUS_3,
		["+2 OR place tendril", "at attacker"],
		["Recover 3 mana", "from Spent Pool"],
	]],
	[[ 2,  6,  3],[
		["Spell also affects", "all neighboring locations"],
		["Move 1 before", "spells take effect"],
		RECOVER_2_THREADS,
		PLUS_3,
	]],
	[[ 1, -6,  4],[
		PLUS_2,
		["Move 2 after spell", "effects complete"],
		["+2 OR -4 to", "opponent's roll"],
		["Recover 4 mana", "from Spent Pool"],
	]],
	[[ 1,  6,  5],[
		["Spell also affects", "a single neighboring location"],
		PLUS_3,
		["Exchange position", "with a Tendril before spell"],
		["+2 OR reflect", "attack back"],
	]],
	[[ 2, -6,  6],[
		["Remove all Tendrils", "from neighboring locations"],
		["Move 3 after spell", "effects complete"],
		RECOVER_1_THREAD,
		PLUS_2,
	]],
	[[-3,  6,  7],[
		PLUS_3,
		["Move 3 after spell", "effects complete"],
		["Recover 3 Theads", "from Tapestry"],
		["Recover 3 mana", "from Spent Pool"],
	]],
	[[ 4,  6, -8],[
		["Spell also affects", "2 neighboring locations"],
		PLUS_3,
		["+2 OR place tendril", "at attacker"],
		["Recover 3 mana", "from Spent Pool"],
	]],
]
