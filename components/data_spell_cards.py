# Spell fragment card data

# Text -> ASCII Art: http://patorjk.com/software/taag/#p=display&f=Rectangles&t=Monster

spell_card_revision = 7

spell_card_categories = [
    'blank',
    'starter',

    #'attack-charge',
    #'attack-tapestry',

    'eye-create',
    'eye-move',
    'eye-defend',  # Protect eyes from being destroyed
    'eye-other-attack',
    'eye-other-move',

    'defend-charge',
    'defend-tapestry',

    'mage-move',
    #'mage-move-astral',
    'mage-defend',  # Shields to prevent HP damage
    'mage-defend-move',  # Prevent mage from being moved
    'mage-other-move',
    'mage-other-attack',  # Damage mage HP

    'tapestry-thread',
    
    #'modify-tapestry',
    #'add-action',
    'terrain',
]

valid_ops = [
    'tapestry',       # Draw tapestry card
    'tapestry-eye',   # Draw tapestry card OR Create eye
    'tapestry-move',  # Draw tapestry card OR Move mage
    'tapestry-thread',# Draw tapestry card OR Recover thread
    'eye',            # Create eye
    'eye-move',       # Create eye OR Move mage
    'eye-thread',     # Create eye OR Recover thread
    'move',           # Move mage
    'move-thread',    # Move mage OR Recover thread
    'thread',         # Recover thread
]

# Core abilities:
# * Map
#   * Move Self
#   * Create eye (in current location)
# * Tapestry
#   * Recover thread (= mental rest to recover)
#   * Gain Tapestry card (= focus on spell casting - new patterns)
# * Spell deck
#   * Trash spell card (= focus spell deck - reduce spells)
#   * Interaction with Spell deck

# Element opposites
#   Air <-> Earth
#   Fire <-> Water

# Spell affinity
#                         Air          Fire          Earth         Water
#                   +-------------+-------------+-------------+-------------+
# Move Self              + + +           +            + +            +
# Move Other              + +            +           + + +          + +
# Defend Move Self
#
# Create Eye              + +            +             +           + + +
# Move Eye                + +           + +            +           + + +
# Move Other Eye
# Defend Move Eye
# Attack Eye               +           + + +          + +            +
# Defend Eye
#
# Create Anchor            +            + +          + + +           +
# Attack Anchor
# Defend Anchor
#
# Attack HP                +           + + +          + +           + +
# Defend HP               + +            +           + + +          + +
# Recover HP              + +            +            + +          + + +
#
# Tapestry                                                         + + +
# Other Tapestry
# Defend Tapestry
#
# Spell
# Other Spell
#
# Astral

# TODO:
# Triggers - spell effects for current turn
#   On <trigger>, do X
#   On push mage into another location, do cause 1 damage
#   On enter location with mage, do push mage out
# Reactions - spell effects in response to another mage's spell
#   If attacked, cast spell to deflect
#   If eye moves onto you, cast spell to dispel, reflect, push away
#   If eye moves next to you, do X

# Data Format:
#   spell_card_data:
#     List of <card>s
#
#   <card>:
#     <title>, <attributes>, <info>
#
#   <attribute>:
#     'element': 'air', 'fire', 'earth', 'water' or 'none'
#     'pattern': name of pattern
#     'op': alternate action at bottom of card
#     'id': spell id
#     'category': <string> to group spells by general category
#     'flavor': flavor text for spell
#
#   <info>:
#     'cast': Description when spell is cast.
#     'charged': Description when spell is charged.
#     'notes': Additional notes
#     'sacrifice': Description when charge is sacrificed.

# Next id = 103
# Unused = 41

