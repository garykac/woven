# Tapestry card data

tapestry_card_data = [

    # +---------+       +---------+
    # |    X  X |  <->  | X  X  X |
    # | X       |       | X  X    |
    # +---------+       +---------+
    {   'name': 'knightl35',
        'pattern': ['1 X X',  'X X X',
                    'X 2 3',  'X X 4'],
        'elements': ['afew', 'wafe', 'ewaf', 'fewa'],
    },

    # +---------+       +---------+
    # | X  X    |  <->  | X  X  X |
    # |       X |       |    X  X |
    # +---------+       +---------+
    {   'name': 'knightr35',
        'pattern': ['X X 3',  'X X X',
                    '1 2 X',  '4 X X'],
        'elements': ['afew', 'wafe', 'ewaf', 'fewa'],
    },

    # +---------+       +---------+
    # | X     X |  <->  | X  X  X |
    # |    X    |       | X     X |
    # +---------+       +---------+
    {   'name': 'v35',
        'pattern': ['X 2 X',  'X X X',
                    '1 X 3',  'X 4 X'],
        'elements': ['afew', 'wafe', 'ewaf', 'fewa'],
    },

    # +---------+       +---------+
    # |    X  X |  <->  | X  X    |
    # | X  X    |       |    X  X |
    # +---------+       +---------+
    {   'name': 'sz4',
        'pattern': ['1 X X',  'X X 4',
                    'X X 2',  '3 X X'],
        # 1: A A W F F E  =  aa ff e w  =  2-af ew
        # 2: F E A E W W  =  a f ee ww  =  af 2-ew
        # 3: W F F A E A  =  aa ff e a  =  2-af ew
        # 4: E W E W A F  =  a f ee ww  =  af 2-ew
        #
        # X X
        # X .  =  aaa fff eee www
        #
        # X X
        # . X  =  aaa fff eee www
        'elements': ['afwe', 'aefw', 'wafe', 'feaw', 'fwea', 'ewaf'],
    },

    # +---------+       +---------+
    # | X  X  X |  <->  | X  X  X |
    # | X       |       |       X |
    # +---------+       +---------+
    {   'name': 'l4',
        'pattern': ['X X X',  'X X X',
                    'X 1 2',  '3 4 X'],
        # 1: A A W F F E  =  aa ff e w
        # 2: F E A E W W  =  a f ee ww
        # 3: W F F A E A  =  aa ff e w
        # 4: E W E W A F  =  a f ee ww
        #
        # X X
        # X .  =  aa ff e w
        #
        # X X
        # . X  =  a f ee ww
        'elements': ['afwe', 'aefw', 'wafe', 'feaw', 'fwea', 'ewaf'],
    },

    # +---------+       +---------+
    # | X     X |  <->  | X     X |
    # | X  X    |       |    X  X |
    # +---------+       +---------+
    {   'name': 'ldot4',
        'pattern': ['X 1 X',  'X 4 X',
                    'X X 2',  '3 X X'],
        # 1: A A W F F E  =  aa ff e w
        # 2: F E A E W W  =  a f ee ww
        # 3: W F F A E A  =  aa ff e w
        # 4: E W E W A F  =  a f ee ww
        #
        # X X
        # X .  =  a f ee ww
        #
        # X X
        # . X  =  aa ff e w
        'elements': ['afwe', 'aefw', 'wafe', 'feaw', 'fwea', 'ewaf'],
    },

    # +---------+       +---------+
    # | X  X  X |  <->  | X  X  X |
    # |    X    |       |    X    |
    # +---------+       +---------+
    {   'name': 't4',
        'pattern': ['X X X',  'X X X',
                    '1 X 2',  '3 X 4'],
        # 1: A E W  =  a e   w
        # 2: W F E  =    e f w
        # 3: F W A  =  a   f w
        # 4: E A F  =  a e f
        #
        # X X
        # X .  =  a ee ff w
        #
        # X X
        # . X  =  aa e f ww
        'elements': ['awfe', 'efwa', 'weaf'],
    },
]
