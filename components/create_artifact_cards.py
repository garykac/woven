#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import getopt
import os
import subprocess
import sys

from svg_card_gen import SVGCardGen

from svg import SVG, Style, Node

from data_artifact_cards import artifact_card_data

# Spell attributes
spell_attributes = [
    'element', 'pattern', 'op', 'vp', 'id', 'category', 'flavor'
]

# Spell description keys
spell_desc_keys = {
    'cast': {
    },
    'react': {
        'prefix': "Reaction",
    },
    'active': {
        'prefix': "While active",
    },
    'charged': {
        'prefix': "While charged",
    },
    'sacrifice': {
        'prefix': "Sacrifice charge",
    },
    'notes': {
    },
}

# Valid Minor Actions
valid_ops = [
    'tapestry',       # Draw tapestry card
    'tapestry-eye',   # Draw tapestry card OR Create eye
    'tapestry-emove', # Draw tapestry card OR Move eye
    'tapestry-mmove', # Draw tapestry card OR Move mage
    'tapestry-thread',# Draw tapestry card OR Recover thread
    'tapestry-tmove', # Draw tapestry card OR Move thread
    'eye',            # Create eye
    'eye-emove',      # Create eye OR Move eye
    'eye-mmove',      # Create eye OR Move mage
    'eye-thread',     # Create eye OR Recover thread
    'eye-tmove',      # Create eye OR Move thread
    'emove',          # Move eye
    'emove-mmove',    # Move eye OR Move mage
    'emove-thread',   # Move eye OR Recover thread
    'emove-tmove',    # Move eye OR Move thread
    'mmove',          # Move mage
    'mmove-thread',   # Move mage OR Recover thread
    'mmove-tmove',    # Move mage OR Move thread
    'thread',         # Recover thread
    'thread-tmove',   # Recover thread OR Move thread
    'tmove',          # Move thread
    'tmove-action',   # Move thread AND take another action
    'action',         # Take another action
    'action-action',  # Take another 2 actions
]


class WovenArtifactCards():
    def __init__(self, options):
        self.name2id = {}
        self.pattern_elements = {}
        self.elements = {}
        self.categories = {}
        self.ops = {}
        self.id2name = {}
        self.id2pattern = {}
        self.id2attrs = {}
        self.id2desc = {}
        self.pattern2id = {}
        self.max_id = 0
        self.blank_count = 0
        self.starters = []
                
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
        
        if not 'category' in attrs:
            raise Exception("{0:s}: Missing 'category' attribute".format(name))
        for cat in attrs['category'].split(','):
            if not cat in self.valid_categories:
                raise Exception("{0:s}: Invalid category: {1}".format(name, cat))

        if not 'id' in attrs:
            raise Exception("{0:s}: Missing 'id' attribute".format(name))
        if attrs['id'] in self.id2name:
            raise Exception("{0} ID {1} already used by {2}"
                            .format(name, str(attrs['id']), self.id2name[attrs['id']]))
        
        if not 'pattern' in attrs:
            raise Exception("{0:s}: Missing 'pattern' attribute".format(name))
        if not attrs['pattern'] in self.card_patterns:
            raise Exception("{0:s}: Invalid pattern: {1}".format(name, attrs['pattern']))

        if not attrs['op'] in self.valid_ops:
            raise Exception("{0:s}: Invalid op: {1}".format(name, attrs['op']))

    def validate_desc(self, name, desc):
        # Ensure all keys are valid.
        for key in desc.keys():
            if not key in spell_desc_keys:
                raise Exception("{0:s}: Unknown key: {1:s}".format(name, key))

        # Ensure charged spells have a charge effect.
        if desc['cast'] == '{{ADD_CHARGE}}':
            if not 'charged' in desc and not 'sacrifice' in desc:
                raise Exception("{0:s}: Charged spell with no effect".format(name))            

    def expand_desc(self, raw_desc):
        desc = []
        for key in spell_desc_keys:
            if not key in raw_desc:
                continue
            d = raw_desc[key]
            d = d.replace('{{ADD_CHARGE}}', 'Place a Charge on this spell.')
            d = d.replace('{{ADD_ACTION}}', 'Take another action.')
            if len(desc) != 0:
                desc.append('-')
                
            if 'prefix' in spell_desc_keys[key]:
                prefix = spell_desc_keys[key]['prefix']
                desc.append("{0}: {1}".format(prefix, d))
            else:
                desc.append(d)
        return desc

    def record_spell_info(self, name, pattern, attrs, desc):
        id = attrs['id']
        self.name2id[name] = id
        self.id2name[id] = name
        if id > self.max_id:
            self.max_id = id

        self.id2pattern[id] = pattern
        self.id2attrs[id] = attrs
        self.id2desc[id] = desc
        
        pattern_id = attrs['pattern']
        if pattern_id == 'blank':
            self.blank_count += 1
        else:
            pattern_key = '{0:s}:{1:s}'.format(pattern_id, attrs['element'])
            if pattern_key in self.pattern2id:
                dup_id = self.pattern2id[pattern_key]
                raise Exception("{0:s}: Pattern {1:s} already assigned to {2:d} ({3:s})"
                      .format(name, pattern_key, dup_id, self.id2name[dup_id]))
            self.pattern2id[pattern_key] = id

        element = attrs['element']
        if not element in self.elements:
            self.elements[element] = []
        self.elements[element].append(id)

        for cat in attrs['category'].split(','):
            if not cat in self.categories:
                self.categories[cat] = []
            self.categories[cat].append(id)
            if cat == 'starter':
                self.starters.append(id)

        op = attrs['op']
        if not op in self.ops:
            self.ops[op] = []
        self.ops[op].append(id)
        
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
        print(name, attrs)

        # Build list of template ids and then load from svg file.
        svg_ids = []
        svg_ids.append('artifact-title')
        svg_ids.extend(['icon-star-{0}'.format(n) for n in [1,2,3]])
        svg_ids.append('separator')
        svg_ids.extend(['op-{0}'.format(op) for op in valid_ops])
        svg.load_ids('spell-cards/spell-template.svg', svg_ids)

        # Add Element and Op masters (hidden, used for cloning).
        g_masters = SVG.group('masters')
        g_masters.set_style("display:none")
        SVG.add_node(svg_group, g_masters)
        for e in [
                'op-tapestry', 'op-eye', 'op-emove', 'op-mmove', 'op-thread',
                'op-tmove', 'op-action',
                ]:
            svg.add_loaded_element(g_masters, e)

        # Draw artifact title.
        title = svg.add_loaded_element(svg_group, 'artifact-title')
        SVG.set_text(title, name)
        
        svg.add_loaded_element(svg_group, 'separator')

        # Draw alternate action.
        svg.add_loaded_element(svg_group, 'op-{0}'.format(attrs['op']))

        self.draw_vp(attrs['vp'], svg, svg_group)

    def draw_description(self, id, raw_desc, svg, svg_group):
        text = svg.add_loaded_element(svg_group, 'description')
        SVG.set_text(text, self.expand_desc(raw_desc))

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
    options['out'] = 'artifact-cards'

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
