# Woven Academy spell card data

spell_card_revision = 17

spell_card_data = [

    #   _____                           _   
    #  |     |___ _ _ ___ _____ ___ ___| |_ 
    #  | | | | . | | | -_|     | -_|   |  _|
    #  |_|_|_|___|\_/|___|_|_|_|___|_|_|_|  
    #

    ["Haste",
        {'element': 'air', 'pattern': 'E2-5', 'range': '01', 'syms': 'aa', 'op': 'gen',
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': "Target moves 2 spaces",
        } ],
    ["Migrate",
        {'element': 'fire', 'pattern': 'E2-40', 'range': '01', 'syms': 'bb', 'op': 'gen',
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': [
                "Two different targets move 1 space each.",
                "-",
                "If solo: Move 2 spaces.",
            ],
        } ],
    ["Push-pull",
        {'element': 'earth', 'pattern': 'E2-59', 'range': '012', 'syms': 'ace', 'op': 'combine',
        }, {
            'target': "{{TEAMMATE_OR_OPPONENT}}",
            'cast': [
                "You anchor yourself and push/pull the target up to 2 spaces.",
                "-",
                "OR",
                "-",
                "Anchor the target and pull yourself to their location.",
            ],
        } ],
    ["Blink",
        {'element': 'water', 'pattern': 'E2-28', 'range': '0', 'syms': 'dd', 'op': 'gen',
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': [
                "Target teleports (bypassing any walls or barriers) instantly to either:",
                " • an ally's position, or",
                " • a room exactly 3 spaces away.",
            ],
        } ],

    #   ____      ___                 
    #  |    \ ___|  _|___ ___ ___ ___ 
    #  |  |  | -_|  _| -_|   |_ -| -_|
    #  |____/|___|_| |___|_|_|___|___|
    #

    ["Redirect",
        {'element': 'air', 'pattern': 'E2-8', 'range': '01', 'syms': 'ab', 'op': 'or2',
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': [
                "A large cudgel appears over the target which will deflect a single incoming attack, redirecting it to attack a foe in the target's location.",
                "-",
                "Dispels at end of turn.",
            ],
        } ],
    ["Glowing Sphere",
        {'element': 'fire', 'pattern': 'E2-12', 'range': '0', 'syms': 'bde', 'op': 'combine',
        }, {
            'target': "{{MAGE_LOCATION}}",
            'cast': [
                "A protective sphere surrounds you and anyone else in your location you choose to include, blocking incoming and outgoing attacks.",
                "-",
                "Dispels at end of turn or if attacked twice.",
            ],
        } ],
    ["Stonewall",
        {'element': 'earth', 'pattern': 'E2-6', 'range': '0', 'syms': 'ad', 'op': 'or2',
        }, {
            'target': "{{PASSAGE_BETWEEN_ROOMS}}",
            'cast': [
                "A stone barrier rises from the earth in the passageway between your room and a neighboring one, blocking all movement and attacks.",
                "-",
                "The barrier remains until it is attacked.",
            ],
        } ],
    ["Faux Mana",
        {'element': 'water', 'pattern': 'E2-32', 'range': '01', 'syms': 'bc', 'op': 'or2',
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': [
                "Target gains false mana that can be sacrificed instead of actual mana when attacked.",
                "-",
                "This false mana cannot be used to cast spells.",
            ],
        } ],

    #   _____ _   _           _   
    #  |  _  | |_| |_ ___ ___| |_ 
    #  |     |  _|  _| .'|  _| '_|
    #  |__|__|_| |_| |__,|___|_,_|
    #

    ["Bodyslam",
        {'element': 'air', 'pattern': 'E2-14', 'range': '01', 'syms': 'bd', 'op': 'or2',
        }, {
            'target': "{{OPPONENT}}",
            'cast': "Two targets in the same location are lifted into the air and smacked into each other, causing an attack to each.",
        } ],
    ["Fireball",
        {'element': 'fire', 'pattern': 'E2-35', 'range': '012', 'syms': 'cd', 'op': 'or2',
        }, {
            'target': "{{OPPONENT}}",
            'cast': [
                "Great balls of fire fly from your outstretched palms to attack the targetted foe.",
                "-",
                "If current element includes Fire, then a 2nd foe along the fireball's path (different rooms) may be targeted.",
            ],
        } ],
    ["Trap",
        {'element': 'earth', 'pattern': 'E2-30', 'range': '01', 'syms': 'abf', 'op': 'combine',
        }, {
            'target': "{{ROOM_OR_NEXT}}",
            'cast': [
                "Lay a trap in your current location or a neighboring one.",
                "-",
                "Trap attacks the next foe that enters the room. Or immediately if there is already a foe in the room.",
            ],
        } ],
    ["Icicle Darts",
        {'element': 'water', 'pattern': 'E2-27', 'range': '012', 'syms': 'cc', 'op': 'gen',
        }, {
            'target': "{{OPPONENT}}",
            'cast': [
                "Icicles form in the air above the target and strike downward to attack.",
                "-",
                "If current element includes Water, then 2 foes in the same location may be targeted.",
            ],
        } ],

    #   _____                 ___               
    #  |_   _|___ ___ ___ ___|  _|___ ___ _____ 
    #    | | |  _| .'|   |_ -|  _| . |  _|     |
    #    |_| |_| |__,|_|_|___|_| |___|_| |_|_|_|
    #

    ["Dive Bomb",
        {'element': 'air', 'pattern': 'E2-15', 'range': '0', 'syms': 'ade', 'op': 'combine',
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': [
                "Target transforms into a falcon and dives into a room 2 spaces away, bypassing any walls or barriers.",
                "-",
                "Choose one:",
                "• Attack 1 foe in that room, or",
                "• Screech to freeze 2 creatures in room (so they can't move or attack).",
            ],
        } ],
    ["Burning Tyger",
        {'element': 'fire', 'pattern': 'E2-44', 'range': '0', 'syms': 'bcf', 'op': 'combine',
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': [
                "Target transforms into a tyger and attacks a foe with brightly burning claws.",
                "-",
                "Before attack, target may optionally teleport (bypassing walls or barriers) to:",
                "• an ally's location, or",
                "• exactly 2 spaces away."
            ],
        } ],
    ["Trample",
        {'element': 'earth', 'pattern': 'E2-1', 'range': '0', 'syms': 'ac', 'op': 'or2',
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': "Target transforms into a stallion and charges into a neighboring room to trample-attack a foe there.",
        } ],
    ["Black Fang",
        {'element': 'water', 'pattern': 'E2-31', 'range': '0', 'syms': 'cdf', 'op': 'combine',
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': [
                "Target transforms into a giant cobra.",
                "-",
                "Choose one:",
                "• Slither into a neighboring space, or",
                "• Bite-attack a foe in current location.",
                "• Hiss to frighten all foes in room (move them into a neighboring room).",
            ],
        } ],

]
