#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import getopt
import os
import platform
import subprocess
import sys

from svg_card_gen import SVGCardGen

from svg import SVG, Style, Node

from data_spell_academy_cards import spell_card_data
from data_spell_academy_cards import spell_card_revision

from data_spell_patterns import spell_card_patterns

from inkscape import Inkscape, InkscapeActions

elem_map = {
    'a': 'air',
    'e': 'earth',
    'f': 'fire',
    'w': 'water',
}

# Spell attributes
spell_attributes = [
    'element', 'pattern', 'id', 'syms', 'starter', 'flavor',
]

SYMBOLS = "acefgwy"

OUTPUT_DIR = os.path.join('..', 'spell-academy-cards')
CARD_TEMPLATE = os.path.join(OUTPUT_DIR, 'spell-template.svg')
PDF_8UP_DIR = os.path.join(OUTPUT_DIR, '8up')

class WovenSpellCards():
    
    def __init__(self, options):
        self.next_id = 0
        self.name2id = {}
        self.pattern_elements = {}
        self.elements = {}
        self.id2name = {}
        self.id2pattern = {}
        self.id2attrs = {}
        self.pattern2id = {}
        self.max_id = 0
        self.blank_count = 0
                
        self.valid_elements = ['none', 'air', 'fire', 'earth', 'water']

        # Poker size cards: 2.5" x 3.5" = 225px x 315px = 63.5mm x 88.9mm
        # Bridge size cards: 2.25" x 3.5" = 202.5px x 315px
        self.width = 63.5
        self.height = 88.9
        options['width'] = self.width
        options['height'] = self.height
        
        # Set data for SVGCardGen.
        self.card_gen = SVGCardGen(self, options)

        # Initialize card patterns.
        self.card_patterns = spell_card_patterns
        self.validate_patterns()

        
    #
    # DATA VALIDATION
    #
    
    # Make sure every pattern ID has an entry.
    def validate_patterns(self):
        simple = ['blank', 'N1']
        ranges = [
            ['N2', 9],
            ['N3', 5],
            ['E1', 9],
            ['E2', 162],
            ['E3', 34],
            ['EE1-1', 3],
            ['EE1-2', 4],
            ['EE1-3', 5],
            ['EE2-1', 14],
            ['EE2-2', 21],
            ['EE2-3', 25],
        ]
        for key in simple:
            self.check_pattern(key)
        for r in ranges:
            base = r[0]
            max = r[1]
            for i in range(1, max+1):
                self.check_pattern('{0:s}-{1:d}'.format(base, i))
            # Check one beyond the last to verify the ranges are correct.
            id = '{0:s}-{1:d}'.format(base, max+1)
            if id in self.card_patterns:
                raise Exception('Pattern id not in valid range: {0:s}-{1:d}'
                                .format(base, max+1))

    def check_pattern(self, id):
        if not id in self.card_patterns:
            raise Exception("Pattern {0}: Not found".format(id))
        pattern = self.card_patterns[id]['pattern']
        
        first_row = True
        num_cols = 0
        for row in pattern:
            cols = row.split()
            if first_row:
                num_cols = len(cols)
                first_row = False
            if len(cols) != num_cols:
                raise Exception("Pattern {0}: Mismatch number of columns in pattern"
                                .format(id))
        
    def pattern_key(self, pattern):
        """Convert pattern array into a simple string that can be used as a key."""
        return '/'.join([''.join(x.split()) for x in pattern])

    def validate_attrs(self, name, attrs):
        # Ensure all attributes are valid.
        for attr in attrs.keys():
            if not attr in spell_attributes:
                raise Exception("{0:s}: Unknown attribute: {1:s}".format(name, attr))
            
        if name in self.name2id:
            raise Exception("{0:s}: Spell name already used by spell ID {1}"
                            .format(name, str(self.name2id[name])))

        if not 'element' in attrs:
            raise Exception("{0:s}: Missing 'element' attribute".format(name))
        if not attrs['element'] in self.valid_elements:
            raise Exception("{0:s}: Invalid element: {1}"
                            .format(name, attrs['element']))
        
        if not 'id' in attrs:
            raise Exception("{0:s}: Missing 'id' attribute".format(name))
        if attrs['id'] in self.id2name:
            raise Exception("{0} ID {1} already used by {2}"
                            .format(name, str(attrs['id']), self.id2name[attrs['id']]))
        
        if not 'pattern' in attrs:
            raise Exception("{0:s}: Missing 'pattern' attribute".format(name))
        if not attrs['pattern'] in self.card_patterns:
            raise Exception("{0:s}: Invalid pattern: {1}".format(name, attrs['pattern']))

        
    #
    # CARD GENERATION
    #

    def generate_cards(self):
        self.card_gen.generate_cards()

    # Returns an iterator that produces an object for each card.
    # This is a callback used by SVGCardGen
    def card_data(self):
        for card in spell_card_data:  #spell_card_blank_data:
            attrs = card[1]
            if 'DISABLE' in attrs:
                continue
        
            # Auto-assign ids
            self.next_id += 1
            attrs['id'] = self.next_id
            yield card

    # Params:
    #   |metadata| - card and file index
    #   |card_data| - data for current card
    #   |svg| - the SVG manager
    #
    # callback from SVGCardGen
    def process_card_data(self, metadata, card_data):
        (svg, svg_group) = self.card_gen.pre_card()
        self.draw_spell_card(metadata, card_data, svg, svg_group)
        self.card_gen.post_card()

    # Params:
    #   |metadata| - card and file index
    #   |card_data| - data for current card
    #   |svg| - the SVG manager
    #   |svg_group| - the svg group node where this card should be added
    def draw_spell_card(self, metadata, card, svg, svg_group):
        id = metadata['id']
        name = card[0]
        attrs = card[1]

        # Validate attributes
        self.validate_attrs(name, attrs)
        pattern_id = attrs['pattern']
        pattern = self.card_patterns[pattern_id]['pattern']
        
        # Make sure pattern is not being re-used.
        if pattern_id != 'blank':
            pe_tag = self.pattern_key(pattern)
            if True:  # If we want to allow different elements to share the same pattern.
                pe_tag += '-' + attrs['element']
            if pe_tag in self.pattern_elements:
                raise Exception(f"Pattern {pattern_id} for '{name}' already used for '{self.pattern_elements[pe_tag]}'")
            self.pattern_elements[pe_tag] = name

        # Verify pattern matches spell element
        element = attrs['element']
        pelem_data = self.card_patterns[pattern_id]['elements']
        pelems = []
        if pelem_data == "none":
            pelems.append("none")
        else:
            pelems = [elem_map[p] for p in pelem_data]
        if pattern_id != 'blank' and not element in pelems:
            raise Exception("{0:s}: Spell pattern does not match element {1:s}"
                  .format(name, element))

        # Build list of template ids and then load from svg file.
        svg_ids = []
        svg_ids.extend(['element-{0}'.format(elem_map[e]) for e in elem_map])
        svg_ids.append('card-border')
        svg_ids.append('spell-title')
        svg_ids.append('spell-pattern-border')
        svg_ids.append('spell-pattern-border-4')
        svg_ids.append('spell-description')
        svg_ids.append('spell-description-4')
        svg_ids.append('spell-flavor')
        svg_ids.append('starter-info')
        #svg_ids.append('class-name')
        #svg_ids.extend(['sidebar-{0}'.format(x) for x in ['hex', 'dots', 'circles', 'diamonds']])
        #svg_ids.append('sidebar-clip')
        #svg_ids.append('spell-info')
        svg_ids.append('rev-id')
        svg_ids.append('spell-id')
        svg_ids.append('spell-id-border')
        #svg_ids.append('range-cards')
        #svg_ids.extend(['range-{0}'.format(x) for x in range(3)])
        #for x in list(SYMBOLS):
        #    svg_ids.append(f'{x}-master')
        svg_ids.extend([f'{x}-master' for x in list(SYMBOLS)])
        svg_ids.append('sym-master-extra')

        svg.load_ids(CARD_TEMPLATE, svg_ids)

        # Add Element and category masters (hidden, used for cloning).
        g_masters = SVG.group('masters')
        g_masters.set_style("display:none")
        SVG.add_node(svg_group, g_masters)
        for (e,elem) in elem_map.items():
            svg.add_loaded_element(g_masters, f"element-{elem}")
        for sym in list(SYMBOLS):
            svg.add_loaded_element(g_masters, f"{sym}-master")
        svg.add_loaded_element(g_masters, f"sym-master-extra")

        svg.add_loaded_element(svg_group, 'card-border')

        # Draw spell title.
        title = svg.add_loaded_element(svg_group, 'spell-title')
        SVG.set_text(title, name)

        #if 'flavor' in attrs:
        #    flavor = svg.add_loaded_element(svg_group, 'spell-flavor')
        #    SVG.set_text(flavor, attrs['flavor'])

        # Draw starter info on starter cards.
        if 'starter' in attrs:
            starter = svg.add_loaded_element(svg_group, 'starter-info')
            SVG.set_text(starter, f"STARTER - {attrs['starter'].capitalize()}")

        # Draw spell id.
        revision_text = svg.add_loaded_element(svg_group, 'rev-id')
        SVG.set_text(revision_text, f"{spell_card_revision}")
        id_text = svg.add_loaded_element(svg_group, 'spell-id')
        SVG.set_text(id_text, f"{attrs['id']}")
        svg.add_loaded_element(svg_group, 'spell-id-border')
		
        # Add spell pattern/description placeholder based on spell pattern height.
        if len(pattern) == 4:
            svg.add_loaded_element(svg_group, 'spell-pattern-border-4')
            spellDesc = svg.add_loaded_element(svg_group, 'spell-description-4')
        else:
            svg.add_loaded_element(svg_group, 'spell-pattern-border')
            spellDesc = svg.add_loaded_element(svg_group, 'spell-description')
        #spellInfo = svg.add_loaded_element(svg_group, 'spell-info')

        syms = attrs['syms']
        symCount = len(syms)
        symOffset = -(7*(symCount-1))
        symDelta = 14
        for s in syms:
            #svg.add_loaded_element(svg_group, f'{s}-master')
            eleclone = SVG.clone(0, f"#{s}-master", symOffset, 0)
            symOffset += symDelta
            SVG.add_node(svg_group, eleclone)

        # Draw description/pattern.
        self.draw_pattern(pattern_id, pattern, element, svg_group)

    def draw_pattern(self, id, pattern_raw, element, svg_group):        
        pattern = [x.split() for x in pattern_raw]
        pheight = len(pattern)
        if pheight == 0:
            raise Exception("Missing pattern for {0}".format(id))
        if pheight > 4:
            raise Exception("Tall pattern for {0}".format(id))
        pwidth = len(pattern[0])

        # Size and spacing for each box in pattern.
        box_size = 7.5
        box_spacing = 9

        # Max pattern width that fits on the card.
        max_width = 7
        # Center of pattern area.
        pcenter_x = (self.width / 2)
        # Upper left corner of pattern area
        px0 = pcenter_x - (((max_width-1) * box_spacing) + box_size) / 2
        # Adjust offsets to center the patterns horizontally.
        if pwidth % 2 == 0:
            px0 += box_spacing / 2
            max_width = 6

        # Tall spells need to use larger pattern area.
        max_height = pheight
        if pheight == 4:
            pcenter_y = 23.9 + 6.4
        else:
            pcenter_y = 23.9 + 2.1
        py0 = pcenter_y - (((max_height-1) * box_spacing) + box_size) / 2

        dot_x0 = px0 + (box_size / 2)
        dot_y0 = py0 + (box_size / 2)

        # The x,y ranges for this pattern (to center on the card)
        x_begin = int((max_width - pwidth) / 2)
        x_end = x_begin + pwidth
        y_begin = int((max_height - pheight) / 2)
        y_end = y_begin + pheight
        
        for iy in range(0, max_height):
            for ix in range(0, max_width):
                if ix >= x_begin and ix < x_end and iy >= y_begin and iy < y_end:
                    x = ix * box_spacing
                    y = iy * box_spacing

                    col = ix - x_begin
                    row = iy - y_begin
                    cell = pattern[row][col]
                    if cell == '@':
                        elemaster = '#element-{0}'.format(element)
                        eleclone = SVG.clone(0, elemaster, px0 + x, py0 + y)
                        SVG.add_node(svg_group, eleclone)
                    elif cell == 'X':
                        box = SVG.rect(0, px0 + x, py0 + y, box_size, box_size)
                        
                        style_box = Style()
                        style_box.set_fill("none")
                        style_box.set_stroke("#000000", 0.5)
                        style_box.set('stroke-linecap', "round")
                        style_box.set('stroke-miterlimit', 2)
                        box.set_style(style_box)

                        SVG.add_node(svg_group, box)
                    elif cell == '.':
                        dot = SVG.circle(0, dot_x0 + x, dot_y0 + y, 0.9)

                        style_dot = Style()
                        style_dot.set_fill("#c0c0c0")
                        style_dot.set_stroke("none")
                        dot.set_style(style_dot)

                        SVG.add_node(svg_group, dot)
                    else:
                        raise Exception("Unrecognized pattern symbol: {0}"
                                        .format(cell))
