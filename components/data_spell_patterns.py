# Data Format:
#   spell_card_patterns:
#     Dictionary of spell <name> to <pattern>
#
#   <name>: string
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

    'blank':    [   ". . . . .",
                    ". . . . .",
                    ". . . . .",
                ],

    #  _____         _           _    ___   
    # |   | |___ _ _| |_ ___ ___| |  |_  |  
    # | | | | -_| | |  _|  _| .'| |   _| |_ 
    # |_|___|___|___|_| |_| |__,|_|  |_____|
    #

    # +---+
    # | X |  Level 0 - Castable on all starting cards.
    # +---+
    'N1':       [   "X",
                ],

    #  _____         _           _    ___ 
    # |   | |___ _ _| |_ ___ ___| |  |_  |
    # | | | | -_| | |  _|  _| .'| |  |  _|
    # |_|___|___|___|_| |_| |__,|_|  |___|
    #

    # +-----+  Level 1 - Castable on all starting cards.
    # | X X |
    # +-----+
    'N2-1':     [   "X X",
                ],

    # +-----+  Level 1 - Castable on all starting cards.
    # | X . |
    # | . X |
    # +-----+
    'N2-2':     [   "X .",
                    ". X",
                ],

    # +-------+  Level 1 - Castable on all starting cards except  xx  xx
    # | X . X |                                                  xx    xx
    # +-------+
    'N2-3':     [   "X . X",
                ],

    # +-------+  Level 1 - Castable on all starting cards except  x    x
    # | X . . |                                                  xxx  xxx
    # | . . X |
    # +-------+
    'N2-4':     [   "X . .",
                    ". . X",
                ],

    # +-------+  Level 2
    # | X . . |
    # | . . . |
    # | . . X |
    # +-------+
    'N2-5':     [   "X . .",
                    ". . .",
                    ". . X",
                ],

    # +---------+  Level 2
    # | X . . X |
    # +---------+
    'N2-6':     [   "X . . X",
                ],

    # +---------+  Level 2
    # | X . . . |
    # | . . . X |
    # +---------+
    'N2-7':     [],

    # +---------+  Level 2
    # | X . . . |
    # | . . . . |
    # | . . . X |
    # +---------+
    # TODO: create 2 eyes
    'N2-8':     [],

    #  _____         _           _    ___ 
    # |   | |___ _ _| |_ ___ ___| |  |_  |
    # | | | | -_| | |  _|  _| .'| |  |_  |
    # |_|___|___|___|_| |_| |__,|_|  |___|
    #

    # +-------+  Level 2
    # | X X X |
    # +-------+
    'N3-1':     [],

    # +-------+  Level 2 - Castable on all starting cards except  x    x
    # | X X . |                                                  xxx  xxx
    # | . . X |
    # +-------+
    'N3-2':     [],

    # +-----+  Level 2 - Castable on all starting cards.
    # | X X |
    # | . X |
    # +-----+
    'N3-3':     [],

    # +-------+  Level 2
    # | X . X |
    # | . X . |
    # +-------+
    'N3-4':     [],

    # +-------+  Level 3
    # | X . . |
    # | . X . |
    # | . . X |
    # +-------+
    'N3-5':     [],

    #  _____ _                   _       _    ___        _      ___   
    # |   __| |___ _____ ___ ___| |_ ___| |  |_  |     _| |_   |_  |  
    # |   __| | -_|     | -_|   |  _| .'| |   _| |_   |_   _|   _| |_ 
    # |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |_____|    |_|    |_____|
    #

    # Air/Earth
    # +-----+  Level 1
    # | @ X |  Threads 1
    # +-----+  Cards 1
    #          Transform 4: 4/2
    'E1-1':     [   "@ X",
                ],

    # Fire/Water
    # +-----+  Level 1         Transforms  3 . 2
    # | @ . |  Threads 1                   . @ .
    # | . X |  Cards 1                     4 . 1
    # +-----+  Transform 4: 4/2
    'E1-2':     [   "@ .",
                    ". X",
                ],

    # Air/Earth
    # +-------+  Level 1
    # | @ . X |  Threads 1
    # +-------+  Cards 1
    #            Transform 4: 4/4
    'E1-3':     [    "@ . X",
                ],

    # All
    # +-------+  Level 1          Transforms  . 6 . 7 .
    # | @ . . |  Threads 1                    5 . . . 8
    # | . . X |  Cards 1                      . . @ . .
    # +-------+  Transform 8: 8/5             4 . . . 1
    #                                         . 3 . 2 .
    'E1-4':     [   "@ . .",
                    ". . X",
                ],

    # Fire/Water
    # +-------+  Level 2          Transforms  3 . . . 2
    # | @ . . |  Threads 1                    . . . . .
    # | . . . |  Cards 2                      . . @ . .
    # | . . X |  Transform 4: 4/6             . . . . .
    # +-------+                               4 . . . 1
    'E1-5':     [   "@ . .",
                    ". . .",
                    ". . X",
                ],

    # Air/Earth
    # +---------+  Level 2
    # | @ . . X |  Threads 1
    # +---------+  Cards 2
    #              Transform 4: 4/6
    'E1-6':     [    "@ . . X",
                ],

    # +---------+  Level 2
    # | @ . . . |  Threads 1
    # | . . . X |  Cards 2
    # +---------+  Transform 8
    'E1-7':     [   "@ . . .",
                    ". . . X",
                ],

    # +---------+  Level 2
    # | @ . . . |  Threads 1
    # | . . . . |  Cards 3
    # | . . . X |  Transform 8
    # +---------+
    'E1-8':     [   "@ . . .",
                    ". . . .",
                    ". . . X",
                ],

    #  _____ _                   _       _    ___        _      ___ 
    # |   __| |___ _____ ___ ___| |_ ___| |  |_  |     _| |_   |_  |
    # |   __| | -_|     | -_|   |  _| .'| |   _| |_   |_   _|  |  _|
    # |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |_____|    |_|    |___|
    #

    # Air/Earth
    # +-------+  Level 2 - Built on +-----+  Transforms  . 2 .
    # | X @ X |  Threads 1          | @ X |              1 @ 1
    # +-------+  Cards 1            +-----+              . 2 .
    #            Transform 2: 4/2
    'E2-1':     [   "X @ X",
                ],

    # Air/Earth
    # +-----+  Level 2 - Built on +-----+  Transforms  . 2 .
    # | @ X |  Threads 2          | @ X |              3 @ 1
    # | X . |  Cards 1            +-----+              . 1 .
    # +-----+  Transform 3: 4/2
    'E2-2':     [   "@ X",
                    "X .",
                ],

    # All
    # +-------+  Level 2 - Built on +-----+     +-----+  Transforms  7 2 5
    # | . @ X |  Threads 2          | @ X | and | @ . |              4 @ 1        
    # | X . . |  Cards 1            +-----+     | . X |              1 6 3
    # +-------+  Transform 7: 8/2               +-----+
    'E2-3':     [   ". @ X",
                    "X . .",
                ],

    # All
    # +-----+  Level 2 - Built on +-----+     +-----+  Transforms  5 4 3
    # | @ . |  Threads 2          | @ X | and | @ . |              6 @ 2
    # | X X |  Cards 1            +-----+     | . X |              7 1 1
    # +-----+  Transform 7: 8/2               +-----+
    'E2-4':     [   "@ .",
                    "X X",
                ],

    # Air/Earth
    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . . 2 . .
    # | @ X X |  Threads 2          | @ X | and | @ . X |              . . 2 . .
    # +-------+  Cards 1            +-----+     +-------+              3 3 @ 1 1
    #            Transform 4: 8/4                                      . . 4 . .
    #                                                                  . . 4 . .
    'E2-5':     [    "@ X X",
                ],

    # Air/Earth
    # +---------+  Level 3 - Built on +-----+     +-------+  Transforms  . . 2 . .
    # | X @ . X |  Threads 2          | @ X | and | @ . X |              . . 4 . .
    # +---------+  Cards 2            +-----+     +-------+              3 1 @ 3 1
    #              Transform 4: 8/4                                      . . 2 . .
    #                                                                    . . 4 . .
    'E2-6':     [   "X @ . X",
                ],

    # Air/Earth
    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . . 4 . .
    # | @ . X |  Threads 2          | @ X | and | @ . X |              . . 2 . .
    # | X . . |  Cards 1            +-----+     +-------+              3 5 @ 4 1
    # +-------+  Transform 6: 8/4                                      . . 1 . .
    #                                                                  . . 6 . .
    'E2-7':     [   "@ . X",
                    "X . .",
                ],

    # Air/Earth
    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . 4 . 3 .
    # | @ X . |  Threads 2          | @ X | and | @ . . |              5 . 3 . 2
    # | . . X |  Cards 1            +-----+     | . . X |              . 5 @ 1 .
    # +-------+  Transform 8: 12/5              +-------+              6 . 7 . 1
    #                                                                  . 7 . 8 .
    'E2-8':     [   "@ X .",
                    ". . X",
                ],

    # Air/Earth
    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . 8 . 5 .
    # | @ . . |  Threads 2          | @ X | and | @ . . |              3 . 3 . 4
    # | X . X |  Cards 1            +-----+     | . . X |              . 7 @ 5 .
    # +-------+  Transform 8: 12/5              +-------+              2 . 1 . 1
    #                                                                  . 7 . 6 .
    'E2-9':     [   "@ . .",
                    "X . X",
                ],

    # Air/Earth
    # +---------+  Level 3 - Built on +-----+     +-------+  Transforms  . 4 . 3 .
    # | X @ . . |  Threads 2          | @ X | and | @ . . |              5 . 7 . 2
    # | . . . X |  Cards 2            +-----+     | . . X |              . 1 @ 5 .
    # +---------+  Transform 8: 12/5              +-------+              6 . 3 . 1
    #                                                                    . 7 . 8 .
    'E2-10':    [   "X @ . .",
                    ". . . X",
                ],

    # Air/Earth
    # +-------+  Level 3 - Built on +-----+     +-------+  Transforms  . 7 . 3 .
    # | X . . |  Threads 2          | @ X | and | @ . . |              6 . 1 . 5
    # | @ . . |  Cards 1            +-----+     | . . X |              . 3 @ 7 .
    # | . . X |  Transform 8: 12/5              +-------+              2 . 5 . 1
    # +-------+                                                        . 8 . 4 .
    'E2-11':    [   "X . .",
                    "@ . .",
                    ". . X",
                ],

    # Air/Earth
    # +---------+  Level 3 - Built on +-----+     +---------+
    # | @ X . X |  Threads 2          | @ X | and | @ . . X |
    # +---------+  Cards 2            +-----+     +---------+
    #              Transform 4: 8/6
    'E2-12':    [   "@ X . X",
                ],

    # Air/Earth
    # +-----------+  Level 3 - Built on +-----+     +---------+
    # | X @ . . X |  Threads 2          | @ X | and | @ . . X |
    # +-----------+  Cards 2            +-----+     +---------+
    #                Transform 4: 8/6
    'E2-13':    [   "X @ . . X",
                ],

    # Air/Earth
    # +---------+  Level 3 - Built on +-----+     +---------+  Transforms  . . . 4 . . .
    # | @ . . X |  Threads 2          | @ X | and | @ . . X |              . . . . . . .
    # | X . . . |  Cards 2            +-----+     +---------+              . . . 2 . . .
    # +---------+  Transform 6: 8/6                                        3 . 5 @ 4 . 1
    #                                                                      . . . 1 . . .
    #                                                                      . . . . . . .
    #                                                                      . . . 6 . . .
    'E2-14':    [   "@ . . X",
                    "X . . .",
                ],

    # Air/Earth
    # +---------+  Level 3 - Built on +-----+     +---------+  Transforms  . . 4 . 3 . .
    # | @ X . . |  Threads 2          | @ X | and | @ . . . |              . . . . . . .
    # | . . . X |  Cards 2            +-----+     | . . . X |              5 . . 3 . . 2
    # +---------+  Transform 8: 12/8              +---------+              . . 5 @ 1 . .
    #                                                                      6 . . 7 . . 1
    #                                                                      . . . . . . .
    #                                                                      . . 7 . 8 . .
    'E2-15':    [   "@ X . .",
                    ". . . X",
                ],

    # Air/Earth
    # +---------+  Level 3 - Built on +-----+     +---------+  Transforms  . . 8 . 5 . .
    # | @ . . . |  Threads 2          | @ X | and | @ . . . |              . . . . . . .
    # | X . . X |  Cards 2            +-----+     | . . . X |              3 . . 3 . . 4
    # +---------+  Transform 8: 12/8              +---------+              . . 7 @ 5 . .
    #                                                                      2 . . 1 . . 1
    #                                                                      . . . . . . .
    #                                                                      . . 7 . 6 . .
    'E2-16':    [   "@ . . .",
                    "X . . X",
                ],

    # Air/Earth
    # +-----------+  Level 3 - Built on +-----+     +---------+
    # | X @ . . . |  Threads 2          | @ X | and | @ . . . |
    # | . . . . X |  Cards 2            +-----+     | . . . X |
    # +-----------+  Transform 8                    +---------+
    'E2-17':    [],

    # Air/Earth
    # +---------+  Level 3 - Built on +-----+     +---------+
    # | X . . . |  Threads 2          | @ X | and | @ . . . |
    # | @ . . . |  Cards 3            +-----+     | . . . X |
    # | . . . X |  Transform 8                    +---------+
    # +---------+
    'E2-18':    [],

    # Fire/Water
    # +-------+  Level 2 - Built on +-----+  Transforms  3 . 2
    # | . @ . |  Threads 2          | @ . |              . @ .
    # | X . X |  Cards 1            | . X |              1 . 1
    # +-------+  Transform 3: 4/2   +-----+
    'E2-19':    [   ". @ .",
                    "X . X",
                ],

    # Fire/Water
    # +-------+  Level 3 - Built on +-----+  Transforms  1 . 2
    # | X . . |  Threads 2          | @ . |              . @ .
    # | . @ . |  Cards 2            | . X |              2 . 1
    # | . . X |  Transform 2: 4/2   +-----+
    # +-------+
    'E2-20':    [   "X . .",
                    ". @ .",
                    ". . X",
                ],

    # All
    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . . 3 . .
    # | @ . X |  Threads 2          | @ . | and | @ . X |              . 4 . 2 .
    # | . X . |  Cards 1            | . X |     +-------+              5 . @ . 1
    # +-------+  Transform 7: 8/4   +-----+                            . 6 . 1 .
    #                                                                  . . 7 . .
    'E2-21':    [   "@ . X",
                    ". X .",
                ],

    # All
    # +---------+  Level 3 - Built on +-----+     +-------+  Transforms  . . 3 . .
    # | . @ . X |  Threads 3          | @ . | and | @ . X |              . 2 . 6 .
    # | X . . . |  Cards 2            | . X |     +-------+              7 . @ . 1
    # +---------+  Transform 7: 8/4   +-----+                            . 1 . 4 .
    #                                                                    . . 5 . .
    'E2-22':    [   ". @ . X",
                    "X . . .",
                ],

    # Fire/Water
    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . 6 . 3 .
    # | @ . . |  Threads 2          | @ . | and | @ . . |              5 5 . 3 4
    # | . X X |  Cards 1            | . X |     | . . X |              . . @ . .
    # +-------+  Transform 8: 12/5  +-----+     +-------+              8 7 . 1 1
    #                                                                  . 7 . 2 .
    'E2-23':    [   "@ . .",
                    ". X X",
                ],

    # Fire/Water
    # +---------+  Level 3 - Built on +-----+     +-------+  Transforms  . 2 . 6 .
    # | . @ . . |  Threads 2          | @ . | and | @ . . |              7 3 . 7 3
    # | X . . X |  Cards 2            | . X |     | . . X |              . . @ . .
    # +---------+  Transform 8: 12/5  +-----+     +-------+              5 1 . 5 1
    #                                                                    . 4 . 8 .
    'E2-24':    [   ". @ . .",
                    "X . . X",
                ],

    # Fire/Water
    # +---------+  Level 3 - Built on +-----+     +-------+  Transforms  . 5 . 4 .
    # | X . . . |  Threads 2          | @ . | and | @ . . |              6 1 . 7 3
    # | . @ . . |  Cards 3            | . X |     | . . X |              . . @ . .
    # | . . . X |  Transform 8: 12/5  +-----+     +-------+              8 3 . 5 1
    # +---------+                                                        . 7 . 2 .
    'E2-25':    [   "X . . .",
                    ". @ . .",
                    ". . . X",
                ],

    # Fire/Water
    # +-------+  Level 3 - Built on +-----+     +-------+  Transforms  . 6 . 7 .
    # | . @ . |  Threads 2          | @ . | and | @ . . |              2 7 . 5 4
    # | X . . |  Cards 2            | . X |     | . . X |              . . @ . .
    # | . . X |  Transform 8: 12/5  +-----+     +-------+              8 1 . 3 5
    # +-------+                                                        . 3 . 1 .
    'E2-26':    [   ". @ .",
                    "X . .",
                    ". . X",
                ],

    # Fire/Water
    # +-------+  Level 3 - Built on +-----+     +-------+  Transforms  3 . . . 2
    # | @ . . |  Threads 2          | @ . | and | @ . . |              . 3 . 2 .
    # | . X . |  Cards 2            | . X |     | . . . |              . . @ . .
    # | . . X |  Transform 4: 8/5   +-----+     | . . X |              . 4 . 1 .
    # +-------+                                 +-------+              4 . . . 1
    'E2-27':    [   "@ . .",
                    ". X .",
                    ". . X",
                ],

    # All
    # +---------+  Level 3 - Built on +-----+     +---------+  Transforms  . . . 3 . . .
    # | @ . . X |  Threads 2          | @ . | and | @ . . X |              . . . . . . .
    # | . X . . |  Cards 2            | . X |     +---------+              . . 4 . 2 . .
    # +---------+  Transform 7: 8/6   +-----+                              5 . . @ . . 1
    #                                                                      . . 6 . 1 . .
    #                                                                      . . . . . . .
    #                                                                      . . . 7 . . .
    'E2-28':    [   "@ . . X",
                    ". X . .",
                ],

    # All
    # +-----------+  Level 3 - Built on +-----+     +---------+  Transforms  . . . 2 . . .
    # | . @ . . X |  Threads 2          | @ . | and | @ . . X |              . . . . . . .
    # | X . . . . |  Cards 2            | . X |     +---------+              . . 7 . 5 . .
    # +-----------+  Transform 7: 8/6   +-----+                              4 . . @ . . 1
    #                                                                        . . 1 . 3 . .
    #                                                                        . . . . . . .
    #                                                                        . . . 6 . . .
    'E2-29':    [   ". @ . . X",
                    "X . . . .",
                ],

    # Fire/Water
    # +---------+  Level 3 - Built on +-----+     +---------+  Transforms  . . 6 . 7 . .
    # | @ . . . |  Threads 2          | @ . | and | @ . . . |              . . . . . . .
    # | . X . X |  Cards 2            | . X |     | . . . X |              5 . 5 . 7 . 8
    # +---------+  Transform 8: 12/8  +-----+     +---------+              . . . @ . . .
    #                                                                      4 . 3 . 1 . 1
    #                                                                      . . . . . . .
    #                                                                      . . 3 . 2 . .
    'E2-30':    [   "@ . . .",
                    ". X . X",
                ],

    # Fire/Water
    # +---------+  Level 3 - Built on +-----+     +---------+  Transforms  . . 2 . 3 . .
    # | . X . . |  Threads 2          | @ . | and | @ . . . |              . . . . . . .
    # | @ . . . |  Cards 3            | . X |     | . . . X |              5 . 3 . 1 . 8
    # | . . . X |  Transform 8: 12/8  +-----+     +---------+              . . . @ . . .
    # +---------+                                                          4 . 5 . 7 . 1
    #                                                                      . . . . . . .
    #                                                                      . . 7 . 6 . .
    'E2-31':    [   ". X . .",
                    "@ . . .",
                    ". . . X",
                ],

    # Fire/Water
    # +-----------+  Level 3 - Built on +-----+     +---------+
    # | . @ . . . |  Threads 2          | @ . | and | @ . . . |
    # | X . . . X |  Cards 2            | . X |     | . . . X |
    # +-----------+  Transform 8: 12/8  +-----+     +---------+
    'E2-32':    [],

    # Fire/Water
    # +-----------+  Level 3 - Built on +-----+     +---------+
    # | X . . . . |  Threads 2          | @ . | and | @ . . . |
    # | . @ . . . |  Cards 4            | . X |     | . . . X |
    # | . . . . X |  Transform 8: 12/8  +-----+     +---------+
    # +-----------+
    'E2-33':    [],
    
    # Fire/Water
    # +---------+  Level 3 - Build on +-----+     +---------=
    # | @ . . . |  Threads 2          | @ . | and | @ . . . |
    # | . X . . |  Cards 3            | . X |     | . . . . |
    # | . . . X |  Transform 8        +-----+     | . . . X |
    # +---------+                                 +---------+
    # + 3 variants
    'E2-34':    [],
    'E2-35':    [],
    'E2-36':    [],
    'E2-37':    [],

    # Air/Earth
    # +-----------+  Level 3 - Built on +-------+
    # | X . @ . X |  Threads 2          | @ . X |
    # +-----------+  Cards 2            +-------+
    #                Transform 2: 4/4
    'E2-38':    [   "X . @ . X",
                ],

    # Air/Earth
    # +-------+  Level 3 - Build on +-------+
    # | @ . X |  Threads 2          | @ . X |
    # | . . . |  Cards 2            +-------+
    # | X . . |  Transform 3: 4/4
    # +-------+
    'E2-39':    [   "@ . X",
                    ". . .",
                    "X . .",
                ],

    # Air/Earth
    # +-------+  Level 2 - Built on +-------+     +-------+  Transforms  . 4 3 3 .
    # | @ . X |  Threads 2          | @ . X | and | @ . . |              5 . . . 2
    # | . . X |  Cards 1            +-------+     | . . X |              5 . @ . 1
    # +-------+  Transform 8: 12/5                +-------+              6 . . . 1
    #                                                                    . 7 7 8 .
    'E2-40':    [   "@ . X",
                    ". . X",
                ],

    # Air/Earth
    # +-------+  Level 2 - Built on +-------+     +-------+  Transforms  . 3 7 2 .
    # | @ . X |  Threads 2          | @ . X | and | @ . . |              8 . . . 7
    # | . . . |  Cards 2            +-------+     | . . X |              3 . @ . 1
    # | . X . |  Transform 8: 12/5                +-------+              6 . . . 5
    # +-------+                                                          . 4 5 1 .
    'E2-41':    [   "@ . X",
                    ". . .",
                    ". X .",
                ],

    # Air/Earth
    # +-----------+  Level 3 - Built on +-------+     +-------+
    # | X . @ . . |  Threads 2          | @ . X | and | @ . . |
    # | . . . . X |  Cards 2            +-------+     | . . X |
    # +-----------+  Transform 8: 12/5                +-------+
    'E2-42':    [   "X . @ . .",
                    ". . . . X",
                ],

    # Air/Earth
    # +---------+  Level 2 - Built on +-------+     +-------+
    # | . @ . X |  Threads 2          | @ . X | and | @ . . |
    # | . . . . |  Cards 3            +-------+     | . . X |
    # | X . . . |  Trnsform 8: 12/5                 +-------+
    # +---------+
    'E2-43':    [],

    # Air/Earth
    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . X X |  Threads 2          | @ . X | and | @ . . X |
    # +---------+  Cards 2            +-------+     +---------+
    #              Transform 4: 8/5
    'E2-44':    [],

    # Air/Earth
    # +-------------+  Level 3 - Built on +-------+     +---------+
    # | X . @ . . X |  Threads 2          | @ . X | and | @ . . X |
    # +-------------+  Cards 3            +-------+     +---------+
    #                  Transform 4: 8/5
    'E2-45':    [],

    # Air/Earth
    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . . X |  Threads 2          | @ . X | and | @ . . X |
    # | . . . . |  Cards 3            +-------+     +---------+
    # | X . . . |  Transform 6: 8/5
    # +---------+
    'E2-46':    [   "@ . . X",
                    ". . . .",
                    "X . . .",
                ],

    # Air/Earth
    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . X . |  Threads 2          | @ . X | and | @ . . . |
    # | . . . X |  Cards 2            +-------+     | . . . X |
    # +---------+  Transform 8: 12/8                +---------+
    # + 3 variants
    'E2-47':    [],
    'E2-48':    [],
    'E2-49':    [],
    'E2-50':    [],

    # Air/Earth
    # +-----------+  Level 3 - Built on +-------+     +-----------+
    # | @ . X . . |  Threads 2          | @ . X | and | @ . . . . |
    # | . . . . X |  Cards 2            +-------+     | . . . . X |
    # +-----------+  Transform 8: 12/                 +-----------+
    # + 3 variants
    'E2-51':    [],
    'E2-52':    [],
    'E2-53':    [],
    'E2-54':    [],

    # All
    # +-------+  Level 3 - Built on +-------+  Transforms  . 3 . 3 .
    # | . @ . |  Threads 2          | @ . . |              4 . . . 2
    # | . . . |  Cards 2            | . . X |              . . @ . .
    # | X . X |  Transform 4: 8/5   +-------+              4 . . . 2
    # +-------+                                            . 1 . 1 .
    'E2-55':    [   ". @ .",
                    ". . .",
                    "X . X",
                ],

    # All
    # +---------+  Level 3 - Built on +-------+
    # | . @ . . |  Threads 2          | @ . . |
    # | . . . X |  Cards 3            | . . X |
    # | X . . . |  Transform 6: 8/5   +-------+
    # +---------+
    'E2-56':    [],

    # All
    # +-----------+  Level 3 - Built on +-------+
    # | . . @ . . |  Threads 2          | @ . . |
    # | X . . . X |  Cards 2            | . . X |
    # +-----------+  Transform 6: 8/5   +-------+
    'E2-57':    [],

    # All
    # +-----------+  Level 3 - Built on +-------+
    # | X . . . . |  Threads 2          | @ . . |
    # | . . @ . . |  Cards 4            | . . X |
    # | . . . . X |  Transform 4: 8/5   +-------+
    # +-----------+
    'E2-58':    [],

    # All
    # +---------+  Level 3 - Built on +-------+  Transforms  . 2 . 3 .
    # | . . . X |  Threads 2          | @ . . |              4 . . . 1
    # | . @ . . |  Cards 4            | . . X |              . . @ . .
    # | . . . . |  Transform 4: 8/5   +-------+              3 . . . 2
    # | X . . . |                                            . 1 . 4 .
    # +---------+
    'E2-59':    [],

    # Air/Earth
    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . . X |  Threads 2          | @ . . | and | @ . . X |
    # | . . X . |  Cards 2            | . . X |     +---------+
    # +---------+  Transform 8: 12/   +-------+
    # + 3 variants
    'E2-60':    [],
    'E2-61':    [],
    'E2-62':    [],
    'E2-63':    [],

    # All
    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . . . |  Threads 2          | @ . . | and | @ . . . |
    # | . . X X |  Cards 2            | . . X |     | . . . X |
    # +---------+  Transform 8: 16/   +-------+     +---------+
    # + 3 variants
    'E2-64':    [],
    'E2-65':    [],
    'E2-66':    [],
    'E2-67':    [],

    # All
    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . . . |  Threads 2          | @ . . | and | @ . . . |
    # | . . X . |  Cards 3            | . . X |     | . . . . |
    # | . . . X |  Transform 8: 16/   +-------+     | . . . X |
    # +---------+                                   +---------+
    # + 3 variants
    'E2-68':    [],
    'E2-69':    [],
    'E2-70':    [],
    'E2-71':    [],

    # Air/Earth
    # +-----------+  Level 3 - Built on +-------+     +-----------+
    # | @ . . . X |  Threads 2          | @ . . | and | @ . . . X |
    # | . . X . . |  Cards 2            | . . X |     +-----------+
    # +-----------+  Transform 8: 12/   +-------+
    # + 3 variants
    'E2-72':    [],
    'E2-73':    [],
    'E2-74':    [],
    'E2-75':    [],

    # All
    # +-----------+  Level 3 - Built on +-------+     +-----------+
    # | @ . . . . |  Threads 2          | @ . . | and | @ . . . . |
    # | . . X . X |  Cards 2            | . . X |     | . . . . X |
    # +-----------+  Transform 8: 16/   +-------+     +-----------+
    # + 3 variants
    'E2-76':    [],
    'E2-77':    [],
    'E2-78':    [],
    'E2-79':    [],

    # All
    # +-----------+  Level 3 - Built on +-------+     +-----------+
    # | @ . . . . |  Threads 2          | @ . . | and | @ . . . . |
    # | . . X . . |  Cards 4            | . . X |     | . . . . . |
    # | . . . . X |  Transform 8: 12/   +-------+     | . . . . X |
    # +-----------+                                   +-----------+
    # + 3 variants
    'E2-80':    [],
    'E2-81':    [],
    'E2-82':    [],
    'E2-83':    [],

    #  _____ _                   _       _    ___        _      ___ 
    # |   __| |___ _____ ___ ___| |_ ___| |  |_  |     _| |_   |_  |
    # |   __| | -_|     | -_|   |  _| .'| |   _| |_   |_   _|  |_  |
    # |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |_____|    |_|    |___|
    #

    # All
    # +-------+  Level 4 - Build on +-----+     +-------+
    # | @ . X |  Threads 3          | @ . | and | @ . X |
    # | . X . |  Cards 2            | . X |     +-------+
    # | X . . |  Transform 4: 8/5   +-----+
    # +-------+
    'E3-1':     [],

    # All
    # +-------+  Level 4 - Build on +-----+     +-------+  Transforms  3 . . . 2
    # | @ X . |  Threads 3          | @ X | and | @ . . |              . . 2 . .
    # | X . . |  Cards 2            +-----+     | . . . |              . 3 @ 1 .
    # | . . X |  Transform 4: 8/5               | . . X |              . . 1 . .
    # +-------+                                 +-------+              4 . . . 1
    'E3-2':     [],

    # All
    # +-------+  Level 4 - Build on +-------+     +-------+  Transforms  3 . 2 . 2
    # | @ . X |  Threads 3          | @ . X | and | @ . . |              . . . . .
    # | . . . |  Cards 2            +-------+     | . . . |              3 . @ . 1
    # | X . X |  Transform 4: 8/6                 | . . X |              . . . . .
    # +-------+                                   +-------+              4 . 1 . 1
    'E3-3':     [],

    #  _____ _                   _       _    ___      _      ___   
    # |   __| |___ _____ ___ ___| |_ ___| |  |_  |   _| |_   |_  |  
    # |   __| | -_|     | -_|   |  _| .'| |  |  _|  |_   _|   _| |_ 
    # |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |___|    |_|    |_____|
    #

    # Air/Earth
    # +-------+  Level 2 - Built on +-----+
    # | @ X @ |  Threads 1          | @ X |
    # +-------+  Cards 2            +-----+
    #            Transform 1: 1/
    'EE1-1':    [],

    # Air/Earth
    # +-----+  Level 2 - Built on +-----+
    # | @ X |  Threads 1          | @ X |
    # | . @ |  Cards 2            +-----+
    # +-----+  Transform 2: 2/
    'EE1-2':    [],

    # Air/Earth
    # +-------+  Level 2 - Built on +-----+     +-------+
    # | @ @ X |  Threads 1          | @ X | and | @ . X |
    # +-------+  Cards 2            +-----+     +-------+
    #            Transform 2: 2/
    'EE1-3':    [],

    # Fire/Water
    # +-------+  Level 3 - Built on +-----+
    # | @ . . |  Threads 1          | @ . |
    # | . X . |  Cards 2            | . X |
    # | . . @ |  Transform 1: 1/    +-----+
    # +-------+
    'EE1-4':    [   "@ . .",
                    ". X .",
                    ". . @",
                ],

    # Fire/Water
    # +-------+  Level 2 - Built on +-----+
    # | @ . @ |  Threads 1          | @ . |
    # | . X . |  Cards 2            | . X |
    # +-------+  Transform 2: 2/    +-----+
    'EE1-5':    [   "@ . @",
                    ". X .",
                ],

    # All
    # +-----------+  Level 3 - Built on +-------+
    # | @ . . . . |  Threads 1          | @ . . |
    # | . . X . . |  Cards 4            | . . X |
    # | . . . . @ |  Transform 1: 1/    +-------+
    # +-----------+
    'EE1-6':    [   "@ . . . .",
                    ". . X . .",
                    ". . . . @",
                ],

    #  _____ _                   _       _    ___      _      ___ 
    # |   __| |___ _____ ___ ___| |_ ___| |  |_  |   _| |_   |_  |
    # |   __| | -_|     | -_|   |  _| .'| |  |  _|  |_   _|  |  _|
    # |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |___|    |_|    |___|
    #

    # Air/Earth
    # +-----+  Level 3 - Built on +-----+
    # | @ X |  Threads 2          | @ X |
    # | X @ |  Cards 2            +-----+
    # +-----+  Transform 1: 2/
    'EE2-1':    [   "@ X",
                    "X @",
                ],

    # Air/Earth
    # +-------+  Level 3 - Built on +-----+  Transforms  . 2 . .
    # | @ X . |  Threads 2          | @ X |              3 @ 1 .
    # | . @ X |  Cards 2            +-----+              . 3 @ 1
    # +-------+  Transform 4: 6/                         . . 4 .
    'EE2-2':    [   "@ X .",
                    ". @ X",
                ],

    # Air/Earth
    # +-------+  Level 4 - Built on +-----+
    # | X . . |  Threads 2          | @ X |
    # | @ . . |  Cards 2            +-----+
    # | . @ X |  Transform 2; 4/
    # +-------+
    'EE2-3':    [],

    # Air/Earth
    # +---------+  Level 3 - Built on +-----+
    # | X @ . . |  Threads 2          | @ X |
    # | . . @ X |  Cards 2            +-----+
    # +---------+  Transform 2: 4/
    'EE2-4':    [   "X @ . .",
                    ". . @ X",
                ],

    # Air/Earth
    # +-------+  Level 3 - Built on +-----+  Transforms  . 2 . .
    # | @ . . |  Threads 2          | @ X |              3 @ 3 .
    # | X @ X |  Cards 2            +-----+              . 1 @ 1
    # +-------+  Transform 4: 6/                         . . 4 .
    'EE2-5':    [   "@ . .",
                    "X @ X",
                ],

    # Fire/Water
    # +-------+  Level 4 - Built on +-----+
    # | . @ . |  Threads 2          | @ . |
    # | X . X |  Cards 2            | . X |
    # | . @ . |  Transform 1: 1/    +-----+
    # +-------+
    'EE2-6':    [   ". @ .",
                    "X . X",
                    ". @ .",
                ],

    # Fire/Water
    # +---------+  Level 4 - Built on +-----+
    # | . @ @ . |  Threads 2          | @ . |
    # | X . . X |  Cards 2            | . X |
    # +---------+  Transform 2: 4/    +-----+
    'EE2-7':    [],

    # Fire/Water
    # +---------+  Level 4 - Built on +-----+
    # | X . . . |  Threads 2          | @ . |
    # | . @ @ . |  Cards 3            | . X |
    # | . . . X |  Transform 2: 4/    +-----+
    # +---------+
    'EE2-8':    [   "X . . .",
                    ". @ @ .",
                    ". . . X",
                ],

}
