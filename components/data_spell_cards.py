# Spell fragment card data

# Text -> ASCII Art: http://patorjk.com/software/taag/#p=display&f=Rectangles&t=Monster

spell_card_revision = 7

spell_card_categories = [
    'blank',
    'starter',

    #'attack-mage',
    'attack-eye',
    'attack-charge',
    'attack-tapestry',

    'create-eye',

    #'defend-mage',
    'defend-move',
    'defend-eye',
    'defend-charge',
    'defend-tapestry',

    'move-mage',
    #'move-astral',
    'move-eye',

    'move-other-mage',
    'move-other-eye',

    'thread',
    
    'modify-tapestry',
    'add-action',
    'terrain',
]

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

    # +-----+  Level 1
    # | @ X |  Threads 1
    # +-----+  Cards 1
    #          Transform 4: 4/2
    'E1-1':     [   "@ X",
                ],

    # +-----+  Level 1         Transforms  3 . 2
    # | @ . |  Threads 1                   . @ .
    # | . X |  Cards 1                     4 . 1
    # +-----+  Transform 4: 4/2
    'E1-2':     [   "@ .",
                    ". X",
                ],

    # +-------+  Level 1
    # | @ . X |  Threads 1
    # +-------+  Cards 1
    #            Transform 4: 4/4
    'E1-3':     [    "@ . X",
                ],

    # +-------+  Level 1          Transforms  . 6 . 7 .
    # | @ . . |  Threads 1                    5 . . . 8
    # | . . X |  Cards 1                      . . @ . .
    # +-------+  Transform 8: 8/5             4 . . . 1
    #                                         . 3 . 2 .
    'E1-4':     [   "@ . .",
                    ". . X",
                ],

    # +-------+  Level 2          Transforms  3 . . . 2
    # | @ . . |  Threads 1                    . . . . .
    # | . . . |  Cards 2                      . . @ . .
    # | . . X |  Transform 4: 4/6             . . . . .
    # +-------+                               4 . . . 1
    'E1-5':     [   "@ . .",
                    ". . .",
                    ". . X",
                ],

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

    # +-------+  Level 2 - Built on +-----+  Transforms  . 2 .
    # | X @ X |  Threads 1          | @ X |              1 @ 1
    # +-------+  Cards 1            +-----+              . 2 .
    #            Transform 2: 4/2
    'E2-1':     [   "X @ X",
                ],

    # +-----+  Level 2 - Built on +-----+  Transforms  . 2 .
    # | @ X |  Threads 2          | @ X |              3 @ 1
    # | X . |  Cards 1            +-----+              . 1 .
    # +-----+  Transform 3: 4/2
    'E2-2':     [   "@ X",
                    "X .",
                ],

    # +-------+  Level 2 - Built on +-----+     +-----+  Transforms  7 2 5
    # | . @ X |  Threads 2          | @ X | and | @ . |              4 @ 1        
    # | X . . |  Cards 1            +-----+     | . X |              1 6 3
    # +-------+  Transform 7: 8/2               +-----+
    'E2-3':     [   ". @ X",
                    "X . .",
                ],

    # +-----+  Level 2 - Built on +-----+     +-----+  Transforms  5 4 3
    # | @ . |  Threads 2          | @ X | and | @ . |              6 @ 2
    # | X X |  Cards 1            +-----+     | . X |              7 1 1
    # +-----+  Transform 7: 8/2               +-----+
    'E2-4':     [   "@ .",
                    "X X",
                ],

    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . . 2 . .
    # | @ X X |  Threads 2          | @ X | and | @ . X |              . . 2 . .
    # +-------+  Cards 1            +-----+     +-------+              3 3 @ 1 1
    #            Transform 4: 8/4                                      . . 4 . .
    #                                                                  . . 4 . .
    'E2-5':     [    "@ X X",
                ],

    # +---------+  Level 3 - Built on +-----+     +-------+  Transforms  . . 2 . .
    # | X @ . X |  Threads 2          | @ X | and | @ . X |              . . 4 . .
    # +---------+  Cards 2            +-----+     +-------+              3 1 @ 3 1
    #              Transform 4: 8/4                                      . . 2 . .
    #                                                                    . . 4 . .
    'E2-6':     [   "X @ . X",
                ],

    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . . 4 . .
    # | @ . X |  Threads 2          | @ X | and | @ . X |              . . 2 . .
    # | X . . |  Cards 1            +-----+     +-------+              3 5 @ 4 1
    # +-------+  Transform 6: 8/4                                      . . 1 . .
    #                                                                  . . 6 . .
    'E2-7':     [   "@ . X",
                    "X . .",
                ],

    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . 4 . 3 .
    # | @ X . |  Threads 2          | @ X | and | @ . . |              5 . 3 . 2
    # | . . X |  Cards 1            +-----+     | . . X |              . 5 @ 1 .
    # +-------+  Transform 8: 12/5              +-------+              6 . 7 . 1
    #                                                                  . 7 . 8 .
    'E2-8':     [   "@ X .",
                    ". . X",
                ],

    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . 8 . 5 .
    # | @ . . |  Threads 2          | @ X | and | @ . . |              3 . 3 . 4
    # | X . X |  Cards 1            +-----+     | . . X |              . 7 @ 5 .
    # +-------+  Transform 8: 12/5              +-------+              2 . 1 . 1
    #                                                                  . 7 . 6 .
    'E2-9':     [   "@ . .",
                    "X . X",
                ],

    # +---------+  Level 3 - Built on +-----+     +-------+  Transforms  . 4 . 3 .
    # | X @ . . |  Threads 2          | @ X | and | @ . . |              5 . 7 . 2
    # | . . . X |  Cards 2            +-----+     | . . X |              . 1 @ 5 .
    # +---------+  Transform 8: 12/5              +-------+              6 . 3 . 1
    #                                                                    . 7 . 8 .
    'E2-10':    [   "X @ . .",
                    ". . . X",
                ],

    # +-------+  Level 3 - Built on +-----+     +-------+  Transforms  . 7 . 3 .
    # | X . . |  Threads 2          | @ X | and | @ . . |              6 . 1 . 5
    # | @ . . |  Cards 1            +-----+     | . . X |              . 3 @ 7 .
    # | . . X |  Transform 8: 12/5              +-------+              2 . 5 . 1
    # +-------+                                                        . 8 . 4 .
    'E2-11':    [   "X . .",
                    "@ . .",
                    ". . X",
                ],

    # +---------+  Level 3 - Built on +-----+     +---------+
    # | @ X . X |  Threads 2          | @ X | and | @ . . X |
    # +---------+  Cards 2            +-----+     +---------+
    #              Transform 4: 8/6
    'E2-12':    [   "@ X . X",
                ],

    # +-----------+  Level 3 - Built on +-----+     +---------+
    # | X @ . . X |  Threads 2          | @ X | and | @ . . X |
    # +-----------+  Cards 2            +-----+     +---------+
    #                Transform 4: 8/6
    'E2-13':    [   "X @ . . X",
                ],

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

    # +-----------+  Level 3 - Built on +-----+     +---------+
    # | X @ . . . |  Threads 2          | @ X | and | @ . . . |
    # | . . . . X |  Cards 2            +-----+     | . . . X |
    # +-----------+  Transform 8                    +---------+
    'E2-17':    [],

    # +---------+  Level 3 - Built on +-----+     +---------+
    # | X . . . |  Threads 2          | @ X | and | @ . . . |
    # | @ . . . |  Cards 3            +-----+     | . . . X |
    # | . . . X |  Transform 8                    +---------+
    # +---------+
    'E2-18':    [],

    # +-------+  Level 2 - Built on +-----+  Transforms  3 . 2
    # | . @ . |  Threads 2          | @ . |              . @ .
    # | X . X |  Cards 1            | . X |              1 . 1
    # +-------+  Transform 3: 4/2   +-----+
    'E2-19':    [   ". @ .",
                    "X . X",
                ],

    # +-------+  Level 3 - Built on +-----+  Transforms  1 . 2
    # | X . . |  Threads 2          | @ . |              . @ .
    # | . @ . |  Cards 2            | . X |              2 . 1
    # | . . X |  Transform 2: 4/2   +-----+
    # +-------+
    'E2-20':    [   "X . .",
                    ". @ .",
                    ". . X",
                ],

    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . . 3 . .
    # | @ . X |  Threads 2          | @ . | and | @ . X |              . 4 . 2 .
    # | . X . |  Cards 1            | . X |     +-------+              5 . @ . 1
    # +-------+  Transform 7: 8/4   +-----+                            . 6 . 1 .
    #                                                                  . . 7 . .
    'E2-21':    [   "@ . X",
                    ". X .",
                ],

    # +---------+  Level 3 - Built on +-----+     +-------+  Transforms  . . 3 . .
    # | . @ . X |  Threads 3          | @ . | and | @ . X |              . 2 . 6 .
    # | X . . . |  Cards 2            | . X |     +-------+              7 . @ . 1
    # +---------+  Transform 7: 8/4   +-----+                            . 1 . 4 .
    #                                                                    . . 5 . .
    'E2-22':    [   ". @ . X",
                    "X . . .",
                ],

    # +-------+  Level 2 - Built on +-----+     +-------+  Transforms  . 6 . 3 .
    # | @ . . |  Threads 2          | @ . | and | @ . . |              5 5 . 3 4
    # | . X X |  Cards 1            | . X |     | . . X |              . . @ . .
    # +-------+  Transform 8: 12/5  +-----+     +-------+              8 7 . 1 1
    #                                                                  . 7 . 2 .
    'E2-23':    [   "@ . .",
                    ". X X",
                ],

    # +---------+  Level 3 - Built on +-----+     +-------+  Transforms  . 2 . 6 .
    # | . @ . . |  Threads 2          | @ . | and | @ . . |              7 3 . 7 3
    # | X . . X |  Cards 2            | . X |     | . . X |              . . @ . .
    # +---------+  Transform 8: 12/5  +-----+     +-------+              5 1 . 5 1
    #                                                                    . 4 . 8 .
    'E2-24':    [   ". @ . .",
                    "X . . X",
                ],

    # +---------+  Level 3 - Built on +-----+     +-------+  Transforms  . 5 . 4 .
    # | X . . . |  Threads 2          | @ . | and | @ . . |              6 1 . 7 3
    # | . @ . . |  Cards 3            | . X |     | . . X |              . . @ . .
    # | . . . X |  Transform 8: 12/5  +-----+     +-------+              8 3 . 5 1
    # +---------+                                                        . 7 . 2 .
    'E2-25':    [   "X . . .",
                    ". @ . .",
                    ". . . X",
                ],

    # +-------+  Level 3 - Built on +-----+     +-------+  Transforms  . 6 . 7 .
    # | . @ . |  Threads 2          | @ . | and | @ . . |              2 7 . 5 4
    # | X . . |  Cards 2            | . X |     | . . X |              . . @ . .
    # | . . X |  Transform 8: 12/5  +-----+     +-------+              8 1 . 3 5
    # +-------+                                                        . 3 . 1 .
    'E2-26':    [   ". @ .",
                    "X . .",
                    ". . X",
                ],

    # +-------+  Level 3 - Built on +-----+     +-------+  Transforms  3 . . . 2
    # | @ . . |  Threads 2          | @ . | and | @ . . |              . 3 . 2 .
    # | . X . |  Cards 2            | . X |     | . . . |              . . @ . .
    # | . . X |  Transform 4: 8/5   +-----+     | . . X |              . 4 . 1 .
    # +-------+                                 +-------+              4 . . . 1
    'E2-27':    [   "@ . .",
                    ". X .",
                    ". . X",
                ],

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

    # +-----------+  Level 3 - Built on +-----+     +---------+
    # | . @ . . . |  Threads 2          | @ . | and | @ . . . |
    # | X . . . X |  Cards 2            | . X |     | . . . X |
    # +-----------+  Transform 8: 12/8  +-----+     +---------+
    'E2-32':    [],

    # +-----------+  Level 3 - Built on +-----+     +---------+
    # | X . . . . |  Threads 2          | @ . | and | @ . . . |
    # | . @ . . . |  Cards 4            | . X |     | . . . X |
    # | . . . . X |  Transform 8: 12/8  +-----+     +---------+
    # +-----------+
    'E2-33':    [],
    
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

    # +-----------+  Level 3 - Built on +-------+
    # | X . @ . X |  Threads 2          | @ . X |
    # +-----------+  Cards 2            +-------+
    #                Transform 2: 4/4
    'E2-38':    [   "X . @ . X",
                ],

    # +-------+  Level 3 - Build on +-------+
    # | @ . X |  Threads 2          | @ . X |
    # | . . . |  Cards 2            +-------+
    # | X . . |  Transform 3: 4/4
    # +-------+
    'E2-39':    [   "@ . X",
                    ". . .",
                    "X . .",
                ],

    # +-------+  Level 2 - Built on +-------+     +-------+  Transforms  . 4 3 3 .
    # | @ . X |  Threads 2          | @ . X | and | @ . . |              5 . . . 2
    # | . . X |  Cards 1            +-------+     | . . X |              5 . @ . 1
    # +-------+  Transform 8: 12/5                +-------+              6 . . . 1
    #                                                                    . 7 7 8 .
    'E2-40':    [   "@ . X",
                    ". . X",
                ],

    # +-------+  Level 2 - Built on +-------+     +-------+  Transforms  . 3 7 2 .
    # | @ . X |  Threads 2          | @ . X | and | @ . . |              8 . . . 7
    # | . . . |  Cards 2            +-------+     | . . X |              3 . @ . 1
    # | . X . |  Transform 8: 12/5                +-------+              6 . . . 5
    # +-------+                                                          . 4 5 1 .
    'E2-41':    [   "@ . X",
                    ". . .",
                    ". X .",
                ],

    # +-----------+  Level 3 - Built on +-------+     +-------+
    # | X . @ . . |  Threads 2          | @ . X | and | @ . . |
    # | . . . . X |  Cards 2            +-------+     | . . X |
    # +-----------+  Transform 8: 12/5                +-------+
    'E2-42':    [   "X . @ . .",
                    ". . . . X",
                ],

    # +---------+  Level 2 - Built on +-------+     +-------+
    # | . @ . X |  Threads 2          | @ . X | and | @ . . |
    # | . . . . |  Cards 3            +-------+     | . . X |
    # | X . . . |  Trnsform 8: 12/5                 +-------+
    # +---------+
    'E2-43':    [],

    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . X X |  Threads 2          | @ . X | and | @ . . X |
    # +---------+  Cards 2            +-------+     +---------+
    #              Transform 4: 8/5
    'E2-44':    [],

    # +-------------+  Level 3 - Built on +-------+     +---------+
    # | X . @ . . X |  Threads 2          | @ . X | and | @ . . X |
    # +-------------+  Cards 3            +-------+     +---------+
    #                  Transform 4: 8/5
    'E2-45':    [],

    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . . X |  Threads 2          | @ . X | and | @ . . X |
    # | . . . . |  Cards 3            +-------+     +---------+
    # | X . . . |  Transform 6: 8/5
    # +---------+
    'E2-46':    [   "@ . . X",
                    ". . . .",
                    "X . . .",
                ],

    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . X . |  Threads 2          | @ . X | and | @ . . . |
    # | . . . X |  Cards 2            +-------+     | . . . X |
    # +---------+  Transform 8: 12/8                +---------+
    # + 3 variants
    'E2-47':    [],
    'E2-48':    [],
    'E2-49':    [],
    'E2-50':    [],

    # +-----------+  Level 3 - Built on +-------+     +-----------+
    # | @ . X . . |  Threads 2          | @ . X | and | @ . . . . |
    # | . . . . X |  Cards 2            +-------+     | . . . . X |
    # +-----------+  Transform 8: 12/                 +-----------+
    # + 3 variants
    'E2-51':    [],
    'E2-52':    [],
    'E2-53':    [],
    'E2-54':    [],

    # +-------+  Level 3 - Built on +-------+  Transforms  . 3 . 3 .
    # | . @ . |  Threads 2          | @ . . |              4 . . . 2
    # | . . . |  Cards 2            | . . X |              . . @ . .
    # | X . X |  Transform 4: 8/5   +-------+              4 . . . 2
    # +-------+                                            . 1 . 1 .
    'E2-55':    [   ". @ .",
                    ". . .",
                    "X . X",
                ],

    # +---------+  Level 3 - Built on +-------+
    # | . @ . . |  Threads 2          | @ . . |
    # | . . . X |  Cards 3            | . . X |
    # | X . . . |  Transform 6: 8/5   +-------+
    # +---------+
    'E2-56':    [],

    # +-----------+  Level 3 - Built on +-------+
    # | . . @ . . |  Threads 2          | @ . . |
    # | X . . . X |  Cards 2            | . . X |
    # +-----------+  Transform 6: 8/5   +-------+
    'E2-57':    [],

    # +-----------+  Level 3 - Built on +-------+
    # | X . . . . |  Threads 2          | @ . . |
    # | . . @ . . |  Cards 4            | . . X |
    # | . . . . X |  Transform 4: 8/5   +-------+
    # +-----------+
    'E2-58':    [],

    # +---------+  Level 3 - Built on +-------+  Transforms  . 2 . 3 .
    # | . . . X |  Threads 2          | @ . . |              4 . . . 1
    # | . @ . . |  Cards 4            | . . X |              . . @ . .
    # | . . . . |  Transform 4: 8/5   +-------+              3 . . . 2
    # | X . . . |                                            . 1 . 4 .
    # +---------+
    'E2-59':    [],

    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . . X |  Threads 2          | @ . . | and | @ . . X |
    # | . . X . |  Cards 2            | . . X |     +---------+
    # +---------+  Transform 8: 12/   +-------+
    # + 3 variants
    'E2-60':    [],
    'E2-61':    [],
    'E2-62':    [],
    'E2-63':    [],

    # +---------+  Level 3 - Built on +-------+     +---------+
    # | @ . . . |  Threads 2          | @ . . | and | @ . . . |
    # | . . X X |  Cards 2            | . . X |     | . . . X |
    # +---------+  Transform 8: 16/   +-------+     +---------+
    # + 3 variants
    'E2-64':    [],
    'E2-65':    [],
    'E2-66':    [],
    'E2-67':    [],

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

    # +-----------+  Level 3 - Built on +-------+     +-----------+
    # | @ . . . X |  Threads 2          | @ . . | and | @ . . . X |
    # | . . X . . |  Cards 2            | . . X |     +-----------+
    # +-----------+  Transform 8: 12/   +-------+
    # + 3 variants
    'E2-72':    [],
    'E2-73':    [],
    'E2-74':    [],
    'E2-75':    [],

    # +-----------+  Level 3 - Built on +-------+     +-----------+
    # | @ . . . . |  Threads 2          | @ . . | and | @ . . . . |
    # | . . X . X |  Cards 2            | . . X |     | . . . . X |
    # +-----------+  Transform 8: 16/   +-------+     +-----------+
    # + 3 variants
    'E2-76':    [],
    'E2-77':    [],
    'E2-78':    [],
    'E2-79':    [],

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

    # +-------+  Level 4 - Build on +-----+     +-------+
    # | @ . X |  Threads 3          | @ . | and | @ . X |
    # | . X . |  Cards 2            | . X |     +-------+
    # | X . . |  Transform 4: 8/5   +-----+
    # +-------+
    'E3-1':     [],

    # +-------+  Level 4 - Build on +-----+     +-------+  Transforms  3 . . . 2
    # | @ X . |  Threads 3          | @ X | and | @ . . |              . . 2 . .
    # | X . . |  Cards 2            +-----+     | . . . |              . 3 @ 1 .
    # | . . X |  Transform 4: 8/5               | . . X |              . . 1 . .
    # +-------+                                 +-------+              4 . . . 1
    'E3-2':     [],

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

    # +-------+  Level 2 - Built on +-----+
    # | @ X @ |  Threads 1          | @ X |
    # +-------+  Cards 2            +-----+
    #            Transform 1: 1/
    'EE1-1':    [],

    # +-----+  Level 2 - Built on +-----+
    # | @ X |  Threads 1          | @ X |
    # | . @ |  Cards 2            +-----+
    # +-----+  Transform 2: 2/
    'EE1-2':    [],

    # +-------+  Level 2 - Built on +-----+     +-------+
    # | @ @ X |  Threads 1          | @ X | and | @ . X |
    # +-------+  Cards 2            +-----+     +-------+
    #            Transform 2: 2/
    'EE1-3':    [],

    # +-------+  Level 3 - Built on +-----+
    # | @ . . |  Threads 1          | @ . |
    # | . X . |  Cards 2            | . X |
    # | . . @ |  Transform 1: 1/    +-----+
    # +-------+
    'EE1-4':    [   "@ . .",
                    ". X .",
                    ". . @",
                ],

    # +-------+  Level 2 - Built on +-----+
    # | @ . @ |  Threads 1          | @ . |
    # | . X . |  Cards 2            | . X |
    # +-------+  Transform 2: 2/    +-----+
    'EE1-5':    [   "@ . @",
                    ". X .",
                ],

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

    # +-----+  Level 3 - Built on +-----+
    # | @ X |  Threads 2          | @ X |
    # | X @ |  Cards 2            +-----+
    # +-----+  Transform 1: 2/
    'EE2-1':    [   "@ X",
                    "X @",
                ],

    # +-------+  Level 3 - Built on +-----+  Transforms  . 2 . .
    # | @ X . |  Threads 2          | @ X |              3 @ 1 .
    # | . @ X |  Cards 2            +-----+              . 3 @ 1
    # +-------+  Transform 4: 6/                         . . 4 .
    'EE2-2':    [   "@ X .",
                    ". @ X",
                ],

    # +-------+  Level 4 - Built on +-----+
    # | X . . |  Threads 2          | @ X |
    # | @ . . |  Cards 2            +-----+
    # | . @ X |  Transform 2; 4/
    # +-------+
    'EE2-3':    [],

    # +---------+  Level 3 - Built on +-----+
    # | X @ . . |  Threads 2          | @ X |
    # | . . @ X |  Cards 2            +-----+
    # +---------+  Transform 2: 4/
    'EE2-4':    [   "X @ . .",
                    ". . @ X",
                ],

    # +-------+  Level 3 - Built on +-----+  Transforms  . 2 . .
    # | @ . . |  Threads 2          | @ X |              3 @ 3 .
    # | X @ X |  Cards 2            +-----+              . 1 @ 1
    # +-------+  Transform 4: 6/                         . . 4 .
    'EE2-5':    [   "@ . .",
                    "X @ X",
                ],

    # +-------+  Level 4 - Built on +-----+
    # | . @ . |  Threads 2          | @ . |
    # | X . X |  Cards 2            | . X |
    # | . @ . |  Transform 1: 1/    +-----+
    # +-------+
    'EE2-6':    [   ". @ .",
                    "X . X",
                    ". @ .",
                ],

    # +---------+  Level 4 - Built on +-----+
    # | . @ @ . |  Threads 2          | @ . |
    # | X . . X |  Cards 2            | . X |
    # +---------+  Transform 2: 4/    +-----+
    'EE2-7':    [],

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

