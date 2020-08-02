# Spell fragment card data

# Text -> ASCII Art: http://patorjk.com/software/taag/#p=display&f=Rectangles&t=Monster

spell_card_revision = 7

spell_card_categories = [
    'blank',
    'starter',

    'attack-charge',
    'attack-tapestry',

    'eye-create',
    'eye-move',
    'eye-defend',  # Protect eyes from being destroyed
    'eye-other-attack',
    'eye-other-move',

    'defend-charge',
    'defend-tapestry',

    'mage-move',
    #'mage-move-astral',
    'mage-anchor',  # Prevent mage from being moved
    'mage-defend',  # Shields to prevent HP damage
    'mage-other-move',
    'mage-other-attack',  # Damage mage HP

    'tapestry-thread',
    
    #'modify-tapestry',
    #'add-action',
    'terrain',
]

valid_ops = [
    'eye',            # Create eye
    'move',           # Move mage
    'move-eye',       # Move mage OR Create eye
    'tapestry-eye',   # Draw tapestry card OR Create eye
    'thread',         # Recover thread
]

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
#     <title>, <attributes>, <info>
#
#   <attribute>:
#     'element': 'air', 'fire', 'earth', 'water' or 'none'
#     'pattern': name of pattern
#     'op': alternate action at bottom of card
#     'id': spell id
#     'category': <string> to group spells by general category
#
#   <info>:
#     'cast': Description when spell is cast.
#     'charged': Description when spell is charged.
#     'comment': Additional comment (not shown on spell).
#     'notes': Additional notes
#     'sacrifice': Description when charge is sacrificed.

# Next id = 98
# Unused = 41

