#!/bin/bash

# Map tiles
python create_map.py --load ../maps/map_data.csv

# Tapestry cards
python create_tapestry_cards.py --png

# Spell cards
python create_spell_cards.py --summary --png

# Regenerate 9-up PDFs for spell cards. Script must be run from subdir.
(cd ../spell-cards/9up && ./build.sh)
