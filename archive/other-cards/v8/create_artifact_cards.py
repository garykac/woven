#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getopt
import sys

from svg_card_gen import SVGCardGen

from svg import SVG, Style, Node

from data_artifact_cards import artifact_card_data
from data_ops import valid_ops

# Artifact attributes
artifact_attributes = [
    'op', 'vp', 'description', 'bonus', 'flavor'
]

class WovenArtifactCards():
    OUTPUT_DIR = 'artifact-cards'
    CARD_TEMPLATE = 'woven-card-template.svg'
    
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
            if not attr in artifact_attributes:
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
        #for card in artifact_card_data:
        #    yield card
        return artifact_card_data

    # Params:
    #   |metadata| - card and file index
    #   |card_data| - data for current card
    #   |svg| - the SVG manager
    #
    # callback from SVGCardGen
    def process_card_data(self, metadata, card_data):
        (svg, svg_group) = self.card_gen.pre_card()
        self.draw_artifact_card(metadata, card_data, svg, svg_group)
        self.card_gen.post_card()

    # Params:
    #   |metadata| - card and file index
    #   |card_data| - data for current card
    #   |svg| - the SVG manager
    #   |svg_group| - the svg group node where this card should be added
    def draw_artifact_card(self, metadata, card, svg, svg_group):
        id = metadata['id']
        name = card[0]
        attrs = card[1]

        # Validate attributes
        self.validate_attrs(name, attrs)

        # Build list of template ids and then load from svg file.
        svg_ids = []
        svg_ids.append('artifact-title')
        svg_ids.extend(['icon-star-{0}'.format(n) for n in [1,2,3]])
        svg_ids.append('artifact-description')
        svg_ids.append('artifact-extra-action')
        svg_ids.append('artifact-bonus')
        svg_ids.append('artifact-bonus-border')
        svg_ids.append('artifact-flavor')
        #svg_ids.append('separator')
        svg_ids.extend(['op-{0}'.format(op) for op in valid_ops])
        svg.load_ids(WovenArtifactCards.CARD_TEMPLATE, svg_ids)

        # Add Op masters (hidden, used for cloning).
        g_masters = SVG.group('masters')
        g_masters.set_style("display:none")
        SVG.add_node(svg_group, g_masters)
        for e in [
                'op-tapestry', 'op-eye', 'op-mmove', 'op-thread', 'op-action',
                ]:
            svg.add_loaded_element(g_masters, e)

        # Draw artifact title.
        title = svg.add_loaded_element(svg_group, 'artifact-title')
        SVG.set_text(title, name)

        self.draw_description(attrs, 'description', svg, svg_group)
        svg.add_loaded_element(svg_group, 'artifact-extra-action')
        self.draw_bonus(attrs, 'bonus', svg, svg_group)
        self.draw_flavor(attrs, 'flavor', svg, svg_group)
        
        #svg.add_loaded_element(svg_group, 'separator')

        # Draw alternate action.
        #svg.add_loaded_element(svg_group, 'op-{0}'.format(attrs['op']))

        self.draw_vp(attrs['vp'], svg, svg_group)

    def draw_description(self, attrs, attr_name, svg, svg_group):
        if not attr_name in attrs:
            return
        text = attrs[attr_name]
        if text == '':
            return
        desc = svg.add_loaded_element(svg_group, 'artifact-description')
        SVG.set_text(desc, text)

    def draw_bonus(self, attrs, attr_name, svg, svg_group):
        if not attr_name in attrs:
            return
        text = attrs[attr_name]
        if text == '':
            return
        svg.add_loaded_element(svg_group, 'artifact-bonus-border')
        bonus = svg.add_loaded_element(svg_group, 'artifact-bonus')
        SVG.set_text(bonus, text)

    def draw_flavor(self, attrs, attr_name, svg, svg_group):
        if not attr_name in attrs:
            return
        text = attrs[attr_name]
        if text == '':
            return
        flavor = svg.add_loaded_element(svg_group, 'artifact-flavor')
        SVG.set_text(flavor, text)

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
    options['out'] = WovenArtifactCards.OUTPUT_DIR

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
    cgen = WovenArtifactCards(options)
    cgen.generate_cards()

if __name__ == '__main__':
    main()