#     _____ _     
#    |  _  |_|___ 
#    |     | |  _|
#    |__|__|_|_|  
#
# Primary: Move Self, Move Other
# Secondary:
# Opposite: Earth

#     _____ _         
#    |   __|_|___ ___ 
#    |   __| |  _| -_|
#    |__|  |_|_| |___|
#
# Primary: Attack HP, Attack Eye
# Secondary:
# Opposite: Water

#     _____         _   _   
#    |   __|___ ___| |_| |_ 
#    |   __| .'|  _|  _|   |
#    |_____|__,|_| |_| |_|_|
#
# Primary: Defend Eye, Defend HP, Defend Move Self, Charge
# Secondary: Rough Terrain
# Opposite: Air

#     _ _ _     _           
#    | | | |___| |_ ___ ___ 
#    | | | | .'|  _| -_|  _|
#    |_____|__,|_| |___|_|  
#
# Primary: Create Eye, Move Eye, Heal HP, Thread
# Secondary: Water Terrain
# Opposite: Fire
    
# Unassigned:
#   Tapestry, Other Tapestry, Defend Tapestry
#   Move Other Eye, Defend Move Eye
#   Spell, Other Spell
#   Terrain

# Data Format:
#   spell_card_data:
#     List of <card>s
#
#   <card>:
#     <title>, <attributes>, List of <description> strings
#
#   <attribute>:
#     'element': 'air', 'fire', 'earth', 'water' or 'none'
#     'category': <string> to group spells by general category
#     'id': spell id
#     'pattern': name of pattern