spell_card_data = [

    #     _____         _           _ 
    #    |   | |___ _ _| |_ ___ ___| |
    #    | | | | -_| | |  _|  _| .'| |
    #    |_|___|___|___|_| |_| |__,|_|
    #
    # Neutral spells are basic spells that are always worse than corresponding
    # elemental spells.
    
    #     _____ _           _           
    #    |   __| |_ ___ ___| |_ ___ ___ 
    #    |__   |  _| .'|  _|  _| -_|  _|
    #    |_____|_| |__,|_| |_| |___|_|  
    #
    # Representative spells for each element.

    # Doubled by Blur
    ["Haste",
        {'element': 'air', 'pattern': 'E1-1', 'op': 'eye', 'vp': 0, 'cost': 0,
         'id': 3, 'category': 'starter,mage-move'},
        {
            'cast': "Move 4",
        } ],

    ["Endurance",
        {'element': 'earth', 'pattern': 'E1-1', 'op': 'tapestry-eye', 'vp': 0, 'cost': 0,
         'id': 45, 'category': 'starter,terrain,mage-move'},
        {
            'cast': "While this spell is active, you may ignore the movement penalty for rough terrain or changing elevation.",
        } ],

    ["Fire Shards",
        {'element': 'fire', 'pattern': 'E1-2', 'op': 'eye-thread', 'vp': 0, 'cost': 0,
         'id': 22, 'category': 'starter,mage-other-attack'},
        {
            'cast': "Consume one of your Eyes to Attack 1 at that location.",
        } ],

    ["Spread",
        {'element': 'water', 'pattern': 'E1-2', 'op': 'eye-move', 'vp': 0, 'cost': 0,
         'id': 75, 'category': 'starter,eye-move'},
        {
            'cast': "Move all your Eyes 2 spaces.",
        } ],

    #     _____                _____     _ ___ 
    #    |     |___ _ _ ___   |   __|___| |  _|
    #    | | | | . | | | -_|  |__   | -_| |  _|
    #    |_|_|_|___|\_/|___|  |_____|___|_|_|
    #
    # Move mage

    ["Stone Hand",
        {'element': 'earth', 'pattern': 'E2-6', 'op': 'eye-thread', 'vp': 1, 'cost': 1,
         'id': 20, 'category': 'mage-move,mage-other-move'},
        {
            'cast': "Move into an adjacent location without crossing water. If there were any mages in that location, push them out into an adjacent location.",
            'notes': "If there are multiple mages, they can be pushed into different locations."
        } ],

    ["Bridge",
        {'element': 'earth', 'pattern': 'E1-3', 'op': 'thread', 'vp': 1, 'cost': 1,
         'id': 99, 'category': 'terrain,mage-move',
         'flavor': "Rising columns of mud form a temporary bridge."},
        {
            'cast': "Cross over a river into an adjacent space, ignoring the terrain cost.",
        } ],

    ["Blur",
        {'element': 'air', 'pattern': 'E2-1', 'op': 'eye', 'vp': 2, 'cost': 2,
         'id': 19, 'category': 'mage-move'},
        {
            'cast': "Move 8",
        } ],

    ["Forest Blink",
        {'element': 'air', 'pattern': 'E2-14', 'op': 'eye-thread', 'vp': 1, 'cost': 1,
         'id': 11, 'category': 'terrain,mage-move'},
        {
            'cast': "If you are in a forest location, you may jump to any connected forest location, ignoring any terrain costs.",
        } ],

    ["Dark Passage",
        {'element': 'air', 'pattern': 'E2-9', 'op': 'thread', 'vp': 1, 'cost': 1,
         'id': 93, 'category': 'terrain,mage-move'},
        {
            'cast': "If in a Dense Forest location, jump to another Dense Forest location no more than 5 spaces away.",
        } ],

    ["Dodge",
        {'element': 'air', 'pattern': 'E2-86', 'op': 'eye-thread', 'vp': 1, 'cost': 1,
         'id': 102, 'category': 'mage-move'},
        {
            'cast': "Move 6",
            'react': "When attacked, cast to move into adjacent (by land) location.",
        } ],

    #     _____                _____ _   _           
    #    |     |___ _ _ ___   |     | |_| |_ ___ ___ 
    #    | | | | . | | | -_|  |  |  |  _|   | -_|  _|
    #    |_|_|_|___|\_/|___|  |_____|_| |_|_|___|_|
    #
    # Attack by moving another player's mage
    
    #     ____      ___           _    _____                _____     _ ___ 
    #    |    \ ___|  _|___ ___ _| |  |     |___ _ _ ___   |   __|___| |  _|
    #    |  |  | -_|  _| -_|   | . |  | | | | . | | | -_|  |__   | -_| |  _|
    #    |____/|___|_| |___|_|_|___|  |_|_|_|___|\_/|___|  |_____|___|_|_|
    #
    # Defend against being moved by another mage

    #     _____             _          _____         
    #    |     |___ ___ ___| |_ ___   |   __|_ _ ___ 
    #    |   --|  _| -_| .'|  _| -_|  |   __| | | -_|
    #    |_____|_| |___|__,|_| |___|  |_____|_  |___|
    #                                       |___|
    #
    # Convert mana into an Eye on the map

    ["Duplicate",
        {'element': 'water', 'pattern': 'E2-35', 'op': 'eye-move', 'vp': 1, 'cost': 1,
         'id': 8, 'category': 'eye-create'},
        {
            'cast': "In a location where you have at least one Eye, split each of your Eyes into two separate Eyes.",
        } ],

    ["Traceback",
        {'element': 'water', 'pattern': 'E2-32', 'op': 'eye-move', 'vp': 1, 'cost': 1,
         'id': 79, 'category': 'eye-create'},
        {
            'cast': "If in a location with another mage's Eye, you may place an Eye at that Mage's location.",
            'react': "You may cast this when an opponent's Eye is moved into your location.",
        } ],
    
    #     _____                _____         
    #    |     |___ _ _ ___   |   __|_ _ ___ 
    #    | | | | . | | | -_|  |   __| | | -_|
    #    |_|_|_|___|\_/|___|  |_____|_  |___|
    #                               |___|
    #
    # Move your Eyes on the map
    
    ["Gust",
        {'element': 'air', 'pattern': 'E1-3', 'op': 'move', 'vp': 1, 'cost': 1,
         'id': 90, 'category': 'eye-move'},
        {
            'cast': "Move your Eyes 4 spaces, split among any number of Eyes.",
        } ],
    
    ["Expand",
        {'element': 'water', 'pattern': 'E2-27', 'op': 'move', 'vp': 2, 'cost': 2,
         'id': 73, 'category': 'eye-create,eye-move'},
        {
            'cast': "Duplicate an existing Eye and then move it 4 spaces.",
        } ],

    ["Burst",
        {'element': 'water', 'pattern': 'E2-47', 'op': 'move', 'vp': 1, 'cost': 1,
         'id': 67, 'category': 'eye-create,eye-move'},
        {
            'cast': "Move all your Eyes 4 spaces each.",
        } ],

    ["Bolt",
        {'element': 'fire', 'pattern': 'E2-79', 'op': 'move', 'vp': 1, 'cost': 1,
         'id': 30, 'category': 'eye-move'},
        {
            'cast': "Move a single Eye 4 spaces.",
        } ],

    #     _____                _____ _   _              _____         
    #    |     |___ _ _ ___   |     | |_| |_ ___ ___   |   __|_ _ ___ 
    #    | | | | . | | | -_|  |  |  |  _|   | -_|  _|  |   __| | | -_|
    #    |_|_|_|___|\_/|___|  |_____|_| |_|_|___|_|    |_____|_  |___|
    #                                                        |___|
    #
    # Move an opponent's Eye

    ["Unbind",
        {'element': 'earth', 'pattern': 'E2-1', 'op': 'tapestry-eye', 'vp': 1, 'cost': 1,
         'id': 42, 'category': 'eye-other-attack'},
        {
            'cast': "Remove all Anchors from your location. Move all Eyes in your location 3 spaces in any valid direction.",
        } ],

    #     ____      ___           _    _____                _____         
    #    |    \ ___|  _|___ ___ _| |  |     |___ _ _ ___   |   __|_ _ ___ 
    #    |  |  | -_|  _| -_|   | . |  | | | | . | | | -_|  |   __| | | -_|
    #    |____/|___|_| |___|_|_|___|  |_|_|_|___|\_/|___|  |_____|_  |___|
    #                                                            |___|
    #
    # Defend against an opponent moving your Eyes
    
    ["Anchor",
        {'element': 'earth', 'pattern': 'E2-14', 'op': 'thread', 'vp': 2, 'cost': 2,
         'id': 97, 'category': 'eye-defend'},
        {
            'cast': "Convert an Eye into an Anchor. Any other Eyes in that location are removed. Any Eyes adjacent to the Anchor must be moved 1 space away.",
            'notes': "No Eyes are allowed adjacent to an Anchor.",
            # "You may remove this Anchor at any time on your turn.",
        } ],

    #     _____ _   _           _      _____         
    #    |  _  | |_| |_ ___ ___| |_   |   __|_ _ ___ 
    #    |     |  _|  _| .'|  _| '_|  |   __| | | -_|
    #    |__|__|_| |_| |__,|___|_,_|  |_____|_  |___|
    #                                       |___|
    #
    # Remove an opponent's Eye

    ["Dispel",
        {'element': 'fire', 'pattern': 'E2-36', 'op': 'tapestry-eye', 'vp': 1, 'cost': 1,
         'id': 92, 'category': 'eye-other-attack'},
        {
            'cast': "Consume one of your Eyes to remove all Eyes at that location.",
        } ],

    ["Scorch",
        {'element': 'fire', 'pattern': 'E2-31', 'op': 'eye-thread', 'vp': 1, 'cost': 1,
         'id': 65, 'category': 'eye-move,eye-other-attack'},
        {
            'cast': "Move one of your Eyes 3 spaces, removing one opponent Eye from each location it moves into this turn. Consume this Eye.",
        } ],

    #     ____      ___           _    _____         
    #    |    \ ___|  _|___ ___ _| |  |   __|_ _ ___ 
    #    |  |  | -_|  _| -_|   | . |  |   __| | | -_|
    #    |____/|___|_| |___|_|_|___|  |_____|_  |___|
    #                                       |___|
    #
    # Defend against an opponent removing one of your eyes

    #     _____ _   _           _        _____ _____ 
    #    |  _  | |_| |_ ___ ___| |_     |  |  |  _  |
    #    |     |  _|  _| .'|  _| '_|    |     |   __|
    #    |__|__|_| |_| |__,|___|_,_|    |__|__|__|
    #
    # Attack another mage

    ["Fiery Fire Flame",
        {'element': 'fire', 'pattern': 'E2-35', 'op': 'eye', 'vp': 2, 'cost': 2,
         'id': 24, 'category': 'mage-other-attack'},
        {
            'cast': "Consume one of your Eyes to Attack 1 at location adjacent to that Eye.",
        } ],

    ["Redirect",
        {'element': 'fire', 'pattern': 'E2-106', 'op': 'eye-move', 'vp': 1, 'cost': 1,
         'id': 101, 'category': 'mage-other-attack'},
        {
            'cast': "Attack 1 at one of your Eyes.",
            'react': "When attacked, cast to redirect the attack to one of your Eyes.",
            'notes': "Cannot be cast if you have no Eyes.",
        } ],

    #     ____      ___           _      _____ _____ 
    #    |    \ ___|  _|___ ___ _| |    |  |  |  _  |
    #    |  |  | -_|  _| -_|   | . |    |     |   __|
    #    |____/|___|_| |___|_|_|___|    |__|__|__|
    #
    # Defend against being attacked

    ["Shield",
        {'element': 'earth', 'pattern': 'E2-15', 'op': 'eye-move', 'vp': 1, 'cost': 1,
         'id': 36, 'category': 'mage-defend'},
        {
            'cast': "{{ADD_CHARGE}}",
            'sacrifice': "Remove a charge to deflect an attack of 1 damage.",
        } ],

    ["Deflect",
        {'element': 'earth', 'pattern': 'E2-7', 'op': 'tapestry-eye', 'vp': 1, 'cost': 1,
         'id': 100, 'category': 'mage-defend'},
        {
            'cast': "Deflect an attack of 1",
            'react': "When attacked, cast to deflect attack.",
        } ],

    #     _____                 _           
    #    |_   _|___ ___ ___ ___| |_ ___ _ _ 
    #      | | | .'| . | -_|_ -|  _|  _| | |
    #      |_| |__,|  _|___|___|_| |_| |_  |
    #              |_|                 |___|
    #
    # Tapestry modification
    # Spell: Remove thread from tapestry. Take another action.

    #     _____ _   _              _____                 _           
    #    |     | |_| |_ ___ ___   |_   _|___ ___ ___ ___| |_ ___ _ _ 
    #    |  |  |  _|   | -_|  _|    | | | .'| . | -_|_ -|  _|  _| | |
    #    |_____|_| |_|_|___|_|      |_| |__,|  _|___|___|_| |_| |_  |
    #                                       |_|                 |___|
    # Attack an opponent's tapestry
    # Spell: Attack tapestry, cover a spot in another mage's tapestry.

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
    # Copy effect of another's spell

    # Blank card (for TTS)
    #["???",
    #    {'element': 'none', 'pattern': 'blank',
    #      'id': 0, 'category': 'blank'},
    #    {
    #        'cast': "???",
    #    } ],

]
