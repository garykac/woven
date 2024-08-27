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
#  * Cards - min-cards: max-overlap
#      min number of cards to create pattern for single cast
#      max card overlap (using min # of cards)
#  * Transform - max-cast: max-threads/max-cards
#      max-cast: max times this spell can be repeated when centered on the element,
#         rotating and mirroring as required
#      max-threads: number of threads to cast max times
#      max-cards: min number of cards to cast max times


# Element pattern affinity

# Air / Earth
# +-----+  +-------+  +---------+               . . . c . . .
# | @ X |  | @ . X |  | @ . . X |               . . . b . . .
# +-----+  +-------+  +---------+               . . . a . . .
# base     long base  long long base            c b a @ a b c
#                                               . . . a . . .
#                                               . . . b . . .
#                                               . . . c . . .

# Fire / Water 
# +-----+  +-------+  +---------+               c . . . . . c
# | @ . |  | @ . . |  | @ . . . |               . b . . . b .
# | . X |  | . . . |  | . . . . |               . . a . a . .
# +-----+  | . . X |  | . . . . |               . . . @ . . .
#          +-------+  | . . . X |               . . a . a . .
#                     +---------+               . b . . . b .
# base     long base  long long base            c . . . . . c

# Knight's move - Neutral - All elements
# +-------+                                     . . . . . . .
# | @ . . |                                     . . * . * . .
# | . . X |                                     . * . . . * .
# +-------+                                     . . . @ . . .
#                                               . * . . . * .
#                                               . . * . * . .
#                                               . . . . . . .

# Long knight's move - weak Air / Earth
# +---------+                                   . . a . a . .
# | @ . . . |                                   . . . . . . .
# | . . . X |                                   a . . . . . a
# +---------+                                   . . . @ . . .
#                                               a . . . . . a
#                                               . . . . . . .
#                                               . . a . a . .

# Long, wide knight's move - weak Fire / Water
# +---------+                                   . f . . . f .
# | @ . . . |                                   f . . . . . f
# | . . . . |                                   . . . . . . .
# | . . . X |                                   . . . @ . . .
# +---------+                                   . . . . . . .
#                                               f . . . . . f
#                                               . f . . . f .

# Summary:
# +---------------+   A = Air/Earth
# | F f a A a f F |   a = weak Air/Earth
# | f F * A * F f |
# | a * F A F * a |   F = Fire/Water
# | A A A @ A A A |   f = weak Fire/Water
# | a * F A F * a |
# | f F * A * F f |   * = Neutral
# | F f a A a f F |
# +---------------+

# Spell pattern for Elements

# Air
# ---------
# Base: E1-1
# Doubled: E2-1, E2-2
# Extended: E2-5, E2-6, E2-7
# Long extended: E2-14, E2-15, E2-16
# Weak long extended:  E2-17, E2-18, E2-19, E2-20
# Neutral extended: E2-8, E2-9, E2-10, E2-11

# Long base: E1-3
# Base boosted: E2-5, E2-6, E2-7
# Doubled: E2-51, E2-52
# Extended: E2-59, E2-60, E2-61
# Weak extended: E2-62, E2-63, E2-64, E2-65
# Neutral extended: E2-53, E2-54, E2-55, E2-56

# Long long base: E1-6
# Base boosted: E2-14, *E2-15, E2-16
# Extension boosted: E2-59, E2-60, E2-61
# Doubled: E2-121, E2-122
# Weak extended: E2-123, E2-124, E2-125, E2-126
# Neutral extended: E2-82, E2-83, E2-84, E2-85

# Earth
# ---------
# Base: E1-1
# Doubled: E2-1, E2-2
# Extended: E2-5, E2-6, E2-7
# Long extended: E2-14, E2-15, E2-16
# Weak long extended:  E2-17, E2-18, E2-19, E2-20
# Neutral extended: E2-8, E2-9, E2-10, E2-11

# Long base: E1-3
# Base boosted: E2-5, E2-6, E2-7
# Doubled: E2-51, E2-52
# Extended: E2-59, E2-60, E2-61
# Weak extended: E2-62, E2-63, E2-64, E2-65
# Neutral extended: E2-53, E2-54, E2-55, E2-56

# Long long base: E1-6
# Base boosted: E2-14, E2-15, E2-16
# Extension boosted: E2-59, E2-60, E2-61
# Doubled: E2-121, E2-122
# Weak extended: E2-123, E2-124, E2-125, E2-126
# Neutral extended: E2-82, E2-83, E2-84, E2-85

