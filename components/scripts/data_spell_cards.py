# Spell fragment card data

# Text -> ASCII Art: http://patorjk.com/software/taag/#p=display&f=Rectangles&t=Monster

spell_card_revision = 13

spell_card_categories = [
    'blank',        # Cannot be combined with other categories.

    'anchor-create',
    'anchor-move',
    'anchor-attack',

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

    'thread-move',
    
    #'modify-tapestry',
    #'add-action',
    'terrain',
]

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
#   * Move thread (within Tapestry without casting)
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
# Attack Anchor                        + + +
# Defend Anchor
# Move Anchor                                        + + +
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
#     'DISABLE': if present, skip over this card when generating
#     'category': <string> to group spells by general category
#     'flavor': flavor text for spell
#
#   <info>:
#     'cast': Description when spell is cast.
#     'react': Indicates that spells can be cast immediately in reaction to an event
#     'charged': Description when spell is charged.
#     'note': Additional notes
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

    # Set S1

    ["Cloudslap",
        {'element': 'air', 'pattern': 'E2-56', 'set': "S1",
         'category': 'mage-other-move,mage-other-attack',
        }, {
            'target': "{{EYE_LOCATION}}",
            'cost': "{{EYE_SACRIFICE}}",
            'cast': [
                "All creatures in target space are surrounded by cloud puffs and pushed into the same neighboring space.",
                "If they are pushed through a barrier (off a cliff, into a cliff wall, or over a river), then that's really unfortunate (Attack 1)."
            ],
        } ],

    ["Extend (Land)",
        {'element': 'earth', 'pattern': 'E2-10', 'set': "S1",
         'category': 'eye-move',
        }, {
            'target': "{{EYE}}",
            'prereq': "Target Eye must not be over water",
            'cast': "Move one of your Eyes 5 spaces, but it may not cross water.",
        } ],

    ["Plainswalker",
        {'element': 'fire', 'pattern': 'E2-44', 'companion': True, 'set': "S1",
         'category': 'mage-move',
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'prereq': "Target is in lowland",
            'cast': "Move yourself 6 spaces through lowlands.",
        } ],

    ["Asunder",
        {'element': 'water', 'pattern': 'E2-27', 'set': "S1",
         'category': 'eye-create,eye-move',
        }, {
            'target': "{{EYE}}",
            'cast': "Duplicate one of your Eyes and then move it 2 spaces.",
        } ],

    # Set S2

    ["Airwalk",
        {'element': 'air', 'pattern': 'E2-60', 'companion': True, 'set': "S2",
         'category': 'mage-move',
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': [
                "A perfectly flat-top cloud walkway forms between the start and end location.",
                "Move yourself 5 spaces across this walkway, passing over any barriers and water.",
                "The walkway must end at the same elevation as the start location, and it may not pass through a higher elevation space."
            ],
        } ],

    ["Tumbler",
        {'element': 'earth', 'pattern': 'E2-16', 'set': "S2",
         'category': 'mage-other-attack',
        }, {
            'prereq': "{{TARGET_HI_MID}}",
            'target': "{{EYE_LOCATION}}",
            'cost': "{{EYE_SACRIFICE}}",
            'cast': [
                "A cascade of rock tumbles from the target location into an adjacent space of lower elevation.",
                "All creatures in the lower space are crushed (Attack 1)."
            ],
        } ],

    ["Scorch",
        {'element': 'fire', 'pattern': 'E2-78', 'set': "S2",
         'category': 'eye-move,eye-other-attack',
        }, {
            'target': "{{EYE}}",
            'cast': "Move one of your Eyes 3 spaces, removing one opponent Eye from each location it moves into this turn.",
            'cost': "{{EYE_SACRIFICE}}",
        } ],

    ["Disperse (+Water)",
        {'element': 'water', 'pattern': 'E2-28', 'set': "S2",
         'category': 'eye-move',
        }, {
            'target': "{{EYES}}",
            'cast': [
                "Move your Eyes a total of 4 spaces.",
                "Each Eye moves +1 space if at some point it crosses a river."
            ],
        } ],

    # Set S3
    
    ["Extend",
        {'element': 'air', 'pattern': 'E2-1', 'set': "S3",
         'category': 'eye-move',
        }, {
            'target': "{{EYE}}",
            'cast': "Move one of your Eyes 5 spaces.",
        } ],

    ["Ground",
        {'element': 'earth', 'pattern': 'E2-51', 'set': "S3",
         'category': 'eye-other-attack',
        }, {
            'target': "{{MAGE_LOCATION}}",
            'cast': "Remove all Eyes from your location and all adjacent spaces.",
        } ],

    ["Flambough",
        {'element': 'fire', 'pattern': 'E2-48', 'set': "S3",
         'category': 'mage-other-attack',
        }, {
            'prereq': "Target Eye must be in Forest space",
            'target': "{{EYE_LOCATION}}",
            'cost': "{{EYE_SACRIFICE}}",
            'cast': [
                "The trees in the target location burst into flame and the main boughs shoot out in all directions.",
                "All creatures in the target space (and in one neighboring space at the same elevation) are pierced in an unpleasant manner (Attack 1)."
            ],
        } ],

    ["Waterstride",
        {'element': 'water', 'pattern': 'E2-79', 'companion': True, 'set': "S3",
         'category': 'mage-move',
        }, {
            'prereq': "Target must be adjacent to river",
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': "Move yourself 6 spaces along the river, switching sides at will.",
        } ],

    # Set S4
    
    ["Repel",
        {'element': 'air', 'pattern': 'E2-14', 'companion': True, 'set': "S4",
         'category': 'eye-other-attack',
        }, {
            'cast': "{{ADD_CHARGE}}",
            'react': "You may cast this when an Eye moves into your location.",
            'trigger': "{{EYE_ENTERS_LOCATION}}",
            'sacrifice': "When an Eye moves into your location, you may spend a Charge to destroy that Eye.",
        } ],

    ["Longarm", # Brachiate
        {'element': 'earth', 'pattern': 'E2-9', 'companion': True, 'set': "S4",
         'category': 'mage-move',
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': "You swing from treetop to treetop into neighboring forest spaces (max 5), ignoring barriers like rivers and cliffs.",
        } ],

     ["Extend (+Highland)",
        {'element': 'fire', 'pattern': 'E2-35', 'set': "S4",
         'category': 'eye-move',
        }, {
            'target': "{{EYE}}",
            'cast': "Move one of your Eyes 3 spaces, +1 space if the start location is within 2 spaces of highland.",
        } ],

    ["River Lurker",
        {'element': 'water', 'pattern': 'E2-36', 'set': "S4",
         'category': 'mage-other-attack',
        }, {
            'prereq': "Target Eye that is adjacent to river",
            'target': "{{SEE_DESC}}",
            'cost': "{{EYE_SACRIFICE}}",
            'cast': [
                "Select a target location downriver (or upriver) from the target Eye, no more than 9 river segments away.",
                "Tendrils of water reach out and grab all creatures in the target location, dragging them into the water (Attack 1).",
            ],
        } ],
  
    # Extra spells
    
    ["Slipstream",
        {'element': 'air', 'pattern': 'E2-8', 'companion': True,
         'category': 'mage-move,mage-defend',
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': "You catch a gust of air which transports you to a neighboring location (of your choice), bypassing any barriers.",
            'trigger': "{{WHEN_ATTACKED}}",
            'react': "Same effect as when cast normally, with the added bonus of avoiding the attack.",
        } ],

    ["Switch",
        {'element': 'earth', 'pattern': 'E2-53', 'companion': True,
         'category': 'eye-defend',
        }, {
            'cast': "{{ADD_CHARGE}}",
            'charged': "When you need to remove an Eye, you may instead remove one of your other Eyes.",
            'react': "You may cast this when one of your Eyes is attacked.",
        } ],

    ["Lava Shield",
        {'element': 'fire', 'pattern': 'E2-37', 'companion': True,
         'category': 'mage-defend',
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'prereq': "{{TARGET_HI_MID}}",
            'trigger': "{{WHEN_ATTACKED}}",
            'react': "Molten rock and metal shoot up from the ground to form a protective barrier (Defend 1) around you before melting back into the ground.",
        } ],

    ["Riverbank",
        {'element': 'water', 'pattern': 'E2-31',
         'category': 'eye-create',
        }, {
            'cast': "If next to a river, place an Eye in any location along that river within 5 spaces.",
        } ],

    ["Haste",
        {'element': 'air', 'pattern': 'E2-5', 'companion': True,
         'category': 'mage-move',
        }, {
            'cast': "Move 3 along the same elevation.",
        } ],

    ["Beetlefeet",
        {'element': 'earth', 'pattern': 'E2-59', 'companion': True,
         'category': 'mage-move',
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': "{{ADD_CHARGE}}",
            'charged': "When you enter a space with a cliff edge, you may immediately (for no cost) scramble up or down that cliff edge into the neighboring space.",
            'note': "Only once per movement action (physical or magical) per charge.",
        } ],

    ["Dispel",
        {'element': 'fire', 'pattern': 'E2-40',
         'category': 'eye-other-attack',
        }, {
            'cast': ["Consume one of your Eyes to remove all Eyes in that space."],
        } ],

    ["Fjord",
        {'element': 'water', 'pattern': 'E2-32', 'companion': True,
         'category': 'mage-move',
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': "{{ADD_CHARGE}}",
            'charged': "When you enter a space with a river edge, you may force the waters to part so you can (immediately, for no additional cost) walk across the muddy riverbed to the space on the other side.",
            'note': "Only once per movement action (physical or magical) per charge."
        } ],

    # v12 starters
    
    ["Fire Shards",
        {'element': 'fire', 'pattern': 'blank', 'DISABLE': True,
         'category': 'mage-other-attack',
        }, {
            'cast': "Consume one of your Eyes to Attack 1 at that location.",
        } ],

    ["Shield",
        {'element': 'earth', 'pattern': 'blank', 'companion': True, 'DISABLE': True,
         'category': 'mage-defend',
        }, {
            'cast': "{{ADD_CHARGE}}",
            'react': "When attacked, you may immediately cast this spell.",
            'sacrifice': "Remove a charge to cancel an attack of 1 damage.",
        } ],


    #     _____                _____     _ ___ 
    #    |     |___ _ _ ___   |   __|___| |  _|
    #    | | | | . | | | -_|  |__   | -_| |  _|
    #    |_|_|_|___|\_/|___|  |_____|___|_|_|
    #
    # Move mage on map
    
    ["Endurance",
        {'element': 'earth', 'pattern': 'blank', 'companion': True, 'DISABLE': True,
         'category': 'terrain,mage-move',
        }, {
            'cast': "{{ADD_CHARGE}}",
            'charged': "Your max movement range is increased by 2 whenever you cast a spell that moves yourself.",
        } ],

    ["Blur",
        {'element': 'air', 'pattern': 'blank', 'DISABLE': True,
         'category': 'mage-move',
        }, {
            'cast': "Move 5 through any terrain.",
        } ],

    ["Forest Passage",
        {'element': 'air', 'pattern': 'blank', 'companion': True, 'DISABLE': True,
         'category': 'terrain,mage-move',
        }, {
            'cast': "If you are in a Forest location, you may move to any connected Forest location up to 6 spaces away, ignoring any terrain costs and crossing rivers.",
        } ],

    ["Forest Home",
        {'element': 'air', 'pattern': 'blank', 'companion': True, 'DISABLE': True,
         'category': 'terrain,mage-move,mage-defend',
        }, {
            'cast': "If in a Forest location, jump to another Forest location no more than 4 spaces away.",
            'react': "If attacked while in a Forest, you may cast this to move into a neighboring location within the same Forest.",
        } ],

    ["Dodge",
        {'element': 'air', 'pattern': 'blank', 'companion': True, 'DISABLE': True,
         'category': 'mage-move,mage-defend',
        }, {
            'cast': "Move 4 through any terrain.",
            'react': "When attacked, cast to move into any valid adjacent location.",
        } ],

    #     _____                _____ _   _           
    #    |     |___ _ _ ___   |     | |_| |_ ___ ___ 
    #    | | | | . | | | -_|  |  |  |  _|   | -_|  _|
    #    |_|_|_|___|\_/|___|  |_____|_| |_|_|___|_|
    #
    # Attack another mage's position on the map
    
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

    ["Woodland Target",
        {'element': 'earth', 'pattern': 'blank', 'DISABLE': True,
         'category': 'eye-create',
        }, {
            'cast': "If in a forest, place an Eye in any connected forest location.",
        } ],

    ["Traceback",
        {'element': 'water', 'pattern': 'blank', 'DISABLE': True,
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
        {'element': 'air', 'pattern': 'blank', 'DISABLE': True,
         'category': 'eye-create,eye-move',
        }, {
            'cast': "Create an Eye and then move it 4.",
        } ],
    
    ["Seek",
        {'element': 'air', 'pattern': 'blank', 'DISABLE': True,
         'category': 'eye-move',
        }, {
            'cast': "Move one of your Eyes 2 spaces. If it ends in the same location as another Mage's Eye, then move your Eye to that Mage's location.",
        } ],
    
    ["Gust",
        {'element': 'air', 'pattern': 'blank', 'DISABLE': True,
         'category': 'eye-move',
        }, {
            'cast': "Move your Eyes 6 spaces, split among any number of Eyes.",
        } ],
    
    ["Spread",
        {'element': 'water', 'pattern': 'blank', 'DISABLE': True,
         'category': 'eye-move',
        }, {
            'cast': "Move all your Eyes 3 spaces each.",
        } ],

    ["Bolt",
        {'element': 'fire', 'pattern': 'blank', 'DISABLE': True,
         'category': 'eye-move,mage-other-attack',
        }, {
            'cast': "Move a single Eye 2 spaces and then consume it to Attack 1.",
            'cost': "{{EYE_SACRIFICE}}",
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
        {'element': 'air', 'pattern': 'blank', 'DISABLE': True,
         'category': 'eye-move,eye-other-move',
        }, {
            'cast': "Move one of your Eyes 3 spaces. When moving this Eye into a space, push any Eyes already in that space into an adjacent space.",
        } ],

    ["Control",
        {'element': 'water', 'pattern': 'blank', 'DISABLE': True,
         'category': 'eye-other-move',
        }, {
            'cast': "If you have an Eye in the same location as another Eye (yours or someone else's), then you may move that other Eye 4 spaces.",
            'react': "When another Eye moves into the same space as one of your Eyes, you may immediately cast this spell.",
        } ],

    ["Control Burst",
        {'element': 'water', 'pattern': 'blank', 'DISABLE': True,
         'category': 'eye-other-move',
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
        {'element': 'earth', 'pattern': 'blank', 'companion': True, 'DISABLE': True,
         'category': 'eye-defend',
        }, {
            'cast': "{{ADD_CHARGE}}",
            'react': "You may cast this when one of your Eyes is attacked.",
            'sacrifice': "When you need to remove an Eye, you may instead remove a Charge from this spell.",
        } ],

    #     _____                _____         _           
    #    |     |___ _ _ ___   |  _  |___ ___| |_ ___ ___ 
    #    | | | | . | | | -_|  |     |   |  _|   | . |  _|
    #    |_|_|_|___|\_/|___|  |__|__|_|_|___|_|_|___|_|  
    #                                                    
    # Move Anchor

    ["Move Anchor",
        {'element': 'earth', 'pattern': 'blank', 'DISABLE': True,
         'category': 'anchor-move',
        }, {
            'cast': ["Move one of your Anchors one space.", "You may not move your Anchor adjacent to any existing Anchor."],
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

    ["Turbo Ignis",
        {'element': 'fire', 'pattern': 'blank', 'DISABLE': True,
         'category': 'mage-other-attack',
        }, {
            'cast': "Consume one of your Eyes to Attack 1 at location adjacent to that Eye.",
        } ],

    ["Redirect",
        {'element': 'fire', 'pattern': 'blank', 'DISABLE': True,
         'category': 'mage-other-attack,mage-defend',
        }, {
            'cast': "Attack 1 at one of your Eyes, consuming it.",
            'react': "When attacked, cast to redirect the attack to one of your Eyes.",
        } ],

    ["Wall of Flame",
        {'element': 'fire', 'pattern': 'blank', 'DISABLE': True,
         'category': 'mage-other-attack',
        }, {
            'cast': ["{{ADD_CHARGE}} Choose a single group of 3 connected Eyes that you control.", "Those Eyes cause 1 Damage to any creature as long as this spell is charged and the Eyes are connected. These Eyes move at half speed (rounded down) while they are aflame."],
        } ],

    ["Lavastone",
        {'element': 'fire', 'pattern': 'blank', 'DISABLE': True,
         'category': 'mage-other-attack',
        }, {
            'cast': "Attack 2 at one of your Eyes. Attack 3 if targeting rough terrain or high elevation.",
        } ],

    ["Boost",
        {'element': 'fire', 'pattern': 'blank', 'DISABLE': True,
         'category': 'mage-other-attack',
        }, {
            'cast': "{{ADD_CHARGE}}",
            'sacrifice': "Spend a Charge to increase Attack strength by 1.",
        } ],

    ["Geyser",
        {'element': 'water', 'pattern': 'blank', 'DISABLE': True,
         'category': 'mage-other-attack',
        }, {
            'cast': "Attack 1 at two of your Eyes, consuming one of them.",
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
    # "Vines reach out and form a protective barrier around you before fading back into the ground.",

    ["Deflect",
        {'element': 'earth', 'pattern': 'blank', 'companion': True, 'DISABLE': True,
         'category': 'mage-defend,mage-other-attack',
        }, {
            'cast': "{{ADD_CHARGE}}",
            'react': "When attacked, you may immediately cast this spell.",
            'sacrifice': "Remove a charge to deflect an attack of 1 into a neighboring space.",
        } ],

    ["Reflect",
        {'element': 'fire', 'pattern': 'blank', 'DISABLE': True,
         'category': 'mage-defend,mage-other-attack',
        }, {
            'cast': "Reflect an attack of 1 back at the attacker.",
            'react': "When attacked, you may immediately cast this spell.",
        } ],

    #     _____                 _           
    #    |_   _|___ ___ ___ ___| |_ ___ _ _ 
    #      | | | .'| . | -_|_ -|  _|  _| | |
    #      |_| |__,|  _|___|___|_| |_| |_  |
    #              |_|                 |___|
    # Tapestry modification
    # Remove thread from tapestry. Take another action.
    # Move a thread within the tapestry
    # Recovery shield - Protection shield 1, but:
    #     Charge may be sacrificed to recover 2 threads
    #     If attacked, recover 2 threads

    ["Introspect",
        {'element': 'water', 'pattern': 'blank', 'DISABLE': True,
         'category': 'thread-move',
        }, {
            'cast': "Move a Thread in your Tapestry to another square. If this completes a spell, you may cast it.",
        } ],

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
    # While charged, Eyes represent terrain type

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
