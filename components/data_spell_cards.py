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
    #'mage-defend',  # Shields to prevent HP damage
    'mage-other-move',
    'mage-other-attack',  # Damage mage HP

    'tapestry-thread',
    
    #'modify-tapestry',
    #'add-action',
    'terrain',
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
#     <title>, <attributes>, List of <description> strings
#
#   <attribute>:
#     'element': 'air', 'fire', 'earth', 'water' or 'none'
#     'category': <string> to group spells by general category
#     'id': spell id
#     'pattern': name of pattern

# Next id = 97
# Unused = 41

spell_card_data = [

    #     _____         _           _ 
    #    |   | |___ _ _| |_ ___ ___| |
    #    | | | | -_| | |  _|  _| .'| |
    #    |_|___|___|___|_| |_| |__,|_|
    #
    # Neutral spells are basic spells that are always worse than corresponding elemental spells.
    
    ["Create Eye",
        {'element': 'none', 'category': 'starter,eye-create', 'id': 89, 'pattern': 'N1'},
        {
            'cast': "Create a EYE in your location.",
        } ],
    ["Move Eye",
        {'element': 'none', 'category': 'starter,eye-move', 'id': 90, 'pattern': 'N2-4'},
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
        {'element': 'air', 'category': 'starter,mage-move', 'id': 3, 'pattern': 'E1-1'},
        {
            'cast': "Move 6mp.",
        } ],
    ["Eye for Eye",
        {'element': 'fire', 'category': 'starter,eye-other-attack', 'id': 92, 'pattern': 'E1-2'},
        {
            'cast': "Remove an opponent's EYE at one of your EYE's location. Consume this EYE.",
        } ],
    ["Eye Protection",
        {'element': 'earth', 'category': 'starter,eye-defend', 'id': 4, 'pattern': 'E1-1'},
        {
            'cast': "{{ADD_CHARGE}}",
            'sacrifice': "Sacrifice a charge to prevent one of your EYEs from being removed.",
        } ],
    ["Creep",
        {'element': 'water', 'category': 'starter,eye-create,eye-move', 'id': 73, 'pattern': 'E1-2'},
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
        {'element': 'air', 'category': 'mage-move,terrain', 'id': 7, 'pattern': 'E2-6'},
        {
            'cast': "Move through 5 contiguous Plains locations.",
        } ],
    ["Forest Run",
        {'element': 'air', 'category': 'terrain,mage-move', 'id': 11, 'pattern': 'E2-14'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "If you start your turn in a Forest location, you may immediately move through up to 5 connected Forest locations.",
        } ],
    ["Forest Jump",
        {'element': 'air', 'category': 'terrain,mage-move', 'id': 93, 'pattern': 'E2-13'},
        {
            'cast': "If in a Forest location, swap positions with one of your EYEs that is in a Forest location no more than 5 spaces away. You may immediately repeat this spell.",
            'notes': "You may only use each EYE once when you cast this spell.",
        } ],
    ["Blur",
        {'element': 'air', 'category': 'mage-move', 'id': 19, 'pattern': 'E2-42'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "Once per turn (per charge), you may move into a neighboring location ignoring terrain cost.",
        } ],
    ["Quick Drop",
        {'element': 'air', 'category': 'mage-move,eye-create', 'id': 66, 'pattern': 'E2-10'},
        {
            'cast': "Move 5mp. Place a EYE in your final location.",
        } ],
    ["Air Walk",
        {'element': 'air', 'category': 'mage-move', 'id': 70, 'pattern': 'E2-11'},
        {
            'cast': "Move up to 4 spaces over the same or lower terrain than your starting position. You must end your move on a space of the same level.",
        } ],

    #     _____                _____ _   _           
    #    |     |___ _ _ ___   |     | |_| |_ ___ ___ 
    #    | | | | . | | | -_|  |  |  |  _|   | -_|  _|
    #    |_|_|_|___|\_/|___|  |_____|_| |_|_|___|_|
    #
    # Attack by moving another player's mage
                                                                         
    ["Push",
        {'element': 'air', 'category': 'mage-move,mage-other-move', 'id': 20, 'pattern': 'E2-5'},
        {
            'cast': "Push all mages out of an adjacent location and then move into that location. You choose which location each mage moves into.",
            'notes': "If there are multiple mages, they can be pushed into different locations."
        } ],
    ["Barrier",
        {'element': 'earth', 'category': 'mage-other-move', 'id': 87, 'pattern': 'E2-10'},
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

    ["Stance",
        {'element': 'earth', 'category': 'mage-anchor', 'id': 39, 'pattern': 'E2-16'},
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
        {'element': 'water', 'category': 'eye-create', 'id': 8, 'pattern': 'E2-27'},
        {
            'cast': "Place a new EYE in a location where you already have a EYE.",
        } ],
    ["Mountain Eye",
        {'element': 'earth', 'category': 'terrain,eye-create', 'id': 12, 'pattern': 'E2-11'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "If in or next to a Mountain location, add a EYE adjacent to any Mountain location connected to that Mountain location.",
        } ],
    ["Snapback",
        {'element': 'water', 'category': 'eye-create', 'id': 79, 'pattern': 'E2-25'},
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
        {'element': 'air', 'category': 'mage-move,eye-create,eye-move', 'id': 67, 'pattern': 'E2-46'},
        {
            'cast': "Move 1 space, place a EYE, then move that EYE 2 spaces.",
        } ],
    ["Spread",
        {'element': 'water', 'category': 'eye-create,eye-move', 'id': 75, 'pattern': 'E2-20'},
        {
            'cast': "Place a EYE. Move all of your EYEs 1 space.",
        } ],
    ["Burst",
        {'element': 'water', 'category': 'eye-create,eye-move', 'id': 74, 'pattern': 'E2-31'},
        {
            'cast': "Place 2 EYEs. Move 3 of your EYEs 2 spaces each.",
        } ],
    ["Traceback",
        {'element': 'water', 'category': 'eye-move,eye-create', 'id': 69, 'pattern': 'E2-41'},
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
        {'element': 'fire', 'category': 'eye-other-attack', 'id': 72, 'pattern': 'E2-19'},
        {
            'cast': "If in a location with a EYE controlled by another mage, you may remove 2 of their EYEs.",
        } ],
    ["Prune",
        {'element': 'earth', 'category': 'eye-other-attack', 'id': 33, 'pattern': 'E2-23'},
        {
            'cast': "Remove all opponent EYEs from a location where you control a EYE. Consume this EYE.",
        } ],
    ["Prune Neighbor",
        {'element': 'fire', 'category': 'eye-other-attack', 'id': 42, 'pattern': 'E2-31'},
        {
            'cast': "Remove all EYEs from a location adjacent to where you control a EYE. Consume this EYE.",
        } ],
    ["Erase",
        {'element': 'fire', 'category': 'eye-move,eye-other-attack', 'id': 65, 'pattern': 'E2-28'},
        {
            'cast': "Move one of your EYEs 3 spaces, removing one opponent EYE from each location it moves into this turn. Consume this EYE.",
        } ],
    ["Fire Burst",
        {'element': 'fire', 'category': 'eye-other-attack', 'id': 23, 'pattern': 'E2-30'},
        {
            'cast': "Remove all EYEs in all locations adjacent to one of your EYEs. Consume that EYE.",
        } ],
    ["Nudge",
        {'element': 'earth', 'category': 'eye-other-move', 'id': 85, 'pattern': 'E2-8'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "At the end of your turn, if another mage's EYE is in the same location or adjacent to one of your EYEs, you may move their EYE 1 space. Choose one for each charge on this spell.",
            'sacrifice': "Sacrifice a charge to move the eye(s) 4 spaces."
        } ],
    ["Sneak Attack",
        {'element': 'fire', 'category': 'eye-other-attack,mage-move', 'id': 64, 'pattern': 'E2-55'},
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
        {'element': 'earth', 'category': 'eye-defend', 'id': 83, 'pattern': 'E1-6'},
        {
            'cast': "{{ADD_CHARGE}}",
            'sacrifice': "You may sacrifice this CHARGE to prevent one of your EYEs from being removed or consumed.",
        } ],
    ["Harden Shell",
        {'element': 'earth', 'category': 'eye-defend', 'id': 86, 'pattern': 'E2-9'},
        {
            'cast': "{{ADD_CHARGE}}", 
            'charged': "If the number of EYEs you have is less than or equal to the number of CHARGEs on this spell, then they are protected from being removed by another mage (but they can still be consumed).",
        } ],
    ["Whiplash",
        {'element': 'water', 'category': 'eye-defend', 'id': 76, 'pattern': 'E2-21'},
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

    ["Fire Ball",
        {'element': 'fire', 'category': 'mage-other-attack', 'id': 22, 'pattern': 'E2-26'},
        {
            'cast': "Attack 1 at one of your EYEs. Consume that EYE.",
        } ],

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
        {'element': 'water', 'category': 'tapestry-thread', 'id': 58, 'pattern': 'E2-19'},
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

    ["Water Moccasins",
        {'element': 'water', 'category': 'mage-move,terrain', 'id': 54, 'pattern': 'E2-24'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "Rivers cost 0mp to cross. Water locations cost 1mp to enter.",
            'sacrifice': "If you are adjacent to River/Water, sacrifice charge to place a EYE up to 3 spaces away along water.",
        } ],


    # Blank card (for TTS)
    #["???",
    #    {'element': 'none', 'category': 'starter', 'id': 0, 'pattern': 'blank'},
    #    {
    #        'cast': "???",
    #    } ],

]