# Next id = 97
# Unused: 70

spell_card_data = [

    # Blank card (for TTS)
    #["???",
    #    {'element': 'none', 'category': 'starter', 'id': 0, 'pattern': 'blank'},
    #    {
    #        'cast': "???",
    #    } ],

    #     _____         _           _ 
    #    |   | |___ _ _| |_ ___ ___| |
    #    | | | | -_| | |  _|  _| .'| |
    #    |_|___|___|___|_| |_| |__,|_|
    #
    # Neutral spells are basic spells that are always worse than corresponding elemental spells.
    
    ["Create Eye",
        {'element': 'none', 'category': 'starter,create-eye', 'id': 89, 'pattern': 'N1'},
        {
            'cast': "Create a EYE in your location.",
        } ],
    ["Move Eye",
        {'element': 'none', 'category': 'starter,move-eye', 'id': 90, 'pattern': 'N2-4'},
        {
            'cast': "Move one of your EYEs one space.",
        } ],
             
    #     _____ _           _           
    #    |   __| |_ ___ ___| |_ ___ ___ 
    #    |__   |  _| .'|  _|  _| -_|  _|
    #    |_____|_| |__,|_| |_| |___|_|  
    #
    # Representative spell for each element.

    ["Haste",
        {'element': 'air', 'category': 'starter,move-mage', 'id': 3, 'pattern': 'E1-1'},
        {
            'cast': "Move 5 spaces along a road.",
        } ],
    ["Burn Eye",
        {'element': 'fire', 'category': 'starter,attack-eye', 'id': 92, 'pattern': 'E1-2'},
        {
            'cast': "Remove an opponent's EYE at one of your EYE's location. Consume this EYE.",
        } ],
    ["Protection",
        {'element': 'earth', 'category': 'starter,defend-eye', 'id': 4, 'pattern': 'E1-1'},
        {
            'cast': "{{ADD_CHARGE}}",
            'sacrifice': "Sacrifice a charge to prevent one of your EYEs from being removed.",
        } ],
    ["Creep",
        {'element': 'water', 'category': 'starter,create-eye,move-eye', 'id': 73, 'pattern': 'E1-2'},
        {
            'cast': "Place a EYE. Move one of your EYEs 2 spaces.",
        } ],

    #     _____                _____     _ ___ 
    #    |     |___ _ _ ___   |   __|___| |  _|
    #    | | | | . | | | -_|  |__   | -_| |  _|
    #    |_|_|_|___|\_/|___|  |_____|___|_|_|
    #
    # Move mage

    ["Plains Walker",
        {'element': 'air', 'category': 'move-mage,terrain', 'id': 7, 'pattern': 'E2-6'},
        {
            'cast': "Move through 5 contiguous Plains locations.",
        } ],
    ["Forest Run",
        {'element': 'air', 'category': 'terrain,move-mage', 'id': 11, 'pattern': 'E2-14'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "If in or next to a Forest location, pay 2mp to move through any number of connected Forest locations, bypassing any Rivers.",
        } ],
    ["Forest Jump",
        {'element': 'air', 'category': 'terrain,move-mage', 'id': 93, 'pattern': 'E2-13'},
        {
            'cast': "If in a Forest location, swap positions with one of your EYEs that is in a Forest location no more than 5 spaces away. You may immediately repeat this spell.",
            'notes': "You may only use each EYE once when you cast this spell.",
        } ],
    ["Blur",
        {'element': 'air', 'category': 'move-mage', 'id': 19, 'pattern': 'E2-42'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "Once per turn (per charge), you may move into a neighboring location ignoring terrain cost.",
        } ],
    ["Quick Drop",
        {'element': 'air', 'category': 'move-mage,create-eye', 'id': 66, 'pattern': 'E2-10'},
        {
            'cast': "Move 5mp. Place a EYE in your final location.",
        } ],

    #     _____                _____ _   _           
    #    |     |___ _ _ ___   |     | |_| |_ ___ ___ 
    #    | | | | . | | | -_|  |  |  |  _|   | -_|  _|
    #    |_|_|_|___|\_/|___|  |_____|_| |_|_|___|_|
    #
    # Attack by moving another player's mage
                                                                         
    ["Push",
        {'element': 'air', 'category': 'move-mage,move-other-mage', 'id': 20, 'pattern': 'E2-5'},
        {
            'cast': "Push all mages out of an adjacent location and then move into that location. You choose which location each mage moves into.",
            'notes': "If there are multiple mages, they can be pushed in to different locations."
        } ],
    ["Teleport Random",
        {'element': 'fire', 'category': 'move-other-mage', 'id': 95, 'pattern': 'E2-8'},
        {
            'cast': "Move all mages at one of your EYEs to a random star location. Consume that EYE.",
        } ],
    ["Barrier",
        {'element': 'earth', 'category': 'move-other-mage', 'id': 87, 'pattern': 'E2-10'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "All locations adjacent to your EYEs are obstacles that other mages may not move into.",
        } ],

    #     ____      ___           _    _____                _____     _ ___ 
    #    |    \ ___|  _|___ ___ _| |  |     |___ _ _ ___   |   __|___| |  _|
    #    |  |  | -_|  _| -_|   | . |  | | | | . | | | -_|  |__   | -_| |  _|
    #    |____/|___|_| |___|_|_|___|  |_|_|_|___|\_/|___|  |_____|___|_|_|
    #
    # Defend against being moved by another mage

    ["Anchor",
        {'element': 'earth', 'category': 'defend-move', 'id': 39, 'pattern': 'E2-16'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "You may not be involuntarily moved by other mages.",
        } ],

    #     _____             _          _____         
    #    |     |___ ___ ___| |_ ___   |   __|_ _ ___ 
    #    |   --|  _| -_| .'|  _| -_|  |   __| | | -_|
    #    |_____|_| |___|__,|_| |___|  |_____|_  |___|
    #                                       |___|
    #
    # Convert mana into an Eye on the map

    ["Split",
        {'element': 'water', 'category': 'create-eye', 'id': 8, 'pattern': 'E2-27'},
        {
            'cast': "Place a new EYE in a location where you already have a EYE.",
        } ],
    ["Mountain Eye",
        {'element': 'earth', 'category': 'terrain,create-eye', 'id': 12, 'pattern': 'E2-11'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "If in or next to a Mountain location, add a EYE adjacent to any Mountain location connected to that Mountain location.",
        } ],
    ["Snapback",
        {'element': 'water', 'category': 'create-eye', 'id': 79, 'pattern': 'E2-25'},
        {
            'cast': "{{ADD_CHARGE}}",
            'sacrifice': "If at same location as another mage's EYE, you may sacrifice a charge to place a EYE at that mage's location.",
        } ],

    #     _____                _____         
    #    |     |___ _ _ ___   |   __|_ _ ___ 
    #    | | | | . | | | -_|  |   __| | | -_|
    #    |_|_|_|___|\_/|___|  |_____|_  |___|
    #                               |___|
    #
    # Move one of your Eyes on the map
    
    ["Run and Toss",
        {'element': 'air', 'category': 'move-mage,create-eye,move-eye', 'id': 67, 'pattern': 'E2-46'},
        {
            'cast': "Move 1 space, place a EYE, then move that EYE 2 spaces.",
        } ],
    ["Spread",
        {'element': 'water', 'category': 'create-eye,move-eye', 'id': 75, 'pattern': 'E2-20'},
        {
            'cast': "Place a EYE. Move all of your EYEs 1 space.",
        } ],
    ["Burst",
        {'element': 'water', 'category': 'create-eye,move-eye', 'id': 74, 'pattern': 'E2-31'},
        {
            'cast': "Place 2 EYEs. Move 3 of your EYEs 2 spaces each.",
        } ],
    ["Traceback",
        {'element': 'water', 'category': 'move-eye,create-eye', 'id': 69, 'pattern': 'E2-41'},
        {
            'cast': "Move a EYE 2. If you have a EYE in the same location as a EYE owned by another mage, move your EYE to that mage's location.",
        } ],

    #     _____                _____ _   _              _____         
    #    |     |___ _ _ ___   |     | |_| |_ ___ ___   |   __|_ _ ___ 
    #    | | | | . | | | -_|  |  |  |  _|   | -_|  _|  |   __| | | -_|
    #    |_|_|_|___|\_/|___|  |_____|_| |_|_|___|_|    |_____|_  |___|
    #                                                        |___|
    #
    # Move an opponent's Eye

    #     ____      ___           _    _____                _____         
    #    |    \ ___|  _|___ ___ _| |  |     |___ _ _ ___   |   __|_ _ ___ 
    #    |  |  | -_|  _| -_|   | . |  | | | | . | | | -_|  |   __| | | -_|
    #    |____/|___|_| |___|_|_|___|  |_|_|_|___|\_/|___|  |_____|_  |___|
    #                                                            |___|
    #
    # Defend against an opponent moving your Eyes
    
    #     _____ _   _           _      _____         
    #    |  _  | |_| |_ ___ ___| |_   |   __|_ _ ___ 
    #    |     |  _|  _| .'|  _| '_|  |   __| | | -_|
    #    |__|__|_| |_| |__,|___|_,_|  |_____|_  |___|
    #                                       |___|
    #
    # Remove an opponent's Eye

    ["Remove Eye",
        {'element': 'fire', 'category': 'attack-eye', 'id': 72, 'pattern': 'E2-19'},
        {
            'cast': "If in a location with a EYE controlled by another mage, you may remove 2 of their EYEs.",
        } ],
    ["Prune",
        {'element': 'fire', 'category': 'attack-eye', 'id': 33, 'pattern': 'E2-23'},
        {
            'cast': "Remove all opponent EYEs from a location where you control a EYE. Consume this EYE.",
        } ],
    ["Prune Neighbor",
        {'element': 'fire', 'category': 'attack-eye', 'id': 42, 'pattern': 'E2-31'},
        {
            'cast': "Remove all EYEs from a location adjacent to where you control a EYE. Consume this EYE.",
        } ],
    ["Erase",
        {'element': 'fire', 'category': 'move-eye,attack-eye', 'id': 65, 'pattern': 'E2-28'},
        {
            'cast': "Move one of your EYEs 3 spaces, removing one opponent EYE from each location it moves into this turn. Consume this EYE.",
        } ],
    ["Fire Burst",
        {'element': 'fire', 'category': 'attack-eye', 'id': 23, 'pattern': 'E2-30'},
        {
            'cast': "Remove all EYEs in all locations adjacent to one of your EYEs. Consume that EYE.",
        } ],
    ["Nudge",
        {'element': 'earth', 'category': 'move-other-eye', 'id': 85, 'pattern': 'E2-8'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "At the end of your turn, if another mage's EYE is in the same location or adjacent to one of your EYEs, you may move their EYE 1 space. Choose one for each charge on this spell.",
            'sacrifice': "Sacrifice a charge to move the eye(s) 4 spaces."
        } ],
    ["Sneak Attack",
        {'element': 'fire', 'category': 'attack-eye,move-mage', 'id': 64, 'pattern': 'E2-55'},
        {
            'cast': "Remove EYEs from a adjacent location and then move into that location.",
        } ],

    #     ____      ___           _    _____         
    #    |    \ ___|  _|___ ___ _| |  |   __|_ _ ___ 
    #    |  |  | -_|  _| -_|   | . |  |   __| | | -_|
    #    |____/|___|_| |___|_|_|___|  |_____|_  |___|
    #                                       |___|
    #
    # Defend against an opponent removing one of your eyes

    ["Eye Shield",
        {'element': 'earth', 'category': 'defend-eye', 'id': 83, 'pattern': 'E1-6'},
        {
            'cast': "{{ADD_CHARGE}}",
            'sacrifice': "You may sacrifice this CHARGE to prevent one of your EYEs from being removed or consumed.",
        } ],
    ["Harden Shell",
        {'element': 'earth', 'category': 'defend-eye', 'id': 86, 'pattern': 'E2-9'},
        {
            'cast': "{{ADD_CHARGE}}", 
            'charged': "If the number of EYEs you have is less than or equal to the number of CHARGEs on this spell, then they are protected from being removed by another mage (but they can still be consumed).",
        } ],
    ["Whiplash",
        {'element': 'water', 'category': 'defend-eye', 'id': 76, 'pattern': 'E2-21'},
        {
            'cast': "{{ADD_CHARGE}}",
            'sacrifice': "You may sacrifice one of your EYEs to prevent another EYE from being removed/consumed.",
        } ],

    #     _____ _   _           _        _____ _____ 
    #    |  _  | |_| |_ ___ ___| |_     |  |  |  _  |
    #    |     |  _|  _| .'|  _| '_|    |     |   __|
    #    |__|__|_| |_| |__,|___|_,_|    |__|__|__|
    #
    # Attack another mage

    #     ____      ___           _      _____ _____ 
    #    |    \ ___|  _|___ ___ _| |    |  |  |  _  |
    #    |  |  | -_|  _| -_|   | . |    |     |   __|
    #    |____/|___|_| |___|_|_|___|    |__|__|__|
    #
    # Defend against being attacked

    #     _____                 _           
    #    |_   _|___ ___ ___ ___| |_ ___ _ _ 
    #      | | | .'| . | -_|_ -|  _|  _| | |
    #      |_| |__,|  _|___|___|_| |_| |_  |
    #              |_|                 |___|
    #
    # Tapestry modification
    # Spell: Remove thread from tapestry. Take another action.

    ["Rest",
        {'element': 'water', 'category': 'thread', 'id': 58, 'pattern': 'E2-19'},
        {
            'cast': "Remove 3 THREADs from your TAPESTRY.",
        } ],

    #     _____ _   _              _____                 _           
    #    |     | |_| |_ ___ ___   |_   _|___ ___ ___ ___| |_ ___ _ _ 
    #    |  |  |  _|   | -_|  _|    | | | .'| . | -_|_ -|  _|  _| | |
    #    |_____|_| |_|_|___|_|      |_| |__,|  _|___|___|_| |_| |_  |
    #                                       |_|                 |___|
    # Attack an opponent's tapestry
    # Spell: Attack tapestry, cover a spot in another mage's tapestry.

    ["Burn",
        {'element': 'fire', 'category': 'attack-tapestry', 'id': 91, 'pattern': 'E2-20'},
        {
            'cast': "Disrupt the tapestry of a mage at one of your EYEs by placing one of your mana in their tapestry to cover an element. Consume the EYE used to target the mage.",
        } ],

    #     ____      ___           _    _____                 _           
    #    |    \ ___|  _|___ ___ _| |  |_   _|___ ___ ___ ___| |_ ___ _ _ 
    #    |  |  | -_|  _| -_|   | . |    | | | .'| . | -_|_ -|  _|  _| | |
    #    |____/|___|_| |___|_|_|___|    |_| |__,|  _|___|___|_| |_| |_  |
    #                                           |_|                 |___|
    # Defend tapestry from attack

    #     _____         _ _ 
    #    |   __|___ ___| | |
    #    |__   | . | -_| | |
    #    |_____|  _|___|_|_|
    #          |_|
    # Interact with your spells
    # Spell: Duplicate Charge

    #     _____ _   _              _____         _ _ 
    #    |     | |_| |_ ___ ___   |   __|___ ___| | |
    #    |  |  |  _|   | -_|  _|  |__   | . | -_| | |
    #    |_____|_| |_|_|___|_|    |_____|  _|___|_|_|
    #                                   |_|
    # Remove a charge from an opponent's spell

    ["Drain",
        {'element': 'air', 'category': 'attack-charge', 'id': 71, 'pattern': 'E2-12'},
        {
            'cast': "A mage at one of your EYEs must remove 2 of their CHARGEs. Consume that EYE.",
        } ],
    ["Copy Charge",
        {'element': 'earth', 'category': 'attack-charge', 'id': 94, 'pattern': 'E2-13'},
        {
            'cast': "If you have a EYE on or adjacent to another mage, you may add a charge to one of their spells. You gain all the effects of that spell.",
            'notes': "Even if mage removes their charge, yours stays active.",
        } ],
    

    #     _____     _   _         
    #    |  _  |___| |_|_|___ ___ 
    #    |     |  _|  _| | . |   |
    #    |__|__|___|_| |_|___|_|_|
    #
    # Gain an extra action

    ["Store Action",
        {'element': 'earth', 'category': 'add-action', 'id': 96, 'pattern': 'E2-39'},
        {
            'cast': "{{ADD_CHARGE}}",
            'sacrifice': "During your turn, you may sacrifice a charge to gain an extra action.",
        } ],
    
    #     _____                 _     
    #    |_   _|___ ___ ___ ___|_|___ 
    #      | | | -_|  _|  _| .'| |   |
    #      |_| |___|_| |_| |__,|_|_|_|

    ["Water Moccasins",
        {'element': 'water', 'category': 'move-mage,terrain', 'id': 54, 'pattern': 'E2-24'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "Rivers cost 0mp to cross. Water locations cost 1mp to enter.",
            'sacrifice': "If you are adjacent to River/Water, sacrifice charge to place a EYE up to 3 spaces away along water.",
        } ],

]