def export_png(name):
	print(f"Exporting {name}.png")
	actions = InkscapeActions()
	actions.exportFilename(os.path.join(OUTPUT_DIR, f'{name}.png'))
	actions.exportDpi(300)
	actions.exportAreaPage()
	actions.exportDo()
	Inkscape.run_actions(os.path.join(OUTPUT_DIR, f'{name}.svg'), actions)

def export_all_png():
	export_png("spells-starter")
	export_png("spells-non-starter")

def export_8up_pdf(name):
	print(f"Exporting {name}")
	actions = InkscapeActions()
	actions.exportFilename(os.path.join(PDF_8UP_DIR, f'{name}.pdf'))
	actions.exportDpi(300)
	actions.exportAreaPage()
	actions.exportDo()
	Inkscape.run_actions(os.path.join(PDF_8UP_DIR, f'{name}.svg'), actions)

def export_8up_pdfs():
	outfiles = [f"8up-page{x}" for x in range(0,6)]
	for f in outfiles:
		export_8up_pdf(f)
	
	# gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=temp.pdf ../spell-academy-cards/8up/8up*.pdf
	cmd = ['gs']
	if platform.system() == 'Darwin': # MacOS
		cmd = ['/opt/homebrew/bin/gs']
	cmd.append("-dBATCH")
	cmd.append("-dNOPAUSE")
	cmd.append("-q")
	cmd.append("-sDEVICE=pdfwrite")
	cmd.append(f"-sOutputFile={OUTPUT_DIR}/combined.pdf")

	for f in outfiles:
		cmd.append(f"{PDF_8UP_DIR}/{f}.pdf")
	#subprocess.run(cmd, stdout = subprocess.DEVNULL)
	subprocess.run(cmd)

    
