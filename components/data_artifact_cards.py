# Artifact card data

_descriptions = {
    'description*': "Pull 1 Thread back into your Mana Pool.",
    'description*': "Move 2 Threads to new locations in your Tapestry.",
    'description*': "Duplicate an Eye and move it 3 spaces.",
    'description*': "Move all your Eyes 2 spaces each.",
    'description*': "Move 5 at the same elevation.",
    'description*': "Move 5 through forest.",
    'description*': "Move 5 along a river.",
    'description*': "Anchor one of your Eyes.",
    'description*': "Remove all Eyes within 2 spaces of an Eye. Un-anchor any Anchored Eyes within that range. Consume that Eye.",
    'description*': "Attack 1 at one of your Eyes. Consume that Eye.",
    'description*': "Attack 1 adjacent to one of your Eyes. Consume that Eye.",
    'description*': "Defend 2 when Active. May be played from hand when attacked.",
    'description*': "While active, you cannot be detected by creatures.",
    'description*': "You may cross over rivers with no movement penalty.",
    'description*': "You may change elevation with no movement penalty.",
    'description*': "Draw an extra Spell card into your hand.",
    'description': "Move an Eye 5 spaces.",
    'description': "You may enter rough terrain with no movement penalty.",
}
_bonuses = {
    'bonus*': "+1 for each set of 2 diagonally adjacent Air in Tapestry.",
    'bonus*': "+1 for each set of 2 diagonally adjacent Earth in Tapestry.",
    'bonus*': "+1 for each set of 2 orthogonally adjacent Fire in Tapestry.",
    'bonus*': "+1 for each set of 2 orthogonally adjacent Water in Tapestry.",
    'bonus*': "+1 for every 2 squares in your Tapestry orthogonally adjacent to Air.",
    'bonus*': "+1 for every 2 squares in your Tapestry orthogonally adjacent to Earth.",
    'bonus*': "+1 for every 2 squares in your Tapestry diagonally adjacent to Fire.",
    'bonus*': "+1 for every 2 squares in your Tapestry diagonally adjacent to Water.",
    'bonus*': "+1 VP for every 2 Air spells in your Spell or Treasure decks.",
    'bonus*': "+1 VP for every 2 Earth spells in your Spell or Treasure decks.",
    'bonus*': "+1 VP for every 2 Fire spells in your Spell or Treasure decks.",
    'bonus*': "+1 VP for every 2 Water spells in your Spell or Treasure decks.",
    'bonus*': "+1 for every set of 4 elements in your Tapestry.",
    'bonus*': "+1 for every 2x2 block of 4 element symbols (regardless of type) in your Tapestry. Each symbol may only contribute to a single 2x2 block.",
    #'bonus': "If you successfully attack another player while The Blade is active, you win instantly.",
}