# Fire
# ----------
# Base: E1-2
# Doubled: E2-27, E2-28]
# Extended: E2-35, E2-36, E2-37
# Long extended: E2-48, E2-49, E2-50
# Weak long extended: E2-44, E2-45, E2-46, E2-47
# Neutral extended: E2-31, E2-32, E2-33, E2-34

# Long base: E1-5
# Base boosted: E2-35, E2-36, E2-37
# Doubled: E2-106, E2-107
# Extended: E2-118, E2-119, E2-120
# Weak extended: E2-114, E2-115, E2-116, E2-117
# Neutral extended: E2-78, E2-79, E2-80, E2-81

# Long long base: E1-9
# Base boosted: E2-48, E2-49, E2-50
# Extension boosted: E2-118, E2-119, E2-120
# Doubled: E2-163, E2-164
# Weak extended: E2-159, E2-160, E2-161, E2-162
# Neutral extended: E2-102, E1-103, E2-104, E2-105

# Water
# ----------
# Base: E1-2
# Doubled: E2-27, E2-28
# Extended: E2-35, E2-36, E2-37
# Long extended: E2-48, E2-49, E2-50
# Weak long extended: E2-44, E2-45, E2-46, E2-47
# Neutral extended: E2-31, E2-32, E2-33, E2-34

# Long base: E1-5
# Base boosted: E2-35, E2-36, E2-37
# Doubled: E2-106, E2-107
# Extended: E2-118, E2-119, E2-120
# Weak extended: E2-114, E2-115, E2-116, E2-117
# Neutral extended: E2-78, E2-79, E2-80, E2-81

# Long long base: E1-9
# Base boosted: E2-48, E2-49, E2-50
# Extension boosted: E2-118, E2-119, E2-120
# Doubled: E2-163, E2-164
# Weak extended: E2-159, E2-160, E2-161, E2-162
# Neutral extended: E2-102, E1-103, E2-104, E2-105

from data_spell_patterns_n2 import spell_patterns_n2
from data_spell_patterns_n3 import spell_patterns_n3
from data_spell_patterns_e1 import spell_patterns_e1
from data_spell_patterns_e2 import spell_patterns_e2
from data_spell_patterns_e3 import spell_patterns_e3
from data_spell_patterns_ee1 import spell_patterns_ee1
from data_spell_patterns_ee2 import spell_patterns_ee2
from data_spell_patterns_ee3 import spell_patterns_ee3
from data_spell_patterns_eee1 import spell_patterns_eee1

spell_card_patterns = {

    'blank':    {'elements': 'none',
                 'pattern': [   ". . . . .",
                                ". . . . .",
                                ". . . . .",   ]},

    #  _____         _           _    ___   
    # |   | |___ _ _| |_ ___ ___| |  |_  |  
    # | | | | -_| | |  _|  _| .'| |   _| |_ 
    # |_|___|___|___|_| |_| |__,|_|  |_____|
    #

    # +---+
    # | X |  Level 0 - Castable on all starting cards.
    # +---+
    'N1':       {'elements': 'none',
                 'pattern': [   "X",   ]},

    #  _____ _                   _       _    ___      _      ___ 
    # |   __| |___ _____ ___ ___| |_ ___| |  |_  |   _| |_   |_  |
    # |   __| | -_|     | -_|   |  _| .'| |  |_  |  |_   _|  |  _|
    # |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |___|    |_|    |___|
    #

    #  _____ _                   _       _    ___      _      ___ 
    # |   __| |___ _____ ___ ___| |_ ___| |  |_  |   _| |_   |_  |
    # |   __| | -_|     | -_|   |  _| .'| |  |_  |  |_   _|  |_  |
    # |_____|_|___|_|_|_|___|_|_|_| |__,|_|  |___|    |_|    |___|
    #


}

# Neutral (no element) spells
spell_card_patterns.update(spell_patterns_n2)
spell_card_patterns.update(spell_patterns_n3)

# Single Elemental spells (with 1-3 threads)
spell_card_patterns.update(spell_patterns_e1)
spell_card_patterns.update(spell_patterns_e2)
spell_card_patterns.update(spell_patterns_e3)

# Double Elemental spells (with 1-3 threads)
spell_card_patterns.update(spell_patterns_ee1)
spell_card_patterns.update(spell_patterns_ee2)
spell_card_patterns.update(spell_patterns_ee3)

# Triple Elemental spells (with 1-3 threads)
spell_card_patterns.update(spell_patterns_eee1)