spell_card_data = [

    #     _____         _           _ 
    #    |   | |___ _ _| |_ ___ ___| |
    #    | | | | -_| | |  _|  _| .'| |
    #    |_|___|___|___|_| |_| |__,|_|
    #
    # Neutral spells are basic spells that are always worse than corresponding elemental spells.
    
    #     _____ _           _           
    #    |   __| |_ ___ ___| |_ ___ ___ 
    #    |__   |  _| .'|  _|  _| -_|  _|
    #    |_____|_| |__,|_| |_| |___|_|  
    #
    # Representative spell for each element.

    ["Haste",
        {'element': 'air', 'pattern': 'E1-4', 'op': 'eye',
         'id': 3, 'category': 'starter,mage-move'},
        {
            'cast': "Move 4mp.",
        } ],

    ["Dispel",
        {'element': 'fire', 'pattern': 'E1-5', 'op': 'tapestry-eye',
         'id': 92, 'category': 'starter,eye-other-attack'},
        {
            'cast': "Consume one of your Eyes to remove all Eyes at that location.",
        } ],

    ["Creep",
        {'element': 'water', 'pattern': 'E1-4', 'op': 'move',
         'id': 73, 'category': 'starter,eye-create,eye-move'},
        {
            'cast': "Place a Eye. Move one of your Eyes 2 spaces.",
        } ],

    #     _____                _____     _ ___ 
    #    |     |___ _ _ ___   |   __|___| |  _|
    #    | | | | . | | | -_|  |__   | -_| |  _|
    #    |_|_|_|___|\_/|___|  |_____|___|_|_|
    #
    # Move mage

    #     _____                _____ _   _           
    #    |     |___ _ _ ___   |     | |_| |_ ___ ___ 
    #    | | | | . | | | -_|  |  |  |  _|   | -_|  _|
    #    |_|_|_|___|\_/|___|  |_____|_| |_|_|___|_|
    #
    # Attack by moving another player's mage
    
    ["Bellor's Giant Hand",
        {'element': 'air', 'pattern': 'E2-5', 'op': 'eye',
         'id': 20, 'category': 'starter,mage-move,mage-other-move'},
        {
            'cast': "Push all mages out of an adjacent location and then move into that location (ignoring terrain cost). You choose which location each mage moves into.",
            'notes': "If there are multiple mages, they can be pushed into different locations."
        } ],

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

    ["Reduplication",
        {'element': 'water', 'pattern': 'E2-35', 'op': 'move-eye',
         'id': 8, 'category': 'starter,eye-create'},
        {
            'cast': "Place a new Eye in a location where you already have a Eye.",
        } ],

    #     _____                _____         
    #    |     |___ _ _ ___   |   __|_ _ ___ 
    #    | | | | . | | | -_|  |   __| | | -_|
    #    |_|_|_|___|\_/|___|  |_____|_  |___|
    #                               |___|
    #
    # Move your Eyes on the map
    
    ["Spread",
        {'element': 'water', 'pattern': 'E2-28', 'op': 'move',
         'id': 75, 'category': 'starter,eye-move'},
        {
            'cast': "Move up to 3 different Eyes 1 space each.",
        } ],

    #     _____                _____ _   _              _____         
    #    |     |___ _ _ ___   |     | |_| |_ ___ ___   |   __|_ _ ___ 
    #    | | | | . | | | -_|  |  |  |  _|   | -_|  _|  |   __| | | -_|
    #    |_|_|_|___|\_/|___|  |_____|_| |_|_|___|_|    |_____|_  |___|
    #                                                        |___|
    #
    # Move an opponent's Eye

    ["Disperse Magic",
        {'element': 'earth', 'pattern': 'E2-41', 'op': 'thread',
         'id': 42, 'category': 'eye-other-attack'},
        {
            'cast': "Move all Eyes in your location one space in any direction. If there is an Anchored Eye in your location, it is un-Anchored before being moved.",
        } ],

    #     ____      ___           _    _____                _____         
    #    |    \ ___|  _|___ ___ _| |  |     |___ _ _ ___   |   __|_ _ ___ 
    #    |  |  | -_|  _| -_|   | . |  | | | | . | | | -_|  |   __| | | -_|
    #    |____/|___|_| |___|_|_|___|  |_|_|_|___|\_/|___|  |_____|_  |___|
    #                                                            |___|
    #
    # Defend against an opponent moving your Eyes
    
    ["Anchor",
        {'element': 'earth', 'pattern': 'E2-14', 'op': 'thread',
         'id': 97, 'category': 'starter,eye-defend'},
        {
            'cast': "Anchor one of your Eyes in its current location. Any other Eyes in that location, they are removed. Any Eyes adjacent to this Eye must be moved 1 space away.",
            'notes': "While anchored, this Eye may not be moved and no Eyes may enter an adjacent location.",
            'comment': "This Eye can be un-Anchored at any time during your turn.",
        } ],

    #     _____ _   _           _      _____         
    #    |  _  | |_| |_ ___ ___| |_   |   __|_ _ ___ 
    #    |     |  _|  _| .'|  _| '_|  |   __| | | -_|
    #    |__|__|_| |_| |__,|___|_,_|  |_____|_  |___|
    #                                       |___|
    #
    # Remove an opponent's Eye

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

    ["Shards of Fire",
        {'element': 'fire', 'pattern': 'E2-34', 'op': 'thread',
         'id': 22, 'category': 'starter,mage-other-attack'},
        {
            'cast': "Attack for 1 damage all creatures at one of your Eyes. Consume that Eye.",
        } ],

    #     ____      ___           _      _____ _____ 
    #    |    \ ___|  _|___ ___ _| |    |  |  |  _  |
    #    |  |  | -_|  _| -_|   | . |    |     |   __|
    #    |____/|___|_| |___|_|_|___|    |__|__|__|
    #
    # Defend against being attacked

    ["Shield",
        {'element': 'earth', 'pattern': 'E2-15', 'op': 'move-eye',
         'id': 36, 'category': 'starter,mage-defend'},
        {
            'cast': "{{ADD_CHARGE}}",
            'sacrifice': "Remove a charge to deflect an attack of 1 damage.",
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

    #     _____     _   _         
    #    |  _  |___| |_|_|___ ___ 
    #    |     |  _|  _| | . |   |
    #    |__|__|___|_| |_|___|_|_|
    #
    # Gain an extra action

    #     _____                 _     
    #    |_   _|___ ___ ___ ___|_|___ 
    #      | | | -_|  _|  _| .'| |   |
    #      |_| |___|_| |_| |__,|_|_|_|


    # Blank card (for TTS)
    #["???",
    #    {'element': 'none', 'pattern': 'blank',
    #      'id': 0, 'category': 'starter'},
    #    {
    #        'cast': "???",
    #    } ],

]
