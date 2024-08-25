spell_patterns_e1 = {

    #  _____ _                   _       _    ___        _      ___   
    # |   __| |___ _____ ___ ___| |_ ___| |  |_  |     _| |_   |_  |  
    # |   __| | -_|     | -_|   |  _| .'| |   _| |_   |_   _|   _| |_ 
    # |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |_____|    |_|    |_____|
    #

    # +-----+  Level 1            Transforms  . 2 .
    # | @ X |  Threads 1                      3 @ 1
    # +-----+  Cards 1                        . 4 .
    #          Transform 4: 4/2
    #
    # Matching element:
    #   This pattern is doubled by E2-1, E2-2
    #   This pattern is extended by E2-5, E2-6, E2-7
    #   This pattern is long extended by E2-14, E2-15, E2-16
    # Weak matching:
    #   This pattern is long extended by E2-17, E2-18, E2-19, E2-20
    # Neutral:
    #   Neutral extension with E2-8, E2-9, E2-10, E2-11
    # Weak opposing:
    #   This pattern is long extended by E2-21, E2-22, E2-23, E2-24
    # Opposing element:
    #   Opposing base with E2-3, E2-4
    #   Opposing extension with E2-12, E2-13
    #   Opposing long extension with E2-25, E2-26
    'E1-1':     {'elements': 'ae',
                 'pattern': [   "@ X",   ]},

    # +-----+  Level 1            Transforms  3 . 2
    # | @ . |  Threads 1                      . @ .
    # | . X |  Cards 1                        4 . 1
    # +-----+  Transform 4: 4/2
    #
    # Matching element:
    #   This pattern is doubled by E2-27, E2-28
    #   This pattern is extended by E2-35, E2-36, E2-37
    #   This pattern is long extended by E2-48, E2-49, E2-50
    # Weak matching:
    #   This pattern is long extended by E2-44, E2-45, E2-46, E2-47
    # Neutral:
    #   Neutral extension with E2-31, E2-32, E2-33, E2-34
    # Weak opposing:
    #   This pattern is long extended by E2-40, E2-41, E2-42, E2-43
    # Opposing element:
    #   Opposing base with E2-3, E2-4
    #   Opposing extension with E2-29, E2-30
    #   Opposing long extension with E2-38, E2-39
    'E1-2':     {'elements': 'fw',
                 'pattern': [   "@ .",
                                ". X",   ]},

    # +-------+  Level 1          Transforms  . . 2 . .
    # | @ . X |  Threads 1                    . . . . .
    # +-------+  Cards 1                      3 . @ . 1
    #            Transform 4: 4/4             . . . . .
    #                                         . . 4 . .
    # Matching element:
    #   This pattern is base boosted by E2-5, E2-6, E2-7
    #   This pattern is doubled by E2-51, E2-52
    #   This pattern is extended by E2-59, E2-60, E2-61
    # Weak matching:
    #   This pattern is extended by E2-62, E2-63, E2-64, E2-65
    # Neutral:
    #   Neutral extension with E2-53, E2-54, E2-55, E2-56
    # Weak opposing:
    #   This pattern is extended by E2-66, E2-67, E2-68, E2-69
    # Opposing element:
    #   Opposing base with E2-29, E2-30
    #   Opposing extension with E2-57, E2-58
    #   Opposing long extension with E2-70, E2-71
    'E1-3':     {'elements': 'ae',
                 'pattern': [    "@ . X",   ]},

    # +-------+  Level 1          Transforms  . 6 . 7 .
    # | @ . . |  Threads 1                    5 . . . 8
    # | . . X |  Cards 1                      . . @ . .
    # +-------+  Transform 8: 8/5             4 . . . 1
    #                                         . 3 . 2 .
    # With Air, Earth:
    #   With A/E base: E2-8, E2-9, E2-10, E2-11
    #   With A/E extension: E2-53, E2-54, E2-55, E2-56
    #   With A/E long extension: E2-82, E2-83, E2-84, E2-85
    # With weak Air, Earth:
    #   Extended by E2-86, E2-87, E2-88, E2-89, E2-90, E2-91, E2-92, E2-93
    # Pure Neutral:
    #   Doubled by E2-72, E2-73, E2-74, E2-75, E2-76, E2-77
    # With weak Fire, Water:
    #   Extended by E2-94, E2-95, E2-96, E2-97, E2-98, E2-99, E2-100, E2-101
    # With Fire, Water:
    #   With F/W base: E2-31, E2-32, E2-33, E2-34
    #   With F/W extension: E2-78, E2-79, E2-80, E2-81
    #   With F/W long extension: E2-102, E1-103, E2-104, E2-105
    'E1-4':     {'elements': 'aefw',
                 'pattern': [   "@ . .",
                                ". . X",   ]},

    # +-------+  Level 2          Transforms  3 . . . 2
    # | @ . . |  Threads 1                    . . . . .
    # | . . . |  Cards 2: 4                   . . @ . .
    # | . . X |  Transform 4: 4/6             . . . . .
    # +-------+                               4 . . . 1
    #
    # Matching element:
    #   This pattern is base boosted by E2-35, E2-36, E2-37
    #   This pattern is doubled by E2-106, E2-107
    #   This pattern is extended by E2-118, E2-119, E2-120
    # Weak matching:
    #   This pattern is extended by E2-114, E2-115, E2-116, E2-117
    # Neutral:
    #   Neutral extension with E2-78, E2-79, E2-80, E2-81
    # Weak opposing:
    #   This pattern is extended by E2-110, E2-111, E2-112, E2-113
    # Opposing element:
    #   Opposing base with E2-12, E2-13
    #   Opposing extension with E2-57, E2-58
    #   Opposing long extension with E2-108, E2-109
    'E1-5':     {'elements': 'fw',
                 'pattern': [   "@ . .",
                                ". . .",
                                ". . X",   ]},

    # +---------+  Level 2        Transforms  . . . 2 . . .
    # | @ . . X |  Threads 1                  . . . . . . .
    # +---------+  Cards 2: 4                 . . . . . . .
    #              Transform 4: 4/6           3 . . @ . . 1
    #                                         . . . . . . .
    #                                         . . . . . . .
    #                                         . . . 4 . . .
    # Matching element:
    #   This pattern is base boosted by E2-14, E2-15, E2-16
    #   This pattern is extension boosted by E2-59, E2-60, E2-61
    #   This pattern is doubled by E2-121, E2-122
    # Weak matching:
    #   This pattern is extended by E2-123, E2-124, E2-125, E2-126
    # Neutral:
    #   Neutral extension with E2-82, E2-83, E2-84, E2-85
    # Weak opposing:
    #   This pattern is extended by E2-127, E2-128, E2-129, E2-130
    # Opposing element:
    #   Opposing base with E2-38, E2-39
    #   Opposing extension with E2-108, E2-109
    #   Opposing long extension with E2-131, E2-132
    'E1-6':     {'elements': 'ae',
                 'pattern': [    "@ . . X",   ]},

    # +---------+  Level 2        Transforms  . . 4 . 3 . .
    # | @ . . . |  Threads 1                  . . . . . . .
    # | . . . X |  Cards 2: 4                 5 . . . . . 2
    # +---------+  Transform 8: 8             . . . @ . . .
    #                                         6 . . . . . 1
    #                                         . . . . . . .
    #                                         . . 7 . 8 . .
    # Matching base element:
    #   Base boost: E2-17, E2-18, E2-19, E2-20
    #   Base extension: E2-62, E2-63, E2-64, E2-65
    #   Base long extension: E2-123, E2-124, E2-125, E2-126
    # Weak matching (self):
    #   Doubled by E2-133, E2-134, E2-135, E2-136, E2-137, E2-138, E2-139
    # Neutral:
    #   Extended by E2-86, E2-87, E2-88, E2-89, E2-90, E2-91, E2-92, E2-93
    # Weak opposing:
    #   Extended by E2-140, E2-141, E2-142, E2-143, E2-144, E2-145, E2-146, E2-147
    # Opposing base element:
    #   Opposing base: E2-40, E2-41, E2-42, E2-43
    #   Opposing extension: E2-110, E2-111, E2-112, E2-113
    #   Opposing long extension: E2-148, E2-149, E2-150, E2-151
    'E1-7':     {'elements': 'ae',
                 'pattern': [   "@ . . .",
                                ". . . X",   ]},

    # +---------+  Level 2        Transforms  . 4 . . . 3 .
    # | @ . . . |  Threads 1                  5 . . . . . 2
    # | . . . . |  Cards 2: 2                 . . . . . . .
    # | . . . X |  Transform 8: 8             . . . @ . . .
    # +---------+                             . . . . . . .
    #                                         6 . . . . . 1
    #                                         . 7 . . . 8 .
    # Matching base element:
    #   Base boost: E2-44, E2-45, E2-46, E2-47
    #   Base extension: E2-114, E2-115, E2-116, E2-117
    #   Base long extension: E2-159, E2-160, E2-161, E2-162
    # Weak matching (self):
    #   Doubled by E2-152, E2-153, E2-154, E2-155, E2-156, E2-157, E2-158
    # Neutral:
    #   Extended by E2-94, E2-95, E2-96, E2-97, E2-98, E2-99, E2-100, E2-101
    # Weak opposing:
    #   Extended by E2-140, E2-141, E2-142, E2-143, E2-144, E2-145, E2-146, E2-147
    # Opposing base element:
    #   Opposing base: E2-21, E2-22, E2-23, E2-24
    #   Opposing extension: E2-66, E2-67, E2-68, E2-69
    #   Opposing long extension: E2-127, E2-128, E2-129, E2-130
    'E1-8':     {'elements': 'fw',
                 'pattern': [   "@ . . .",
                                ". . . .",
                                ". . . X",   ]},

    # +---------+  Level 2        Transforms  3 . . . . . 2
    # | @ . . . |  Threads 1                  . . . . . . .
    # | . . . . |  Cards 2: 1                 . . . . . . .
    # | . . . . |  Transform 4: 4/8           . . . @ . . .
    # | . . . X |                             . . . . . . .
    # +---------+                             . . . . . . .
    #                                         4 . . . . . 1
    # Matching element:
    #   This pattern is base boosted by E2-48, E2-49, E2-50
    #   This pattern is extension boosted by E2-118, E2-119, E2-120
    #   This pattern is doubled by E2-163, E2-164
    # Weak matching:
    #   This pattern is extended by E2-159, E2-160, E2-161, E2-162
    # Neutral:
    #   Neutral extension with E2-102, E1-103, E2-104, E2-105
    # Weak opposing:
    #   This pattern is extended by E2-148, E2-149, E2-150, E2-151
    # Opposing element:
    #   Opposing base with E2-25, E2-26
    #   Opposing extension with E2-70, E2-71
    #   Opposing long extension with E2-131, E2-132
    'E1-9':     {'elements': 'fw',
                 'pattern': [   "@ . . .",
                                ". . . .",
                                ". . . .",
                                ". . . X",   ]},

}