# Comparator to zero-pad the spell index so that they sort correctly.
def _pattern_sort_(x):
    (key, count) = x
    (info, element) = key.split(':')
    (eleCount, index) = info.split('-')
    return f"{eleCount}-{index.zfill(3)}:{element}"

def usage(options):
    print("Usage: %s <options>" % sys.argv[0])
    print("where <options> are:")
    for opt,info in options.items():
        if info['type'] == 'bool':
            print(" --{0} {1}".format(opt, info['desc']))
        else:
            print(" --{0} <arg> {1}".format(opt, info['desc']))
    sys.exit(2)

def parse_options():
    option_defs = {}
    option_defs.update(SVGCardGen.OPTIONS)
    option_defs.update({
        #'summary': {'type': 'bool', 'default': False, 'desc': "Generate spell summary"},
        })
    short_opts = ""
    long_opts = []
    for opt,info in option_defs.items():
        if 'short' in info:
            short_opts += info['short']
            if info['type'] != 'bool':
                short_opts += ':'
        long_opt = opt
        if info['type'] != 'bool':
            long_opt += '='
        long_opts.append(long_opt)

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        usage(option_defs)

    options = {}
    for opt,info in option_defs.items():
        options[opt] = info['default']
    options['out'] = OUTPUT_DIR

    for opt,arg in opts:
        # Build list of short and fullname for this option
        for opt_name, opt_info in option_defs.items():
            option_flags = []
            if 'short' in opt_info:
                option_flags.append('-{0}'.format(opt_info['short']))
            option_flags.append('--{0}'.format(opt_name))

            # If matches this option
            if opt in option_flags:
                type = opt_info['type']
                if type == 'bool':
                    options[opt_name] = True
                elif type == 'int':
                    options[opt_name] = int(arg)
                else:
                    options[opt_name] = str(arg)

    return options
    
def main():
    options = parse_options()
    
    # Force png output for spell cards.
    options['png'] = True
    
    cgen = WovenSpellCards(options)
    cgen.generate_cards()

    export_all_png()
    export_8up_pdfs()

if __name__ == '__main__':
    main()
