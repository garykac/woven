# Data Format:
#   spell_card_patterns:
#     Dictionary of spell <name> to <pattern-info>
#
#   <name>: string
#
#   <pattern-info>: dict
#     'elements' String with valid elements for this pattern
#     'pattern': <pattern>
#
#   <pattern>:
#     List of strings (one for each row of the pattern)

# Spell patterns are normalized:
#  * If spell has '@', then it should be in upper-left corner
#    * If not possible, then in top row as close as possible to upper-left corner
#      * If multiple options, then choose option with '.' in upper-left
#  * Else 'X' in upper-left corner. 
#  * Prefer wider spells over taller spells.

# Complexity info for each spell:
#  * Level - rough indicator of complexity
#  * Threads - number of threads for single cast
#  * Cards - min number of cards to create pattern for single cast
#  * Transform - max-cast: max-threads/max-cards
#      max-cast: max times this spell can be repeated when centered on the element,
#         rotating and mirroring as required
#      max-threads: number of threads to cast max times
#      max-cards: min number of cards to cast max times

spell_card_patterns = {

    'blank':    {'elements': 'none',
                 'pattern': [   ". . . . .",
                                ". . . . .",
                                ". . . . .",
                            ],
                },

    #  _____         _           _    ___   
    # |   | |___ _ _| |_ ___ ___| |  |_  |  
    # | | | | -_| | |  _|  _| .'| |   _| |_ 
    # |_|___|___|___|_| |_| |__,|_|  |_____|
    #

    # +---+
    # | X |  Level 0 - Castable on all starting cards.
    # +---+
    'N1':       {'elements': 'none',
                 'pattern': [   "X",
                            ],
                },

    #  _____         _           _    ___ 
    # |   | |___ _ _| |_ ___ ___| |  |_  |
    # | | | | -_| | |  _|  _| .'| |  |  _|
    # |_|___|___|___|_| |_| |__,|_|  |___|
    #

    # +-----+  Level 1 - Castable on all starting cards.
    # | X X |
    # +-----+
    'N2-1':     {'elements': 'none',
                 'pattern': [   "X X",
                            ],
                },

    # +-----+  Level 1 - Castable on all starting cards.
    # | X . |
    # | . X |
    # +-----+
    'N2-2':     {'elements': 'none',
                 'pattern': [   "X .",
                                ". X",
                            ],
                },

    # +-------+  Level 1 - Castable on all starting cards except  xx  xx
    # | X . X |                                                  xx    xx
    # +-------+
    'N2-3':     {'elements': 'none',
                 'pattern': [   "X . X",
                            ],
                },

    # +-------+  Level 1 - Castable on all starting cards except  x    x
    # | X . . |                                                  xxx  xxx
    # | . . X |
    # +-------+
    'N2-4':     {'elements': 'none',
                 'pattern': [   "X . .",
                                ". . X",
                            ],
                },

    # +-------+  Level 2
    # | X . . |
    # | . . . |
    # | . . X |
    # +-------+
    'N2-5':     {'elements': 'none',
                 'pattern': [   "X . .",
                                ". . .",
                                ". . X",
                            ],
                },

    # +---------+  Level 2
    # | X . . X |
    # +---------+
    'N2-6':     {'elements': 'none',
                 'pattern': [   "X . . X",
                            ],
                },

    # +---------+  Level 2
    # | X . . . |
    # | . . . X |
    # +---------+
    'N2-7':     {'elements': 'none',
                 'pattern': [],
                },

    # +---------+  Level 2
    # | X . . . |
    # | . . . . |
    # | . . . X |
    # +---------+
    'N2-8':     {'elements': 'none',
                 'pattern': [],
                },

    #  _____         _           _    ___ 
    # |   | |___ _ _| |_ ___ ___| |  |_  |
    # | | | | -_| | |  _|  _| .'| |  |_  |
    # |_|___|___|___|_| |_| |__,|_|  |___|
    #

    # +-------+  Level 2
    # | X X X |
    # +-------+
    'N3-1':     {'elements': 'none',
                 'pattern': [],
                },

    # +-------+  Level 2 - Castable on all starting cards except  x    x
    # | X X . |                                                  xxx  xxx
    # | . . X |
    # +-------+
    'N3-2':     {'elements': 'none',
                 'pattern': [],
                },

    # +-----+  Level 2 - Castable on all starting cards.
    # | X X |
    # | . X |
    # +-----+
    'N3-3':     {'elements': 'none',
                 'pattern': [],
                },

    # +-------+  Level 2
    # | X . X |
    # | . X . |
    # +-------+
    'N3-4':     {'elements': 'none',
                 'pattern': [],
                },

    # +-------+  Level 3
    # | X . . |
    # | . X . |
    # | . . X |
    # +-------+
    'N3-5':     {'elements': 'none',
                 'pattern': [],
                },

    #  _____ _                   _       _    ___        _      ___   
    # |   __| |___ _____ ___ ___| |_ ___| |  |_  |     _| |_   |_  |  
    # |   __| | -_|     | -_|   |  _| .'| |   _| |_   |_   _|   _| |_ 
    # |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |_____|    |_|    |_____|
    #

    # +-----+  Level 1
    # | @ X |  Threads 1
    # +-----+  Cards 1
    #          Transform 4: 4/2
    'E1-1':     {'elements': 'ae',
                 'pattern': [   "@ X",
                            ],
                },

    # +-----+  Level 1         Transforms  3 . 2
    # | @ . |  Threads 1                   . @ .
    # | . X |  Cards 1                     4 . 1
    # +-----+  Transform 4: 4/2
    'E1-2':     {'elements': 'fw',
                 'pattern': [   "@ .",
                                ". X",
                            ],
                },

    # +-------+  Level 1
    # | @ . X |  Threads 1
    # +-------+  Cards 1
    #            Transform 4: 4/4
    'E1-3':     {'elements': 'ae',
                 'pattern': [    "@ . X",
                            ],
                },

    # +-------+  Level 1          Transforms  . 6 . 7 .
    # | @ . . |  Threads 1                    5 . . . 8
    # | . . X |  Cards 1                      . . @ . .
    # +-------+  Transform 8: 8/5             4 . . . 1
    #                                         . 3 . 2 .
    'E1-4':     {'elements': 'aefw',
                 'pattern': [   "@ . .",
                                ". . X",
                            ],
                },

    # +-------+  Level 2          Transforms  3 . . . 2
    # | @ . . |  Threads 1                    . . . . .
    # | . . . |  Cards 2                      . . @ . .
    # | . . X |  Transform 4: 4/6             . . . . .
    # +-------+                               4 . . . 1
    'E1-5':     {'elements': 'fw',
                 'pattern': [   "@ . .",
                                ". . .",
                                ". . X",
                            ],
                },

    # +---------+  Level 2
    # | @ . . X |  Threads 1
    # +---------+  Cards 2
    #              Transform 4: 4/6
    'E1-6':     {'elements': 'ae',
                 'pattern': [    "@ . . X",
                            ],
                },

    # +---------+  Level 2
    # | @ . . . |  Threads 1
    # | . . . X |  Cards 2
    # +---------+  Transform 8
    'E1-7':     {'elements': 'aefw',
                 'pattern': [   "@ . . .",
                                ". . . X",
                            ],
                },

    # +---------+  Level 2
    # | @ . . . |  Threads 1
    # | . . . . |  Cards 3
    # | . . . X |  Transform 8
    # +---------+
    'E1-8':     {'elements': 'aefw',
                 'pattern': [   "@ . . .",
                                ". . . .",
                                ". . . X",
                            ],
                },

    #  _____ _                   _       _    ___        _      ___ 
    # |   __| |___ _____ ___ ___| |_ ___| |  |_  |     _| |_   |_  |
    # |   __| | -_|     | -_|   |  _| .'| |   _| |_   |_   _|  |  _|
    # |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |_____|    |_|    |___|
    #

    # +-------+  Level 2 - Built on +-----+  Transforms  . 2 .
    # | X @ X |  Threads 1          | @ X |              1 @ 1
    # +-------+  Cards 1            +-----+              . 2 .
    #            Transform 2: 4/2
    'E2-1':     {'elements': 'ae',
                 'pattern': [   "X @ X",
                            ],
                },

    # +-----+  Level 2 - Built on +-----+  Transforms  . 2 .
    # | @ X |  Threads 2          | @ X |              3 @ 1
    # | X . |  Cards 1            +-----+              . 1 .
    # +-----+  Transform 3: 4/2
    'E2-2':     {'elements': 'ae',
                 'pattern': [   "@ X",
                                "X .",
                            ],
                },

    # +-------+  Level 2 - Built on +-----+     +-----+  Transforms  7 2 5
    # | . @ X |  Threads 2          | @ X | and | @ . |              4 @ 1        
    # | X . . |  Cards 1            +-----+     | . X |              1 6 3
    # +-------+  Transform 7: 8/2               +-----+
    'E2-3':     {'elements': 'aefw',
                 'pattern': [   ". @ X",
                                "X . .",
                            ],
                },

    # +-----+  Level 2 - Built on +-----+     +-----+  Transforms  5 4 3
    # | @ . |  Threads 2          | @ X | and | @ . |              6 @ 2
    # | X X |  Cards 1            +-----+     | . X |              7 1 1
    # +-----+  Transform 7: 8/2               +-----+
    'E2-4':     {'elements': 'aefw',
                 'pattern': [   "@ .",
                                "X X",
                            ],
                },

    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . . 2 . .
    # | @ X X |  Threads 2          | @ X | and | @ . X |              . . 2 . .
    # +-------+  Cards 1            +-----+     +-------+              3 3 @ 1 1
    #            Transform 4: 8/4                                      . . 4 . .
    #                                                                  . . 4 . .
    'E2-5':     {'elements': 'ae',
                 'pattern': [    "@ X X",
                            ],
                },

    # +---------+  Level 3 - Built on +-----+     +-------+  Transforms  . . 2 . .
    # | X @ . X |  Threads 2          | @ X | and | @ . X |              . . 4 . .
    # +---------+  Cards 2            +-----+     +-------+              3 1 @ 3 1
    #              Transform 4: 8/4                                      . . 2 . .
    #                                                                    . . 4 . .
    'E2-6':     {'elements': 'ae',
                 'pattern': [   "X @ . X",
                            ],
                },

    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . . 4 . .
    # | @ . X |  Threads 2          | @ X | and | @ . X |              . . 2 . .
    # | X . . |  Cards 1            +-----+     +-------+              3 5 @ 4 1
    # +-------+  Transform 6: 8/4                                      . . 1 . .
    #                                                                  . . 6 . .
    'E2-7':     {'elements': 'ae',
                 'pattern': [   "@ . X",
                                "X . .",
                            ],
                },

    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . 4 . 3 .
    # | @ X . |  Threads 2          | @ X | and | @ . . |              5 . 3 . 2
    # | . . X |  Cards 1            +-----+     | . . X |              . 5 @ 1 .
    # +-------+  Transform 8: 12/5              +-------+              6 . 7 . 1
    #                                                                  . 7 . 8 .
    'E2-8':     {'elements': 'ae',
                 'pattern': [   "@ X .",
                                ". . X",
                            ],
                },

    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . 8 . 5 .
    # | @ . . |  Threads 2          | @ X | and | @ . . |              3 . 3 . 4
    # | X . X |  Cards 1            +-----+     | . . X |              . 7 @ 5 .
    # +-------+  Transform 8: 12/5              +-------+              2 . 1 . 1
    #                                                                  . 7 . 6 .
    'E2-9':     {'elements': 'ae',
                 'pattern': [   "@ . .",
                                "X . X",
                            ],
                },

    # +---------+  Level 3 - Built on +-----+     +-------+  Transforms  . 4 . 3 .
    # | X @ . . |  Threads 2          | @ X | and | @ . . |              5 . 7 . 2
    # | . . . X |  Cards 2            +-----+     | . . X |              . 1 @ 5 .
    # +---------+  Transform 8: 12/5              +-------+              6 . 3 . 1
    #                                                                    . 7 . 8 .
    'E2-10':    {'elements': 'ae',
                 'pattern': [   "X @ . .",
                                ". . . X",
                            ],
                },

    # +-------+  Level 3 - Built on +-----+     +-------+  Transforms  . 7 . 3 .
    # | X . . |  Threads 2          | @ X | and | @ . . |              6 . 1 . 5
    # | @ . . |  Cards 1            +-----+     | . . X |              . 3 @ 7 .
    # | . . X |  Transform 8: 12/5              +-------+              2 . 5 . 1
    # +-------+                                                        . 8 . 4 .
    'E2-11':    {'elements': 'ae',
                 'pattern': [   "X . .",
                                "@ . .",
                                ". . X",
                            ],
                },

    # +---------+  Level 3 - Built on +-----+     +---------+
    # | @ X . X |  Threads 2          | @ X | and | @ . . X |
    # +---------+  Cards 2            +-----+     +---------+
    #              Transform 4: 8/6
    'E2-12':    {'elements': 'ae',
                 'pattern': [   "@ X . X",
                            ],
                },

    # +-----------+  Level 3 - Built on +-----+     +---------+
    # | X @ . . X |  Threads 2          | @ X | and | @ . . X |
    # +-----------+  Cards 2            +-----+     +---------+
    #                Transform 4: 8/6
    'E2-13':    {'elements': 'ae',
                 'pattern': [   "X @ . . X",
                            ],
                },

    # +---------+  Level 3 - Built on +-----+     +---------+  Transforms  . . . 4 . . .
    # | @ . . X |  Threads 2          | @ X | and | @ . . X |              . . . . . . .
    # | X . . . |  Cards 2            +-----+     +---------+              . . . 2 . . .
    # +---------+  Transform 6: 8/6                                        3 . 5 @ 4 . 1
    #                                                                      . . . 1 . . .
    #                                                                      . . . . . . .
    #                                                                      . . . 6 . . .
    'E2-14':    {'elements': 'ae',
                 'pattern': [   "@ . . X",
                                "X . . .",
                            ],
                },

    # +---------+  Level 3 - Built on +-----+     +---------+  Transforms  . . 4 . 3 . .
    # | @ X . . |  Threads 2          | @ X | and | @ . . . |              . . . . . . .
    # | . . . X |  Cards 2            +-----+     | . . . X |              5 . . 3 . . 2
    # +---------+  Transform 8: 12/8              +---------+              . . 5 @ 1 . .
    #                                                                      6 . . 7 . . 1
    #                                                                      . . . . . . .
    #                                                                      . . 7 . 8 . .
    'E2-15':    {'elements': 'ae',
                 'pattern': [   "@ X . .",
                                ". . . X",
                            ],
                },

    # +---------+  Level 3 - Built on +-----+     +---------+  Transforms  . . 8 . 5 . .
    # | @ . . . |  Threads 2          | @ X | and | @ . . . |              . . . . . . .
    # | X . . X |  Cards 2            +-----+     | . . . X |              3 . . 3 . . 4
    # +---------+  Transform 8: 12/8              +---------+              . . 7 @ 5 . .
    #                                                                      2 . . 1 . . 1
    #                                                                      . . . . . . .
    #                                                                      . . 7 . 6 . .
    'E2-16':    {'elements': 'ae',
                 'pattern': [   "@ . . .",
                                "X . . X",
                            ],
                },

    # +-----------+  Level 3 - Built on +-----+     +---------+
    # | X @ . . . |  Threads 2          | @ X | and | @ . . . |
    # | . . . . X |  Cards 2            +-----+     | . . . X |
    # +-----------+  Transform 8                    +---------+
    'E2-17':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+  Level 3 - Built on +-----+     +---------+
    # | X . . . |  Threads 2          | @ X | and | @ . . . |
    # | @ . . . |  Cards 3            +-----+     | . . . X |
    # | . . . X |  Transform 8                    +---------+
    # +---------+
    'E2-18':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-------+  Level 2 - Built on +-----+  Transforms  3 . 2
    # | . @ . |  Threads 2          | @ . |              . @ .
    # | X . X |  Cards 1            | . X |              1 . 1
    # +-------+  Transform 3: 4/2   +-----+
    'E2-19':    {'elements': 'fw',
                 'pattern': [   ". @ .",
                                "X . X",
                            ],
                },

    # +-------+  Level 3 - Built on +-----+  Transforms  1 . 2
    # | X . . |  Threads 2          | @ . |              . @ .
    # | . @ . |  Cards 2            | . X |              2 . 1
    # | . . X |  Transform 2: 4/2   +-----+
    # +-------+
    'E2-20':    {'elements': 'fw',
                 'pattern': [   "X . .",
                                ". @ .",
                                ". . X",
                            ],
                },

    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . . 3 . .
    # | @ . X |  Threads 2          | @ . | and | @ . X |              . 4 . 2 .
    # | . X . |  Cards 1            | . X |     +-------+              5 . @ . 1
    # +-------+  Transform 7: 8/4   +-----+                            . 6 . 1 .
    #                                                                  . . 7 . .
    'E2-21':    {'elements': 'aefw',
                 'pattern': [   "@ . X",
                                ". X .",
                            ],
                },

    # +---------+  Level 3 - Built on +-----+     +-------+  Transforms  . . 3 . .
    # | . @ . X |  Threads 3          | @ . | and | @ . X |              . 2 . 6 .
    # | X . . . |  Cards 2            | . X |     +-------+              7 . @ . 1
    # +---------+  Transform 7: 8/4   +-----+                            . 1 . 4 .
    #                                                                    . . 5 . .
    'E2-22':    {'elements': 'aefw',
                 'pattern': [   ". @ . X",
                                "X . . .",
                            ],
                },

    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . 6 . 3 .
    # | @ . . |  Threads 2          | @ . | and | @ . . |              5 5 . 3 4
    # | . X X |  Cards 1            | . X |     | . . X |              . . @ . .
    # +-------+  Transform 8: 12/5  +-----+     +-------+              8 7 . 1 1
    #                                                                  . 7 . 2 .
    'E2-23':    {'elements': 'fw',
                 'pattern': [   "@ . .",
                                ". X X",
                            ],
                },

    # +---------+  Level 3 - Built on +-----+     +-------+  Transforms  . 2 . 6 .
    # | . @ . . |  Threads 2          | @ . | and | @ . . |              7 3 . 7 3
    # | X . . X |  Cards 2            | . X |     | . . X |              . . @ . .
    # +---------+  Transform 8: 12/5  +-----+     +-------+              5 1 . 5 1
    #                                                                    . 4 . 8 .
    'E2-24':    {'elements': 'fw',
                 'pattern': [   ". @ . .",
                                "X . . X",
                            ],
                },

    # +---------+  Level 3 - Built on +-----+     +-------+  Transforms  . 5 . 4 .
    # | X . . . |  Threads 2          | @ . | and | @ . . |              6 1 . 7 3
    # | . @ . . |  Cards 3            | . X |     | . . X |              . . @ . .
    # | . . . X |  Transform 8: 12/5  +-----+     +-------+              8 3 . 5 1
    # +---------+                                                        . 7 . 2 .
    'E2-25':    {'elements': 'fw',
                 'pattern': [   "X . . .",
                                ". @ . .",
                                ". . . X",
                            ],
                },

    # +-------+  Level 3 - Built on +-----+     +-------+  Transforms  . 6 . 7 .
    # | . @ . |  Threads 2          | @ . | and | @ . . |              2 7 . 5 4
    # | X . . |  Cards 2            | . X |     | . . X |              . . @ . .
    # | . . X |  Transform 8: 12/5  +-----+     +-------+              8 1 . 3 5
    # +-------+                                                        . 3 . 1 .
    'E2-26':    {'elements': 'fw',
                 'pattern': [   ". @ .",
                                "X . .",
                                ". . X",
                            ],
                },

    # +-------+  Level 3 - Built on +-----+     +-------+  Transforms  3 . . . 2
    # | @ . . |  Threads 2          | @ . | and | @ . . |              . 3 . 2 .
    # | . X . |  Cards 2            | . X |     | . . . |              . . @ . .
    # | . . X |  Transform 4: 8/5   +-----+     | . . X |              . 4 . 1 .
    # +-------+                                 +-------+              4 . . . 1
    'E2-27':    {'elements': 'fw',
                 'pattern': [   "@ . .",
                                ". X .",
                                ". . X",
                            ],
                },

    # +---------+  Level 3 - Built on +-----+     +---------+  Transforms  . . . 3 . . .
    # | @ . . X |  Threads 2          | @ . | and | @ . . X |              . . . . . . .
    # | . X . . |  Cards 2            | . X |     +---------+              . . 4 . 2 . .
    # +---------+  Transform 7: 8/6   +-----+                              5 . . @ . . 1
    #                                                                      . . 6 . 1 . .
    #                                                                      . . . . . . .
    #                                                                      . . . 7 . . .
    'E2-28':    {'elements': 'aefw',
                 'pattern': [   "@ . . X",
                                ". X . .",
                            ],
                },

    # +-----------+  Level 3 - Built on +-----+     +---------+  Transforms  . . . 2 . . .
    # | . @ . . X |  Threads 2          | @ . | and | @ . . X |              . . . . . . .
    # | X . . . . |  Cards 2            | . X |     +---------+              . . 7 . 5 . .
    # +-----------+  Transform 7: 8/6   +-----+                              4 . . @ . . 1
    #                                                                        . . 1 . 3 . .
    #                                                                        . . . . . . .
    #                                                                        . . . 6 . . .
    'E2-29':    {'elements': 'aefw',
                 'pattern': [   ". @ . . X",
                                "X . . . .",
                            ],
                },

    # +---------+  Level 3 - Built on +-----+     +---------+  Transforms  . . 6 . 7 . .
    # | @ . . . |  Threads 2          | @ . | and | @ . . . |              . . . . . . .
    # | . X . X |  Cards 2            | . X |     | . . . X |              5 . 5 . 7 . 8
    # +---------+  Transform 8: 12/8  +-----+     +---------+              . . . @ . . .
    #                                                                      4 . 3 . 1 . 1
    #                                                                      . . . . . . .
    #                                                                      . . 3 . 2 . .
    'E2-30':    {'elements': 'fw',
                 'pattern': [   "@ . . .",
                                ". X . X",
                            ],
                },

    # +---------+  Level 3 - Built on +-----+     +---------+  Transforms  . . 2 . 3 . .
    # | . X . . |  Threads 2          | @ . | and | @ . . . |              . . . . . . .
    # | @ . . . |  Cards 3            | . X |     | . . . X |              5 . 3 . 1 . 8
    # | . . . X |  Transform 8: 12/8  +-----+     +---------+              . . . @ . . .
    # +---------+                                                          4 . 5 . 7 . 1
    #                                                                      . . . . . . .
    #                                                                      . . 7 . 6 . .
    'E2-31':    {'elements': 'fw',
                 'pattern': [   ". X . .",
                                "@ . . .",
                                ". . . X",
                            ],
                },

    # +-----------+  Level 3 - Built on +-----+     +---------+
    # | . @ . . . |  Threads 2          | @ . | and | @ . . . |
    # | X . . . X |  Cards 2            | . X |     | . . . X |
    # +-----------+  Transform 8: 12/8  +-----+     +---------+
    'E2-32':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-----------+  Level 3 - Built on +-----+     +---------+
    # | X . . . . |  Threads 2          | @ . | and | @ . . . |
    # | . @ . . . |  Cards 4            | . X |     | . . . X |
    # | . . . . X |  Transform 8: 12/8  +-----+     +---------+
    # +-----------+
    'E2-33':    {'elements': 'fw',
                 'pattern': [],
                },
    
    # +---------+  Level 3 - Build on +-----+     +---------=
    # | @ . . . |  Threads 2          | @ . | and | @ . . . |
    # | . X . . |  Cards 3            | . X |     | . . . . |
    # | . . . X |  Transform 8        +-----+     | . . . X |
    # +---------+                                 +---------+
    # + 3 variants
    'E2-34':    {'elements': 'fw',
                 'pattern': [],
                },
    'E2-35':    {'elements': 'fw',
                 'pattern': [],
                },
    'E2-36':    {'elements': 'fw',
                 'pattern': [],
                },
    'E2-37':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-----------+  Level 3 - Built on +-------+
    # | X . @ . X |  Threads 2          | @ . X |
    # +-----------+  Cards 2            +-------+
    #                Transform 2: 4/4
    'E2-38':    {'elements': 'ae',
                 'pattern': [   "X . @ . X",
                            ],
                },

    # +-------+  Level 3 - Build on +-------+
    # | @ . X |  Threads 2          | @ . X |
    # | . . . |  Cards 2            +-------+
    # | X . . |  Transform 3: 4/4
    # +-------+
    'E2-39':    {'elements': 'ae',
                 'pattern': [   "@ . X",
                                ". . .",
                                "X . .",
                            ],
                },

    # +-------+  Level 2 - Built on +-------+     +-------+  Transforms  . 4 3 3 .
    # | @ . X |  Threads 2          | @ . X | and | @ . . |              5 . . . 2
    # | . . X |  Cards 1            +-------+     | . . X |              5 . @ . 1
    # +-------+  Transform 8: 12/5                +-------+              6 . . . 1
    #                                                                    . 7 7 8 .
    'E2-40':    {'elements': 'ae',
                 'pattern': [   "@ . X",
                                ". . X",
                            ],
                },

    # +-------+  Level 2 - Built on +-------+     +-------+  Transforms  . 3 7 2 .
    # | @ . X |  Threads 2          | @ . X | and | @ . . |              8 . . . 7
    # | . . . |  Cards 2            +-------+     | . . X |              3 . @ . 1
    # | . X . |  Transform 8: 12/5                +-------+              6 . . . 5
    # +-------+                                                          . 4 5 1 .
    'E2-41':    {'elements': 'ae',
                 'pattern': [   "@ . X",
                                ". . .",
                                ". X .",
                            ],
                },

    # +-----------+  Level 3 - Built on +-------+     +-------+
    # | X . @ . . |  Threads 2          | @ . X | and | @ . . |
    # | . . . . X |  Cards 2            +-------+     | . . X |
    # +-----------+  Transform 8: 12/5                +-------+
    'E2-42':    {'elements': 'ae',
                 'pattern': [   "X . @ . .",
                                ". . . . X",
                            ],
                },

    # +---------+  Level 2 - Built on +-------+     +-------+
    # | . @ . X |  Threads 2          | @ . X | and | @ . . |
    # | . . . . |  Cards 3            +-------+     | . . X |
    # | X . . . |  Trnsform 8: 12/5                 +-------+
    # +---------+
    'E2-43':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . X X |  Threads 2          | @ . X | and | @ . . X |
    # +---------+  Cards 2            +-------+     +---------+
    #              Transform 4: 8/5
    'E2-44':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-------------+  Level 3 - Built on +-------+     +---------+
    # | X . @ . . X |  Threads 2          | @ . X | and | @ . . X |
    # +-------------+  Cards 3            +-------+     +---------+
    #                  Transform 4: 8/5
    'E2-45':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . . X |  Threads 2          | @ . X | and | @ . . X |
    # | . . . . |  Cards 3            +-------+     +---------+
    # | X . . . |  Transform 6: 8/5
    # +---------+
    'E2-46':    {'elements': 'ae',
                 'pattern': [   "@ . . X",
                                ". . . .",
                                "X . . .",
                            ],
                },

    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . X . |  Threads 2          | @ . X | and | @ . . . |
    # | . . . X |  Cards 2            +-------+     | . . . X |
    # +---------+  Transform 8: 12/8                +---------+
    # + 3 variants
    'E2-47':    {'elements': 'ae',
                 'pattern': [],
                },
    'E2-48':    {'elements': 'ae',
                 'pattern': [],
                },
    'E2-49':    {'elements': 'ae',
                 'pattern': [],
                },
    'E2-50':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-----------+  Level 3 - Built on +-------+     +-----------+
    # | @ . X . . |  Threads 2          | @ . X | and | @ . . . . |
    # | . . . . X |  Cards 2            +-------+     | . . . . X |
    # +-----------+  Transform 8: 12/                 +-----------+
    # + 3 variants
    'E2-51':    {'elements': 'ae',
                 'pattern': [],
                },
    'E2-52':    {'elements': 'ae',
                 'pattern': [],
                },
    'E2-53':    {'elements': 'ae',
                 'pattern': [],
                },
    'E2-54':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-------+  Level 3 - Built on +-------+  Transforms  . 3 . 3 .
    # | . @ . |  Threads 2          | @ . . |              4 . . . 2
    # | . . . |  Cards 2            | . . X |              . . @ . .
    # | X . X |  Transform 4: 8/5   +-------+              4 . . . 2
    # +-------+                                            . 1 . 1 .
    'E2-55':    {'elements': 'aefw',
                 'pattern': [   ". @ .",
                                ". . .",
                                "X . X",
                            ],
                },

    # +---------+  Level 3 - Built on +-------+
    # | . @ . . |  Threads 2          | @ . . |
    # | . . . X |  Cards 3            | . . X |
    # | X . . . |  Transform 6: 8/5   +-------+
    # +---------+
    'E2-56':    {'elements': 'aefw',
                 'pattern': [],
                },

    # +-----------+  Level 3 - Built on +-------+
    # | . . @ . . |  Threads 2          | @ . . |
    # | X . . . X |  Cards 2            | . . X |
    # +-----------+  Transform 6: 8/5   +-------+
    'E2-57':    {'elements': 'aefw',
                 'pattern': [],
                },

    # +-----------+  Level 3 - Built on +-------+
    # | X . . . . |  Threads 2          | @ . . |
    # | . . @ . . |  Cards 4            | . . X |
    # | . . . . X |  Transform 4: 8/5   +-------+
    # +-----------+
    'E2-58':    {'elements': 'aefw',
                 'pattern': [],
                },

    # +---------+  Level 3 - Built on +-------+  Transforms  . 2 . 3 .
    # | . . . X |  Threads 2          | @ . . |              4 . . . 1
    # | . @ . . |  Cards 4            | . . X |              . . @ . .
    # | . . . . |  Transform 4: 8/5   +-------+              3 . . . 2
    # | X . . . |                                            . 1 . 4 .
    # +---------+
    'E2-59':    {'elements': 'aefw',
                 'pattern': [],
                },

    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . . X |  Threads 2          | @ . . | and | @ . . X |
    # | . . X . |  Cards 2            | . . X |     +---------+
    # +---------+  Transform 8: 12/   +-------+
    # + 3 variants
    'E2-60':    {'elements': 'ae',
                 'pattern': [],
                },
    'E2-61':    {'elements': 'ae',
                 'pattern': [],
                },
    'E2-62':    {'elements': 'ae',
                 'pattern': [],
                },
    'E2-63':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . . . |  Threads 2          | @ . . | and | @ . . . |
    # | . . X X |  Cards 2            | . . X |     | . . . X |
    # +---------+  Transform 8: 16/   +-------+     +---------+
    # + 3 variants
    'E2-64':    {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-65':    {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-66':    {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-67':    {'elements': 'aefw',
                 'pattern': [],
                },

    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . . . |  Threads 2          | @ . . | and | @ . . . |
    # | . . X . |  Cards 3            | . . X |     | . . . . |
    # | . . . X |  Transform 8: 16/   +-------+     | . . . X |
    # +---------+                                   +---------+
    # + 3 variants
    'E2-68':    {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-69':    {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-70':    {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-71':    {'elements': 'aefw',
                 'pattern': [],
                },

    # +-----------+  Level 3 - Built on +-------+     +-----------+
    # | @ . . . X |  Threads 2          | @ . . | and | @ . . . X |
    # | . . X . . |  Cards 2            | . . X |     +-----------+
    # +-----------+  Transform 8: 12/   +-------+
    # + 3 variants
    'E2-72':    {'elements': 'ae',
                 'pattern': [],
                },
    'E2-73':    {'elements': 'ae',
                 'pattern': [],
                },
    'E2-74':    {'elements': 'ae',
                 'pattern': [],
                },
    'E2-75':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-----------+  Level 3 - Built on +-------+     +-----------+
    # | @ . . . . |  Threads 2          | @ . . | and | @ . . . . |
    # | . . X . X |  Cards 2            | . . X |     | . . . . X |
    # +-----------+  Transform 8: 16/   +-------+     +-----------+
    # + 3 variants
    'E2-76':    {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-77':    {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-78':    {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-79':    {'elements': 'aefw',
                 'pattern': [],
                },

    # +-----------+  Level 3 - Built on +-------+     +-----------+
    # | @ . . . . |  Threads 2          | @ . . | and | @ . . . . |
    # | . . X . . |  Cards 4            | . . X |     | . . . . . |
    # | . . . . X |  Transform 8: 12/   +-------+     | . . . . X |
    # +-----------+                                   +-----------+
    # + 3 variants
    'E2-80':    {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-81':    {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-82':    {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-83':    {'elements': 'aefw',
                 'pattern': [],
                },

    #  _____ _                   _       _    ___        _      ___ 
    # |   __| |___ _____ ___ ___| |_ ___| |  |_  |     _| |_   |_  |
    # |   __| | -_|     | -_|   |  _| .'| |   _| |_   |_   _|  |_  |
    # |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |_____|    |_|    |___|
    #

    # +-------+  Level 4 - Build on +-----+     +-------+
    # | @ . X |  Threads 3          | @ . | and | @ . X |
    # | . X . |  Cards 2            | . X |     +-------+
    # | X . . |  Transform 4: 8/5   +-----+
    # +-------+
    'E3-1':     {'elements': 'aefw',
                 'pattern': [],
                },

    # +-------+  Level 4 - Build on +-----+     +-------+  Transforms  3 . . . 2
    # | @ X . |  Threads 3          | @ X | and | @ . . |              . . 2 . .
    # | X . . |  Cards 2            +-----+     | . . . |              . 3 @ 1 .
    # | . . X |  Transform 4: 8/5               | . . X |              . . 1 . .
    # +-------+                                 +-------+              4 . . . 1
    'E3-2':     {'elements': 'aefw',
                 'pattern': [],
                },

    # +-------+  Level 4 - Build on +-------+     +-------+  Transforms  3 . 2 . 2
    # | @ . X |  Threads 3          | @ . X | and | @ . . |              . . . . .
    # | . . . |  Cards 2            +-------+     | . . . |              3 . @ . 1
    # | X . X |  Transform 4: 8/6                 | . . X |              . . . . .
    # +-------+                                   +-------+              4 . 1 . 1
    'E3-3':     {'elements': 'aefw',
                 'pattern': [],
                },

    #  _____ _                   _       _    ___      _      ___   
    # |   __| |___ _____ ___ ___| |_ ___| |  |_  |   _| |_   |_  |  
    # |   __| | -_|     | -_|   |  _| .'| |  |  _|  |_   _|   _| |_ 
    # |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |___|    |_|    |_____|
    #

    # +-------+  Level 2 - Built on +-----+
    # | @ X @ |  Threads 1          | @ X |
    # +-------+  Cards 2            +-----+
    #            Transform 1: 1/
    'EE1-1':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-----+  Level 2 - Built on +-----+
    # | @ X |  Threads 1          | @ X |
    # | . @ |  Cards 2            +-----+
    # +-----+  Transform 2: 2/
    'EE1-2':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-------+  Level 2 - Built on +-----+     +-------+
    # | @ @ X |  Threads 1          | @ X | and | @ . X |
    # +-------+  Cards 2            +-----+     +-------+
    #            Transform 2: 2/
    'EE1-3':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-------+  Level 3 - Built on +-----+
    # | @ . . |  Threads 1          | @ . |
    # | . X . |  Cards 2            | . X |
    # | . . @ |  Transform 1: 1/    +-----+
    # +-------+
    'EE1-4':    {'elements': 'fw',
                 'pattern': [   "@ . .",
                                ". X .",
                                ". . @",
                            ],
                },

    # +-------+  Level 2 - Built on +-----+
    # | @ . @ |  Threads 1          | @ . |
    # | . X . |  Cards 2            | . X |
    # +-------+  Transform 2: 2/    +-----+
    'EE1-5':    {'elements': 'fw',
                 'pattern': [   "@ . @",
                                ". X .",
                            ],
                },

    # +-----------+  Level 3 - Built on +-------+
    # | @ . . . . |  Threads 1          | @ . . |
    # | . . X . . |  Cards 4            | . . X |
    # | . . . . @ |  Transform 1: 1/    +-------+
    # +-----------+
    'EE1-6':    {'elements': 'aefw',
                 'pattern': [   "@ . . . .",
                                ". . X . .",
                                ". . . . @",
                            ],
                },

    #  _____ _                   _       _    ___      _      ___ 
    # |   __| |___ _____ ___ ___| |_ ___| |  |_  |   _| |_   |_  |
    # |   __| | -_|     | -_|   |  _| .'| |  |  _|  |_   _|  |  _|
    # |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |___|    |_|    |___|
    #

    # +-----+  Level 3 - Built on +-----+
    # | @ X |  Threads 2          | @ X |
    # | X @ |  Cards 2            +-----+
    # +-----+  Transform 1: 2/
    'EE2-1':    {'elements': 'ae',
                 'pattern': [   "@ X",
                                "X @",
                            ],
                },

    # +-------+  Level 3 - Built on +-----+  Transforms  . 2 . .
    # | @ X . |  Threads 2          | @ X |              3 @ 1 .
    # | . @ X |  Cards 2            +-----+              . 3 @ 1
    # +-------+  Transform 4: 6/                         . . 4 .
    'EE2-2':    {'elements': 'ae',
                 'pattern': [   "@ X .",
                                ". @ X",
                            ],
                },

    # +-------+  Level 4 - Built on +-----+
    # | X . . |  Threads 2          | @ X |
    # | @ . . |  Cards 2            +-----+
    # | . @ X |  Transform 2; 4/
    # +-------+
    'EE2-3':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+  Level 3 - Built on +-----+
    # | X @ . . |  Threads 2          | @ X |
    # | . . @ X |  Cards 2            +-----+
    # +---------+  Transform 2: 4/
    'EE2-4':    {'elements': 'ae',
                 'pattern': [   "X @ . .",
                                ". . @ X",
                            ],
                },

    # +-------+  Level 3 - Built on +-----+  Transforms  . 2 . .
    # | @ . . |  Threads 2          | @ X |              3 @ 3 .
    # | X @ X |  Cards 2            +-----+              . 1 @ 1
    # +-------+  Transform 4: 6/                         . . 4 .
    'EE2-5':    {'elements': 'ae',
                 'pattern': [   "@ . .",
                                "X @ X",
                            ],
                },

    # +-------+  Level 4 - Built on +-----+
    # | . @ . |  Threads 2          | @ . |
    # | X . X |  Cards 2            | . X |
    # | . @ . |  Transform 1: 1/    +-----+
    # +-------+
    'EE2-6':    {'elements': 'fw',
                 'pattern': [   ". @ .",
                                "X . X",
                                ". @ .",
                            ],
                },

    # +---------+  Level 4 - Built on +-----+
    # | . @ @ . |  Threads 2          | @ . |
    # | X . . X |  Cards 2            | . X |
    # +---------+  Transform 2: 4/    +-----+
    'EE2-7':    {'elements': 'fw',
                 'pattern': [],
                },

    # +---------+  Level 4 - Built on +-----+
    # | X . . . |  Threads 2          | @ . |
    # | . @ @ . |  Cards 3            | . X |
    # | . . . X |  Transform 2: 4/    +-----+
    # +---------+
    'EE2-8':    {'elements': 'fw',
                 'pattern': [   "X . . .",
                                ". @ @ .",
                                ". . . X",
                            ],
                },

}
