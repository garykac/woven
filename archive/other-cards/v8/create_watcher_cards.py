#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getopt
import sys

from svg_card_gen import SVGCardGen

from svg import SVG, Style, Node

# Watcher attributes
watcher_attributes = [
    'vp', 'attack', 'detect', 'pursuit', 'dir', 'name'
]

watcher_card_data = [
    {'vp': 2, 'attack': 2, 'detect': 'yes', 'pursuit': 1, 'dir': 'next',    'name': "Rupert"},
    {'vp': 2, 'attack': 3, 'detect': 'no',  'pursuit': 1, 'dir': 'next',    'name': "Aurora"},
    {'vp': 3, 'attack': 2, 'detect': 'yes', 'pursuit': 1, 'dir': 'next',    'name': "Fergus"},
    {'vp': 3, 'attack': 3, 'detect': 'no',  'pursuit': 1, 'dir': 'next',    'name': "Ramona"},
    {'vp': 2, 'attack': 3, 'detect': 'yes', 'pursuit': 2, 'dir': 'next',    'name': "Percy"},
    {'vp': 2, 'attack': 2, 'detect': 'no',  'pursuit': 2, 'dir': 'next',    'name': "Bartholomew"},
    {'vp': 3, 'attack': 3, 'detect': 'yes', 'pursuit': 2, 'dir': 'next',    'name': "Clementine"},
    {'vp': 3, 'attack': 2, 'detect': 'no',  'pursuit': 2, 'dir': 'next',    'name': "Archibald"},
    {'vp': 2, 'attack': 3, 'detect': 'yes', 'pursuit': 1, 'dir': 'reverse', 'name': "Phineas"},
    {'vp': 2, 'attack': 3, 'detect': 'no',  'pursuit': 1, 'dir': 'reverse', 'name': "Matilda"},
    {'vp': 2, 'attack': 3, 'detect': 'yes', 'pursuit': 1, 'dir': 'skip',    'name': "Magnus"},
    {'vp': 2, 'attack': 3, 'detect': 'no',  'pursuit': 1, 'dir': 'skip',    'name': "Edmund"},
]

class WovenWatcherCards():
    OUTPUT_DIR = 'watcher-cards'
    CARD_TEMPLATE = 'woven-card-template.svg'
    
    def __init__(self, options):
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
    
    def validate_attrs(self, attrs):
        # Ensure all attributes are valid.
        for attr in attrs.keys():
            if not attr in watcher_attributes:
                raise Exception("Watcher: Unknown attribute: {0:s}".format(attr))

    #
    # CARD GENERATION
    #

    def generate_cards(self):
        self.card_gen.generate_cards()

    # Returns an iterator that produces an object for each card.
    # callback from SVGCardGen
    def card_data(self):
        #for card in artifact_card_data:
        #    yield card
        return watcher_card_data

    # Params:
    #   |metadata| - card and file index
    #   |card_data| - data for current card
    #   |svg| - the SVG manager
    #
    # callback from SVGCardGen
    def process_card_data(self, metadata, card_data):
        (svg, svg_group) = self.card_gen.pre_card()
        self.draw_watcher_card(metadata, card_data, svg, svg_group)
        self.card_gen.post_card()

    # Params:
    #   |metadata| - card and file index
    #   |card_data| - data for current card
    #   |svg| - the SVG manager
    #   |svg_group| - the svg group node where this card should be added
    def draw_watcher_card(self, metadata, card, svg, svg_group):
        id = metadata['id']
        attrs = card

        # Validate attributes
        self.validate_attrs(attrs)
        name = attrs['name']

        # Build list of template ids and then load from svg file.
        svg_ids = []
        svg_ids.append('watcher-title')
        svg_ids.extend(['icon-star-{0}'.format(n) for n in [1,2,3]])
        svg_ids.append('watcher-image')
        svg_ids.append('watcher-flavor')
        svg_ids.extend(['attack-{0}'.format(n) for n in [2,3]])
        svg_ids.extend(['pursuit-{0}'.format(n) for n in [1,2]])
        svg_ids.extend(['detect-{0}'.format(d) for d in ['yes', 'no']])
        svg_ids.extend(['target-{0}'.format(t) for t in ['next', 'skip', 'reverse']])
        svg.load_ids(WovenWatcherCards.CARD_TEMPLATE, svg_ids)

        # Draw artifact title.
        title = svg.add_loaded_element(svg_group, 'watcher-title')
        SVG.set_text(title, "Watcher")

        svg.add_loaded_element(svg_group, 'watcher-image')
        svg.add_loaded_element(svg_group, 'attack-{0}'.format(attrs['attack']))
        svg.add_loaded_element(svg_group, 'detect-{0}'.format(attrs['detect']))
        svg.add_loaded_element(svg_group, 'pursuit-{0}'.format(attrs['pursuit']))
        svg.add_loaded_element(svg_group, 'target-{0}'.format(attrs['dir']))

        flavor = svg.add_loaded_element(svg_group, 'watcher-flavor')
        SVG.set_text(flavor, "Detect Range = 3")
        
        self.draw_vp(attrs['vp'], svg, svg_group)

    def draw_vp(self, vp, svg, svg_group):
        if vp != 0:
            svg.add_loaded_element(svg_group, 'icon-star-1')
            if vp > 1:
                svg.add_loaded_element(svg_group, 'icon-star-2')
            if vp > 2:
                svg.add_loaded_element(svg_group, 'icon-star-3')
                
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
        'summary': {'type': 'bool', 'default': False,
                    'desc': "Generate spell summary"},
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
    options['out'] = WovenWatcherCards.OUTPUT_DIR

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
    cgen = WovenWatcherCards(options)
    cgen.generate_cards()

if __name__ == '__main__':
    main()
