_unused_ = [

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

    #     _____                _____     _ ___ 
    #    |     |___ _ _ ___   |   __|___| |  _|
    #    | | | | . | | | -_|  |__   | -_| |  _|
    #    |_|_|_|___|\_/|___|  |_____|___|_|_|
    #
    # Move mage

    ["Teleport",
        {'element': 'air', 'category': 'mage-move', 'id': 78, 'pattern': 'E2-31'},
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

    #     _____                _____ _   _           
    #    |     |___ _ _ ___   |     | |_| |_ ___ ___ 
    #    | | | | . | | | -_|  |  |  |  _|   | -_|  _|
    #    |_|_|_|___|\_/|___|  |_____|_| |_|_|___|_|
    #
    # Attack by moving another player's mage
                                                                         
    ["Teleport Random",
        {'element': 'fire', 'category': 'mage-other-move', 'id': 95, 'pattern': 'E2-8'},
        {
            'cast': "Move all mages at one of your EYEs to a random star location. Consume that EYE.",
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

    #     _____                _____         
    #    |     |___ _ _ ___   |   __|_ _ ___ 
    #    | | | | . | | | -_|  |   __| | | -_|
    #    |_|_|_|___|\_/|___|  |_____|_  |___|
    #                               |___|
    #
    # Move one of your Eyes on the map
    
    ["Diasporate",
        {'element': 'water', 'category': 'eye-create,eye-move', 'id': 77, 'pattern': 'EE2-2'},
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

    ["Whirlwind",
        {'element': 'air', 'category': 'eye', 'id': 13},
        ["Place CHARGE on this spell.", "-", "While CHARGEd, all EYEs you control are obstacles that other mages may not move into or pass through."] ],

    ["Delete All 2",
        {'element': 'earth', 'category': 'eye,attack', 'id': 43},
        ["When in a location with a EYE controlled by another mage, remove all of that mage's EYEs.", "-", "If multiple mages, choose one."] ],

    ["Distraction",
        {'element': 'fire', 'category': 'eye', 'id': 34},
        ["When in the same location as a EYE controlled by another mage, remove any one of their EYEs."] ],

    ["Delete",
        {'element': 'fire', 'category': 'eye-other-attack', 'id': 43, 'pattern': 'E1-2'},
        {
            'cast': "Remove all opponent EYEs at one of your EYE's location. Consume this EYE.",
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

    ["Ricochet Blast",
        {'element': 'fire', 'category': 'mage-other-attack', 'id': 24, 'pattern': 'E1-5'},
        {
            'cast': "Attack 1 at location adjacent to one of your EYEs. Consume that EYE.",
        } ],

    ["Fire Reign",
        {'element': 'fire', 'category': 'mage-other-attack', 'id': 26, 'pattern': 'E2-27'},
        {
            'cast': "Attack 1 at all of your EYEs. Consume all of your EYEs except one.",
        } ],

    ["Hands of Flame",
        {'element': 'fire', 'category': 'mage-move,mage-other-attack', 'id': 63, 'pattern': 'EE2-6'},
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

    #     ____      ___           _      _____ _____ 
    #    |    \ ___|  _|___ ___ _| |    |  |  |  _  |
    #    |  |  | -_|  _| -_|   | . |    |     |   __|
    #    |____/|___|_| |___|_|_|___|    |__|__|__|
    #
    # Defend against being attacked

    ["Stone Reflection",
        {'element': 'earth', 'category': 'mage-defend,mage-other-attack', 'id': 88, 'pattern': 'E2-4'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "You take 1/2 damage (rounded down) from attacks. Full attack damage is reflected back at your attacker.",
        } ],

    ["Double Shield",
        {'element': 'earth', 'category': 'mage-defend', 'id': 36, 'pattern': 'E2-13'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "Defend 2.",
        } ],

    ["Eye Coil",
        {'element': 'water', 'category': 'mage-defend', 'id': 81, 'pattern': 'E2-22'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "If you are in the same location as one of your EYEs, that EYE acts as a shield to Defend 2.",
        } ],

    ["Deflect",
        {'element': 'water', 'category': 'mage-defend,mage-other-attack,eye-other-attack', 'id': 80, 'pattern': 'E2-25'},
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

    #     _____                 _           
    #    |_   _|___ ___ ___ ___| |_ ___ _ _ 
    #      | | | .'| . | -_|_ -|  _|  _| | |
    #      |_| |__,|  _|___|___|_| |_| |_  |
    #              |_|                 |___|
    #
    # Tapestry modification
    # Spell: Remove thread from tapestry. Take another action.

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

    ["Recovery Shield",
        {'element': 'earth', 'category': 'mage-defend,modify-tapestry', 'id': 82, 'pattern': 'E2-39'},
        {
            'cast': "{{ADD_CHARGE}}",
            'charged': "Defend 1",
            'sacrifice': "During your turn, you may choose to remove a CHARGE from this spell to recover 2 mana from your TAPESTRY into your MANA POOL.",
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
