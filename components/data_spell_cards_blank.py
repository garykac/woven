# Spell fragment card data

# Text -> ASCII Art: http://patorjk.com/software/taag/#p=display&f=Rectangles&t=Monster


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

spell_card_blank_data = [

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'tapestry-eye', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'tapestry-mmove', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'tapestry-thread', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'eye-mmove', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'eye-thread', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'mmove-thread', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    # Duplicate to fill 2 pages

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'tapestry-eye', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'tapestry-mmove', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'tapestry-thread', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'eye-mmove', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'eye-thread', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'mmove-thread', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'tapestry-eye', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'tapestry-mmove', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'tapestry-thread', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'eye-mmove', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'eye-thread', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

    ["",
        {'element': 'none', 'pattern': 'blank', 'op': 'mmove-thread', 'vp': 0,
         'category': 'blank',
        }, {
            'cast': "",
        } ],

]
