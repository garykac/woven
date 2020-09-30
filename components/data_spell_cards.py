# Spell fragment card data

# Text -> ASCII Art: http://patorjk.com/software/taag/#p=display&f=Rectangles&t=Monster

spell_card_revision = 8

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

# Basic abilities
#   Create eye in current location
#   Small move self
#   Recover Thread
#   Expand tapestry

# Required spell types
#   Move self/target
#     using river
#     using forest
#     using dense forest
#     using rough terrain
#     ignoring rough terrain
#     through unobstructed terrain
#     to location at same elevation
#   Create eye distant
#     anywhere in connected forest/rough/river
#     in same location as existing eye
#     follow another's eye back to mage
#   Move eye
#     single eye
#     multiple eyes
#     n spaces split between eyes
#     to another mage when eye overlaps
#     n spaces along matching terrain
#   Attack eye
#     Remove eye in same location
#     Remove eyes adjacent
#     Move other eye
#   Defend eye against attack
#     Sacrifice charge to defend eye
#   Defend eye from being consumed
#   Defend eye move - Anchor eye
#   Attack creature
#     at eye
#     at eye in a forest/mountain
#     by targeting one of their eyes
#   Defend self against attack
#     Defend target against attack
#     Reflect attack back at attacker
#     Deflect attack to adjacent
#     shield if in same location as eye
#     shield that also recovers Thread when attacked

#   Hide from detection
#   Push adjacent creature/mage
#   Anchor (to counter push)
#   Teleport to eye
#     Exchange locations with an eye
#   Levitate/fly
#     + move while levitated
#   Charges
#     extra action
#     copy charge on another's spell

#   Terraform
#     add/remove forest
#     add/remove rough terrain
#     area around an eye changes type: forest, water
#     change elevation
#   Attack tapestry
#     cover an element
#     cover a space
#   Defend tapestry

# Spell combos:
#   Move + create eye

