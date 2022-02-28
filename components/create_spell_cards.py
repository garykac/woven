#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import getopt
import sys

from svg_card_gen import SVGCardGen

from svg import SVG, Style, Node

from data_spell_cards import spell_card_data
from data_spell_cards import spell_card_revision
from data_spell_cards import spell_card_categories

from data_spell_cards_blank import spell_card_blank_data

from data_spell_patterns import spell_card_patterns

from data_ops import valid_ops

elem_map = {
    'a': 'air',
    'e': 'earth',
    'f': 'fire',
    'w': 'water',
}

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


class WovenSpellCards():
    OUTPUT_DIR = 'spell-cards'
    CARD_TEMPLATE = 'woven-card-template.svg'
    
    def __init__(self, options):
        self.next_id = 0
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
                
        self.valid_elements = ['none', 'air', 'fire', 'earth', 'water']
        self.valid_categories = spell_card_categories
        self.valid_ops = valid_ops

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
            ['E2', 164],
            ['E3', 32],
            ['EE1', 7],
            ['EE2', 8],
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
        for card in spell_card_data:  #spell_card_blank_data:
            # Auto-assign ids
            attrs = card[1]
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
        desc = card[2]

        # Validate attributes
        if attrs['category'] != 'blank':
            self.validate_attrs(name, attrs)
        pattern_id = attrs['pattern']
        pattern = self.card_patterns[pattern_id]['pattern']
        if attrs['category'] != 'blank':
            self.record_spell_info(name, pattern, attrs, desc)
        
        if attrs['category'] != 'blank' and pattern_id != 'blank':
            pe_tag = self.pattern_key(pattern) + '-' + attrs['element']
            if pe_tag in self.pattern_elements:
                raise Exception('Pattern for "{0:s}" already used for "{1:s}"'
                      .format(name, self.pattern_elements[pe_tag]))
            self.pattern_elements[pe_tag] = name

        # Validate desc
        self.validate_desc(name, desc)
        
        # Verify pattern matches spell element
        element = attrs['element']
        pelem_data = self.card_patterns[pattern_id]['elements']
        pelems = []
        if pelem_data == "none":
            pelems.append("none")
        else:
            pelems = [elem_map[p] for p in pelem_data]
        if not element in pelems:
            raise Exception("{0:s}: Spell pattern does not match element {1:s}"
                  .format(name, element))

        # Build list of template ids and then load from svg file.
        svg_ids = []
        svg_ids.extend(['element-{0}'.format(elem_map[e]) for e in elem_map])
        svg_ids.append('spell-title')
        svg_ids.append('spell-pattern-border')
        svg_ids.append('spell-description')
        svg_ids.append('spell-id')
        svg_ids.extend(['icon-star-{0}'.format(n) for n in [1,2,3]])
        svg_ids.append('icon-vp')
        svg_ids.append('spell-flavor')
        svg_ids.append('separator')
        svg_ids.extend(['op-{0}'.format(op) for op in valid_ops])
        svg.load_ids(WovenSpellCards.CARD_TEMPLATE, svg_ids)

        # Add Element and Op masters (hidden, used for cloning).
        g_masters = SVG.group('masters')
        g_masters.set_style("display:none")
        SVG.add_node(svg_group, g_masters)
        for e in [
                'op-tapestry', 'op-eye', 'op-mmove', 'op-thread', 'op-action',
                'element-air', 'element-earth', 'element-fire', 'element-water',
                ]:
            svg.add_loaded_element(g_masters, e)

        if attrs['category'] != 'blank':
            # Draw spell title.
            title = svg.add_loaded_element(svg_group, 'spell-title')
            SVG.set_text(title, name)
            
            # Draw elements in title bar
            elemaster = '#element-{0}'.format(element)
            SVG.add_node(svg_group, SVG.clone(0, elemaster, 4, 4))
            SVG.add_node(svg_group, SVG.clone(0, elemaster, 54, 4))

            # Draw spell id.
            id_text = svg.add_loaded_element(svg_group, 'spell-id')
            SVG.set_text(id_text,
                         "{0:d}/{1:d}".format(spell_card_revision, attrs['id']))
            
            # Draw flavor text (if present).
            if 'flavor' in attrs:
                flavor_text = svg.add_loaded_element(svg_group, 'spell-flavor')
                SVG.set_text(flavor_text, attrs['flavor'])
            
            svg.add_loaded_element(svg_group, 'separator')

        # Draw alternate action.
        svg.add_loaded_element(svg_group, 'op-{0}'.format(attrs['op']))

        # Add spell pattern.
        self.draw_pattern(pattern_id, pattern, element, svg_group)
        svg.add_loaded_element(svg_group, 'spell-pattern-border')

        if attrs['category'] != 'blank':
            self.draw_description(attrs['id'], desc, svg, svg_group)

        self.draw_vp(attrs['vp'], svg, svg_group)

    def draw_description(self, id, raw_desc, svg, svg_group):
        text = svg.add_loaded_element(svg_group, 'spell-description')
        SVG.set_text(text, self.expand_desc(raw_desc))

    def draw_vp(self, vp, svg, svg_group):
        if vp != 0:
            svg.add_loaded_element(svg_group, 'icon-star-1')
            if vp > 1:
                svg.add_loaded_element(svg_group, 'icon-star-2')
            if vp > 2:
                svg.add_loaded_element(svg_group, 'icon-star-3')
                
    def draw_pattern(self, id, pattern_raw, element, svg_group):        
        pattern = [x.split() for x in pattern_raw]
        pheight = len(pattern)
        if pheight == 0:
            raise Exception("Missing pattern for {0}".format(id))
        if pheight > 3:
            raise Exception("Tall pattern for {0}".format(id))
        pwidth = len(pattern[0])

        # Max pattern size that fits on the card.
        max_width = 7
        max_height = 3

        # Center of pattern area.
        pcenter_x = self.width / 2
        pcenter_y = 22.4

        # Size and spacing for each box in pattern.
        box_size = 5.5
        box_spacing = 7

        # Upper left corner of pattern area
        px0 = pcenter_x - (((max_width-1) * box_spacing) + box_size) / 2
        py0 = pcenter_y - (((max_height-1) * box_spacing) + box_size) / 2

        # Calc offsets to center the patterns that are less than max size.
        if pwidth % 2 == 0:
            px0 += box_spacing / 2
            max_width = 6
        else:
            max_width = 7
        if pheight % 2 == 0:
            py0 += box_spacing / 2
            max_height = 2
        else:
            max_height = 3

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
                        dot = SVG.circle(0, dot_x0 + x, dot_y0 + y, 0.8)

                        style_dot = Style()
                        style_dot.set_fill("#c0c0c0")
                        style_dot.set_stroke("none")
                        dot.set_style(style_dot)

                        SVG.add_node(svg_group, dot)
                    else:
                        raise Exception("Unrecognized pattern symbol: {0}"
                                        .format(cell))

    #
    # Summary
    #

    # Create a markdown style link for the spell.
    def spell_link(self, sid):
        name = self.id2name[sid]
        link_name = '-'.join(name.lower().split())
        return ('[{0:s}](#{1:s})'.format(name, link_name))

    def element_name(self, e):
        if e == 'none':
            return 'Neutral'
        else:
            return e[0].upper() + e[1:]

    def category_list(self, cats):
        uppercats = []
        for cat in cats.split(','):
            uppercat = ' '.join([catword[0].upper() + catword[1:]
                                 for catword in cat.split('-')])
            uppercats.append(uppercat)
        catstr = ', '.join(uppercats)
        return catstr

    def gen_spell_summary(self):
        summary = open('../docs/spell-list.md', "w")

        summary.write('# List of Spell Fragments\n\n')

        now = datetime.datetime.now()
        summary.write('Generated on {0:04d}/{1:02d}/{2:02d} @ {3:02d}:{4:02d}\n\n'
                      .format(now.year, now.month, now.day, now.hour, now.minute))

        summary.write('## By Category\n\n')
        print('Categories')

        for c in sorted(self.valid_categories):
            if not c in self.categories:
                continue
            summary.write('{0:s} ({1:d})\n\n'
                          .format(self.category_list(c), len(self.categories[c])))
            print('  {0:s} ({1:d})'
                  .format(self.category_list(c), len(self.categories[c])))

            names = [self.id2name[id] for id in self.categories[c]]
            for name in sorted(names):
                sid = self.name2id[name]
                summary.write('* {0:s} - _{1:s}_\n'
                              .format(self.spell_link(sid),
                                      self.element_name(self.id2attrs[sid]['element'])))

            summary.write('\n')
            
        summary.write('## By Element\n\n')
        print('Element')

        for e in self.valid_elements:
            eName = self.element_name(e)
            if not e in self.elements:
                continue
                
            summary.write('{0:s} ({1:d})\n\n'.format(eName, len(self.elements[e])))
            print('  {0:s} ({1:d})'.format(eName, len(self.elements[e])))

            names = [self.id2name[id] for id in self.elements[e]]
            for name in sorted(names):
                sid = self.name2id[name]
                summary.write('* {0:s} - _{1:s}_\n'
                              .format(self.spell_link(sid),
                                      self.category_list(self.id2attrs[sid]['category'])))

            summary.write('\n')

        print('Ops')
        for op in ['tapestry', 'eye', 'mmove', 'thread']:
            exact_count = 0
            extra_count = 0
            for k,v in self.ops.items():
                if k == op:
                    exact_count += len(v)
                elif k.find(op) != -1:
                    extra_count += len(v)
            print(' {0:s} ({1:d}) + {2:d} = {3:d}'
                  .format(op, exact_count, extra_count, exact_count + extra_count))
        for k,v in sorted(self.ops.items()):
            if k.find('-') != -1:
                print(' {0:s} ({1:d})'.format(k, len(v)))
        
        summary.write('## By Pattern\n\n')
        print('Patterns')
        for pattern_key,sid in sorted(self.pattern2id.items()):
            print(' ', pattern_key, '-', self.id2name[sid])
            (pattern, element) = pattern_key.split(':')
            sid = self.pattern2id[pattern_key]
            summary.write('* {0:s} {1:s} ({2:s})\n'
                          .format(pattern, self.spell_link(sid), element))
        summary.write('\n')
        
        summary.write('## By Name\n\n')
        count = 0

        for name,sid in sorted(self.name2id.items()):
            count += 1
            summary.write('### {0:s}\n'.format(self.id2name[sid]))
            summary.write('```\n')
            for prow in self.id2pattern[sid]:
                summary.write(prow + '\n')
            summary.write('```\n')
            summary.write('Element: {0:s}\n\n'
                          .format(self.element_name(self.id2attrs[sid]['element'])))

            summary.write('Category: ')
            summary.write(self.category_list(self.id2attrs[sid]['category']))
            summary.write('\n\n')

            for d in self.expand_desc(self.id2desc[sid]):
                if d == '-':
                    continue
                summary.write(d + '\n')
                summary.write('\n')

        print('Starters')
        for s in self.starters:
            attr = self.id2attrs[s]
            print(' {0} - {1} - {2}'
                  .format(self.id2name[s], attr['element'], attr['op']))

        summary.close()
        print('Total spell count = {0:d}'.format(count))
        if self.blank_count != 0:
            print('*** BLANK SPELLS *** = {0:d}'.format(self.blank_count))
        
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
        'summary': {'type': 'bool', 'default': False, 'desc': "Generate spell summary"},
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
    options['out'] = WovenSpellCards.OUTPUT_DIR

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
    cgen = WovenSpellCards(options)
    cgen.generate_cards()

    if options['summary']:
        cgen.gen_spell_summary()

if __name__ == '__main__':
    main()