artifact_card_data = [

    ["Amulet of Mental Acuity",
        {'op': 'action-action', 'vp': 2,
         'description': "Pull 1 Thread back into your Mana Pool",
         'bonus': "+1 for each set of 2 adjacent Water in Tapestry",
         'flavor': "",
        } ],

    ["Visbeth's Eye",
        {'op': 'action-action', 'vp': 2,
         'description': "You may change elevation with no movement penalty.",
         'bonus': "+1 for every set of 4 elements in Tapestry",
         'flavor': "Always watching",
        } ],

    ["Grizelia's Left Boot of Binding",
        {'op': 'action-action', 'vp': 2,
         'description': "Move 5 at the same elevation.",
         'bonus': "+1 VP for every 2 Earth spells in your Spell or Treasure decks.",
         'flavor': "",
        } ],

    ["Mirror of the Abyss",
        {'op': 'action-action', 'vp': 2,
         'description': "Move 2 Threads to new locations in your Tapestry.",
         'bonus': "+1 for every 2 squares in your Tapestry diagonally adjacent to Water.",
         'flavor': "",
        } ],

    ["Ring of the Infernal Queen",
        {'op': 'action-action', 'vp': 2,
         'description': "Duplicate an Eye and move it 3 spaces.",
         'bonus': "+1 VP for every 2 Water spells in your Spell or Treasure decks.",
         'flavor': "",
        } ],

    ["Blade of the Dark Flame",
        {'op': 'action-action', 'vp': 2,
         'description': "Attack 1 adjacent to one of your Eyes. Consume that Eye.",
         'bonus': "+1 for each set of 2 orthogonally adjacent Fire in Tapestry.",
         'flavor': "",
        } ],

    ["Book of Divine Contemplation",
        {'op': 'action-action', 'vp': 2,
         'description': "Draw an extra Spell card into your hand.",
         'bonus': "+1 for every 2x2 block of 4 element symbols (regardless of type) in your Tapestry. Each symbol may only contribute to a single 2x2 block.",
         'flavor': "",
        } ],

    ["Chimera Mask",
        {'op': 'action-action', 'vp': 2,
         'description': "Move all your Eyes 2 spaces each.",
         'bonus': "+1 for every 2 squares in your Tapestry orthogonally adjacent to Air.",
         'flavor': "",
        } ],

    ["Orb of Midnight Neverending",
        {'op': 'action-action', 'vp': 2,
         'description': "Remove all Eyes within 2 spaces of an Eye. Un-anchor any Anchored Eyes within that range. Consume that Eye.",
         'bonus': "+1 VP for every 2 Fire spells in your Spell or Treasure decks.",
         'flavor': "",
        } ],

    ["Glowspider Necklace",
        {'op': 'action-action', 'vp': 2,
         'description': "Anchor one of your Eyes.",
         'bonus': "+1 for each set of 2 diagonally adjacent Earth in Tapestry.",
         'flavor': "",
        } ],

    ["Key of the Marked Guardian",
        {'op': 'action-action', 'vp': 2,
         'description': "Attack 1 at one of your Eyes. Consume that Eye.",
         'bonus': "+1 for every 2 squares in your Tapestry diagonally adjacent to Fire.",
         'flavor': "",
        } ],

    ["Lamp of Endless Dawn",
        {'op': 'action-action', 'vp': 2,
         'description': "Defend 2 when Active. May be played from hand when attacked.",
         'bonus': "+1 for every 2 squares in your Tapestry orthogonally adjacent to Earth.",
         'flavor': "",
        } ],

    ["Cloak of the Watcher",
        {'op': 'action-action', 'vp': 2,
         'description': "Move 5 through forest.",
         'bonus': "+1 VP for every 2 Air spells in your Spell or Treasure decks.",
         'flavor': "",
        } ],

    ["The Elder's Heart",
        {'op': 'action-action', 'vp': 2,
         'description': "Move 5 along a river.",
         'bonus': "+1 for every set of 4 elements in your Tapestry.",
         'flavor': "",
        } ],

    ["Cloak of Concealment",
        {'op': 'action-action', 'vp': 2,
         'description': "While active, you cannot be detected by creatures.",
         'bonus': "+1 for each set of 2 diagonally adjacent Air in Tapestry.",
         'flavor': "Protection from Detection",
        } ],

    ["Boots of Waterwalking",
        {'op': 'action-action', 'vp': 2,
         'description': "You may cross over rivers with no movement penalty.",
         'bonus': "+1 VP for every 2 Water spells",
         'flavor': "",
        } ],

    # Special Abilities:
    # Hold more cards in hand. Draw more cards into hand.
    
    # Items:
    # Amulet, Ark, Armor, Arrow, Axe
    # Blade, Bolt, Book, Boots, Bottle, Bow,
    #   Bracelet, Bracer, Brooch, Broom, Buckler
    # Cap, Carapace, Chalice, Charm, Claw, Cleaver, Cloak, Club,
    #   Codex, Collar, Concoction, Coronet, Crown, Crossbow, Cup
    # Dagger, Draught
    # Egg, Elixir, Essence, Eye
    # Fang, Flask, Flute
    # Gauntlet, Glaive, Globe, Glove, Grimoire
    # Hammer, Hand, Heart, Helm, Helmet, Horn, Hourglass
    # Idol
    # Jar
    # Key
    # Lamp, Lance, Leviathan, Locket, Longbow
    # Mace, Manual, Mask, Medallion, Mirror
    # Necklace, Needle
    # Obelisk, Ointment, Orb
    # Paw, Pendant, Potion, Prism
    # Quiver
    # Ring, Robe, Rod, Rope
    # Sarcophagus, Scale, Sceptor, Scroll, Scythe,
    #   Shade, Shard, Shield, Sickle, Sigil, Skull,
    #   Spark, Spear, Sphere, Staff, Statue, Stone, Sword
    # Talisman, Tear, Thorn, Tiara, Token, Tome, Tonic
    # Urn
    # Veil, Vestments
    # Wand, Ward, Whip

    # Adj:
    # Abyss, Absorption, Adamantine, Ancient,
    #   Annihiliation, Anti, Arcane, Arch, Autumn
    # Balanced, Binding, Black, Blessed, Blood, Blur,
    #   Bond, Boon, Bottled, Brass, Brew, Burrowing
    # Chain, Champion, Chimera, Clear, Cobalt,
    #   Command, Concealing, Control, Cunning, Cursed
    # Damned, Dark, Dawn, Death, Defender, Devil, Dimension,
    #   Discord, Disguise, Dispel, Divine, Doom, Dragon, Dread
    # Ebony, Elder, Eldritch, Elemental,
    #   Endless, Endurance, Energy, Entanglement, Entrapment, Eternal,
    #   Ever, Exalted, Excavation, Expedient, Expeditious, Explosive
    # Faceless, Faerie, Fairy, Famine, Fey, Fidelity, Fiend, Fire, First,
    #   Flame, Flare, Fortitude, Frost, Fury
    # Gentle, Giant, Glass, Glowing, Gold, Great, Guardian
    # Hallowed, Healing, Hell, High, Holy, Horns, Howling
    # Ice, Illusion, Incarnate, Infection,
    #   Infernal, Infinite, Intuition, Invulnerable, Iron
    # King
    # Lash, Last, Light, Lightning, Lord, Luck, Lunar
    # Magi, Major, Mark, Meld, Midnight, Might, Mind,
    #   Minor, Moon, Moonlight, Morph, Mutate
    # Necromancer, Never-ending, Night
    # Ocean, Omniscience, Order
    # Peace, Perpetual, Plentiful, Portal,
    #   Powdered, Power, Prismatic, Psychic, Pure
    # Queen
    # Razor, Recall, Refreshing, Rejuvenation,
    #   Removal, Rend, Replenishment, Retribution, Ripper, Ruby
    # Scorpion, Secret, Seeker, Seering, Shadow, Shatter, Shielding,
    #   Silver, Slayer, Sleep, Song, Sorrow, Soul, Spawn,
    #   Spectral, Spider, Spirit, Splendor, Spring, Stability, Star,
    #   Starlight, Steal, Stoic, Stoneskin, Storm, Strength, Summer, Sun
    # Thunder, Time, True
    # Umber, Unbreakable, Unending, Unraveling, Unrelenting
    # Vanguard, Vigor, Vile, Vision, Vitriolic, Void
    # Weeping, Whisper, Winter, Wisdom, Witch, Wrath, Wretched
    
    # Animals/Monsters:
    # Bear, Bull
    # Cat, Crow
    # Eagle
    # Fox
    # Goblin
    # Owl
    # Rat, Raven
    # Troll
]