# Artifact abilities
#   Recover Thread
#   Move Threads
#   Concealment
#   Ignore terrain penalty


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
#     'category': <string> to group spells by general category
#     'flavor': flavor text for spell
#
#   <info>:
#     'cast': Description when spell is cast.
#     'charged': Description when spell is charged.
#     'notes': Additional notes
#     'sacrifice': Description when charge is sacrificed.

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

    ["Haste",
        {'element': 'air', 'pattern': 'E1-1', 'op': 'eye', 'vp': 0,
         'category': 'starter,mage-move',
        }, {
            'cast': "Move 4",
        } ],

    ["Endurance",
        {'element': 'earth', 'pattern': 'E1-1', 'op': 'tapestry-eye', 'vp': 0,
         'category': 'starter,terrain,mage-move',
        }, {
            'cast': "{{ADD_ACTION}}",
            'active': "You may ignore the movement penalty for rough terrain or changing elevation.",
        } ],

    ["Fire Shards",
        {'element': 'fire', 'pattern': 'E1-2', 'op': 'eye-thread', 'vp': 0,
         'category': 'starter,mage-other-attack',
        }, {
            'cast': "Consume one of your Eyes to Attack 1 at that location.",
        } ],

    ["Extend",
        {'element': 'water', 'pattern': 'E1-2', 'op': 'eye-mmove', 'vp': 0,
         'category': 'starter,eye-move',
        }, {
            'cast': "Move one of your Eyes 2 spaces.",
        } ],

    #     _____                _____     _ ___ 
    #    |     |___ _ _ ___   |   __|___| |  _|
    #    | | | | . | | | -_|  |__   | -_| |  _|
    #    |_|_|_|___|\_/|___|  |_____|___|_|_|
    #
    # Move mage N spaces
    # Move mage N spaces, create eye
    # Move into adjacent location via land (w/o crossing water)
    # Cross over river
    # Ignore movement penalty: rough terrain, elevation, cross rivers
    # Move through connected terrain type (forest, dense forest, river, plain)
    # Dense forest teleport within 5 spaces
    # React: when attacked, move to adjacent location
    # Air walk: move along same or lower terrain. must end at same level.
    # Teleport link: within forest, swap positions with an Eye.
    # Levitate/Fly - ignore terrain cost, easier to detect
    # Move into location and push others
    
    ["Airwalk",
        {'element': 'air', 'pattern': 'E2-7', 'op': 'eye-thread', 'vp': 1,
         'category': 'terrain,mage-move',
        }, {
            'cast': "If at mid or high-elevation, move 5 spaces over same of lower elevation. You must end at the same elevation as your start.",
        } ],

    ["Plainswalker",
        {'element': 'earth', 'pattern': 'E2-2', 'op': 'tapestry-eye', 'vp': 1,
         'category': 'terrain,mage-move',
        }, {
            'cast': "If in low-elevation, move 7 spaces through low-elevation, ignoring terrain cost.",
        } ],

    ["Waterwalk",
        {'element': 'water', 'pattern': 'E2-34', 'op': 'eye-thread', 'vp': 1,
         'category': 'terrain,mage-move',
         #'flavor': "Rising columns of mud form a temporary bridge.",
        }, {
            'cast': "If adjacent to a river, move 5 spaces along that river, switching sides at will.",
        } ],

    # Pattern is Doubled form of Haste
    ["Blur",
        {'element': 'air', 'pattern': 'E2-1', 'op': 'tapestry-eye', 'vp': 1,
         'category': 'mage-move',
        }, {
            'cast': "Move 8",
        } ],

    ["Forest Blink",
        {'element': 'air', 'pattern': 'E2-59', 'op': 'eye-thread', 'vp': 1,
         'category': 'terrain,mage-move',
        }, {
            'cast': "If you are in a forest location, you may move to any connected forest location, ignoring any terrain costs and crossing rivers.",
        } ],

    ["Dense Passage",
        {'element': 'air', 'pattern': 'E2-60', 'op': 'eye-thread', 'vp': 1,
         'category': 'terrain,mage-move',
        }, {
            'cast': "If in a Dense Forest location, jump to another Dense Forest location no more than 5 spaces away.",
            'react': "If attacked while in a Dense Forest, jump to the nearest Dense Forest",
        } ],

    ["Dodge",
        {'element': 'air', 'pattern': 'E1-3', 'op': 'eye-thread', 'vp': 1,
         'category': 'mage-move',
        }, {
            'cast': "Move 6",
            'react': "When attacked, cast to move into any valid adjacent location.",
        } ],

    #     _____                _____ _   _           
    #    |     |___ _ _ ___   |     | |_| |_ ___ ___ 
    #    | | | | . | | | -_|  |  |  |  _|   | -_|  _|
    #    |_|_|_|___|\_/|___|  |_____|_| |_|_|___|_|
    #
    # Attack another mage's position on the map
    # Locations next to eyes are barriers that others cannot move into
    # Teleport other
    # Target is prevented from moving out of current location
    # Move into adjacent location, pushing any mage there into another location
    #    moving them to one of your Eye locations
    
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
    # Duplicate Eye - double number of eyes
    # When in location of opponent's Eye, create Eye in their location
    # When in location of opponent's Eye, create Eye in one of their Eye's location
    # When in forest/water, create Eye in same terrain within N spaces

    ["Water Target",
        {'element': 'water', 'pattern': 'E1-5', 'op': 'mmove-thread', 'vp': 1,
         'category': 'eye-create',
        }, {
            'cast': "If next to a river, place an Eye in any location along that river within 5 spaces.",
        } ],

    ["Woodland Target",
        {'element': 'earth', 'pattern': 'E2-10', 'op': 'tapestry-mmove', 'vp': 1,
         'category': 'eye-create',
        }, {
            'cast': "If in a forest, place an Eye in any connected forest location.",
        } ],

    ["Duplicate",
        {'element': 'water', 'pattern': 'E2-27', 'op': 'eye-mmove', 'vp': 1,
         'category': 'eye-create',
        }, {
            'cast': "In a location where you have at least one Eye, split each of your Eyes into two separate Eyes.",
        } ],

    ["Traceback",
        {'element': 'water', 'pattern': 'E2-36', 'op': 'tapestry-thread', 'vp': 1,
         'category': 'eye-create',
        }, {
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
    # Move one 1 Eye N spaces
    # Move all Eyes N spaces each
    # Move N spaces, split among M Eyes
    # Move N spaces, split among any number of Eyes
    # Duplicate an Eye and then move it N spaces
    # Create Eye, then move Eyes
    # Move Eye N spaces, if Eye in same location as another mage's Eye,
    #    move Eye to that mage's location
    # Move Eye in plain/water/forest N spaces within that terrain
    # Move Eye in plain/water/forest to another within N spaces
    
    ["Eyedrop",
        {'element': 'air', 'pattern': 'E2-14', 'op': 'mmove-thread', 'vp': 1,
         'category': 'eye-move',
        }, {
            'cast': "Create an Eye and then move it 4.",
        } ],
    
    ["Seek",
        {'element': 'air', 'pattern': 'E2-15', 'op': 'eye-mmove', 'vp': 1,
         'category': 'eye-move',
        }, {
            'cast': "Move one of your Eyes 4 spaces. If it ends in the same location as another Mage's Eye, then move your Eye to that Mage's location.",
        } ],
    
    ["Gust",
        {'element': 'air', 'pattern': 'E1-6', 'op': 'eye-mmove', 'vp': 1,
         'category': 'eye-move',
        }, {
            'cast': "Move your Eyes 6 spaces, split among any number of Eyes.",
        } ],
    
    ["Spread",
        {'element': 'water', 'pattern': 'E2-31', 'op': 'eye-thread', 'vp': 1,
         'category': 'eye-move',
        }, {
            'cast': "Move all your Eyes 3 spaces.",
        } ],

    ["Expand",
        {'element': 'water', 'pattern': 'E2-35', 'op': 'mmove-thread', 'vp': 1,
         'category': 'eye-create,eye-move',
         'flavor': "The air crackles as the Eye splits and one half shoots away. ",
        }, {
            'cast': "Duplicate an existing Eye and then move it 6 spaces.",
        } ],

    ["Bolt",
        {'element': 'fire', 'pattern': 'E1-8', 'op': 'eye-mmove', 'vp': 1,
         'category': 'eye-move',
        }, {
            'cast': "Move a single Eye 8 spaces.",
        } ],

    #     _____                _____ _   _              _____         
    #    |     |___ _ _ ___   |     | |_| |_ ___ ___   |   __|_ _ ___ 
    #    | | | | . | | | -_|  |  |  |  _|   | -_|  _|  |   __| | | -_|
    #    |_|_|_|___|\_/|___|  |_____|_| |_|_|___|_|    |_____|_  |___|
    #                                                        |___|
    #
    # Move an opponent's Eye
    # Move all eyes in your location N spaces
    # Move all eyes from adjacent spaces
    # Move self N spaces, for each space entered move all Eyes 1 space
    # Move Eye N spaces, for each space entered move all Eyes 1 space

    ["Disperse",
        {'element': 'air', 'pattern': 'E2-53', 'op': 'eye-mmove', 'vp': 1,
         'category': 'eye-move',
        }, {
            'cast': "Move one of your Eyes 3 spaces, pushing any existing Eyes into an adjacent space.",
        } ],

    ["Control",
        {'element': 'water', 'pattern': 'E2-78', 'op': 'eye-mmove', 'vp': 1,
         'category': 'eye-move',
        }, {
            'cast': "If you have an Eye in the same location as another Eye, then you may move that other Eye 4 spaces.",
        } ],

    ["Control Burst",
        {'element': 'water', 'pattern': 'E2-79', 'op': 'mmove-thread', 'vp': 1,
         'category': 'eye-move',
        }, {
            'cast': "If you have an Eye in the same location as other Eyes, then you may move all other Eyes 2 spaces each.",
        } ],

    #     ____      ___           _    _____                _____         
    #    |    \ ___|  _|___ ___ _| |  |     |___ _ _ ___   |   __|_ _ ___ 
    #    |  |  | -_|  _| -_|   | . |  | | | | . | | | -_|  |   __| | | -_|
    #    |____/|___|_| |___|_|_|___|  |_|_|_|___|\_/|___|  |_____|_  |___|
    #                                                            |___|
    #
    # Defend against an opponent moving your Eyes
    # Create Anchored Eye
    # Anchor remote eye
    
    ["Anchor",
        {'element': 'earth', 'pattern': 'E1-6', 'op': 'tapestry-thread', 'vp': 1,
         'category': 'eye-defend',
        }, {
            'cast': "Create a new Eye and then Anchor it.",
        } ],

    ["Remote Anchor",
        {'element': 'earth', 'pattern': 'E2-15', 'op': 'mmove-thread', 'vp': 1,
         'category': 'eye-defend',
        }, {
            'cast': "Anchor one of your Eyes.",
        } ],

    #     _____ _   _           _      _____         
    #    |  _  | |_| |_ ___ ___| |_   |   __|_ _ ___ 
    #    |     |  _|  _| .'|  _| '_|  |   __| | | -_|
    #    |__|__|_| |_| |__,|___|_,_|  |_____|_  |___|
    #                                       |___|
    #
    # Move or destroy an opponent's Eye
    # Cast: Remove all Eyes at location
    # Charge: When opponent's eye moves into your location, destroy Eye
    # Remove all Eyes from 1 location adjacent to Eye (or all locations adjacent)
    # Cast: Move 3 spaces, removing 1 Eye from each location you enter.
    # Cast: If in location with other Eye, remove 1 of that mage's Eyes
    # Charge: At end of turn, move co-located Eye 1 space.
    #    Sacrifice charge to move 4 spaces.
    # Remove Eye from adjacent location and move into that space

    ["Dispel",
        {'element': 'fire', 'pattern': 'E1-5', 'op': 'tapestry-eye', 'vp': 1,
         'category': 'eye-other-attack',
        }, {
            'cast': "Consume one of your Eyes to remove all Eyes at that location.",
        } ],

    ["Ground",
        {'element': 'earth', 'pattern': 'E2-60', 'op': 'tapestry-mmove', 'vp': 1,
         'category': 'eye-other-attack',
        }, {
            'cast': "Remove all Eyes from your location and all adjacent locations.",
        } ],

    ["Scorch",
        {'element': 'fire', 'pattern': 'E2-36', 'op': 'eye-thread', 'vp': 1,
         'category': 'eye-move,eye-other-attack',
        }, {
            'cast': "Move one of your Eyes 3 spaces, removing one opponent Eye from each location it moves into this turn. Consume this Eye.",
        } ],

    ["Repel",
        {'element': 'fire', 'pattern': 'E2-35', 'op': 'tapestry-thread', 'vp': 1,
         'category': 'eye-move,eye-other-attack',
        }, {
            'cast': "{{ADD_CHARGE}}",
            'react': "You may cast this when an Eye move into your location.",
            'sacrifice': "When an Eye moves into your location, you may spend a Charge to destroy that Eye.",
        } ],

    #     ____      ___           _    _____         
    #    |    \ ___|  _|___ ___ _| |  |   __|_ _ ___ 
    #    |  |  | -_|  _| -_|   | . |  |   __| | | -_|
    #    |____/|___|_| |___|_|_|___|  |_____|_  |___|
    #                                       |___|
    #
    # Defend against an opponent removing one of your eyes
    # Charge: Sacrifice charge to substitute one Eye for another being removed
    # Charge: Sacrifice charge to prevent Eye from being removed
    # N charges protects N Eyes on map
    # Anchor Eye
    # Charge: all Eyes become anchors

    ["Sacrificium",
        {'element': 'earth', 'pattern': 'E2-8', 'op': 'eye-mmove', 'vp': 1,
         'category': 'mage-defend',
        }, {
            'cast': "{{ADD_CHARGE}}",
            'react': "You may cast this when one of your Eyes is attacked.",
            'sacrifice': "When you need to remove an Eye, you may instead remove a Charge from this spell.",
        } ],

    ["Switch",
        {'element': 'earth', 'pattern': 'E2-11', 'op': 'eye-thread', 'vp': 1,
         'category': 'mage-defend',
        }, {
            'cast': "{{ADD_CHARGE}}",
            'react': "You may cast this when one of your Eyes is attacked.",
            'sacrifice': "When you need to remove an Eye, you may instead remove one of your other Eyes.",
        } ],

    #     _____ _   _           _        _____ _____ 
    #    |  _  | |_| |_ ___ ___| |_     |  |  |  _  |
    #    |     |  _|  _| .'|  _| '_|    |     |   __|
    #    |__|__|_| |_| |__,|___|_,_|    |__|__|__|
    #
    # Attack another mage/creature
    # Attack at Eye
    # Attack adjacent to Eye
    # React: Redirect attack to one of your Eyes
    # Charge: When opponent's eye moves into your location, attack 1 at mage
    # Attack 1 at all Eyes
    # Attack 2 in all Eyes in Forest/Rough/next to water
    # Attack 3 in neighboring location to Eye in mountain
    # Move 1 and then attack 1 adjacent to new location
    # Charge: Sacrifice to boost power of attack by 1
    # Groups of 3 Eyes are Wall of Flame. Charge lost if group broken
    # Extra damage against shield spell

    ["Ignis",
        {'element': 'fire', 'pattern': 'E2-27', 'op': 'eye-thread', 'vp': 1,
         'category': 'mage-other-attack',
        }, {
            'cast': "Consume one of your Eyes to Attack 1 at location adjacent to that Eye.",
        } ],

    ["Redirect",
        {'element': 'fire', 'pattern': 'E2-32', 'op': 'eye-mmove', 'vp': 1,
         'category': 'mage-other-attack',
        }, {
            'cast': "Attack 1 at one of your Eyes.",
            'react': "When attacked, cast to redirect the attack to one of your Eyes.",
        } ],

    ["Lavastone",
        {'element': 'fire', 'pattern': 'E2-31', 'op': 'eye-thread', 'vp': 1,
         'category': 'mage-other-attack',
        }, {
            'cast': "Attack 2 at one of your Eyes. Attack 3 if targeting rough terrain or high elevation.",
        } ],

    ["Boost",
        {'element': 'fire', 'pattern': 'E2-28', 'op': 'tapestry-thread', 'vp': 1,
         'category': 'mage-other-attack',
        }, {
            'cast': "{{ADD_CHARGE}}",
            'sacrifice': "Spend a Charge to increase Attack strength by 1.",
        } ],

    ["Geyser",
        {'element': 'water', 'pattern': 'E1-8', 'op': 'eye-thread', 'vp': 1,
         'category': 'mage-other-attack',
        }, {
            'cast': "Attack 1 at two of your Eyes.",
        } ],

    #     ____      ___           _      _____ _____ 
    #    |    \ ___|  _|___ ___ _| |    |  |  |  _  |
    #    |  |  | -_|  _| -_|   | . |    |     |   __|
    #    |____/|___|_| |___|_|_|___|    |__|__|__|
    #
    # Defend against being attacked
    # Charge: Defend 1 damage
    # React: Cast to defend
    # Charge: Defend from attack, but attack reflected back at attacker
    # Charge: If in same location as Eye, that Eye acts as shield 2
    # Charge: Deflect attack into adjacent location
    # Charge: Boost defense power by 1

    ["Shield",
        {'element': 'earth', 'pattern': 'E1-3', 'op': 'eye-mmove', 'vp': 1,
         'category': 'mage-defend',
        }, {
            'cast': "{{ADD_CHARGE}}",
            'sacrifice': "Remove a charge to cancel an attack of 1 damage.",
        } ],

    ["Deflect",
        {'element': 'earth', 'pattern': 'E2-5', 'op': 'tapestry-eye', 'vp': 1,
         'category': 'mage-defend',
        }, {
            'cast': "Deflect an attack of 1",
            'react': "When attacked, cast to deflect attack.",
        } ],

    ["Reflect",
        {'element': 'fire', 'pattern': 'E2-44', 'op': 'eye-thread', 'vp': 1,
         'category': 'mage-defend',
        }, {
            'cast': "{{ADD_CHARGE}}",
            'sacrifice': "Remove a charge to reduce damage to 1/2 (round down) and reflect full damage back at the attacker.",
        } ],

    #     _____                 _           
    #    |_   _|___ ___ ___ ___| |_ ___ _ _ 
    #      | | | .'| . | -_|_ -|  _|  _| | |
    #      |_| |__,|  _|___|___|_| |_| |_  |
    #              |_|                 |___|
    # Tapestry modification
    # Remove thread from tapestry. Take another action.
    # Recovery shield - Protection shield 1, but:
    #     Charge may be sacrificed to recover 2 threads
    #     If attacked, recover 2 threads

    #     _____ _   _              _____                 _           
    #    |     | |_| |_ ___ ___   |_   _|___ ___ ___ ___| |_ ___ _ _ 
    #    |  |  |  _|   | -_|  _|    | | | .'| . | -_|_ -|  _|  _| | |
    #    |_____|_| |_|_|___|_|      |_| |__,|  _|___|___|_| |_| |_  |
    #                                       |_|                 |___|
    # Attack an opponent's tapestry
    # Attack: Cover a element spot in another mage's tapestry.
    # Attack: Cover a normal space in opponent's tapestry
    # Attack: Opponent is forced to add mana to their tapestry
    #    New mana must be placed adjacent to existing mana

    #     ____      ___           _    _____                 _           
    #    |    \ ___|  _|___ ___ _| |  |_   _|___ ___ ___ ___| |_ ___ _ _ 
    #    |  |  | -_|  _| -_|   | . |    | | | .'| . | -_|_ -|  _|  _| | |
    #    |____/|___|_| |___|_|_|___|    |_| |__,|  _|___|___|_| |_| |_  |
    #                                           |_|                 |___|
    # Defend tapestry from attack

    #     _____                 _     
    #    |_   _|___ ___ ___ ___|_|___ 
    #      | | | -_|  _|  _| .'| |   |
    #      |_| |___|_| |_| |__,|_|_|_|
    #
    # Change terrain type: -> water, forest, rough
    # While charges, Eyes represent terrain type

    #     _____         _ _ 
    #    |   __|___ ___| | |
    #    |__   | . | -_| | |
    #    |_____|  _|___|_|_|
    #          |_|
    # Interact with your spells
    # Duplicate Charge on one of your spells

    #     _____ _   _              _____         _ _ 
    #    |     | |_| |_ ___ ___   |   __|___ ___| | |
    #    |  |  |  _|   | -_|  _|  |__   | . | -_| | |
    #    |_____|_| |_|_|___|_|    |_____|  _|___|_|_|
    #                                   |_|
    # Remove a charge from an opponent's spell
    # Copy effect of another's spell
    # Copy charge - if Eye adjacent to mage, add charge to one of their spells

    #     _____     _   _         
    #    |  _  |___| |_|_|___ ___ 
    #    |     |  _|  _| | . |   |
    #    |__|__|___|_| |_|___|_|_|
    #
    # Gain an extra action
    # Store an action for later - sacrifice charge

    #     _____     _           _ 
    #    |  _  |___| |_ ___ ___| |
    #    |     |_ -|  _|  _| .'| |
    #    |__|__|___|_| |_| |__,|_|
    #
    # Teleport self - go to astral plane
    # Teleport return - return from astral to an Eye
    # Teleport other - move other mage at Eye to astral
    # Teleport return other - move other mage from astral to Eye

    #     _____ _         
    #    |     |_|___ ___ 
    #    | | | | |_ -|  _|
    #    |_|_|_|_|___|___|
    #
    # Hide from detection
    
    # Blank card (for TTS)
    #["???",
    #    {'element': 'none', 'pattern': 'blank',
    #      'category': 'blank'},
    #    {
    #        'cast': "???",
    #    } ],

]
