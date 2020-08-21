# Spell card patterns for Woven
# Gary Kacmarcik
#
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


# Element pattern affinity

# Air / Earth
# +-----+  +-------+  +---------+
# | @ X |  | @ . X |  | @ . . X |
# +-----+  +-------+  +---------+

# Fire / Water
# +-----+  +-------+  +---------+
# | @ . |  | @ . . |  | @ . . . |
# | . X |  | . . . |  | . . . . |
# +-----+  | . . X |  | . . . . |
#          +-------+  | . . . X |
#                     +---------+

# Knight's move - All elements
# +-------+
# | @ . . |
# | . . X |
# +-------+

# Long knight's move - Air / Earth
# +---------+
# | @ . . . |
# | . . . X |
# +---------+

# Long, wide knight's move - Fire / Water
# +---------+
# | @ . . . |
# | . . . . |
# | . . . X |
# +---------+

# Summary: (a = Air/Earth; f = Fire/Water; * = all)
# +---------------+
# | F f a A a f F |
# | f F * a * F f |
# | a * F A F * a |
# | A A A @ A A A |
# | a * F A F * a |
# | f F * A * F f |
# | F f a A a f F |
# +---------------+

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

    # +---------+  Level 2
    # | X . . . |
    # | . . . . |
    # | . . . . |
    # | . . . X |
    # +---------+
    'N2-9':     {'elements': 'none',
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

    # +-----+  Level 1            Transforms  . 2 .
    # | @ X |  Threads 1                      3 @ 1
    # +-----+  Cards 1                        . 4 .
    #          Transform 4: 4/2
    'E1-1':     {'elements': 'ae',
                 'pattern': [   "@ X",
                            ],
                },

    # +-----+  Level 1            Transforms  3 . 2
    # | @ . |  Threads 1                      . @ .
    # | . X |  Cards 1                        4 . 1
    # +-----+  Transform 4: 4/2
    'E1-2':     {'elements': 'fw',
                 'pattern': [   "@ .",
                                ". X",
                            ],
                },

    # +-------+  Level 1          Transforms  . . 2 . .
    # | @ . X |  Threads 1                    . . . . .
    # +-------+  Cards 1                      3 . @ . 1
    #            Transform 4: 4/4             . . . . .
    #                                         . . 4 . .
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

    # +---------+  Level 2        Transforms  . . . 2 . . .
    # | @ . . X |  Threads 1                  . . . . . . .
    # +---------+  Cards 2                    . . . . . . .
    #              Transform 4: 4/6           3 . . @ . . 1
    #                                         . . . . . . .
    #                                         . . . . . . .
    #                                         . . . 4 . . .
    'E1-6':     {'elements': 'ae',
                 'pattern': [    "@ . . X",
                            ],
                },

    # +---------+  Level 2        Transforms  . . 4 . 3 . .
    # | @ . . . |  Threads 1                  . . . . . . .
    # | . . . X |  Cards 2                    5 . . . . . 2
    # +---------+  Transform 8                . . . @ . . .
    #                                         6 . . . . . 1
    #                                         . . . . . . .
    #                                         . . 7 . 8 . .
    'E1-7':     {'elements': 'ae',
                 'pattern': [   "@ . . .",
                                ". . . X",
                            ],
                },

    # +---------+  Level 2        Transforms  . 4 . . . 3 .
    # | @ . . . |  Threads 1                  5 . . . . . 2
    # | . . . . |  Cards 2                    . . . . . . .
    # | . . . X |  Transform 8                . . . @ . . .
    # +---------+                             . . . . . . .
    #                                         6 . . . . . 1
    #                                         . 7 . . . 8 .
    'E1-8':     {'elements': 'fw',
                 'pattern': [   "@ . . .",
                                ". . . .",
                                ". . . X",
                            ],
                },

    # +---------+  Level 2        Transforms  3 . . . . . 2
    # | @ . . . |  Threads 1                  . . . . . . .
    # | . . . . |  Cards 2                    . . . . . . .
    # | . . . . |  Transform 4: 4/8           . . . @ . . .
    # | . . . X |                             . . . . . . .
    # +---------+                             . . . . . . .
    #                                         4 . . . . . 1
    'E1-9':     {'elements': 'fw',
                 'pattern': [   "@ . . .",
                                ". . . .",
                                ". . . .",
                                ". . . X",
                            ],
                },

    #  _____ _                   _       _    ___        _      ___ 
    # |   __| |___ _____ ___ ___| |_ ___| |  |_  |     _| |_   |_  |
    # |   __| | -_|     | -_|   |  _| .'| |   _| |_   |_   _|  |  _|
    # |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |_____|    |_|    |___|
    #

    #                                                                 #
    # +-----+   +-----+                                               #
    # | @ X | + | @ X |                                               #
    # +-----+   +-----+                                               #
    #                                                                 #

    # . . . . . . .    a = 1
    # . . . . . . .    b = 2
    # . . . a . . .
    # . . b @ X . .
    # . . . a . . .
    # . . . . . . .
    # . . . . . . .
    
    # +-----+  Level 2            Transforms  . 2 .
    # | @ X |  Threads 2                      3 @ 1
    # | X . |  Cards 1                        . 1 .
    # +-----+  Transform 3: 4/2
    'E2-1':     {'elements': 'ae',
                 'pattern': [   "@ X",
                                "X .",
                            ],
                },

    # +-------+  Level 2          Transforms  . 2 .
    # | X @ X |  Threads 1                    1 @ 1
    # +-------+  Cards 1                      . 2 .
    #            Transform 2: 4/2
    'E2-2':     {'elements': 'ae',
                 'pattern': [   "X @ X",
                            ],
                },

    #                                                                 #
    # +-----+   +-----+                                               #
    # | @ X | + | @ . |                                               #
    # +-----+   | . X |                                               #
    #           +-----+                                               #
    #                                                                 #    

    # . . . . . . .    a = 3
    # . . . . . . .    b = 4
    # . . . b . . .
    # . . b @ a . .
    # . . . a X . .
    # . . . . . . .
    # . . . . . . .
    
    # +-----+  Level 2            Transforms  5 4 3
    # | @ . |  Threads 2                      6 @ 2
    # | X X |  Cards 1                        7 1 1
    # +-----+  Transform 7: 8/2
    'E2-3':     {'elements': 'aefw',
                 'pattern': [   "@ .",
                                "X X",
                            ],
                },

    # +-------+  Level 2          Transforms  7 2 5
    # | . @ X |  Threads 2                    4 @ 1        
    # | X . . |  Cards 1                      1 6 3
    # +-------+  Transform 7: 8/2
    'E2-4':     {'elements': 'aefw',
                 'pattern': [   ". @ X",
                                "X . .",
                            ],
                },

    #                                                                 #
    # +-----+   +-------+                                             #
    # | @ X | + | @ . X |                                             #
    # +-----+   +-------+                                             #
    #                                                                 #

    # . . . . . . .    a = 5
    # . . . . . . .    b = 6
    # . . . b . . .    c = 7
    # . . c @ a X .
    # . . . b . . .
    # . . . . . . .
    # . . . . . . .
    
    # +-------+  Level 2          Transforms  . . 2 . .
    # | @ X X |  Threads 2                    . . 2 . .
    # +-------+  Cards 1                      3 3 @ 1 1
    #            Transform 4: 8/4             . . 4 . .
    #                                         . . 4 . .
    'E2-5':     {'elements': 'ae',
                 'pattern': [    "@ X X",
                            ],
                },

    # +-------+  Level 2          Transforms  . . 4 . .
    # | @ . X |  Threads 2                    . . 2 . .
    # | X . . |  Cards 1                      3 5 @ 4 1
    # +-------+  Transform 6: 8/4             . . 1 . .
    #                                         . . 6 . .
    'E2-6':     {'elements': 'ae',
                 'pattern': [   "@ . X",
                                "X . .",
                            ],
                },

    # +---------+  Level 3        Transforms  . . 2 . .
    # | X @ . X |  Threads 2                  . . 4 . .
    # +---------+  Cards 2                    3 1 @ 3 1
    #              Transform 4: 8/4           . . 2 . .
    #                                         . . 4 . .
    'E2-7':     {'elements': 'ae',
                 'pattern': [   "X @ . X",
                            ],
                },

    #                                                                 #
    # +-----+   +-------+                                             #
    # | @ X | + | @ . . |                                             #
    # +-----+   | . . X |                                             #
    #           +-------+                                             #
    #                                                                 #

    # . . . . . . .    . . . . . . .    a = 8
    # . . . . . . .    . . b . d . .    b = 9
    # . . . b . . .    . c . . . a .    c = 10
    # . . c @ a . .    . . . @ X . .    d = 11
    # . . . d . X .    . c . . . a .
    # . . . . . . .    . . b . d . .
    # . . . . . . .    . . . . . . .
    
    # +-------+  Level 2          Transforms  . 4 . 3 .
    # | @ X . |  Threads 2                    5 . 3 . 2
    # | . . X |  Cards 1                      . 5 @ 1 .
    # +-------+  Transform 8: 12/5            6 . 7 . 1
    #                                         . 7 . 8 .
    'E2-8':     {'elements': 'ae',
                 'pattern': [   "@ X .",
                                ". . X",
                            ],
                },

    # +-------+  Level 3          Transforms  . 7 . 3 .
    # | X . . |  Threads 2                    6 . 1 . 5
    # | @ . . |  Cards 1                      . 3 @ 7 .
    # | . . X |  Transform 8: 12/5            2 . 5 . 1
    # +-------+                               . 8 . 4 .
    'E2-9':     {'elements': 'ae',
                 'pattern': [   "X . .",
                                "@ . .",
                                ". . X",
                            ],
                },

    # +---------+  Level 3        Transforms  . 4 . 3 .
    # | X @ . . |  Threads 2                  5 . 7 . 2
    # | . . . X |  Cards 2                    . 1 @ 5 .
    # +---------+  Transform 8: 12/5          6 . 3 . 1
    #                                         . 7 . 8 .
    'E2-10':    {'elements': 'ae',
                 'pattern': [   "X @ . .",
                                ". . . X",
                            ],
                },

    # +-------+  Level 2          Transforms  . 8 . 5 .
    # | @ . . |  Threads 2                    3 . 3 . 4
    # | X . X |  Cards 1                      . 7 @ 5 .
    # +-------+  Transform 8: 12/5            2 . 1 . 1
    #                                         . 7 . 6 .
    'E2-11':    {'elements': 'ae',
                 'pattern': [   "@ . .",
                                "X . X",
                            ],
                },

    #                                                                 #
    # +-----+   +-------+                                             #
    # | @ X | + | @ . . |                                             #
    # +-----+   | . . . |                                             #
    #           | . . X |                                             #
    #           +-------+                                             #
    #                                                                 #

    # . . . . . . .    a = 12
    # . . . . . . .    b = 13
    # . . . b . . .
    # . . b @ a . .
    # . . . a . . .
    # . . . . . X .
    # . . . . . . .
    
    # +-------+  Level 2          Transforms  4 . . . 2
    # | @ X . |  Threads 2                    . . 3 . .
    # | . . . |  Cards 2                      . 5 @ 1 .
    # | . . X |  Transform 7: 8/6             . . 7 . ,
    # +-------+                               6 . . . 1
    'E2-12':    {'elements': 'aefw',
                 'pattern': [   "@ X .",
                                ". . .",
                                ". . X",
                            ],
                },

    # +---------+  Level 3        Transforms  4 . . . 2
    # | X @ . . |  Threads 2                  . . 7 . .
    # | . . . . |  Cards 2                    . 1 @ 5 .
    # | . . . X |  Transform 7: 8/6           . . 3 . .
    # +---------+                             6 . . . 1
    'E2-13':    {'elements': 'aefw',
                 'pattern': [   "X @ . .",
                                ". . . .",
                                ". . . X",
                            ],
                },

    #                                                                 #
    # +-----+   +---------+                                           #
    # | @ X | + | @ . . X |                                           #
    # +-----+   +---------+                                           #
    #                                                                 #

    # . . . . . . .    a = 14
    # . . . . . . .    b = 15
    # . . . b . . .    c = 16
    # . . c @ a . X
    # . . . b . . .
    # . . . . . . .
    # . . . . . . .
    
    # +---------+  Level 3        Transforms  . . . 2 . . .
    # | @ X . X |  Threads 2                  . . . . . . .
    # +---------+  Cards 2                    . . . 2 . . .
    #              Transform 4: 8/6           3 . 3 @ 1 . 1
    #                                         . . . 4 . . .
    #                                         . . . . . . .
    #                                         . . . 4 . . .
    'E2-14':    {'elements': 'ae',
                 'pattern': [   "@ X . X",
                            ],
                },

    # +---------+  Level 3        Transforms  . . . 4 . . .
    # | @ . . X |  Threads 2                  . . . . . . .
    # | X . . . |  Cards 2                    . . . 2 . . .
    # +---------+  Transform 6: 8/6           3 . 5 @ 4 . 1
    #                                         . . . 1 . . .
    #                                         . . . . . . .
    #                                         . . . 6 . . .
    'E2-15':    {'elements': 'ae',
                 'pattern': [   "@ . . X",
                                "X . . .",
                            ],
                },

    # +-----------+  Level 3      Transforms  . . . 2 . . .
    # | X @ . . X |  Threads 2                . . . . . . .
    # +-----------+  Cards 2                  . . . 4 . . .
    #                Transform 4: 8/6         3 . 1 @ 3 . 1
    #                                         . . . 2 . . .
    #                                         . . . . . . .
    #                                         . . . 4 . . .
    'E2-16':    {'elements': 'ae',
                 'pattern': [   "X @ . . X",
                            ],
                },

    #                                                                 #
    # +-----+   +---------+                                           #
    # | @ X | + | @ . . . |                                           #
    # +-----+   | . . . X |                                           #
    #           +---------+                                           #
    #                                                                 #

    # . . . . . . .    . . b . d . .    a = 17
    # . . . . . . .    . . . . . . .    b = 18
    # . . . b . . .    c . . . . . a    c = 19
    # . . c @ a . .    . . . @ X . .    d = 20
    # . . . d . . X    c . . . . . a
    # . . . . . . .    . . . . . . .
    # . . . . . . .    . . b . d . .
    
    # +---------+  Level 3        Transforms  . . 4 . 3 . .
    # | @ X . . |  Threads 2                  . . . . . . .
    # | . . . X |  Cards 2                    5 . . 3 . . 2
    # +---------+  Transform 8: 12/8          . . 5 @ 1 . .
    #                                         6 . . 7 . . 1
    #                                         . . . . . . .
    #                                         . . 7 . 8 . .
    'E2-17':    {'elements': 'ae',
                 'pattern': [   "@ X . .",
                                ". . . X",
                            ],
                },

    # +---------+  Level 3
    # | X . . . |  Threads 2
    # | @ . . . |  Cards 3
    # | . . . X |  Transform 8
    # +---------+
    'E2-18':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-----------+  Level 3
    # | X @ . . . |  Threads 2
    # | . . . . X |  Cards 2
    # +-----------+  Transform 8
    'E2-19':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+  Level 3        Transforms  . . 8 . 5 . .
    # | @ . . . |  Threads 2                  . . . . . . .
    # | X . . X |  Cards 2                    3 . . 3 . . 4
    # +---------+  Transform 8: 12/8          . . 7 @ 5 . .
    #                                         2 . . 1 . . 1
    #                                         . . . . . . .
    #                                         . . 7 . 6 . .
    'E2-20':    {'elements': 'ae',
                 'pattern': [   "@ . . .",
                                "X . . X",
                            ],
                },

    #                                                                 #
    # +-----+   +---------+                                           #
    # | @ X | + | @ . . . |                                           #
    # +-----+   | . . . . |                                           #
    #           | . . . X |                                           #
    #           +---------+                                           #
    #                                                                 #

    # . . . . . . .    . b . . . d .    a = 21
    # . . . . . . .    c . . . . . a    b = 22
    # . . . b . . .    . . . . . . .    c = 23
    # . . c @ a . .    . . . @ X . .    d = 24
    # . . . d . . .    . . . . . . .
    # . . . . . . X    c . . . . . a
    # . . . . . . .    . b . . . d .
    
    # +---------+  Level 3        Transforms  . 4 . . . 3 .
    # | @ X . . |  Threads 2                  5 . . . . . 2
    # | . . . . |  Cards 2                    . . . 3 . . .
    # | . . . X |  Transform 8: 12/8          . . 5 @ 1 . .
    # +---------+                             . . . 7 . . .
    #                                         6 . . . . . 1
    #                                         . 7 . . . 8 .
    'E2-21':    {'elements': 'ae',
                 'pattern': [   "@ X . .",
                                ". . . X",
                            ],
                },

    # +---------+  Level 
    # | X . . . |  Threads 
    # | @ . . . |  Cards 
    # | . . . . |  Transform 
    # | . . . X |
    # +---------+
    'E2-22':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-----------+  Level 
    # | X @ . . . |  Threads 
    # | . . . . . |  Cards 
    # | . . . . X |  Transform 
    # +-----------+
    'E2-23':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+  Level 3        Transforms  . 8 . . . 5 .
    # | @ . . . |  Threads 2                  3 . . . . . 4
    # | X . . . |  Cards 2                    . . . 3 . . .
    # | . . . X |  Transform 8: 12/8          . . 7 @ 5 . .
    # +---------+                             . . . 1 . . .
    #                                         2 . . . . . 1
    #                                         . 7 . . . 6 .
    'E2-24':    {'elements': 'ae',
                 'pattern': [   "@ . . .",
                                "X . . X",
                            ],
                },

    #                                                                 #
    # +-----+   +---------+                                           #
    # | @ X | + | @ . . . |                                           #
    # +-----+   | . . . . |                                           #
    #           | . . . . |                                           #
    #           | . . . X |                                           #
    #           +---------+                                           #
    #                                                                 #

    # . . . . . . .    b . . . . . a    a = 25
    # . . . . . . .    . . . . . . .    b = 26
    # . . . b . . .    . . . . . . .
    # . . b @ a . .    . . . @ X . .
    # . . . a . . .    . . . . . . .
    # . . . . . . .    . . . . . . .
    # . . . . . . X    b . . . . . a
    
    # +---------+  Level 
    # | @ X . . |  Threads 
    # | . . . . |  Cards 
    # | . . . . |  Transform 
    # | . . . X |
    # +---------+
    'E2-25':    {'elements': 'aefw',
                 'pattern': [],
                },

    # +-----------+  Level 
    # | X @ . . . |  Threads 
    # | . . . . . |  Cards 
    # | . . . . . |  Transform 
    # | . . . . X |
    # +-----------+
    'E2-26':    {'elements': 'aefw',
                 'pattern': [],
                },
    
    #                                                                 #
    # +-----+   +-----+                                               #
    # | @ . | + | @ . |                                               #
    # | . X |   | . X |                                               #
    # +-----+   +-----+                                               #
    #                                                                 #

    # . . . . . . .    a = 27
    # . . . . . . .    b = 28
    # . . b . a . .
    # . . . @ . . .
    # . . a . X . .
    # . . . . . . .
    # . . . . . . .
    
    # +-------+  Level 2          Transforms  3 . 2
    # | . @ . |  Threads 2                    . @ .
    # | X . X |  Cards 1                      1 . 1
    # +-------+  Transform 3: 4/2
    'E2-27':    {'elements': 'fw',
                 'pattern': [   ". @ .",
                                "X . X",
                            ],
                },

    # +-------+  Level 3          Transforms  1 . 2
    # | X . . |  Threads 2                    . @ .
    # | . @ . |  Cards 2                      2 . 1
    # | . . X |  Transform 2: 4/2
    # +-------+
    'E2-28':    {'elements': 'fw',
                 'pattern': [   "X . .",
                                ". @ .",
                                ". . X",
                            ],
                },

    #                                                                 #
    # +-----+   +-------+                                             #
    # | @ . | + | @ . X |                                             #
    # | . X |   +-------+                                             #
    # +-----+                                                         #
    #                                                                 #

    # . . . . . . .    a = 29
    # . . . . . . .    b = 30
    # . . b . a . .
    # . . . @ . X .
    # . . b . a . .
    # . . . . . . .
    # . . . . . . .
    
    # +-------+  Level 2          Transforms  . . 3 . .
    # | @ . X |  Threads 2                    . 4 . 2 .
    # | . X . |  Cards 1                      5 . @ . 1
    # +-------+  Transform 7: 8/4             . 6 . 1 .
    #                                         . . 7 . .
    'E2-29':    {'elements': 'aefw',
                 'pattern': [   "@ . X",
                                ". X .",
                            ],
                },

    # +---------+  Level 3        Transforms  . . 3 . .
    # | . @ . X |  Threads 3                  . 2 . 6 .
    # | X . . . |  Cards 2                    7 . @ . 1
    # +---------+  Transform 7: 8/4           . 1 . 4 .
    #                                         . . 5 . .
    'E2-30':    {'elements': 'aefw',
                 'pattern': [   ". @ . X",
                                "X . . .",
                            ],
                },

    #                                                                 #
    # +-----+   +-------+                                             #
    # | @ . | + | @ . . |                                             #
    # | . X |   | . . X |                                             #
    # +-----+   +-------+                                             #
    #                                                                 #

    # . . . . . . .    . . . . . . .    a = 31
    # . . . . . . .    . . c . d . .    b = 32
    # . . c . b . .    . c . . . b .    c = 33
    # . . . @ . . .    . . . @ . . .    d = 34
    # . . d . a X .    . d . . X a .
    # . . . . . . .    . . b . a . .
    # . . . . . . .    . . . . . . .

    # +-------+  Level 2          Transforms  . 6 . 3 .
    # | @ . . |  Threads 2                    5 5 . 3 4
    # | . X X |  Cards 1                      . . @ . .
    # +-------+  Transform 8: 12/5            8 7 . 1 1
    #                                         . 7 . 2 .
    'E2-31':    {'elements': 'fw',
                 'pattern': [   "@ . .",
                                ". X X",
                            ],
                },

    # +-------+  Level 3          Transforms  . 6 . 7 .
    # | . @ . |  Threads 2                    2 7 . 5 4
    # | X . . |  Cards 2                      . . @ . .
    # | . . X |  Transform 8: 12/5            8 1 . 3 5
    # +-------+                               . 3 . 1 .
    'E2-32':    {'elements': 'fw',
                 'pattern': [   ". @ .",
                                "X . .",
                                ". . X",
                            ],
                },

    # +---------+  Level 3        Transforms  . 5 . 4 .
    # | X . . . |  Threads 2                  6 1 . 7 3
    # | . @ . . |  Cards 3                    . . @ . .
    # | . . . X |  Transform 8: 12/5          8 3 . 5 1
    # +---------+                             . 7 . 2 .
    'E2-33':    {'elements': 'fw',
                 'pattern': [   "X . . .",
                                ". @ . .",
                                ". . . X",
                            ],
                },

    # +---------+  Level 3        Transforms  . 2 . 6 .
    # | . @ . . |  Threads 2                  7 3 . 7 3
    # | X . . X |  Cards 2                    . . @ . .
    # +---------+  Transform 8: 12/5          5 1 . 5 1
    #                                         . 4 . 8 .
    'E2-34':    {'elements': 'fw',
                 'pattern': [   ". @ . .",
                                "X . . X",
                            ],
                },

    #                                                                 #
    # +-----+   +-------+                                             #
    # | @ . | + | @ . . |                                             #
    # | . X |   | . . . |                                             #
    # +-----+   | . . X |                                             #
    #           +-------+                                             #
    #                                                                 #

    # . . . . . . .    a = 35
    # . . . . . . .    b = 36
    # . . c . b . .    c = 37
    # . . . @ . . .
    # . . b . a . .
    # . . . . . X .
    # . . . . . . .
    
    # +-------+  Level 3          Transforms  3 . . . 2
    # | @ . . |  Threads 2                    . 3 . 2 .
    # | . X . |  Cards 2                      . . @ . .
    # | . . X |  Transform 4: 8/5             . 4 . 1 .
    # +-------+                               4 . . . 1
    'E2-35':    {'elements': 'fw',
                 'pattern': [   "@ . .",
                                ". X .",
                                ". . X",
                            ],
                },

    # +---------+  Level 3
    # | . @ . . |  Threads 2
    # | X . . . |  Cards 2
    # | . . . X |  Transform 4: 8/5
    # +---------+
    'E2-36':    {'elements': 'fw',
                 'pattern': [   ". @ . .",
                                "X . . .",
                                ". . . X",
                            ],
                },

    # +---------+  Level 3
    # | X . . . |  Threads 2
    # | . @ . . |  Cards 2
    # | . . . . |  Transform 4: 8/5
    # | . . . X |
    # +---------+
    'E2-37':    {'elements': 'fw',
                 'pattern': [],
                },

    #                                                                 #
    # +-----+   +---------+                                           #
    # | @ . | + | @ . . X |                                           #
    # | . X |   +---------+                                           #
    # +-----+                                                         #
    #                                                                 #

    # . . . . . . .    . . . b . . .    a = 38
    # . . . . . . .    . . . . . . .    b = 39
    # . . b . a . .    . . . . . . .
    # . . . @ . . X    b . . @ . . a
    # . . b . a . .    . . . . X . .
    # . . . . . . .    . . . . . . .
    # . . . . . . .    . . . a . . .
    
    # +---------+  Level 3        Transforms  . . . 3 . . .
    # | @ . . X |  Threads 2                  . . . . . . .
    # | . X . . |  Cards 2                    . . 4 . 2 . .
    # +---------+  Transform 7: 8/6           5 . . @ . . 1
    #                                         . . 6 . 1 . .
    #                                         . . . . . . .
    #                                         . . . 7 . . .
    'E2-38':    {'elements': 'aefw',
                 'pattern': [   "@ . . X",
                                ". X . .",
                            ],
                },

    # +-----------+  Level 3      Transforms  . . . 2 . . .
    # | . @ . . X |  Threads 2                . . . . . . .
    # | X . . . . |  Cards 2                  . . 7 . 5 . .
    # +-----------+  Transform 7: 8/6         4 . . @ . . 1
    #                                         . . 1 . 3 . .
    #                                         . . . . . . .
    #                                         . . . 6 . . .
    'E2-39':    {'elements': 'aefw',
                 'pattern': [   ". @ . . X",
                                "X . . . .",
                            ],
                },

    #                                                                 #
    # +-----+   +---------+                                           #
    # | @ . | + | @ . . . |                                           #
    # | . X |   | . . . X |                                           #
    # +-----+   +---------+                                           #
    #                                                                 #

    # . . . . . . .    . . c . d . .    a = 40
    # . . . . . . .    . . . . . . .    b = 41
    # . . c . b . .    c . . . . . b    c = 42
    # . . . @ . . .    . . . @ . . .    d = 43
    # . . d . a . X    d . . . X . a
    # . . . . . . .    . . . . . . .
    # . . . . . . .    . . b . a . .
    
    # +---------+  Level 3        Transforms  . . 6 . 7 . .
    # | @ . . . |  Threads 2                  . . . . . . .
    # | . X . X |  Cards 2                    5 . 5 . 7 . 8
    # +---------+  Transform 8: 12/8          . . . @ . . .
    #                                         4 . 3 . 1 . 1
    #                                         . . . . . . .
    #                                         . . 3 . 2 . .
    'E2-40':    {'elements': 'aefw',
                 'pattern': [   "@ . . .",
                                ". X . X",
                            ],
                },

    # +---------+  Level 3        Transforms  . . 2 . 3 . .
    # | . X . . |  Threads 2                  . . . . . . .
    # | @ . . . |  Cards 3                    5 . 3 . 1 . 8
    # | . . . X |  Transform 8: 12/8          . . . @ . . .
    # +---------+                             4 . 5 . 7 . 1
    #                                         . . . . . . .
    #                                         . . 7 . 6 . .
    'E2-41':    {'elements': 'aefw',
                 'pattern': [   ". X . .",
                                "@ . . .",
                                ". . . X",
                            ],
                },

    # +-----------+  Level 3
    # | X . . . . |  Threads 2
    # | . @ . . . |  Cards 4
    # | . . . . X |  Transform 8: 12/8
    # +-----------+
    'E2-42':    {'elements': 'aefw',
                 'pattern': [],
                },
    
    # +-----------+  Level 3
    # | . @ . . . |  Threads 2
    # | X . . . X |  Cards 2
    # +-----------+  Transform 8: 12/8
    'E2-43':    {'elements': 'aefw',
                 'pattern': [],
                },

    #                                                                 #
    # +-----+    +---------+                                          #
    # | @ . | +  | @ . . . |                                          #
    # | . X |    | . . . . |                                          #
    # +-----+    | . . . X |                                          #
    #            +---------+                                          #
    #                                                                 #

    # . . . . . . .    . c . . . d .    a = 44
    # . . . . . . .    c . . . . . b    b = 45
    # . . c . b . .    . . . . . . .    c = 46
    # . . . @ . . .    . . . @ . . .    d = 47
    # . . d . a . .    . . . . X . .
    # . . . . . . X    d . . . . . a
    # . . . . . . .    . b . . . a .
    
    # +---------+  Level 3
    # | @ . . . |  Threads 2
    # | . X . . |  Cards 3
    # | . . . X |  Transform 8
    # +---------+
    'E2-44':    {'elements': 'fw',
                 'pattern': [],
                },

    # +---------+  Level 3
    # | . X . . |  Threads 2
    # | @ . . . |  Cards 3
    # | . . . . |  Transform 8
    # | . . . X |
    # +---------+
    'E2-45':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-----------+  Level 3
    # | X . . . . |  Threads 2
    # | . @ . . . |  Cards 3
    # | . . . . . |  Transform 8
    # | . . . . X |
    # +-----------+
    'E2-46':    {'elements': 'fw',
                 'pattern': [   "X . . . .",
                                ". @ . . .",
                                ". . . . .",
                                ". . . . X",
                            ],
                },

    # +-----------+  Level 3
    # | . @ . . . |  Threads 2
    # | X . . . . |  Cards 3
    # | . . . . X |  Transform 8
    # +-----------+
    'E2-47':    {'elements': 'fw',
                 'pattern': [   ". @ . . .",
                                "X . . . .",
                                ". . . . X",
                            ],
                },

    #                                                                 #
    # +-----+   +---------+                                           #
    # | @ . | + | @ . . . |                                           #
    # | . X |   | . . . . |                                           #
    # +-----+   | . . . . |                                           #
    #           | . . . X |                                           #
    #           +---------+                                           #
    #                                                                 #

    # . . . . . . .    a = 48
    # . . . . . . .    b = 49
    # . . c . b . .    c = 50
    # . . . @ . . .
    # . . b . a . .
    # . . . . . . .
    # . . . . . . X
    
    # +---------+  Level 3
    # | @ . . . |  Threads 2
    # | . X . . |  Cards 2
    # | . . . . |  Transform 4: 8/5
    # | . . . X |
    # +---------+
    'E2-48':    {'elements': 'fw',
                 'pattern': [],
                },

    # +---------+  Level 3
    # | . X . . |  Threads 2
    # | @ . . . |  Cards 2
    # | . . . . |  Transform 4: 8/5
    # | . . . . |
    # | . . . X |
    # +---------+
    'E2-49':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-----------+  Level 3
    # | X . . . . |  Threads 2
    # | . @ . . . |  Cards 2
    # | . . . . . |  Transform 4: 8/5
    # | . . . . . |
    # | . . . . X |
    # +-----------+
    'E2-50':    {'elements': 'fw',
                 'pattern': [],
                },

   
    #                                                                 #
    # +-------+   +-------+                                           #
    # | @ . X | + | @ . X |                                           #
    # +-------+   +-------+                                           #
    #                                                                 #

    # . . . . . . .    a = 51
    # . . . a . . .    b = 52
    # . . . . . . .
    # . b . @ . X .
    # . . . . . . .
    # . . . a . . .
    # . . . . . . .

    # +-------+  Level 3
    # | @ . X |  Threads 2
    # | . . . |  Cards 2
    # | X . . |  Transform 3: 4/4
    # +-------+
    'E2-51':    {'elements': 'ae',
                 'pattern': [   "@ . X",
                                ". . .",
                                "X . .",
                            ],
                },

    # +-----------+  Level 3
    # | X . @ . X |  Threads 2
    # +-----------+  Cards 2
    #                Transform 2: 4/4
    'E2-52':    {'elements': 'ae',
                 'pattern': [   "X . @ . X",
                            ],
                },

    #                                                                 #
    # +-------+   +-------+                                           #
    # | @ . X | + | @ . . |                                           #
    # +-------+   | . . X |                                           #
    #             +-------+                                           #
    #                                                                 #

    # . . . . . . .    . . . . . . .    a = 53
    # . . . b . . .    . . b . d . .    b = 54
    # . . . . . . .    . c . . . a .    c = 55
    # . c . @ . a .    . . . @ . X .    d = 56
    # . . . . . X .    . c . . . a .
    # . . . d . . .    . . b . d . .
    # . . . . . . .    . . . . . . .

    # +-------+  Level 2          Transforms  . 4 3 3 .
    # | @ . X |  Threads 2                    5 . . . 2
    # | . . X |  Cards 1                      5 . @ . 1
    # +-------+  Transform 8: 12/5            6 . . . 1
    #                                         . 7 7 8 .
    'E2-53':    {'elements': 'ae',
                 'pattern': [   "@ . X",
                                ". . X",
                            ],
                },

    # +---------+  Level 2
    # | . @ . X |  Threads 2
    # | . . . . |  Cards 3
    # | X . . . |  Trnsform 8: 12/5
    # +---------+
    'E2-54':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-----------+  Level 3
    # | X . @ . . |  Threads 2
    # | . . . . X |  Cards 2
    # +-----------+  Transform 8: 12/5
    'E2-55':    {'elements': 'ae',
                 'pattern': [   "X . @ . .",
                                ". . . . X",
                            ],
                },

    # +-------+  Level 2          Transforms  . 3 7 2 .
    # | @ . X |  Threads 2                    8 . . . 7
    # | . . . |  Cards 2                      3 . @ . 1
    # | . X . |  Transform 8: 12/5            6 . . . 5
    # +-------+                               . 4 5 1 .
    'E2-56':    {'elements': 'ae',
                 'pattern': [   "@ . X",
                                ". . .",
                                ". X .",
                            ],
                },

    #                                                                 #
    # +-------+   +-------+                                           #
    # | @ . X | + | @ . . |                                           #
    # +-------+   | . . . |                                           #
    #             | . . X |                                           #
    #             +-------+                                           #
    #                                                                 #

    # . . . . . . .    a = 57
    # . . . b . . .    b = 58
    # . . . . . . .
    # . b . @ . a .
    # . . . . . . .
    # . . . a . X .
    # . . . . . . .
    
    # +-------+  Level 
    # | @ . X |  Threads 
    # | . . . |  Cards 
    # | . . X |  Transform 
    # +-------+
    'E2-57':    {'elements': 'aefw',
                 'pattern': [],
                },

    # +-----------+  Level 
    # | X . @ . . |  Threads 
    # | . . . . . |  Cards 
    # | . . . . X |  Transform 
    # +-----------+
    'E2-58':    {'elements': 'aefw',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +---------+                                         #
    # | @ . X | + | @ . . X |                                         #
    # +-------+   +---------+                                         #
    #                                                                 #

    # . . . . . . .    a = 59
    # . . . b . . .    b = 60
    # . . . . . . .    c = 61
    # . c . @ . a X
    # . . . . . . .
    # . . . b . . .
    # . . . . . . .

    # +---------+  Level 3
    # | @ . X X |  Threads 2
    # +---------+  Cards 2
    #              Transform 4: 8/5
    'E2-59':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+  Level 3
    # | @ . . X |  Threads 2
    # | . . . . |  Cards 3
    # | X . . . |  Transform 6: 8/5
    # +---------+
    'E2-60':    {'elements': 'ae',
                 'pattern': [   "@ . . X",
                                ". . . .",
                                "X . . .",
                            ],
                },

    # +-------------+  Level 3
    # | X . @ . . X |  Threads 2
    # +-------------+  Cards 3
    #                  Transform 4: 8/5
    'E2-61':    {'elements': 'ae',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +---------+                                         #
    # | @ . X | + | @ . . . |                                         #
    # +-------+   | . . . X |                                         #
    #             +---------+                                         #
    #                                                                 #

    # . . . . . . .    . . b . d . .    a = 62
    # . . . b . . .    . . . . . . .    b = 63
    # . . . . . . .    c . . . . . a    c = 64
    # . c . @ . a .    . . . @ . X .    d = 65
    # . . . . . . X    c . . . . . a
    # . . . d . . .    . . . . . . .
    # . . . . . . .    . . b . d . .

    # +---------+  Level 3
    # | @ . X . |  Threads 2
    # | . . . X |  Cards 2
    # +---------+  Transform 8: 12/8
    'E2-62':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+  Level 
    # | X . @ . |  Threads 
    # | . . . . |  Cards 
    # | . . . . |  Transform
    # | . . . X |
    # +---------+
    'E2-63':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-------------+  Level 
    # | X . @ . . . |  Threads 
    # | . . . . . X |  Cards 
    # +-------------+  Transform 
    'E2-64':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+  Level 
    # | @ . . . |  Threads 
    # | . . . X |  Cards 
    # | X . . . |  Transform
    # +---------+
    'E2-65':    {'elements': 'ae',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +---------+                                         #
    # | @ . X | + | @ . . . |                                         #
    # +-------+   | . . . . |                                         #
    #             | . . . X |                                         #
    #             +---------+                                         #
    #                                                                 #

    # . . . . . . .    . b . . . d .    a = 66
    # . . . b . . .    c . . . . . a    b = 67
    # . . . . . . .    . . . . . . .    c = 68
    # . c . @ . a .    . . . @ . X .    d = 69
    # . . . . . . .    . . . . . . .
    # . . . d . . X    c . . . . . a
    # . . . . . . .    . b . . . d .
    
    # +---------+  Level 
    # | @ . X . |  Threads 
    # | . . . . |  Cards 
    # | . . . X |  Transform
    # +---------+
    'E2-66':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-----------+  Level 
    # | X . @ . . |  Threads 
    # | . . . . . |  Cards 
    # | . . . . . |  Transform
    # | . . . . X |
    # +-----------+
    'E2-67':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-------------+  Level 
    # | X . @ . . . |  Threads 
    # | . . . . . . |  Cards 
    # | . . . . . X |  Transform
    # +-------------+
    'E2-68':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+  Level 
    # | @ . . . |  Threads 
    # | . . . . |  Cards 
    # | X . . X |  Transform
    # +---------+
    'E2-69':    {'elements': 'ae',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +---------+                                         #
    # | @ . X | + | @ . . . |                                         #
    # +-------+   | . . . . |                                         #
    #             | . . . . |                                         #
    #             | . . . X |                                         #
    #             +---------+                                         #
    #                                                                 #

    # . . . . . . .    a = 70
    # . . . b . . .    b = 71
    # . . . . . . .
    # . b . @ . a .
    # . . . . . . .
    # . . . a . . .
    # . . . . . . X
    
    # +---------+  Level 
    # | @ . X . |  Threads 
    # | . . . . |  Cards 
    # | . . . . |  Transform
    # | . . . X |
    # +---------+
    'E2-70':    {'elements': 'aefw',
                 'pattern': [],
                },

    # +-------------+  Level 
    # | X . @ . . . |  Threads 
    # | . . . . . . |  Cards 
    # | . . . . . . |  Transform
    # | . . . . . X |
    # +-------------+
    'E2-71':    {'elements': 'aefw',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +-------+                                           #
    # | @ . . | + | @ . . |                                           #
    # | . . X |   | . . X |                                           #
    # +-------+   +-------+                                           #
    #                                                                 #

    # . . . . . . .    a = 72
    # . . e . d . .    b = 73
    # . b . . . c .    c = 74
    # . . . @ . . .    d = 75
    # . f . . . b .    e = 76
    # . . X . a . .    f = 77
    # . . . . . . .

    # +-------+  Level 3          Transforms  . 3 . 3 .
    # | . @ . |  Threads 2                    4 . . . 2
    # | . . . |  Cards 2                      . . @ . .
    # | X . X |  Transform 4: 8/5             4 . . . 2
    # +-------+                               . 1 . 1 .
    'E2-72':    {'elements': 'aefw',
                 'pattern': [   ". @ .",
                                ". . .",
                                "X . X",
                            ],
                },

    # +---------+  Level 3
    # | . @ . . |  Threads 2
    # | . . . X |  Cards 3
    # | X . . . |  Transform 6: 8/5
    # +---------+
    'E2-73':    {'elements': 'aefw',
                 'pattern': [   ". @ . .",
                                ". . . X",
                                "X . . .",
                            ],
                },

    # +---------+  Level 3        Transforms  . 2 . 3 .
    # | . . . X |  Threads 2                  4 . . . 1
    # | . @ . . |  Cards 4                    . . @ . .
    # | . . . . |  Transform 4: 8/5           3 . . . 2
    # | X . . . |                             . 1 . 4 .
    # +---------+
    'E2-74':    {'elements': 'aefw',
                 'pattern': [   ". . . X",
                                ". @ . .",
                                ". . . .",
                                "X . . .",
                            ],
                },

    # +-----------+  Level 3
    # | X . . . . |  Threads 2
    # | . . @ . . |  Cards 4
    # | . . . . X |  Transform 4: 8/5
    # +-----------+
    'E2-75':    {'elements': 'aefw',
                 'pattern': [   "X . . . .",
                                ". . @ . .",
                                ". . . . X",
                            ],
                },

    # +-----------+  Level 3
    # | . . @ . . |  Threads 2
    # | X . . . X |  Cards 2
    # +-----------+  Transform 6: 8/5
    'E2-76':    {'elements': 'aefw',
                 'pattern': [   ". . @ . .",
                                "X . . . X",
                            ],
                },

    # +-------+  Level 
    # | . . @ |  Threads 
    # | X . . |  Cards 
    # | . X . |  Transform
    # +-------+
    'E2-77':    {'elements': 'aefw',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +-------+                                           #
    # | @ . . | + | @ . . |                                           #
    # | . . X |   | . . . |                                           #
    # +-------+   | . . X |                                           #
    #             +-------+                                           #

    # . . . . . . .    a = 78
    # . . d . c . .    b = 79
    # . d . . . b .    c = 80
    # . . . @ . . .    d = 81
    # . c . . . a .
    # . . b . a X .
    # . . . . . . .
    
    # +-------+  Level 
    # | @ . . |  Threads 
    # | . . X |  Cards 
    # | . . X |  Transform
    # +-------+
    'E2-78':    {'elements': 'fw',
                 'pattern': [],
                },

    # +---------+  Level 
    # | . @ . . |  Threads 
    # | . . . . |  Cards 
    # | X . . X |  Transform
    # +---------+
    'E2-79':    {'elements': 'fw',
                 'pattern': [   ". @ . .",
                                ". . . .",
                                "X . . X",
                            ],
                },

    # +-----------+  Level 
    # | . . @ . . |  Threads 
    # | X . . . . |  Cards 
    # | . . . . X |  Transform
    # +-----------+
    'E2-80':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-----------+  Level 
    # | X . . . . |  Threads 
    # | . . @ . . |  Cards 
    # | . . . . . |  Transform
    # | . . . . X |
    # +-----------+
    'E2-81':    {'elements': 'fw',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +---------+                                         #
    # | @ . . | + | @ . . X |                                         #
    # | . . X |   +---------+                                         #
    # +-------+                                                       #
    #                                                                 #

    # . . . . . . .    a = 82
    # . . c . b . .    b = 83
    # . d . . . a .    c = 84
    # . . . @ . . X    d = 85
    # . d . . . a .
    # . . c . b . .
    # . . . . . . .
    
    # +---------+  Level 3
    # | @ . . X |  Threads 2
    # | . . X . |  Cards 2
    # +---------+  Transform 8: 12/
    'E2-82':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+  Level 
    # | @ . . X |  Threads 
    # | . . . . |  Cards 
    # | . X . . |  Transform
    # +---------+
    'E2-83':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-----------+  Level 
    # | . @ . . X |  Threads 
    # | . . . . . |  Cards 
    # | X . . . . |  Transform
    # +-----------+
    'E2-84':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-------------+  Level 
    # | . . @ . . X |  Threads 
    # | X . . . . . |  Cards 
    # +-------------+  Transform 
    'E2-85':    {'elements': 'ae',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +---------+                                         #
    # | @ . . | + | @ . . . |                                         #
    # | . . X |   | . . . X |                                         #
    # +-------+   +---------+                                         #
    #                                                                 #

    # . . . . . . .    . . d . g . .    a = 86
    # . . d . c . .    . . . . . . .    b = 87
    # . e . . . b .    e . . . . . b    c = 88
    # . . . @ . . .    . . . @ . . .    d = 89
    # . f . . . a X    f . . . . X a    e = 90
    # . . g . h . .    . . . . . . .    f = 91
    # . . . . . . .    . . c . h . .    g = 92
    #                                   h = 93
    
    # +---------+  Level 3
    # | @ . . . |  Threads 2
    # | . . X X |  Cards 2
    # +---------+  Transform 8: 16/
    'E2-86':    {'elements': 'ae',
                 'pattern': [   "@ . . .",
                                ". . X X",
                            ],
                },

    # +---------+  Level 
    # | . . X . |  Threads 
    # | @ . . . |  Cards 
    # | . . . X |  Transform
    # +---------+
    'E2-87':    {'elements': 'ae',
                 'pattern': [   ". . X .",
                                "@ . . .",
                                ". . . X",
                            ],
                },

    # +---------+  Level 
    # | . X . . |  Threads 
    # | . . . . |  Cards 
    # | @ . . . |  Transform
    # | . . . X |
    # +---------+
    'E2-88':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-----------+  Level 
    # | X . . . . |  Threads 
    # | . . . . . |  Cards 
    # | . @ . . . |  Transform
    # | . . . . X |
    # +-----------+
    'E2-89':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-------------+  Level 
    # | X . . . . . |  Threads 
    # | . . @ . . . |  Cards 
    # | . . . . . X |  Transform
    # +-------------+
    'E2-90':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-------------+  Level 3
    # | . . @ . . . |  Threads 2
    # | X . . . . X |  Cards 2
    # +-------------+  Transform 8: 16/
    'E2-91':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-----------+  Level 3
    # | . @ . . . |  Threads 2
    # | . . . . X |  Cards 2
    # | X . . . . |  Transform 8: 16/
    # +-----------+
    'E2-92':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+  Level 3
    # | @ . . . |  Threads 2
    # | . . . X |  Cards 2
    # | . X . . |  Transform 8: 16/
    # +---------+
    'E2-93':    {'elements': 'ae',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +---------+                                         #
    # | @ . . | + | @ . . . |                                         #
    # | . . X |   | . . . . |                                         #
    # +-------+   | . . . X |                                         #
    #             +---------+                                         #
    #                                                                 #

    # . . . . . . .    . d . . . g .    a = 94
    # . . d . c . .    e . . . . . b    b = 95
    # . e . . . b .    . . . . . . .    c = 96
    # . . . @ . . .    . . . @ . . .    d = 97
    # . f . . . a .    . . . . . X .    e = 98
    # . . g . h . X    f . . . . . a    f = 99
    # . . . . . . .    . c . . . h .    g = 100
    #                                   h = 101
    
    # +---------+  Level 3
    # | @ . . . |  Threads 2
    # | . . X . |  Cards 
    # | . . . X |  Transform 
    # +---------+
    'E2-94':    {'elements': 'fw',
                 'pattern': [],
                },

    # +---------+  Level 3
    # | . @ . . |  Threads 2
    # | . . . . |  Cards 
    # | X . . . |  Transform
    # | . . . X |
    # +---------+
    'E2-95':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-----------+  Level 3
    # | . . @ . . |  Threads 2
    # | X . . . . |  Cards 
    # | . . . . . |  Transform
    # | . . . . X |
    # +-----------+
    'E2-96':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-----------+  Level 3
    # | X . . . . |  Threads 2
    # | . . . . . |  Cards 
    # | . @ . . . |  Transform
    # | . . . . . |
    # | . . . . X |
    # +-----------+
    'E2-97':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-------------+  Level 3
    # | X . . . . . |  Threads 2
    # | . . @ . . . |  Cards 
    # | . . . . . . |  Transform
    # | . . . . . X |
    # +-------------+
    'E2-98':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-------------+  Level 3
    # | . . @ . . . |  Threads 2
    # | X . . . . . |  Cards 
    # | . . . . . X |  Transform
    # +-------------+
    'E2-99':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-----------+  Level 3
    # | . @ . . . |  Threads 2
    # | . . . . . |  Cards 
    # | X . . . X |  Transform
    # +-----------+
    'E2-100':   {'elements': 'fw',
                 'pattern': [],
                },

    # +---------+  Level 3
    # | @ . . . |  Threads 2
    # | . . . . |  Cards 
    # | . X . X |  Transform
    # +---------+
    'E2-101':   {'elements': 'fw',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +---------+                                         #
    # | @ . . | + | @ . . . |                                         #
    # | . . X |   | . . . . |                                         #
    # +-------+   | . . . . |                                         #
    #             | . . . X |                                         #
    #             +---------+                                         #
    #                                                                 #

    # c . . . . . b    . . . . . . .    a = 102
    # . . . . . . .    . . c . d . .    b = 103
    # . . . . . . .    . c . . . b .    c = 104
    # . . . @ . . .    . . . @ . . .    d = 105
    # . . . . . X .    . d . . . a .
    # . . . . . . .    . . b . a . .
    # d . . . . . a    . . . . . . X

    # +---------+  Level 3
    # | @ . . . |  Threads 2
    # | . . X . |  Cards 
    # | . . . . |  Transform
    # | . . . X |
    # +---------+
    'E2-102':   {'elements': 'fw',
                 'pattern': [],
                },

    # +-----------+  Level 3
    # | . @ . . . |  Threads 2
    # | . . . . . |  Cards 
    # | X . . . . |  Transform
    # | . . . . X |
    # +-----------+
    'E2-103':   {'elements': 'fw',
                 'pattern': [],
                },

    # +-------------+  Level 3
    # | X . . . . . |  Threads 2
    # | . . @ . . . |  Cards 
    # | . . . . . . |  Transform
    # | . . . . . . |
    # | . . . . . X |
    # +-------------+
    'E2-104':   {'elements': 'fw',
                 'pattern': [],
                },

    # +-------------+  Level 3
    # | . . @ . . . |  Threads 2
    # | X . . . . . |  Cards 
    # | . . . . . . |  Transform
    # | . . . . . X |
    # +-------------+
    'E2-105':   {'elements': 'fw',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +-------+                                           #
    # | @ . . | + | @ . . |                                           #
    # | . . . |   | . . . |                                           #
    # | . . X |   | . . X |                                           #
    # +-------+   +-------+                                           #
    #                                                                 #

    # . . . . . . .    a = 106
    # . b . . . a .    b = 107
    # . . . . . . .
    # . . . @ . . .
    # . . . . . . .
    # . a . . . X .
    # . . . . . . .
    
    # +-----------+  Level 3
    # | . . @ . . |  Threads 2
    # | . . . . . |  Cards 
    # | X . . . X |  Transform
    # +-----------+
    'E2-106':   {'elements': 'fw',
                 'pattern': [   ". . @ . .",
                                ". . . . .",
                                "X . . . X",
                            ],
                },

    # +-----------+  Level 3
    # | X . . . . |  Threads 2
    # | . . . . . |  Cards 
    # | . . @ . . |  Transform
    # | . . . . . |
    # | . . . . X |
    # +-----------+
    'E2-107':   {'elements': 'fw',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +---------+                                         #
    # | @ . . | + | @ . . X |                                         #
    # | . . . |   +---------+                                         #
    # | . . X |                                                       #
    # +-------+                                                       #
    #                                                                 #

    # . . . b . . .    a = 108
    # . . . . . . .    b = 109
    # . . . . . . .
    # b . . @ . . a
    # . . . . . . .
    # . . . . . X .
    # . . . a . . .

    # +---------+  Level 3
    # | @ . . X |  Threads 2
    # | . . . . |  Cards 
    # | . . X . |  Transform
    # +---------+
    'E2-108':   {'elements': 'aefw',
                 'pattern': [],
                },

    # +-------------+  Level 3
    # | . . @ . . X |  Threads 2
    # | . . . . . . |  Cards 
    # | X . . . . . |  Transform
    # +-----------+
    'E2-109':   {'elements': 'aefw',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +---------+                                         #
    # | @ . . | + | @ . . . |                                         #
    # | . . . |   | . . . X |                                         #
    # | . . X |   +---------+                                         #
    # +-------+                                                       #
    #                                                                 #

    # . . . . . . .    . . c . d . .    a = 110
    # . c . . . b .    . . . . . . .    b = 111
    # . . . . . . .    c . . . . . b    c = 112
    # . . . @ . . .    . . . @ . . .    d = 113
    # . . . . . . X    d . . . . . a
    # . d . . . a .    . . . . . X .
    # . . . . . . .    . . b . a . .
    
    # +---------+  Level 3
    # | @ . . . |  Threads 2
    # | . . . X |  Cards 
    # | . . X . |  Transform
    # +---------+
    'E2-110':   {'elements': 'aefw',
                 'pattern': [],
                },

    # +---------+  Level 3
    # | . . @ . |  Threads 2
    # | . . . . |  Cards 
    # | X . . . |  Transform
    # | . . . X |
    # +---------+
    'E2-111':   {'elements': 'aefw',
                 'pattern': [],
                },

    # +-------------+  Level 3
    # | . . . . . X |  Threads 2
    # | . . @ . . . |  Cards 
    # | . . . . . . |  Transform
    # | X . . . . . |
    # +-------------+
    'E2-112':   {'elements': 'aefw',
                 'pattern': [],
                },

    # +-------------+  Level 3
    # | . . @ . . . |  Threads 2
    # | . . . . . X |  Cards 
    # | X . . . . . |  Transform
    # +-------------+
    'E2-113':   {'elements': 'aefw',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +---------+                                         #
    # | @ . . | + | @ . . . |                                         #
    # | . . . |   | . . . . |                                         #
    # | . . X |   | . . . X |                                         #
    # +-------+   +---------+                                         #
    #                                                                 #

    # . . . . . . .    . c . . . d .    a = 114
    # . c . . . b .    c . . . . . b    b = 115
    # . . . . . . .    . . . . . . .    c = 116
    # . . . @ . . .    . . . @ . . .    d = 117
    # . . . . . . .    . . . . . . .
    # . d . . . a X    d . . . . X a
    # . . . . . . .    . b . . . a .
    
    'E2-114':   {'elements': 'fw',
                 'pattern': [],
                },
    'E2-115':   {'elements': 'fw',
                 'pattern': [],
                },
    'E2-116':   {'elements': 'fw',
                 'pattern': [],
                },
    'E2-117':   {'elements': 'fw',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +---------+                                         #
    # | @ . . | + | @ . . . |                                         #
    # | . . . |   | . . . . |                                         #
    # | . . X |   | . . . . |                                         #
    # +-------+   | . . . X |                                         #
    #             +---------+                                         #
    #                                                                 #

    # . . . . . . .    c . . . . . b   a = 118
    # . c . . . b .    . . . . . . .   b = 119
    # . . . . . . .    . . . . . . .   c = 120
    # . . . @ . . .    . . . @ . . .
    # . . . . . . .    . . . . . . .
    # . b . . . a .    . . . . . X .
    # . . . . . . X    b . . . . . a

    'E2-118':   {'elements': 'fw',
                 'pattern': [],
                },
    'E2-119':   {'elements': 'fw',
                 'pattern': [],
                },
    'E2-120':   {'elements': 'fw',
                 'pattern': [],
                },

    #                                                                 #
    # +---------+   +---------+                                       #
    # | @ . . X | + | @ . . X |                                       #
    # +---------+   +---------+                                       #
    #                                                                 #
    
    # . . . a . . .    a = 121
    # . . . . . . .    b = 122
    # . . . . . . .
    # b . . @ . . X
    # . . . . . . .
    # . . . . . . .
    # . . . a . . .

    'E2-121':   {'elements': 'ae',
                 'pattern': [],
                },
    'E2-122':   {'elements': 'ae',
                 'pattern': [],
                },

    #                                                                 #
    # +---------+   +---------+                                       #
    # | @ . . X | + | @ . . . |                                       #
    # +---------+   | . . . X |                                       #
    #               +---------+                                       #
    #                                                                 #
    
    # . . . b . . .    . . b . d . .    a = 123
    # . . . . . . .    . . . . . . .    b = 124
    # . . . . . . .    c . . . . . a    c = 125
    # c . . @ . . a    . . . @ . . X    d = 126
    # . . . . . . X    c . . . . . a
    # . . . . . . .    . . . . . . .
    # . . . d . . .    . . b . d . .

    'E2-123':   {'elements': 'ae',
                 'pattern': [],
                },
    'E2-124':   {'elements': 'ae',
                 'pattern': [],
                },
    'E2-125':   {'elements': 'ae',
                 'pattern': [],
                },
    'E2-126':   {'elements': 'ae',
                 'pattern': [],
                },

    #                                                                 #
    # +---------+   +---------+                                       #
    # | @ . . X | + | @ . . . |                                       #
    # +---------+   | . . . . |                                       #
    #               | . . . X |                                       #
    #               +---------+                                       #
    #                                                                 #
    
    # . . . b . . .    . b . . . d .    a = 127
    # . . . . . . .    c . . . . . a    b = 128
    # . . . . . . .    . . . . . . .    c = 129
    # c . . @ . . a    . . . @ . . X    d = 130
    # . . . . . . .    . . . . . . .
    # . . . . . . X    c . . . . . a
    # . . . d . . .    . b . . . d .

    'E2-127':   {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-128':   {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-129':   {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-130':   {'elements': 'aefw',
                 'pattern': [],
                },

    #                                                                 #
    # +---------+   +---------+                                       #
    # | @ . . X | + | @ . . . |                                       #
    # +---------+   | . . . . |                                       #
    #               | . . . . |                                       #
    #               | . . . X |                                       #
    #               +---------+                                       #
    #                                                                 #
    
    # . . . b . . .    b . . . . . a    a = 131
    # . . . . . . .    . . . . . . .    b = 132
    # . . . . . . .    . . . . . . .
    # b . . @ . . a    . . . @ . . X
    # . . . . . . .    . . . . . . .
    # . . . . . . .    . . . . . . .
    # . . . a . . X    b . . . . . a

    'E2-131':   {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-132':   {'elements': 'aefw',
                 'pattern': [],
                },

    #                                                                 #
    # +---------+   +---------+                                       #
    # | @ . . . | + | @ . . . |                                       #
    # | . . . X |   | . . . X |                                       #
    # +---------+   +---------+                                       #
    #                                                                 #

    # . . c . b . .    a = 133
    # . . . . . . .    b = 134
    # d . . . . . a    c = 135
    # . . . @ . . .    d = 136
    # e . . . . . X    e = 137
    # . . . . . . .    f = 138
    # . . f . g . .    g = 139

    'E2-133':   {'elements': 'ae',
                 'pattern': [],
                },
    'E2-134':   {'elements': 'ae',
                 'pattern': [],
                },
    'E2-135':   {'elements': 'ae',
                 'pattern': [],
                },
    'E2-136':   {'elements': 'ae',
                 'pattern': [],
                },
    'E2-137':   {'elements': 'ae',
                 'pattern': [],
                },
    'E2-138':   {'elements': 'ae',
                 'pattern': [],
                },
    'E2-139':   {'elements': 'ae',
                 'pattern': [],
                },

    #                                                                 #
    # +---------+   +---------+                                       #
    # | @ . . . | + | @ . . . |                                       #
    # | . . . X |   | . . . . |                                       #
    # +---------+   | . . . X |                                       #
    #               +---------+                                       #
    #                                                                 #

    # . d . . . c .    . . d . c . .    a = 140
    # e . . . . . b    . . . . . . .    b = 141
    # . . . . . . .    e . . . . . b    c = 142
    # . . . @ . . .    . . . @ . . .    d = 143
    # . . . . . . X    f . . . . . a    e = 144
    # f . . . . . a    . . . . . . X    f = 145
    # . g . . . h .    . . g . h . .    g = 146
    #                                   h = 147

    'E2-140':   {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-141':   {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-142':   {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-143':   {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-144':   {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-145':   {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-146':   {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-147':   {'elements': 'aefw',
                 'pattern': [],
                },

    #                                                                 #
    # +---------+   +---------+                                       #
    # | @ . . . | + | @ . . . |                                       #
    # | . . . X |   | . . . . |                                       #
    # +---------+   | . . . . |                                       #
    #               | . . . X |                                       #
    #               +---------+                                       #
    #                                                                 #
    
    # c . . . . . b    . . c . d . .    a = 148
    # . . . . . . .    . . . . . . .    b = 149
    # . . . . . . .    c . . . . . b    c = 150
    # . . . @ . . .    . . . @ . . .    d = 151
    # . . . . . . X    d . . . . . a
    # . . . . . . .    . . . . . . .
    # d . . . . . a    . . b . a . X

    'E2-148':   {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-149':   {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-150':   {'elements': 'aefw',
                 'pattern': [],
                },
    'E2-151':   {'elements': 'aefw',
                 'pattern': [],
                },

    #                                                                 #
    # +---------+   +---------+                                       #
    # | @ . . . | + | @ . . . |                                       #
    # | . . . . |   | . . . . |                                       #
    # | . . . X |   | . . . X |                                       #
    # +---------+   +---------+                                       #
    #                                                                 #
    
    # . c . . . b .    a = 152
    # d . . . . . a    b = 153
    # . . . . . . .    c = 154
    # . . . @ . . .    d = 155
    # . . . . . . .    e = 156
    # e . . . . . X    f = 157
    # . f . . . g .    g = 158

    'E2-152':   {'elements': 'fw',
                 'pattern': [],
                },
    'E2-153':   {'elements': 'fw',
                 'pattern': [],
                },
    'E2-154':   {'elements': 'fw',
                 'pattern': [],
                },
    'E2-155':   {'elements': 'fw',
                 'pattern': [],
                },
    'E2-156':   {'elements': 'fw',
                 'pattern': [],
                },
    'E2-157':   {'elements': 'fw',
                 'pattern': [],
                },
    'E2-158':   {'elements': 'fw',
                 'pattern': [],
                },

    #                                                                 #
    # +---------+   +---------+                                       #
    # | @ . . . | + | @ . . . |                                       #
    # | . . . . |   | . . . . |                                       #
    # | . . . X |   | . . . . |                                       #
    # +---------+   | . . . X |                                       #
    #               +---------+                                       #
    #                                                                 #
    
    # c . . . . . b    . c . . . d .    a = 159
    # . . . . . . .    c . . . . . b    b = 160
    # . . . . . . .    . . . . . . .    c = 161
    # . . . @ . . .    . . . @ . . .    d = 162
    # . . . . . . .    . . . . . . .
    # . . . . . . X    d . . . . . a
    # d . . . . . a    . b . . . a X

    'E2-159':   {'elements': 'fw',
                 'pattern': [],
                },
    'E2-160':   {'elements': 'fw',
                 'pattern': [],
                },
    'E2-161':   {'elements': 'fw',
                 'pattern': [],
                },
    'E2-162':   {'elements': 'fw',
                 'pattern': [],
                },

    #                                                                 #
    # +---------+   +---------+                                       #
    # | @ . . . | + | @ . . . |                                       #
    # | . . . . |   | . . . . |                                       #
    # | . . . . |   | . . . . |                                       #
    # | . . . X |   | . . . X |                                       #
    # +---------+   +---------+                                       #
    #                                                                 #

    # b . . . . . a    a = 163
    # . . . . . . .    b = 164
    # . . . . . . .
    # . . . @ . . .
    # . . . . . . .
    # . . . . . . .
    # a . . . . . X

    'E2-163':   {'elements': 'fw',
                 'pattern': [],
                },
    'E2-164':   {'elements': 'fw',
                 'pattern': [],
                },

    #  _____ _                   _       _    ___        _      ___ 
    # |   __| |___ _____ ___ ___| |_ ___| |  |_  |     _| |_   |_  |
    # |   __| | -_|     | -_|   |  _| .'| |   _| |_   |_   _|  |_  |
    # |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |_____|    |_|    |___|
    #

    #                                                                 #
    # +-----+   +-----+   +-----+                                     #
    # | @ X | + | @ X | + | @ . |                                     #
    # +-----+   +-----+   | . X |                                     #
    #                     +-----+                                     #
    #                                                                 #
    
    # +-----+  Level 3 - Built on +-----+     +-----+  Transforms  3 2 2
    # | @ X |  Threads 3          | @ . | and | @ X |              3 @ 1
    # | X X |  Cards 1            | . X |     +-----+              4 1 1
    # +-----+  Transform 4: 8/2   +-----+
    'E3-1':     {'elements': 'ae',
                 'pattern': [],
                },

    # +-------+  Level 3 - Built on +-----+     +-----+  Transforms  5 2 4
    # | X @ . |  Threads 3          | @ . | and | @ X |              1 @ 3
    # | . X X |  Cards 1            | . X |     +-----+              2 1 1
    # +-------+  Transform 5: 8/2   +-----+
    'E3-2':     {'elements': 'ae',
                 'pattern': [],
                },

    # +-------+  Level 4 - Built on +-----+     +-----+  Transforms  1 3 2
    # | X . . |  Threads 3          | @ . | and | @ X |              2 @ 1
    # | . @ X |  Cards 2            | . X |     +-----+              3 1 4
    # | . X . |  Transform 4: 8/2   +-----+
    # +-------+
    'E3-3':     {'elements': 'ae',
                 'pattern': [],
                },

    # +-------+  Level 3 - Built on +-----+     +-----+  Transforms  3 5 2
    # | X @ X |  Threads 3          | @ . | and | @ X |              1 @ 1
    # | . . X |  Cards 1            | . X |     +-----+              4 5 1
    # +-------+  Transform 5: 8/2   +-----+
    'E3-4':     {'elements': 'ae',
                 'pattern': [],
                },

    #                                                                 #
    # +-----+   +-----+   +-----+                                     #
    # | @ . | + | @ . | + | @ X |                                     #
    # | . X |   | . X |   +-----+                                     #
    # +-----+   +-----+                                               #
    #                                                                 #
    
    # +-------+  Level 3 - Built on +-----+     +-----+  Transforms  2 5 3
    # | . @ X |  Threads 3          | @ . | and | @ X |              4 @ 1
    # | X . X |  Cards 1            | . X |     +-----+              1 2 1
    # +-------+  Transform 5: 8/2   +-----+
    'E3-5':     {'elements': 'fw',
                 'pattern': [],
                },

    # +-------+  Level 3 - Built on +-----+     +-----+  Transforms  2 3 3
    # | . @ . |  Threads 3          | @ . | and | @ X |              2 @ 4
    # | X X X |  Cards 1            | . X |     +-----+              1 1 1
    # +-------+  Transform 4: 8/2   +-----+
    'E3-6':     {'elements': 'fw',
                 'pattern': [],
                },

    # +-------+  Level 4 - Built on +-----+     +-----+  Transforms  2 1 3
    # | . X . |  Threads 3          | @ . | and | @ X |              4 @ 2
    # | . @ . |  Cards 2            | . X |     +-----+              1 3 1
    # | X . X |  Transform 4: 8/2   +-----+
    # +-------+
    'E3-7':     {'elements': 'fw',
                 'pattern': [],
                },

    # +-------+  Level 4 - Built on +-----+     +-----+  Transforms  1 1 3
    # | X X . |  Threads 3          | @ . | and | @ X |              2 @ 4
    # | . @ . |  Cards 2            | . X |     +-----+              3 5 1
    # | . . X |  Transform 5: 8/2   +-----+
    # +-------+
    'E3-8':     {'elements': 'fw',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +-------+   +-----+                                 #
    # | @ . X | + | @ . X | + | @ . |                                 #
    # +-------+   +-------+   | . X |                                 #
    #                         +-----+                                 #
    #                                                                 #

    # +-------+  Level 4 - Built on +-----+     +-------+  Transforms  . . 2 . .
    # | @ . X |  Threads 3          | @ . | and | @ . X |              . 3 . 2 .
    # | . X . |  Cards 2            | . X |     +-------+              3 . @ . 1
    # | X . . |  Transform 4: 8/5   +-----+                            . 4 . 1 .
    # +-------+                                                        . . 1 . .
    'E3-9':     {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+  Level 4 - Built on +-----+     +-------+  Transforms  . . 3 . .
    # | X . . . |  Threads 3          | @ . | and | @ . X |              . 1 . 2 .
    # | . @ . X |  Cards 3            | . X |     +-------+              2 . @ . 1
    # | . . . . |  Transform 4: 8/4   +-----+                            . 4 . 3 .
    # | . X . . |                                                        . . 1 . .
    # +---------+
    'E3-10':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+  Level 4 - Built on +-----+     +-------+  Transforms  . . 3 . .
    # | . @ . X |  Threads 3          | @ . | and | @ . X |              . 3 . 2 .
    # | X . . . |  Cards 2            | . X |     +-------+              4 . @ . 1
    # | . X . . |  Transform 5: 8/5   +-----+                            . 1 . 5 .
    # +---------+                                                        . . 1 . .
    'E3-11':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-----------+  Level 4 - Built on +-----+     +-------+  Transforms  . . 3 . .
    # | X . @ . X |  Threads 3          | @ . | and | @ . X |              . 2 . 4 .
    # | . X . . . |  Cards 2            | . X |     +-------+              1 . @ . 1
    # +-----------+  Transform 5: 8/5   +-----+                            . 1 . 5 .
    #                                                                      . . 3 . .
    'E3-12':    {'elements': 'ae',
                 'pattern': [],
                },

    #                                                                 #
    # +-----+   +-----+   +-------+                                   #
    # | @ . | + | @ . | + | @ . X |                                   #
    # | . X |   | . X |   +-------+                                   #
    # +-----+   +-----+                                               #
    #                                                                 #

    # +---------+
    # | . @ . X |
    # | X . X . |
    # +---------+
    'E3-13':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-------+
    # | . @ . |
    # | X . X |
    # | . X . |
    # +-------+
    'E3-14':    {'elements': 'fw',
                 'pattern': [],
                },

    # +---------+
    # | X . . . |
    # | . @ . X |
    # | X . . . |
    # +---------+
    'E3-15':    {'elements': 'fw',
                 'pattern': [],
                },

    # +---------+
    # | X . . . |
    # | . @ . X |
    # | . . X . |
    # +---------+
    'E3-16':    {'elements': 'fw',
                 'pattern': [],
                },

    #                                                                 #
    # +-----+   +-----+   +-------+                                   #
    # | @ X | + | @ X | + | @ . . |                                   #
    # +-----+   +-----+   | . . . |                                   #
    #                     | . . X |                                   #
    #                     +-------+                                   #
    #                                                                 #

    # +-------+  Level 4 - Built on +-----+     +-------+  Transforms  3 . . . 2
    # | @ X . |  Threads 3          | @ X | and | @ . . |              . . 2 . .
    # | X . . |  Cards 2            +-----+     | . . . |              . 3 @ 1 .
    # | . . X |  Transform 4: 8/5               | . . X |              . . 1 . .
    # +-------+                                 +-------+              4 . . . 1
    'E3-17':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+
    # | X @ . . |
    # | . X . . |
    # | . . . X |
    # +---------+
    'E3-18':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+
    # | . X . . |
    # | X @ . . |
    # | . . . . |
    # | . . . X |
    # +---------+
    'E3-19':    {'elements': 'ae',
                 'pattern': [],
                },

    # +---------+
    # | X @ X . |
    # | . . . . |
    # | . . . X |
    # +---------+
    'E3-20':    {'elements': 'ae',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +-------+   +-----+                                 #
    # | @ . . | + | @ . . | + | @ X |                                 #
    # | . . . |   | . . . |   +-----+                                 #
    # | . . X |   | . . X |                                           #
    # +-------+   +-------+                                           #
    #                                                                 #

    # +-----------+
    # | . . @ . . |
    # | . . X . . |
    # | X . . . X |
    # +-----------+
    'E3-21':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-----------+
    # | . . @ X . |
    # | . . . . . |
    # | X . . . X |
    # +-----------+
    'E3-22':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-----------+
    # | . . X . . |
    # | . . @ . . |
    # | . . . . . |
    # | X . . . X |
    # +-----------+
    'E3-23':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-----------+
    # | X . . . . |
    # | . . X . . |
    # | . . @ . . |
    # | . . . . . |
    # | . . . . X |
    # +-----------+
    'E3-24':    {'elements': 'fw',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +-------+   +-------+                               #
    # | @ . X | + | @ . X | + | @ . . |                               #
    # +-------+   +-------+   | . . . |                               #
    #                         | . . X |                               #
    #                         +-------+                               #
    #                                                                 #

    # +-------+  Level 4 - Built on +-------+     +-------+  Transforms  3 . 2 . 2
    # | @ . X |  Threads 3          | @ . X | and | @ . . |              . . . . .
    # | . . . |  Cards 2            +-------+     | . . . |              3 . @ . 1
    # | X . X |  Transform 4: 8/6                 | . . X |              . . . . .
    # +-------+                                   +-------+              4 . 1 . 1
    'E3-25':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-----------+
    # | X . @ . . |
    # | . . . . . |
    # | . . X . X |
    # +-----------+
    'E3-26':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-----------+
    # | . . X . . |
    # | . . . . . |
    # | X . @ . . |
    # | . . . . . |
    # | . . . . X |
    # +-----------+
    'E3-27':    {'elements': 'ae',
                 'pattern': [],
                },

    # +-----------+
    # | X . @ . X |
    # | . . . . . |
    # | . . . . X |
    # +-----------+
    'E3-28':    {'elements': 'ae',
                 'pattern': [],
                },

    #                                                                 #
    # +-------+   +-------+   +-------+                               #
    # | @ . . | + | @ . . | + | @ . X |                               #
    # | . . . |   | . . . |   +-------+                               #
    # | . . X |   | . . X |                                           #
    # +-------+   +-------+                                           #
    #                                                                 #
    
    # +-----------+
    # | . . @ . . |
    # | . . . . . |
    # | X . X . X |
    # +-----------+
    'E3-29':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-----------+
    # | . . @ . X |
    # | . . . . . |
    # | X . . . X |
    # +-----------+
    'E3-30':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-----------+
    # | . . X . . |
    # | . . . . . |
    # | . . @ . . |
    # | . . . . . |
    # | X . . . X |
    # +-----------+
    'E3-31':    {'elements': 'fw',
                 'pattern': [],
                },

    # +-----------+
    # | X . X . . |
    # | . . . . . |
    # | . . @ . . |
    # | . . . . . |
    # | . . . . X |
    # +-----------+
    'E3-32':    {'elements': 'fw',
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

    # +-------+  Level 3 - Built on +-----+
    # | @ . . |  Threads 1          | @ . |
    # | . X . |  Cards 2            | . X |
    # | . . @ |  Transform 1: 1/    +-----+
    # +-------+
    'EE1-3':    {'elements': 'fw',
                 'pattern': [   "@ . .",
                                ". X .",
                                ". . @",
                            ],
                },

    # +-------+  Level 2 - Built on +-----+
    # | @ . @ |  Threads 1          | @ . |
    # | . X . |  Cards 2            | . X |
    # +-------+  Transform 2: 2/    +-----+
    'EE1-4':    {'elements': 'fw',
                 'pattern': [   "@ . @",
                                ". X .",
                            ],
                },

    # +-----------+  Level 3 - Built on +-------+
    # | @ . . . . |  Threads 1          | @ . . |
    # | . . X . . |  Cards 4            | . . X |
    # | . . . . @ |  Transform 1: 1/    +-------+
    # +-----------+
    'EE1-5':    {'elements': 'aefw',
                 'pattern': [   "@ . . . .",
                                ". . X . .",
                                ". . . . @",
                            ],
                },

    # +-------+  Level 3 - Built on +-------+
    # | @ . . |  Threads 1          | @ . . |
    # | . . X |  Cards 4            | . . X |
    # | @ . . |  Transform 1: 1/    +-------+
    # +-------+
    'EE1-6':    {'elements': 'aefw',
                 'pattern': [   "@ . .",
                                ". . X",
                                "@ . .",
                            ],
                },

    # +-------+  Level 2 - Built on +-----+     +-------+
    # | @ @ X |  Threads 1          | @ X | and | @ . X |
    # +-------+  Cards 2            +-----+     +-------+
    #            Transform 2: 2/
    'EE1-7':    {'elements': 'ae',
                 'pattern': [],
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
