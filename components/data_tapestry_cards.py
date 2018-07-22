# Tapestry card data

tapestry_card_data = [

	# +---------+       +---------+
	# |    X  X |  <->  | X  X  X |
	# | X       |       | X  X    |
	# +---------+       +---------+
	{	'name': 'knightl35',
		'pattern': ['1 X X',  'X X X',
					'X 2 3',  'X X 4'],
		'elements': ['afew', 'wafe', 'ewaf', 'fewa'],
	},

	# +---------+       +---------+
	# | X  X    |  <->  | X  X  X |
	# |       X |       |    X  X |
	# +---------+       +---------+
	{	'name': 'knightr35',
		'pattern': ['X X 3',  'X X X',
					'1 2 X',  '4 X X'],
		'elements': ['afew', 'wafe', 'ewaf', 'fewa'],
	},

	# +---------+       +---------+
	# | X     X |  <->  | X  X  X |
	# |    X    |       | X     X |
	# +---------+       +---------+
	{	'name': 'v35',
		'pattern': ['X 2 X',  'X X X',
					'1 X 3',  'X 4 X'],
		'elements': ['afew', 'wafe', 'ewaf', 'fewa'],
	},

	# +---------+       +---------+
	# |    X  X |  <->  | X  X    |
	# | X  X    |       |    X  X |
	# +---------+       +---------+
	{	'name': 'sz4',
		'pattern': ['1 X X',  'X X 4',
					'X X 2',  '3 X X'],
		# A A W F F E  =  aa ff e w
		# F E A E W W  =  a f ee ww
		# W F F A E A  =  aa ff e a
		# E W E W A F  =  a f ee ww
		'elements': ['afwe', 'aefw', 'wafe', 'feaw', 'fwea', 'ewaf'],
	},

	# +---------+       +---------+
	# | X  X  X |  <->  | X  X  X |
	# | X       |       |       X |
	# +---------+       +---------+
	{	'name': 'l4',
		'pattern': ['X X X',  'X X X',
					'X 1 2',  '3 4 X'],
		'elements': ['afwe', 'aefw', 'wafe', 'feaw', 'fwea', 'ewaf'],
	},

	# +---------+       +---------+
	# | X     X |  <->  | X     X |
	# | X  X    |       |    X  X |
	# +---------+       +---------+
	{	'name': 'ldot4',
		'pattern': ['X 1 X',  'X 4 X',
					'X X 2',  '3 X X'],
		'elements': ['afwe', 'aefw', 'wafe', 'feaw', 'fwea', 'ewaf'],
	},

	# +---------+       +---------+
	# | X  X  X |  <->  | X  X  X |
	# |    X    |       |    X    |
	# +---------+       +---------+
	{	'name': 't4',
		'pattern': ['X X X',  'X X X',
					'1 X 2',  '3 X 4'],
		# A E W  =  a e   w
		# W F E  =    e f w
		# F W A  =  a   f w
		# E A F  =  a e f
		'elements': ['awfe', 'efwa', 'weaf'],
	},
]
