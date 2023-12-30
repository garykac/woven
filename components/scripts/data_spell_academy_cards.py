# Woven Academy spell card data

spell_card_revision = 15

spell_card_data = [
    ["Haste",
        {'element': 'air', 'pattern': 'E2-5', 'range': '01', 'class': "invc220",
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': "Target moves 2 spaces",
        } ],
    ["Migrate",
        {'element': 'fire', 'pattern': 'E2-40', 'range': '01', 'class': "invc220",
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': "Two different targets move 1 space each.",
        } ],
    ["Sproing",
        {'element': 'earth', 'pattern': 'E2-59', 'range': '12', 'class': "invc220",
        }, {
            'target': "{{TEAMMATE}}",
            'cast': "Targetted ally is magically grabbed and tossed to the corresponding space on the opposite side of your location.",
        } ],
    ["Teleport",
        {'element': 'water', 'pattern': 'E2-28', 'range': '0', 'class': "invc220",
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': "Target jumps instantly to an ally's position, bypassing any walls or barriers.",
        } ],

    ["Redirect",
        {'element': 'air', 'pattern': 'E2-8', 'range': '01', 'class': "abjr322",
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': "A large cudgel appears over the target which will deflect an incoming attack, splitting it into 2 separate attacks against foes in the target's location.",
        } ],
    ["Glowing Sphere",
        {'element': 'fire', 'pattern': 'E2-12', 'range': '0', 'class': "abjr322",
        }, {
            'target': "{{MAGE_LOCATION}}",
            'cast': [
            	"A protective sphere surrounds you and anyone else in your location you choose to include.",
            	"Foes must attack it twice to dispel it.",
            ],
        } ],
    ["Wall",
        {'element': 'earth', 'pattern': 'E2-6', 'range': '0', 'class': "abjr322",
        }, {
            'target': "{{PASSAGE_BETWEEN_ROOMS}}",
            'cast': [
            	"A stone barrier rises from the earth in the passage between your room and a neighboring one (your choice), blocking all movement and attacks.",
            	"The barrier can withstand 2 hits before dissipating.",
            ],
        } ],
    ["Mana Shield",
        {'element': 'water', 'pattern': 'E2-32', 'range': '01', 'class': "abjr322",
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': [
                "Target gains false mana that can be sacrificed instead of actual mana when attacked.",
                "This false mana cannot be used to cast spells.",
            ],
        } ],

    ["Push",
        {'element': 'air', 'pattern': 'E2-14', 'range': '01', 'class': "invc301",
        }, {
            'target': "{{OPPONENT}}",
            'cast': "Target is pushed 2 spaces.",
        } ],
    ["Fireball",
        {'element': 'fire', 'pattern': 'E2-35', 'range': '012', 'class': "invc301",
        }, {
            'target': "{{OPPONENT}}",
            'cast': "Great balls of fire appear above the targetted foe and attack.",
        } ],
    ["Trap",
        {'element': 'earth', 'pattern': 'E2-30', 'range': '01', 'class': "invc301",
        }, {
            'target': "{{ROOM_OR_NEXT}}",
            'cast': [
            	"Lay a trap in your current location or a neighboring one.",
            	"Trap attacks the next foe that enters the room. Or immediately if there is already a foe in the room.",
            ],
        } ],
    ["Icicle Darts",
        {'element': 'water', 'pattern': 'E2-27', 'range': '012', 'class': "invc301",
        }, {
            'target': "{{OPPONENT}}",
            'cast': "Icicles form in the air around the target and attack.",
        } ],

    ["Fly",
        {'element': 'air', 'pattern': 'E2-15', 'range': '01', 'class': "trns341",
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': "Target grows wings and moves 2 spaces, bypassing any walls or barriers.",
        } ],
    ["Flaming Talons",
        {'element': 'fire', 'pattern': 'E2-44', 'range': '012', 'class': "trns341",
        }, {
            'target': "{{OPPONENT}}",
            'cast': "Your hands turn into giant flaming claws that shoot out to attack the target.",
        } ],
    ["Stallion",
        {'element': 'earth', 'pattern': 'E2-1', 'range': '01', 'class': "trns341",
        }, {
            'target': "{{SELF_OR_TEAMMATE}}",
            'cast': [
            	"Target grows extra legs which allow them to move 2 spaces, picking up or dropping off allies at any time during the move.",
            	"Not quite a centaur, but disturbingly similar.",
            ],
        } ],
    ["Cobra",
        {'element': 'water', 'pattern': 'E2-31', 'range': '012', 'class': "trns341",
        }, {
            'target': "{{OPPONENT}}",
            'cast': "You bite or spit (depending on the distance) venom to attack the target.",
        } ],

]