_unused_ = [

    # Move Self

    ["Teleport",
        {'element': 'air', 'category': 'move-mage', 'id': 78, 'pattern': 'E2-31'},
        {
            'cast': "Teleport to the location of one of your EYEs. Consume that EYE.",
        } ],
    ["Levitate",
        {'element': 'air', 'category': 'move', 'id': 9},
        ["Place a CHARGE on this spell.", "-", "Spend CHARGE to ignore terrain cost and effects when you move into (or are forced into) a location."] ],
    ["Fly",
        {'element': 'air', 'category': 'move', 'id': 10},
        ["Ignore terrain cost and effects when moving into 4 locations this turn."] ],
    ["Mountain Ranger",
        {'element': 'earth', 'category': 'terrain,move', 'id': 44},
        ["If in a Mountain location, add a EYE to a location in any Mountain range."] ],
    ["River Run",
        {'element': 'water', 'category': 'move,terrain', 'id': 55},
        ["If next to a river or water location, pay terrain cost to move into any other space adjacent to that river or water location.", "-", "Restrictions:", "* Rivers: Without passing a bridge", "* Water: Crossing 4 water locations max."] ],
    ["Mountain Reach",
        {'element': 'earth', 'category': 'terrain,move', 'id': 45},
        ["If in or adjacent to a Mountain location, add a EYE to any location in a 1- or 2-size Mountain range."] ],

    # Attack Other Move

    # Defend Move Self

    # Create Eye

    ["Reverse Eye",
        {'element': 'water', 'category': 'eye', 'id': 52},
        ["When in the same location as an opponent's EYE, add a EYE at the opponent's location."] ],
    ["Forest Bind",
        {'element': 'air', 'category': 'eye,terrain', 'id': 14},
        ["When in a Forest location, add a EYE to any location in Forest that is smaller in size than the one you occupy."] ],
    ["Water Hop",
        {'element': 'water', 'category': 'eye,terrain', 'id': 61},
        ["When next to a river or Water location, add a EYE to any location adjacent to that water.", "-", "Restrictions:", "* Rivers: Without passing a bridge", "* Water: Crossing 3 water locations max."] ],
    ["Water Jump",
        {'element': 'water', 'category': 'eye,terrain', 'id': 62},
        ["When next to a river or Water location, add a EYE to any location adjacent to that water.", "-", "Restrictions:", "* Rivers: Passing at most 1 bridge", "* Water: Crossing 5 water locations max."] ],
    ["Duplicate",
        {'element': 'water', 'category': 'eye', 'id': 53},
        ["When in the same location as an opponent's EYE, add a EYE at any location where that opponent controls a EYE."] ],

    # Move Eye

    ["Diasporate",
        {'element': 'water', 'category': 'create-eye,move-eye', 'id': 77, 'pattern': 'EE2-2'},
        {
            'cast': "Place 3 EYEs. Move 3 of your EYEs 2 spaces each.",
        } ],
    ["Plains Link",
        {'element': 'air', 'category': 'eye,terrain', 'id': 15},
        ["Move a EYE you control that is in a Plains location up to 7 spaces through connecting Plains locations."] ],
    ["Water Skip",
        {'element': 'water', 'category': 'eye,terrain', 'id': 60},
        ["Move a EYE you control that is adjacent to a river or water location into any other space adjacent to that river or water location.", "-", "Restrictions:", "* Rivers: Without passing a bridge", "* Water: Crossing 4 water locations max."] ],
    ["Forest Link Minor",
        {'element': 'air', 'category': 'eye,terrain', 'id': 16},
        ["Move a EYE you control that is in a Forest location to another location in any Forest of size 1 or 2."] ],
    ["Forest Link",
        {'element': 'air', 'category': 'eye,terrain', 'id': 17},
        ["Move a EYE you control that is in a Forest location to another location in any Forest that is smaller then the Forest with the EYE."] ],
    ["Mountain Link",
        {'element': 'air', 'category': 'eye,terrain', 'id': 18},
        ["Move a EYE you control that is in a Mountain location to any other Mountain location."] ],
    ["Exchange Eye",
        {'element': 'water', 'category': 'eye', 'id': 51},
        ["Exchange locations with a EYE you control."] ],
    ["Scatter",
        {'element': 'fire', 'category': 'eye', 'id': 30},
        ["Move all EYEs you control 1 space."] ],
    ["Scatter Far",
        {'element': 'fire', 'category': 'eye', 'id': 32},
        ["Move any 2 EYEs you control a total of 9 spaces."] ],
    ["Scatter Wide",
        {'element': 'fire', 'category': 'eye', 'id': 31},
        ["Move EYEs you control a total of 5 spaces, split amongst any number of EYEs."] ],

    # Attack Eye

    ["Selective Prune",
        {'element': 'earth', 'category': 'eye,attack', 'id': 41},
        ["Remove all EYEs (except the one used for this spell) from a location where you control a EYE."] ],
    ["Whirlwind",
        {'element': 'air', 'category': 'eye', 'id': 13},
        ["Place CHARGE on this spell.", "-", "While CHARGEd, all EYEs you control are obstacles that other mages may not move into or pass through."] ],
    ["Delete All 2",
        {'element': 'earth', 'category': 'eye,attack', 'id': 43},
        ["When in a location with a EYE controlled by another mage, remove all of that mage's EYEs.", "-", "If multiple mages, choose one."] ],
    ["Distraction",
        {'element': 'fire', 'category': 'eye', 'id': 34},
        ["When in the same location as a EYE controlled by another mage, remove any one of their EYEs."] ],
    ["Delete All",
        {'element': 'fire', 'category': 'attack-eye', 'id': 43, 'pattern': 'E1-2'},
        {
            'cast': "Remove all opponent EYEs at one of your EYE's location. Consume this EYE.",
        } ],

    # Defend Eye

    # Attack HP

    ["Ricochet Blast",
        {'element': 'fire', 'category': 'attack-mage', 'id': 24, 'pattern': 'E1-5'},
        {
            'cast': "Attack 1 at location adjacent to one of your EYEs. Consume that EYE.",
        } ],
    ["Fire Ball",
        {'element': 'fire', 'category': 'attack-mage', 'id': 22, 'pattern': 'E2-26'},
        {
            'cast': "Attack 2 at one of your EYEs. Consume that EYE.",
        } ],
    ["Fire Reign",
        {'element': 'fire', 'category': 'attack-mage', 'id': 26, 'pattern': 'E2-27'},
        {
            'cast': "Attack 1 at all of your EYEs. Consume all of your EYEs except one.",
        } ],
    ["Hands of Flame",
        {'element': 'fire', 'category': 'move-mage,attack-mage', 'id': 63, 'pattern': 'EE2-6'},
        {
            'cast': "Move 1 and then Attack 1 at a location adjacent to your new location.",
        } ],
    ["Fire Boost",
        {'element': 'fire', 'category': 'attack', 'id': 27},
        ["Place a CHARGE on this spell.", "-", "Spend this CHARGE to boost the attack power of any spell by 1."] ],
    ["Forest Fire",
        {'element': 'fire', 'category': 'attack,terrain', 'id': 29},
        ["Attack for 2 all locations in a Forest with a EYE you control."] ],
    ["Boulder Tumble",
        {'element': 'fire', 'category': 'attack,terrain', 'id': 28},
        ["Attack for 3 all neighboring locations to a EYE you control that is in a Mountain location."] ],
    ["Wall of Flame",
        {'element': 'fire', 'category': 'attack', 'id': 25},
        ["Place CHARGE on this spell.", "-", "While CHARGEd, all groups of 3 adjacent EYEs you control are on fire and cause 1 damage.", "-", "CHARGE is lost immediately when you do not have 3 adjacent EYEs."] ],
    ["Shield Pierce",
        {'element': 'air', 'category': 'attack', 'id': 21},
        ["Cause 3 points of damage to all shields at a EYE you control."] ],
    ["Meteor Shower",
        {'element': 'earth', 'category': 'attack-charge', 'id': 84},
        {
            'cast': "Remove all CHARGEs from all mages at one of your EYEs.",
        } ],

    # Defend HP

    ["Stone Reflection",
        {'element': 'earth', 'category': 'defend-mage,attack-mage', 'id': 88, 'pattern': 'E2-4'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "You take 1/2 damage (rounded down) from attacks. Full attack damage is reflected back at your attacker.",
        } ],
    ["Double Shield",
        {'element': 'earth', 'category': 'defend-mage', 'id': 36, 'pattern': 'E2-13'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "Defend 2.",
        } ],
    ["Eye Coil",
        {'element': 'water', 'category': 'defend-mage', 'id': 81, 'pattern': 'E2-22'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "If you are in the same location as one of your EYEs, that EYE acts as a shield to Defend 2.",
        } ],
    ["Deflect",
        {'element': 'water', 'category': 'defend-mage,attack-mage,attack-eye', 'id': 80, 'pattern': 'E2-25'},
        {
            'cast': "{{ADD_CHARGE}}",
            'sacrifice': "When attacked, you may remove this CHARGE to deflect the attack to an adjacent location. Attack 1 and remove all EYEs at that location.",
        } ],    
    ["Shield Boost",
        {'element': 'earth', 'category': 'defend', 'id': 37},
        ["Place a CHARGE on this spell.", "-", "Spend this CHARGE to boost the defense power of any spell by 1."] ],
    ["Reactive Shield",
        {'element': 'earth', 'category': 'defend', 'id': 38},
        ["Place a CHARGE on this spell.", "-", "When in the same location as a EYE controlled by another mage, this shield absorbs all damage from attacks.", "-", "Remove CHARGE when it takes 3 or more damage from a single attack."] ],
    ["Resist Shield",
        {'element': 'earth', 'category': 'defend,eye', 'id': 40},
        ["Place a CHARGE on this spell.", "-", "When CHARGEd, this shield absorbs all damage from attacks and prevents others from placing new EYEs on your location.", "-", "Remove CHARGE when it takes 1 or more damage from a single attack."] ],
    ["Reflection Shield",
        {'element': 'fire', 'category': 'defend,attack', 'id': 35},
        ["Place 1 charge on this spell.", "-", "Spend a charge at any time to protect against 1 or more points of damage and reflect 1 point of damage back at the attacker."] ],

    # Tapestry

    ["Recover",
        {'element': 'water', 'category': 'tapestry', 'id': 59},
        ["Remove a THREAD from your TAPESTRY and place it back in your MANA POOL."] ],
    ["Stone Cage",
        {'element': 'earth', 'category': 'attack', 'id': 47},
        ["PLace a CHARGE on this spell.", "-", "While CHARGEd, there is a barrier at a EYE you control that traps the occupants of that location and prevents them from moving out.", "-", "CHARGE is lost if the EYE moves or if the barrier takes 1 damage."] ],
    ["Trap",
        {'element': 'earth', 'category': 'attack', 'id': 48},
        ["Place 1 charge on this spell.", "-", "When an opponent's EYE moves into your location, that opponent takes 1 damage and this CHARGE is removed."] ],
    ["Recovery Shield",
        {'element': 'water', 'category': 'defend,tapestry', 'id': 57},
        ["Place a CHARGE on this spell.", "-", "When CHARGEd, this shield absorbs all damage from attacks.", "-", "Remove CHARGE and 2 THREADs from your TAPESTRY when it takes 1 or more damage from a single attack."] ],

    # Charge

    # Thread

    ["Recovery Shield",
        {'element': 'earth', 'category': 'defend-mage,modify-tapestry', 'id': 82, 'pattern': 'E2-39'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "Defend 1",
            'sacrifice': "During your turn, you may choose to remove a CHARGE from this spell to recover 2 mana from your TAPESTRY into your MANA POOL.",
        } ],

    # Terrain

    ["Flood",
        {'element': 'water', 'category': 'terrain', 'id': 56},
        ["Place CHARGE on this spell.", "-", "While CHARGEd, all groups of 2 or more adjacent EYEs you control change all Plains locations to Water up to 3 spaces away from the EYEs.", "-", "CHARGE is lost immediately when you do not have 2 adjacent EYEs."] ],
    ["Growth",
        {'element': 'earth', 'category': 'terrain', 'id': 46},
        ["Place CHARGE on this spell.", "-", "While CHARGEd, all groups of 2 or more adjacent EYEs you control change all neighboring locations to Forest.", "-", "CHARGE is lost immediately when you do not have 2 adjacent EYEs."] ],

    # Astral

    ["Return",
        {'element': 'none', 'category': 'astral', 'id': 2},
        ["When in the Astral Plane, return to the Physical Realm at a EYE you control or at your home location."] ],
    ["Teleport Away",
        {'element': 'water', 'category': 'astral', 'id': 6},
        ["Move yourself to the Astral Plane."] ],
    ["Teleport Other",
        {'element': 'water', 'category': 'astral', 'id': 49},
        ["Move a mage in the same location as a EYE you control to the Astral Plane."] ],
    ["Return Other",
        {'element': 'water', 'category': 'astral', 'id': 50},
        ["Move a mage in the Astral Plane to any EYE you control."] ],


]
