#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getopt
import sys

from svg_card_gen import SVGCardGen

from svg import SVG, Style, Node

from data_scar_cards import scar_card_data
from data_ops import valid_ops

# Scar attributes
scar_attributes = [
    'op',
]

class WovenScarCards():
    def __init__(self, options):
        self.ops = {}
                
        self.valid_ops = valid_ops

        # Poker size cards: 2.5" x 3.5" = 225px x 315px = 63.5mm x 88.9mm
        # Bridge size cards: 2.25" x 3.5" = 202.5px x 315px
        self.width = 63.5
        self.height = 88.9
        options['width'] = self.width
        options['height'] = self.height
        
        # Set data for SVGCardGen.
        self.card_gen = SVGCardGen(self, options)

    #
    # DATA VALIDATION
    #
    
    def validate_attrs(self, name, attrs):
        # Ensure all attributes are valid.
        for attr in attrs.keys():
            if not attr in scar_attributes:
                raise Exception("{0:s}: Unknown attribute: {1:s}".format(name, attr))
            
        if not attrs['op'] in self.valid_ops:
            raise Exception("{0:s}: Invalid op: {1}".format(name, attrs['op']))

    #
    # CARD GENERATION
    #

    def generate_cards(self):
        self.card_gen.generate_cards()

    # Returns an iterator that produces an object for each card.
    # callback from SVGCardGen
    def card_data(self):
        return scar_card_data

    # Params:
    #   |metadata| - card and file index
    #   |card_data| - data for current card
    #   |svg| - the SVG manager
    #
    # callback from SVGCardGen
    def process_card_data(self, metadata, card_data):
        (svg, svg_group) = self.card_gen.pre_card()
        self.draw_scar_card(metadata, card_data, svg, svg_group)
        self.card_gen.post_card()

    # Params:
    #   |metadata| - card and file index
    #   |card_data| - data for current card
    #   |svg| - the SVG manager
    #   |svg_group| - the svg group node where this card should be added
    def draw_scar_card(self, metadata, card, svg, svg_group):
        id = metadata['id']
        name = card[0]
        attrs = card[1]

        # Validate attributes
        self.validate_attrs(name, attrs)

        # Build list of template ids and then load from svg file.
        svg_ids = []
        svg_ids.append('artifact-title')
        svg_ids.extend(['icon-star-{0}'.format(n) for n in [1,2,3]])
        svg_ids.append('separator')
        svg_ids.extend(['op-{0}'.format(op) for op in valid_ops])
        svg.load_ids('spell-cards/spell-template.svg', svg_ids)

        # Add Op masters (hidden, used for cloning).
        g_masters = SVG.group('masters')
        g_masters.set_style("display:none")
        SVG.add_node(svg_group, g_masters)
        for e in [
                'op-tapestry', 'op-eye', 'op-emove', 'op-mmove', 'op-thread',
                'op-tmove', 'op-action',
                ]:
            svg.add_loaded_element(g_masters, e)

        # Draw scar title.
        title = svg.add_loaded_element(svg_group, 'artifact-title')
        SVG.set_text(title, name)
        
        svg.add_loaded_element(svg_group, 'separator')

        # Draw alternate action.
        svg.add_loaded_element(svg_group, 'op-{0}'.format(attrs['op']))

    def draw_description(self, id, raw_desc, svg, svg_group):
        text = svg.add_loaded_element(svg_group, 'description')
        SVG.set_text(text, self.expand_desc(raw_desc))

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
    options['out'] = 'scar-cards'

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
    cgen = WovenScarCards(options)
    cgen.generate_cards()

if __name__ == '__main__':
    main()
