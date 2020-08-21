#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import getopt
import os
import subprocess
import sys

from card_gen import CardGen
from card_gen import CardGen_ShortFlags
from card_gen import CardGen_LongFlags
from card_gen import CardGen_DefaultOptions
from card_gen import CardGen_ProcessOption
from card_gen import CardGen_OptionDesc
from card_gen import error

from data_spell_cards import spell_card_data
from data_spell_cards import spell_card_revision
from data_spell_cards import spell_card_categories
from data_spell_cards import valid_ops

from data_spell_patterns import spell_card_patterns

elem_map = {
    'a': 'air',
    'e': 'earth',
    'f': 'fire',
    'w': 'water',
}

class SpellCardGen(CardGen):
    def __init__(self, options):
        CardGen.__init__(self, options)

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
        
        self.card_patterns = spell_card_patterns
        self.card_data = spell_card_data
        
        self.validate_patterns()

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
                self.check_pattern('%s-%d' % (base, i))
            # Check one beyond the last to verify the ranges are correct.
            id = '%s-%d' % (base, max+1)
            if id in self.card_patterns:
                print('Pattern id not in valid range: %s-%d' % (base, max+1))
                sys.exit()

    def check_pattern(self, id):
        if not id in self.card_patterns:
            print(id, 'not found')
        pattern = self.card_patterns[id]['pattern']
        
        first_row = True
        num_cols = 0
        for row in pattern:
            cols = row.split()
            if first_row:
                num_cols = len(cols)
                first_row = False
            if len(cols) != num_cols:
                error(id + ": Mismatch number of columns in pattern")
        
    # override
    def process_card_data(self, card_data):
        self.pre_card()
        if self.verbose:
            print(self.curr_file, self.curr_card, card_data[0])
        self.draw_card(self.curr_card, card_data)
        self.post_card()

    # override
    def process_blank_card(self):
        self.pre_card()
        if self.verbose:
            print(self.curr_file, self.curr_card)
        attrs = {
            'element': 'none',
            'category': 'blank',
            'id': 1000 + self.curr_card,
            'pattern': 'blank',
        }
        self.draw_card(self.curr_card, ['', attrs, {}])
        self.post_card()

    def draw_card(self, id, card):
        name = card[0]
        attrs = card[1]
        desc = card[2]
        if attrs['category'] != 'blank':
            self.validate_attrs(name, attrs)
        pattern_id = attrs['pattern']
        pattern = self.card_patterns[pattern_id]['pattern']
        if attrs['category'] != 'blank':
            self.record_spell_info(name, pattern, attrs, desc)
        
        if attrs['category'] != 'blank' and pattern_id != 'blank':
            pe_tag = self.pattern_key(pattern) + '-' + attrs['element']
            if pe_tag in self.pattern_elements:
                error('Pattern for "%s" already used for "%s"'
                      % (name, self.pattern_elements[pe_tag]))
            self.pattern_elements[pe_tag] = name

        # Verify pattern matches spell element
        element = attrs['element']
        pelem_data = self.card_patterns[pattern_id]['elements']
        pelems = []
        if pelem_data == "none":
            pelems.append("none")
        else:
            pelems = [elem_map[p] for p in pelem_data]
        if not element in pelems:
            error('%s: Spell pattern does not match element %s' % (name, element))
        
        self.start_card_page_transform(id)

        if not self.no_border:
            self.draw_border()
        if attrs['category'] != 'blank':
            self.draw_title(name)
            self.draw_title_element(element)
            self.draw_card_id(attrs['id'], 'starter' in attrs['category'].split(','))
            self.draw_separator()
            self.draw_operation(attrs['op'])
            
        self.draw_pattern(pattern_id, pattern, element)
        self.draw_pattern_border()

        if attrs['category'] != 'blank':
            self.draw_desc(attrs['id'], desc)
        
        self.end_card_page_transform()
    
    def draw_title(self, title):
        id = "c%d-title" % self.curr_card
        self.draw_text(id, self.card_width / 2, 30, title, 18, align='center',
                       weight='bold', font='Arial Narrow')
        
    def draw_card_id(self, spell_id, starter):
        card_id = "c%d-spell-id" % self.curr_card
        id_string = 'id #%d (r%d)' % (spell_id, spell_card_revision)
        if starter:
            id_string = 'STARTER - ' + id_string
        self.draw_text(card_id, self.card_width / 2, self.card_height-50,
                       id_string, 10, align='center', style='italic', font='Georgia')

    def draw_separator(self):
        style = "fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
        path = "M 16,293 H 224"
        self.draw_path(style, path, "separator")

    def draw_operation(self, op):
        self.write('<use id="use984" transform="translate(0,-60)" xlink:href="#op-%s" x="0" y="0" width="100%%" height="100%%" />' % op)
        
    def draw_starter(self):
        id = "c%d-starter" % self.curr_card
        self.draw_text(id, self.card_width / 2, self.card_height-25, "STARTER", 10,
                       align='center', style='italic', font='Georgia')

    def draw_desc(self, id, desc):
        width = 160
        if self.card_size == 'poker':
            width += 22.5
        height = 165
        bottom_margin = 25
        x = (self.card_width - width) / 2
        y = self.card_height - bottom_margin - height
        rect = { 'x': x, 'y': y, 'width': width, 'height': height }

        self.draw_flow_text(rect, self.expand_desc(id, desc), size=10)
    
    def draw_title_element(self, element):
        x = 0
        y = -313
        self.write('<use x="0" y="0" xlink:href="#element-%s" transform="translate(%d,%d)" width="100%%" height="100%%" />\n' % (element, x, y))
        x = self.card_width - 47 # bridge=155
        self.write('<use x="0" y="0" xlink:href="#element-%s" transform="translate(%d,%d)" width="100%%" height="100%%" />\n' % (element, x, y))
    
    def draw_pattern_border(self):
        if self.card_size == 'poker':
            self.start_group(transform='translate(%d,%d)' % (18,0))
        self.write('<path')
        self.write(' style="color:#000000;display:inline;overflow:visible;visibility:visible;opacity:1;solid-color:#000000;solid-opacity:1;fill:#808080;fill-opacity:1;fill-rule:nonzero;stroke:none"')
        self.write(' d="m 175.87305,38.369141 c -2.36823,-0.0062 -7.73239,-0.253645 -9.73633,0.0095 -1.24847,0.163933 -1.77243,0.386634 -3.4336,0.5 l -0.0156,1.78125 -3.34961,-1.595703 c -2.78274,0.168193 -4.83311,0.06978 -7.17969,0.150391 l -0.46093,1.089844 -0.47071,-0.835938 c -2.78501,0.08098 -5.84443,0.09035 -10.29687,-0.002 l -2.31641,-0.283203 -0.75586,1.103516 -0.79883,-0.908204 -1.82617,2.486328 -2.52873,-2.560747 c -5.10142,-0.140849 -8.39536,-0.270794 -12.80332,-0.552487 -0.85446,-0.0546 -2.63293,0.01731 -3.78125,0.01563 l 0.45117,0.91211 -4.37304,-0.179688 -0.80469,1.072266 -1.11524,-1.207032 -3.08007,2.144532 -1.5625,-1.427735 -2.09961,2.050782 -0.9375,-2.5 -6.337894,1.74414 -2.655903,-2.1666 c -3.592431,0.187547 -10.425906,0.09657 -11.634315,0.142321 -1.017569,0.03852 -11.87722,0.886312 -14.93283,0.916628 l -0.86914,1.050781 -0.355469,-1.048828 c -4.859652,0.03938 -6.956883,0.523142 -8.682947,0.485042 -2.369492,-0.08897 -4.225181,-1.155877 -9.241327,-1.390225 l -0.902344,1.339844 -0.541015,-1.117188 -1.166016,0.3125 -0.779297,-1.310546 c -3.677787,-0.157044 -6.205688,0.208415 -9.876953,0.140624 L 30.008929,40.436119 27.331195,38.7994 c -4.761365,-0.03194 -6.419907,0.809707 -9.31836,0.939727 l -2.691406,-0.06054 0.81529,6.370257 c 0.217738,0.41461 0.423836,1.334908 0.636719,1.767578 -0.495313,0.680664 -1.522582,2.879301 -1.675782,3.113282 -0.520624,0.795132 0.213937,8.736939 0.149833,9.551897 l 0.966797,4.552719 -1.306641,0.04687 c 0.323973,2.118143 0.362874,3.739342 0.527344,6.476562 0.0751,1.249814 -0.03761,4.544521 -0.166015,7.212891 l 1.792968,1.175786 -1.472656,1.517578 1.382812,1.384766 -2.044921,0.841797 c 0.08224,2.105469 0.362389,3.537759 0.671875,5.552734 0.213227,1.38826 0.227747,3.299953 0.382812,5.488281 l 1.347656,0.75 -0.535156,1.742188 -1.234375,0.992187 c 0.0103,2.13035 0.571167,3.83145 0.136719,5.81836 -0.342436,1.56609 -0.516228,3.40887 -0.794922,5.68164 l 0.642578,0.98828 1.339844,0.80469 -1.550781,1.18555 c -0.09057,0.42322 -1.744931,4.4969 -1.860087,4.86563 -0.236245,0.75646 0.460804,3.98621 0.936774,7.53087 0.475969,3.54466 0.541455,5.82586 0.494183,7.71566 1.367175,-0.0889 3.451852,-0.82344 4.636719,-0.85547 1.768909,-0.0478 3.043869,-0.1037 4.998046,-0.004 l -0.06641,-2.36524 2.019532,2.04102 c 0.899909,-0.13558 1.833405,-0.26085 2.822265,-0.36719 5.18659,-0.55777 10.268284,-0.17793 15.695313,0.46875 l 0.134765,-1.33984 0.728516,1.45507 c 1.504645,0.18321 3.010405,0.37442 4.515625,0.57227 1.163519,0.15293 2.313543,0.25105 3.457031,0.32812 l 1.429688,-2.13281 2.814453,1.96485 1.070312,-1.875 0.486328,2.20898 c 4.046042,-0.015 7.989122,-0.21696 11.861328,-0.11523 0.553714,0.0145 0.910619,0.19396 1.449219,0.19726 l 0.132813,-0.68555 0.558594,0.51172 c 0.215129,1.1e-4 0.387837,0.26858 0.601562,0.26758 l 0.490234,-1.04687 0.736328,0.8164 c 5.389004,-0.0597 9.251947,-0.81924 17.410157,-0.41992 2.55746,0.1252 7.110546,0.7709 11.240235,1.03711 L 105.5,132.75 l 4.01758,0.0898 1.47265,-0.9375 1.40821,1.60743 c 1.83318,-0.0108 4.85422,-0.3997 6.30468,-0.60547 5.42024,-0.17479 10.3649,-0.67587 15.51172,-0.61328 4.51772,0.0549 8.40326,0.0837 14.36719,0.32617 l 2.54297,-2.09961 3.21484,1.78515 0.53516,-1.16015 2.22461,2.22461 2.96875,-0.15039 c 1.23048,0.41713 4.21883,1.00235 7.37695,1.40429 l 2.69922,-1.42382 1.99024,1.4414 c 0.72066,0.11392 2.75127,-0.011 3.4707,-0.0351 0.88366,-0.0296 2.8894,-0.076 5.33398,-0.28907 l 3.66797,-1.29687 1.51953,-2.20117 c -0.31142,-1.46352 -0.27658,-3.02825 -0.47461,-4.27344 -0.18868,-1.18628 -0.45358,-1.77754 -0.61718,-3.39453 l -1.23243,0.0937 1.30079,-2.01563 c -0.12595,-1.36892 0.37372,-4.9869 0.26757,-6.54101 -0.16009,-2.34395 -0.84698,-5.07044 -0.53013,-7.94922 l -0.85937,-0.53906 c 0.47179,-0.48402 0.85304,-0.86897 1.09375,-1.40625 l -0.91407,-1.1836 1.21875,-0.75195 c -0.01,-0.82015 -0.59065,-1.26765 -0.73828,-2.02735 -0.27622,-1.421772 -0.85364,-5.110649 -1.375,-6.367182 1.07093,-1.179536 1.48014,-0.843266 2.33789,-2.580079 -0.70347,-0.411067 -1.24761,-0.977079 -2.08789,-1.478515 1.07767,-0.663373 1.42804,-0.514675 1.86524,-1.097656 -0.32174,-2.636557 -0.39349,-5.433232 -0.20703,-7.22461 0.25886,-2.486906 -1.26988,-7.798335 -0.53125,-11.865234 -0.3838,-0.122128 -0.60268,0.04641 -1.14649,0.0332 0.31411,-0.622004 0.87738,-1.375304 1.3457,-1.65625 -0.36852,-2.729759 0.0709,-6.556462 0.42924,-8.872997 -0.0858,-1.301118 -1.15004,-5.622904 -1.12845,-6.597706 0.0294,-1.326788 1.43157,-2.758456 1.32114,-4.142578 l -0.67968,-0.90625 0.58398,-0.03516 c -0.22069,-1.976798 -0.85648,-3.671658 -1.33398,-4.929687 -0.76955,-2.02747 -1.86326,-4.735159 -2.39454,-4.701172 -0.19944,0.01276 -5.42926,-0.03622 -5.76757,-0.03711 z m -1.36914,1.253906 c 0.91629,-0.026 5.67976,0.06434 6.28125,0.306641 0.64445,0.259601 1.25081,2.15095 1.79687,3.875 0.311,0.98196 0.61385,2.349029 0.79297,3.232421 l -1.7793,0 2.16016,2.375 c 0.0919,0.770505 -1.25299,1.590407 -1.17271,2.552735 0.17833,2.13777 1.47037,6.889368 1.47405,7.758649 -0.14456,0.796782 -0.95216,6.202158 -0.87835,8.708148 -0.51472,0.661135 -1.23531,1.654408 -2.01953,2.658203 0.64988,-0.09001 1.19147,0.109517 1.79297,-0.07227 -0.54276,2.05542 0.79935,7.611001 0.83398,9.410156 0.0511,2.652668 0.0472,6.190211 0.20313,8.634766 -1.18332,0.658841 -1.71566,1.073086 -3.33985,1.673828 0.83028,0.442539 2.16849,0.995565 2.80469,1.3125 -0.80629,1.234423 -1.17719,1.464282 -1.59765,2.080078 0.0128,1.616198 0.49201,4.758675 1.91015,8.087898 -0.72181,0.39026 -1.56888,0.80376 -2,1.32617 0.008,0.26572 0.79388,0.72097 1.42969,0.91992 -0.53579,1.02173 -1.72523,1.13347 -1.41406,1.49805 0.35663,0.41785 0.99426,0.69963 1.51172,1.14258 0.29425,2.49653 -0.27042,7.53895 -0.19253,9.48046 0.0643,1.6023 -0.51011,5.12497 -0.71094,6.25782 l -2.5625,1.57812 2.77344,0 c 0.98893,1.75193 1.05027,5.95432 1.05664,7.0332 0.003,0.57231 -5.52251,1.51248 -10.67578,1.56055 l -1.39844,-1.52539 0.0781,-1.95508 -1.07227,-2.65234 0,2.46289 -0.2207,1.04297 -4.25976,1.75781 c -1.91847,0.79167 -4.06329,-0.60759 -5.83594,-0.81641 -0.98028,-0.11547 -1.92512,-0.20422 -2.86133,-0.2871 l -1.32227,-1.57032 -2.02148,-2.90429 0.12695,2.77734 -2.27343,-1.13672 -1.64063,-3.4082 0.125,3.78711 -2.74609,2.00781 c -3.04451,2.226 -7.06088,0.0486 -9.90821,-0.0508 -5.76554,-0.20128 -15.06697,0.30109 -22.14257,0.91797 -1.06603,0.0929 -2.1719,0.1556 -3.29297,0.20312 l -1.81055,-2.57226 -0.88477,2.01953 -5.30273,-0.125 -2.36914,0.60742 c -3.066358,0.78618 -6.311341,-0.3841 -9.285158,-0.66992 -3.262809,-0.31361 -9.529456,0.52937 -16.822265,0.71679 l -0.714844,-2.76757 -1.113281,2.50586 -2.273438,-1.4043 0.109375,1.61914 c -0.0053,-3e-5 -0.01037,3e-5 -0.01563,0 -3.328661,-0.0218 -7.145264,0.1147 -10.93164,0.0625 l -2.041016,-4.08008 -0.882812,3.03125 -2.904297,-1.51562 -0.572266,-2.83594 -0.402344,3.1543 -1.107421,1.69531 c -0.59084,0.9045 -2.111709,-0.341 -3.089844,-0.5918 -1.36661,-0.35041 -2.662574,-0.60369 -3.925782,-0.81836 l -1.509765,-3.1289 -0.6875,3.17773 c -5.051416,-0.68264 -8.070962,-0.74449 -11.708985,-0.55859 -1.322295,0.0676 -3.872734,0.45531 -5.138671,0.59375 l -3.306641,-2.93946 -1.037109,-1.00976 -0.535157,-2.14258 0.04492,2.72266 0.996094,1.1289 0.330078,3.01367 c -2.411985,-0.0959 -5.011258,-0.10548 -7.050781,0.36915 0.129174,-2.50562 -1.828584,-12.20111 -1.796092,-12.94581 0.380736,-1.00294 1.815314,-3.64927 1.959597,-4.77378 l 3.896484,-1.94727 -2.652344,-0.25195 -0.96289,-1.25391 c -0.811917,-1.05731 0.140803,-2.62633 0.335937,-3.73632 0.467934,-2.66179 0.636582,-5.11599 0.644531,-7.55079 l 2.003907,-0.84375 -1.390625,-0.378906 0.378906,-2.273438 -1.113281,-0.513672 c -0.172025,-3.186864 -0.485555,-6.505487 -0.691407,-10.375 l 2.5625,-0.853515 -1.640625,-1.136719 1.136719,-1.894531 -2.234375,-1.767578 c -0.0098,-1.183117 -0.0073,-2.399614 0.02344,-3.69336 0.01624,-0.68284 -0.530223,-4.281543 -0.527344,-8.36914 l 0.791015,-0.251954 1.339844,0.75586 -0.96289,-1.964844 -0.640625,-4.597656 c -0.119125,-0.854938 -0.634316,-8.484173 -0.03069,-9.032367 0.217891,-0.197881 0.967733,-1.64682 1.360744,-2.758913 l 0.939086,0.275758 1.827927,-0.60996 -1.645335,-0.151025 -0.708984,-0.673828 c -3.69e-4,-0.0032 0.0024,-0.01064 0.002,-0.01367 -0.08469,-0.55531 -1.007021,-3.571382 -1.15904,-5.600726 1.771035,0.127865 5.608579,-0.815157 10.0625,-0.894857 l 2.285156,0.8125 5.703126,-0.951172 c 3.039417,-0.04581 5.548136,-0.422266 8.716796,-0.416016 l 0.664063,1.806641 0.892578,-0.355469 0.494141,1.142578 0.951172,2.242188 0.02734,-2.94336 0.96875,-1.4375 c 2.836789,-0.445028 7.375519,1.280233 8.838251,1.401359 1.791042,0.0059 1.843326,-0.223172 8.123132,-0.410272 l 0.71875,1.923828 1.345703,-2.019532 c 3.230594,-0.110898 12.996786,-1.326459 13.905235,-1.262155 1.154779,0.08174 10.071948,0.09331 11.592083,0.324984 l 3.41323,2.101464 5.863287,-1.660157 1.00585,2.087891 0.13477,2.517578 0.87305,-2.664062 1.48828,-1.212891 1.16211,1.316406 3.60547,-2.222656 0.75781,1.894531 1.00976,-1.515625 5.61524,-0.408203 -0.20508,-0.873047 c 2.41236,-0.05165 4.8629,-0.241848 6.69531,-0.152343 2.97568,0.145347 5.4188,0.326907 8.28184,0.386471 l 2.93496,3.59595 1.80469,-2.927734 0.86133,2.224609 1.03711,-2.605468 c 4.26882,0.01279 7.90147,-0.09631 11.75976,-0.21875 l 1.17383,1.654296 0.61133,-1.710937 c 1.90071,-0.06953 3.74971,0.118663 5.52148,0.02734 l 3.1211,0.683593 2.9082,1.947266 -0.5625,-2.783203 c -0.30559,-1.512051 2.52536,-0.607515 3.92578,-0.714844 0.7961,-0.06101 4.24917,0.230627 6.99805,0.152623 z"')
        self.write(' />\n')
        if self.card_size == 'poker':
            self.end_group()

    def draw_pattern(self, id, pattern_raw, element):
        style_empty = 'opacity:1;fill:#c0c0c0;fill-opacity:1;stroke:none;stroke-width:0;stroke-linecap:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1'
        style_box = 'opacity:1;fill:none;fill-opacity:1;stroke:#000000;stroke-width:2;stroke-linecap:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1'
        
        pattern = [x.split() for x in pattern_raw]
        gheight = len(pattern)
        if gheight == 0:
            error('Missing pattern for %s' % id)
        if gheight > 3:
            error('Tall pattern for %s' % id)
        gwidth = len(pattern[0])

        offset = 26
        px0 = 13.25 + 6
        py0 = 50
        clone_x0 = 0
        clone_y0 = -276
        if gwidth % 2 == 0:
            px0 += offset / 2
            clone_x0 += offset / 2
            max_width = 6
        else:
            max_width = 7
        if gheight % 2 == 0:
            py0 += offset / 2
            clone_y0 += offset / 2
            max_height = 2
        else:
            py0 = 50
            max_height = 3

        dot_x0 = px0 + 10
        dot_y0 = py0 + 10

        x_begin = int((max_width - gwidth) / 2)
        x_end = x_begin + gwidth
        y_begin = int((max_height - gheight) / 2)
        y_end = y_begin + gheight
        
        if self.card_size == 'poker':
            self.start_group(transform='translate(%d,%d)' % (11.25,0))
        self.indent()
        for iy in range(0, max_height):
            for ix in range(0, max_width):
                if ix >= x_begin and ix < x_end and iy >= y_begin and iy < y_end:
                    x = ix * offset
                    y = iy * offset

                    col = ix - x_begin
                    row = iy - y_begin
                    cell = pattern[row][col]
                    if cell == '@':
                        self.write('<use x="0" y="0" xlink:href="#element-%s" transform="translate(%d,%d)" width="100%%" height="100%%" />\n' % (element, clone_x0 + x, clone_y0 + y))
                    elif cell == 'X':
                        self.write('<rect style="%s" width="20" height="20" x="%.3g" y="%.3g" />\n' % (style_box, px0 + x, py0 + y))
                    elif cell == '.':
                        self.write('<circle style="%s" id="center-dot" cx="%.3g" cy="%.3g" r="2.5" />\n' % (style_empty, dot_x0 + x, dot_y0 + y))
                    else:
                        error('Unrecognized pattern symbol: ' + cell)
        self.outdent()
        if self.card_size == 'poker':
            self.end_group()
        
    
    # Spell
    
    def validate_attrs(self, name, attrs):
        if name in self.name2id:
            error(name + ': Spell name already used by spell ID ' + str(self.name2id[name]))

        if not 'element' in attrs:
            error(name + ': Missing "element" attribute')
        if not attrs['element'] in self.valid_elements:
            error(name + ': Invalid element: ' + attrs['element'])
        
        if not 'category' in attrs:
            error(name + ': Missing "category" attribute')
        for cat in attrs['category'].split(','):
            if not cat in self.valid_categories:
                error(name + ': Invalid category: ' + cat)

        if not 'id' in attrs:
            error(name + ': Missing "id" attribute')
        if attrs['id'] in self.id2name:
            error(name + 'ID ' + str(attrs['id']) + ' already used by "'
                  + self.id2name[attrs['id']] +'"')
        
        if not 'pattern' in attrs:
            error(name + ': Missing "pattern" attribute')
        if not attrs['pattern'] in self.card_patterns:
            error(name + ': Invalid pattern: ' + attrs['pattern'])

        if not attrs['op'] in self.valid_ops:
            error(name + ': Invalid op: ' + attrs['op'])
        
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
            pattern_key = '%s:%s' % (pattern_id, attrs['element'])
            if pattern_key in self.pattern2id:
                dup_id = self.pattern2id[pattern_key]
                error('%s: Pattern %s already assigned to %d (%s)'
                      % (name, pattern_key, dup_id, self.id2name[dup_id]))
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
        
    def pattern_key(self, pattern):
        """Convert pattern array into a simple string that can be used as a key."""
        return '/'.join([''.join(x.split()) for x in pattern])
    
    def expand_desc(self, id, raw_desc):
        keys = ['cast', 'react', 'charged', 'sacrifice', 'notes', 'comment']
        prefix = {
            'cast': 'When cast: ',
            'react': 'Reaction: ',
            'charged': 'While charged: ',
            'sacrifice': 'Sacrifice: ',
            'notes': '',
        }

        # Ensure all keys are valid.
        for key in raw_desc.keys():
            if not key in keys:
                error('unknown key: %s' % key)
                
        # Ensure charged spells have a charge effect.
        if raw_desc['cast'] == '{{ADD_CHARGE}}':
            if not 'charged' in raw_desc and not 'sacrifice' in raw_desc:
                error('charged spell with no effect')            

        desc = []
        for key in keys:
            if not key in raw_desc:
                continue
            if key == 'comment':
                continue
            d = raw_desc[key]
            d = d.replace('{{ADD_CHARGE}}', 'Place a CHARGE on this spell.')
            d = d.replace('{{ADD_ACTION}}', 'Take another action.')
            desc.append(prefix[key] + d)
            desc.append('-')
        return desc

    # Utilities

    # override
    def write_svg_header_extra(self):
        self.write('<g inkscape:label="Icon Masters" inkscape:groupmode="layer" style="display:none">\n')

        # Water icon
        self.write('<g id="element-water" transform="matrix(0.33568916,0,0,0.31348783,-44.537788,309.84728)" style="display:inline;filter:url(#filter9446)">\n')
        self.write('<path sodipodi:nodetypes="ccccccccccc" inkscape:connector-curvature="0" id="path8407" d="m 216.17966,66.561481 c -1.5117,0.245633 -3.1675,1.500335 -4.62784,1.955201 -4.49775,1.925116 -9.05232,1.674803 -13.80832,0.540821 -2.12278,-0.375275 -5.32978,-1.191672 -7.43587,-1.591486 -5.85396,-0.506675 -10.5059,2.585118 -14.99395,6.014542 -1.4384,1.355103 -0.024,2.901987 1.93712,2.65801 2.26464,-0.665698 5.0678,-1.014101 7.29982,-2.39671 2.81804,-1.398042 6.96422,-2.08651 10.03167,-0.830718 5.22123,1.560223 9.98052,2.194805 15.34157,0.806822 3.14588,-0.718653 5.14146,-2.094221 7.64699,-4.167305 1.25145,-1.416861 0.49345,-3.14775 -1.39119,-2.989177 z" style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#00007e;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />\n')
        self.write('<path sodipodi:nodetypes="cccccccccc" inkscape:connector-curvature="0" id="path8409" d="m 224.21149,79.164167 c -3.12271,-0.08421 -3.5103,1.883595 -7.88451,1.956941 -5.33478,0.444095 -8.88015,-0.974771 -14.18696,-1.280536 -7.01949,-0.677004 -14.71165,3.567569 -21.10815,5.409683 -1.68954,1.02507 0.1228,3.231431 2.0916,3.402099 1.75093,-0.0063 2.3243,0.412596 4.03219,0.07782 5.28968,-1.691086 8.684,-5.974404 14.1641,-5.291836 5.52858,0.544071 12.97732,3.078023 18.50994,1.869614 1.75091,-0.74805 3.3381,-1.841409 4.59247,-3.21858 0.89156,-1.443524 1.48689,-2.977774 -0.21068,-2.925207 z" style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#00007e;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />\n')
        self.write('<path sodipodi:nodetypes="cccccccccc" inkscape:connector-curvature="0" id="path8411" d="m 227.94003,90.184189 c -2.30667,0.25193 -5.55002,2.748345 -7.90913,2.884383 -4.39755,0.64283 -9.96594,-0.89292 -14.3607,-1.029109 -7.44154,-0.197688 -11.58941,3.367015 -18.49294,5.782161 -1.74596,0.925703 0.05,2.180286 2.0056,2.464466 1.59957,0.1379 4.15708,-0.89902 5.67568,-1.269645 4.12399,-1.468379 7.77185,-2.633032 12.1793,-2.023285 5.82477,1.088337 9.57118,1.627599 15.28231,0.658956 1.86369,-0.574648 3.65164,-2.550727 5.32809,-3.484689 1.51676,-1.318484 2.30214,-4.043109 0.29179,-3.983238 z" style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#00007e;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />\n')
        self.write('</g>\n')

        # Earth icon
        self.write('<g id="element-earth" style="display:inline;filter:url(#filter9446)" transform="matrix(0.33568916,0,0,0.31348783,-78.199398,278.79309)">\n')
        self.write('<path sodipodi:nodetypes="ccccc" inkscape:connector-curvature="0" id="path9283" d="m 301.64648,186.74023 c -1.76614,1.2025 -3.89969,5.27677 -5.24414,9.6875 -1.04233,2.81351 3.17744,4.37762 4.22071,1.56446 0.53628,-3.64672 2.38966,-8.29867 2.38966,-8.29867 0.55702,-1.43946 0.17605,-2.89237 -1.36623,-2.95329 z" style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#004c00;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />\n')
        self.write('<path sodipodi:nodetypes="ccccc" inkscape:connector-curvature="0" id="path9285" d="m 309.29842,188.25454 c -1.24188,0.0183 -2.23406,1.25387 -2.2168,2.49576 l -0.64354,11.39006 c -0.043,3.04273 4.32852,0.68309 4.28548,-2.35964 -0.29494,-2.45976 0.61166,-7.70971 -1.42514,-11.52618 z" style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#004c00;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />\n')
        self.write('<path sodipodi:nodetypes="cccscc" inkscape:connector-curvature="0" id="path9287" d="m 314.91657,186.89588 c -1.70622,0.0862 -1.73256,0.89494 -0.83938,2.35126 0,0 3.40403,6.16758 4.58385,10.02881 1.50948,2.66303 6.25738,2.19611 4.72719,-1.22432 -1.82336,-4.07574 -6.40721,-10.03075 -6.40721,-10.03075 -0.42196,-0.73326 -1.21953,-1.1679 -2.06445,-1.125 z" style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#004c00;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />\n')
        self.write('<path sodipodi:nodetypes="ccccccccc" inkscape:connector-curvature="0" id="path9237" d="m 288.19561,168.1501 c -0.7353,0.0173 -4.2044,3.28883 -4.61093,3.90178 -2.30582,3.47722 -3.83023,5.43548 -6.3757,9.2489 -1.66453,2.49592 1.43507,3.06269 3.1006,0.56744 1.9411,-2.908 6.43135,-8.02229 7.85383,-8.52656 0,0 4.67526,3.61461 6.2249,4.50133 2.60888,1.51447 5.6142,-0.0586 2.98907,-1.54466 0.35219,0.202 -2.26884,-1.88692 -3.32123,-3.25973 -1.48005,-1.84578 -4.05702,-4.20408 -5.86054,-4.8885 z" style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#004c00;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />\n')
        self.write('<path sodipodi:nodetypes="ccscccccscccccsccccc" inkscape:connector-curvature="0" id="path9239" d="m 309.00977,161.41602 c -0.50305,0.0252 -0.98309,0.21846 -1.36329,0.54882 -2.42687,2.10718 -4.33784,5.49414 -6.32862,8.70899 -1.98533,3.20605 -5.75777,8.47897 -6.28787,9.27599 -5.32818,5.98219 -7.41497,11.69385 -13.75049,18.4131 -1.96094,2.27083 2.08885,2.53082 4.04979,0.25999 6.29262,-7.29089 7.89517,-9.709 12.80292,-15.14496 0.0733,-0.0816 2.60744,-2.95705 3.63339,-4.44276 0.91183,-1.36599 1.14455,-2.9044 3.05667,-5.99222 1.30051,-2.10017 2.81587,-4.68505 4.01367,-5.31886 1.54953,1.70978 3.96352,4.03035 6.13378,8.89088 1.82198,2.59687 5.06443,6.47082 5.6005,7.2741 1.66466,2.55908 5.31742,7.21734 5.65912,7.8935 1.35263,2.67911 1.93897,-1.17403 1.01441,-4.38894 -0.71242,-1.40972 -1.23105,-3.38885 -2.90205,-5.95769 -1.671,-2.56883 -3.78371,-4.55609 -4.2171,-5.33305 l -1.73355,-2.93075 c -1.49462,-3.57419 -4.04795,-4.91858 -7.31691,-10.62724 -0.42092,-0.73477 -1.21871,-1.17102 -2.06445,-1.1289 z" style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#004c00;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />\n')
        self.write('</g>\n')

        # Fire icon
        self.write('<path style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#860000;fill-opacity:0.9745098;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;filter:url(#filter9446);color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" d="m 349.83863,15.938294 c -0.64354,0.69716 0.0714,2.14763 0.0714,2.14763 0,0 0.55185,2.37214 0.75843,4.54618 0.20659,2.17404 -0.0378,3.98798 -0.17022,5.27121 -0.21324,2.06596 -1.95026,5.96682 -3.28642,8.1392 -1.33616,2.17237 -2.19347,4.3801 -2.30243,7.06973 -0.0223,0.55126 0.17044,1.61314 0.25358,2.13246 -1.50437,1.76498 -3.13649,2.63382 -4.67579,3.09375 -2.07253,0.61947 -5.30101,2.30797 -8.08852,5.06277 -2.22249,2.19641 -3.11159,4.23435 -3.85907,7.06451 -0.74749,2.83017 -1.21306,5.15441 -0.93594,7.23275 0,0 0.0289,2.43353 0.77968,3.1307 1.01893,0.21451 2.55503,-0.95753 2.55503,-0.95753 3.1676,-2.40708 6.08306,-4.67688 8.56877,-5.48761 2.70803,-0.88325 5.56997,-0.59913 7.42537,0.003 2.43757,0.79138 5.07675,0.43601 7.63086,-0.15625 1.75956,-0.40802 2.93739,-1.34497 4.23186,-2.5433 1.72356,1.41363 2.77621,1.68436 4.00821,2.68074 1.51302,1.22367 3.25735,2.36974 5.94352,3.11842 2.80535,0.78189 6.01463,0.84546 8.99219,0.42773 2.97755,-0.41773 5.70224,-1.19564 7.63867,-2.9707 0,0 1.66343,-1.23799 1.50254,-1.93515 -0.37564,-0.63882 -2.02436,-1.32074 -2.02436,-1.32074 0,0 -1.83025,-0.75564 -3.88996,-1.97265 -2.05971,-1.21704 -3.65008,-3.3477 -5.02999,-4.65331 -1.6333,-1.54536 -2.06831,-3.62018 -2.78284,-5.72362 -0.71077,-2.09239 -1.60086,-4.78144 -4.34961,-6.69727 -1.31692,-0.91786 -2.59747,-1.70064 -3.96875,-2.23828 -0.32734,-1.50008 -0.31121,-2.89988 -0.13507,-4.43879 0.53962,-2.8161 -0.28736,-6.5882 -1.27327,-9.29702 -1.04011,-2.85773 -3.1895,-4.33553 -4.58319,-5.89194 -1.48506,-1.65845 -3.56485,-3.46995 -5.66733,-4.31095 0,0 -1.29946,-0.5793 -3.33733,-0.52567 z m 4.47715,5.8549 c 0.49831,0.41112 2.0104,1.44244 2.76207,2.24067 1.75757,1.86644 3.23372,4.53046 3.54048,6.51195 0.29872,1.92953 -0.0507,3.63254 -0.25797,5.44286 -0.13334,1.16501 0.018,2.45375 0.46432,3.68571 -0.35581,0.0206 -1.24569,0.0523 -1.61292,0.10547 -1.22544,0.17753 -2.52004,0.53511 -3.91601,1.0586 -2.89087,1.01546 -0.65882,1.6327 2.26266,1.3309 2.28051,-0.12522 4.42276,1.08875 5.83067,1.76026 1.15057,0.54878 3.03142,1.93023 3.60063,2.93387 1.1089,1.95521 2.59211,4.33643 2.8076,5.40292 0.39023,1.93127 1.10468,3.78826 3.15006,6.35682 1.84431,2.31606 4.20223,3.10458 6.46617,4.44765 -0.20222,0.66695 -2.03074,1.21656 -2.6028,1.29682 -2.44038,0.34237 -5.07212,-0.23197 -6.85484,-1.21479 -1.94759,-1.07371 -3.25658,-1.07108 -4.89236,-2.17717 -1.07414,-0.72632 -2.53248,-1.23412 -3.28269,-2.75364 0.98947,-2.31732 2.06345,-4.4314 2.4563,-6.69028 0.62494,-3.03096 -2.32705,-0.0432 -3.59738,2.26218 -1.34951,3.05746 -3.53484,5.4073 -6.82388,6.57601 -2.1296,0.75672 -3.95716,0.0463 -5.93421,-0.38116 -1.97703,-0.42738 -4.74167,-0.90022 -8.32812,0.26953 -2.4664,0.80443 -5.70038,1.727 -8.04512,4.49157 -0.25626,-1.42864 0.43116,-2.88637 0.64648,-3.58163 0.70802,-2.2861 2.74177,-4.59831 4.09035,-5.93107 2.05301,-2.02892 4.61944,-2.63372 6.74442,-3.26887 1.57061,-0.46945 2.24348,-0.43339 3.87832,-1.88578 1.19767,2.07265 2.88979,3.78446 4.89649,5.16406 2.47255,1.69995 1.89499,-1.16784 -0.48289,-3.93651 -1.55071,-1.80557 -2.11148,-3.38258 -2.33316,-7.31418 -0.11303,-2.00463 0.81831,-4.20231 2.09537,-6.27861 1.65628,-2.4555 3.0526,-4.61973 3.40006,-7.986 0.20849,-2.6641 0.40821,-6.10123 -0.1281,-7.93816 z" id="element-fire" inkscape:connector-curvature="0" sodipodi:nodetypes="ccssssccsscccssscssscccssssccssccccsscsccsssscssscccscscssscccssccc" transform="matrix(0.33568916,0,0,0.31348783,-96.660538,322.39616)" />\n')

        # Air icon
        self.write('<path style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#303030;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;filter:url(#filter9446);color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" d="m 266.01465,20.022074 c -2.16402,-0.8284 -3.9519,-0.99856 -5.87013,-0.70145 -3.36627,0.52139 -8.04819,1.60863 -11.79423,3.41656 -4.04421,1.95184 -4.97919,3.43786 -8.29607,5.40439 -3.09009,1.83206 -6.21891,3.10498 -8.67834,5.89178 -1.22481,1.38784 -0.14531,2.45627 0.58855,2.20785 4.04323,-1.36867 5.96167,-3.07787 8.41835,-4.65429 2.26034,-1.45044 1.4983,0.1591 5.6097,-2.75252 3.60063,-2.54991 4.31189,-2.96395 6.19587,-3.35206 1.03959,-0.46928 2.11768,-0.9525 3.39564,-1.38115 2.99741,-0.81841 3.38181,-0.58783 7.11477,-0.27515 3.05917,0.25624 6.21552,1.46472 7.57776,2.84244 1.53658,1.55403 4.78665,1.8127 7.75363,8.15531 1.21998,2.60799 1.59561,5.29271 1.34571,7.95703 0.2661,2.05534 1.43491,2.82674 -0.012,9.04492 -1.07426,3.88605 -4.08337,7.53559 -7.94532,9.23828 -4.51384,1.99011 -9.72023,2.33631 -14.19921,1.19727 -4.31442,-1.0972 -8.99174,-5.00508 -9.89255,-9.17996 -0.87827,-4.07043 -1.564,-7.60679 -1.72857,-10.84153 0.35166,-3.99309 4.22352,-3.90769 7.63791,-6.6723 2.33727,-1.00332 3.9923,-2.663 7.20288,-2.663 2.74945,0.40006 5.69059,2.15451 6.7562,4.08005 2.28373,2.31721 3.32408,5.31496 2.61025,9.13339 0.10873,1.92351 -3.15649,5.13369 -5.04286,5.48368 -2.3545,0.43684 -5.31298,-1.52296 -6.77567,-2.25803 -1.39611,-0.4218 -1.30359,-1.00344 -0.72586,-3.17402 0.69608,-1.05513 2.00902,-1.71771 2.80422,-2.24703 0.9617,-0.64015 1.03664,-1.9396 0.76954,-2.98852 -0.58508,-0.87154 -1.16457,-1.48311 -2.57907,-1.0196 -0.96592,0.31652 -2.75435,0.51256 -3.16951,0.92221 -0.67499,0.65674 -2.52925,1.72885 -3.04126,2.48143 -0.48514,1.75438 0.50199,3.68043 0.68579,5.1875 0.23726,1.7865 1.20702,3.84658 3.24415,4.86328 3.07144,1.53291 6.88351,2.30295 9.25093,2.18613 2.89121,-0.3233 8.55766,-2.89879 8.61644,-9.00849 -0.15355,-2.8792 -1.67895,-8.6497 -3.74823,-12.44325 -2.10401,-3.85721 -5.08264,-5.50215 -9.30932,-5.47107 -2.15208,0.19742 -5.2721,0.46643 -9.80439,3.24208 -5.2349,2.09616 -6.0427,2.96843 -9.65488,7.17711 -2.35407,2.74279 -0.29937,7.74981 -0.29937,7.74981 1.66337,3.75798 0.85898,4.20056 2.50553,8.56764 2.1542,5.71353 6.96147,9.97412 12.49609,11.24024 4.47407,1.0235 15.01795,-0.8329 17.30471,-1.39255 6.49182,-1.58879 8.63642,-4.62508 10.53125,-12.54688 1.25967,-5.26636 0.30251,-9.82479 0.0778,-11.65157 -0.2849,-2.31648 -1.0879,-6.15195 -1.72646,-7.85819 -1.46974,-3.56177 -6.22726,-7.07122 -10.05997,-10.5856 -3.56795,-3.18868 -2.76595,-1.2604 -6.14044,-2.55217 z" id="element-air" inkscape:connector-curvature="0" sodipodi:nodetypes="csssssssccsssccssscccccsccscscccsccsccsssssssccsc" transform="matrix(0.33568916,0,0,0.31348783,-64.127898,322.50497)" />\n')

        self.write('</g>\n')  # Icon Masters

        self.write('<g inkscape:label="Op Masters" inkscape:groupmode="layer" style="display:none">\n')

        # Op: Recover Thread
        self.write('<g id="op-thread" transform="matrix(0.26666668,0,0,0.26666668,-323.80782,107.89466)">\n')
        self.write('<g transform="translate(250.53066,344.61599)" id="g1728">')
        self.write('<rect y="612.31451" x="1314.0823" height="77.024132" width="77.024132" id="rect1710" style="fill:#e0e0e0;fill-opacity:1;fill-rule:nonzero;stroke:#000000;stroke-width:3.54330707;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1" />')
        self.write('<circle style="fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#000000;stroke-width:6.37795258;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1" id="circle1712" cx="1352.5944" cy="650.8266" r="27.657145" />')
        self.write('<g id="g1726" transform="rotate(-45,1395.1842,388.72087)">')
        self.write('<g id="g1718">')
        self.write('<path style="color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" d="m 1167.2313,537.94202 h 25.0012" id="path1714" inkscape:connector-curvature="0" />')
        self.write('<path inkscape:connector-curvature="0" id="path1716" d="m 1167.2313,549.94202 h 25.0012" style="color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />')
        self.write('</g>')
        self.write('<g transform="rotate(90,1179.7319,543.94201)" id="g1724">')
        self.write('<path inkscape:connector-curvature="0" id="path1720" d="m 1167.2313,537.94202 h 25.0012" style="color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:3.98622036;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />')
        self.write('<path style="color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:3.98622036;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" d="m 1167.2313,549.94202 h 25.0012" id="path1722" inkscape:connector-curvature="0" />')
        self.write('</g>')
        self.write('</g>')
        self.write('</g>')
        self.write('<circle style="fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#000000;stroke-width:6.37795305;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1" id="circle1730" cx="1734.8711" cy="995.44257" r="27.657146" />')
        self.write('<path inkscape:connector-curvature="0" id="path1732" d="m 1671.8848,972.36053 v 12.20313 h -19.5254 v 21.75784 h 19.5254 v 12.2031 l 25.002,-23.08203 z" style="color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:5;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" sodipodi:nodetypes="cccccccc" />')
        self.write('</g>\n')  # op-thread

        # Op: Create Eye
        self.write('<g transform="matrix(0.26666668,0,0,0.26666667,-326.28493,132.89467)" id="op-eye">')
        self.write('<g transform="translate(273.57095,210.77637)" id="g1704">')
        self.write('<path d="m 1499.5153,712.97971 -38.2151,22.06351 -38.2152,-22.06351 0,-44.12702 38.2152,-22.06351 38.2151,22.06351 z" inkscape:randomized="0" inkscape:rounded="0" inkscape:flatsided="true" sodipodi:arg2="1.0471976" sodipodi:arg1="0.52359878" sodipodi:r2="38.215118" sodipodi:r1="44.127022" sodipodi:cy="690.9162" sodipodi:cx="1461.3002" sodipodi:sides="6" id="path1694" style="fill:#e0e0e0;fill-opacity:1;fill-rule:nonzero;stroke:#000000;stroke-width:3.54330707;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1" sodipodi:type="star" />')
        self.write('<circle style="fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#000000;stroke-width:6.37795258;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1" id="circle1696" cx="1461.3002" cy="690.9162" r="27.657145" />')
        self.write('<g id="g1702" transform="translate(-24.615722,-99.147628)">')
        self.write('<path id="path1698" transform="matrix(0.9375,0,0,0.9375,-5.04417,-48.798175)" d="m 1590.3574,884.07227 a 20.714284,20.714284 0 0 0 -18.125,10.69531 20.714284,20.714284 0 0 0 18.125,10.73242 20.714284,20.714284 0 0 0 18.125,-10.69531 20.714284,20.714284 0 0 0 -18.125,-10.73242 z" style="fill:none;fill-opacity:1;stroke:#000000;stroke-width:4.25196838;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;paint-order:markers fill stroke" inkscape:connector-curvature="0" />')
        self.write('<path id="path1700" transform="matrix(0.9375,0,0,0.9375,-5.04417,-48.798175)" d="m 1590.3496,884.57422 a 20.714284,20.714284 0 0 0 -2.707,10.21094 20.714284,20.714284 0 0 0 2.7207,10.21093 20.714284,20.714284 0 0 0 2.709,-10.21093 20.714284,20.714284 0 0 0 -2.7227,-10.21094 z" style="fill:#000000;fill-opacity:1;stroke:none;stroke-width:4.25196838;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;paint-order:markers fill stroke" inkscape:connector-curvature="0" />')
        self.write('</g>')
        self.write('</g>')
        self.write('<circle style="fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#000000;stroke-width:6.37795305;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1" id="circle1706" cx="1603.125" cy="901.69257" r="27.657146" />')
        self.write('<path inkscape:connector-curvature="0" id="path1708" d="m 1662.5098,878.61053 v 12.20313 h -19.5254 v 21.75782 h 19.5254 v 12.20312 l 25.002,-23.08203 z" style="color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:5;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" sodipodi:nodetypes="cccccccc" />')
        self.write('</g>')  # op-eye

        # Op: Move
        self.write('<g style="display:inline" transform="matrix(0.26666668,0,0,0.26666668,-275.04965,57.894638)" id="op-move">')
        self.write('<path sodipodi:type="star" style="fill:#e0e0e0;fill-opacity:1;fill-rule:nonzero;stroke:#000000;stroke-width:3.54375005;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1" id="path1786-9" sodipodi:sides="6" sodipodi:cx="1443.2209" sodipodi:cy="1182.9426" sodipodi:r1="44.127022" sodipodi:r2="38.215118" sodipodi:arg1="0.52359878" sodipodi:arg2="1.0471976" inkscape:flatsided="true" inkscape:rounded="0" inkscape:randomized="0" d="m 1481.4361,1205.0061 -38.2152,22.0635 -38.2151,-22.0635 0,-44.127 38.2151,-22.0635 38.2152,22.0635 z" />')
        self.write('<path style="color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:5;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" d="m 1443.2209,1152.7807 c -4.9043,0.1751 -7.3301,3.7938 -7.8379,6.2177 -0.5143,2.4545 0.7003,7.1809 0.7003,7.1809 0,0 -6.8245,2.5193 -9.7209,4.6417 -2.4698,1.8098 -5.9666,4.4615 -6.3931,7.7946 -0.2653,2.0729 1.664,3.7354 3.6785,4.2914 2.6403,0.7289 7.6508,-2.4664 9.1078,-0.2628 1.4342,1.7192 -1.3311,6.5358 -3.1529,9.3707 -2.8609,4.4521 -6.8811,13.5207 -4.4662,13.5741 2.5013,0.055 9.0709,-0.046 13.0492,-0.1747 1.5284,-0.049 3.1085,-7.7072 5.0352,-7.7072 1.9267,0 3.5074,7.6578 5.0358,7.7072 3.9783,0.1286 10.5479,0.2301 13.0492,0.1747 2.415,-0.053 -1.6059,-9.122 -4.4669,-13.5741 -1.8217,-2.8349 -4.5864,-7.6515 -3.1522,-9.3707 1.457,-2.2036 6.4675,0.9917 9.1079,0.2628 2.0145,-0.556 3.9431,-2.2185 3.6778,-4.2914 -0.4265,-3.3331 -3.9234,-5.9848 -6.3932,-7.7946 -2.8964,-2.1224 -9.7209,-4.6417 -9.7209,-4.6417 0,0 1.2153,-4.7264 0.7011,-7.1809 -0.5079,-2.4239 -2.9343,-6.0426 -7.8386,-6.2177 z" id="path1788-1" inkscape:connector-curvature="0" />')
        self.write('<path d="m 1557.8664,1205.0061 -38.2152,22.0635 -38.2151,-22.0635 0,-44.127 38.2151,-22.0635 38.2152,22.0635 z" inkscape:randomized="0" inkscape:rounded="0" inkscape:flatsided="true" sodipodi:arg2="1.0471976" sodipodi:arg1="0.52359878" sodipodi:r2="38.215118" sodipodi:r1="44.127022" sodipodi:cy="1182.9426" sodipodi:cx="1519.6512" sodipodi:sides="6" id="path1865-2" style="fill:#e0e0e0;fill-opacity:1;fill-rule:nonzero;stroke:#000000;stroke-width:3.54375005;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1" sodipodi:type="star" />')
        self.write('<path sodipodi:nodetypes="cccccccc" style="color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:5;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" d="m 1493.3778,1159.8605 v 12.2032 h -19.5254 v 21.7578 h 19.5254 v 12.2031 l 25.002,-23.082 z" id="path1867-7" inkscape:connector-curvature="0" />')
        self.write('</g>')  # op-move

        # Op: Move OR Create Eye
        self.write('<g id="op-move-eye" transform="matrix(0.26666668,0,0,0.26666668,-340.2456,57.894638)">')
        self.write('<path style="color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:none;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:5;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" d="m 1715.4749,1139.7388 -22.6987,86.4075" id="path5485-8-6" inkscape:connector-curvature="0" sodipodi:nodetypes="cc" />')
        self.write('<use style="display:inline" x="0" y="0" xlink:href="#op-eye" id="use961-3" transform="matrix(3.7499998,0,0,3.7499998,1411.0684,-217.10495)" width="100%" height="100%" />')
        self.write('<use style="display:inline" x="0" y="0" xlink:href="#op-move" id="use1054" transform="matrix(3.7499998,0,0,3.7499998,1117.6861,-217.10487)" width="100%" height="100%" />')
        self.write('</g>')  # op-move-eye        

        # Op: Draw Tapestry Card OR Create Eye
        self.write('<g id="op-tapestry-eye" transform="matrix(0.26666668,0,0,0.26666668,-372.00644,82.89466)">')
        self.write('<g transform="translate(807.2099,393.41422)" id="g1756">')
        self.write('<rect transform="rotate(90)" rx="13.110236" y="-943.87103" x="655.91614" height="124.01575" width="79.724411" id="rect1740" style="fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#000000;stroke-width:5;stroke-linecap:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />')
        self.write('<g transform="matrix(0.95,0,0,0.95,44.093156,34.788917)" id="g1754">')
        self.write('<rect y="-935.68457" x="661.95691" height="29.642857" width="29.642857" id="rect1742" style="fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;stroke-linecap:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" transform="rotate(90)" />')
        self.write('<rect style="fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;stroke-linecap:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" id="rect1744" width="29.642857" height="29.642857" x="699.95691" y="-935.68457" transform="rotate(90)" />')
        self.write('<rect style="fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;stroke-linecap:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" id="rect1746" width="29.642857" height="29.642857" x="661.95691" y="-896.68451" transform="rotate(90)" />')
        self.write('<rect y="-896.68451" x="699.95691" height="29.642857" width="29.642857" id="rect1748" style="fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;stroke-linecap:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" transform="rotate(90)" />')
        self.write('<rect y="-857.68451" x="661.95691" height="29.642857" width="29.642857" id="rect1750" style="fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;stroke-linecap:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" transform="rotate(90)" />')
        self.write('<rect style="fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:2;stroke-linecap:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" id="rect1752" width="29.642857" height="29.642857" x="699.95691" y="-857.68451" transform="rotate(90)" />')
        self.write('</g>')
        self.write('</g>')
        self.write('<path sodipodi:nodetypes="cc" inkscape:connector-curvature="0" id="path1878" d="m 1818.5999,1045.9888 -22.6987,86.4075" style="color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:none;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:5;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />')
        self.write('<use style="display:inline" x="0" y="0" xlink:href="#op-eye" id="use961" transform="matrix(3.7499998,0,0,3.7499998,1514.1934,-310.85496)" width="100%" height="100%" />')
        self.write('</g>\n')  # op-tapestry-eye
        
        # Op: Draw Tapestry Card OR Create Eye
        self.write('<g id="op-eye-thread" transform="translate(0,20)">')
        self.write('<use height="100%" width="100%" transform="translate(-40,-20)" id="use904" xlink:href="#op-eye" y="0" x="0" />')
        self.write('<use height="100%" width="100%" transform="translate(40,-20)" id="use906" xlink:href="#op-thread" y="0" x="0" />')
        self.write('<path style="color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:none;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:1.33333337;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" d="m 121.83788,341.82502 -6.05299,23.042" id="path1878-3" inkscape:connector-curvature="0" sodipodi:nodetypes="cc" />')
        self.write('</g>\n')

        self.write('</g>\n')  # Op Masters
                   
    def spell_link(self, sid):
        name = self.id2name[sid]
        link_name = '-'.join(name.lower().split())
        return ('[%s](#%s)' % (name, link_name))

    def element_name(self, e):
        if e == 'none':
            return 'Neutral'
        else:
            return e[0].upper() + e[1:]

    def category_list(self, cats):
        uppercats = []
        for cat in cats.split(','):
            uppercat = ' '.join([catword[0].upper() + catword[1:] for catword in cat.split('-')])
            uppercats.append(uppercat)
        catstr = ', '.join(uppercats)
        return catstr

    def gen_spell_summary(self):
        summary = open('../docs/spell-list.md', "w")

        summary.write('# List of Spell Fragments\n\n')

        now = datetime.datetime.now()
        summary.write('Generated on %04d/%02d/%02d @ %02d:%02d\n\n' % (now.year, now.month, now.day, now.hour, now.minute))

        summary.write('## By Category\n\n')
        print('Categories')

        for c in sorted(self.valid_categories):
            if not c in self.categories:
                continue
            summary.write('%s (%d)\n\n' % (self.category_list(c), len(self.categories[c])))
            print('  %s (%d)' % (self.category_list(c), len(self.categories[c])))

            names = [self.id2name[id] for id in self.categories[c]]
            for name in sorted(names):
                sid = self.name2id[name]
                summary.write('* %s - _%s_\n' % (self.spell_link(sid), self.element_name(self.id2attrs[sid]['element'])))

            summary.write('\n')
            
        summary.write('## By Element\n\n')
        print('Element')

        for e in self.valid_elements:
            eName = self.element_name(e)
            if not e in self.elements:
                continue
                
            summary.write('%s (%d)\n\n' % (eName, len(self.elements[e])))
            print('  %s (%d)' % (eName, len(self.elements[e])))

            names = [self.id2name[id] for id in self.elements[e]]
            for name in sorted(names):
                sid = self.name2id[name]
                summary.write('* %s - _%s_\n' % (self.spell_link(sid), self.category_list(self.id2attrs[sid]['category'])))

            summary.write('\n')

        print('Ops')
        for k,v in self.ops.items():
            print(' %s (%d)' % (k, len(v)))
        
        summary.write('## By Pattern\n\n')
        print('Patterns')
        for pattern_key,sid in sorted(self.pattern2id.items()):
            print(' ', pattern_key, '-', self.id2name[sid])
            (pattern, element) = pattern_key.split(':')
            sid = self.pattern2id[pattern_key]
            summary.write('* %s %s (%s)\n' % (pattern, self.spell_link(sid), element))
        summary.write('\n')
        
        summary.write('## By Name\n\n')
        count = 0

        for name,sid in sorted(self.name2id.items()):
            count += 1
            summary.write('### %s\n' % self.id2name[sid])
            summary.write('```\n')
            for prow in self.id2pattern[sid]:
                summary.write(prow + '\n')
            summary.write('```\n')
            summary.write('Element: %s\n\n' % self.element_name(self.id2attrs[sid]['element']))

            summary.write('Category: ')
            summary.write(self.category_list(self.id2attrs[sid]['category']))
            summary.write('\n\n')

            for d in self.expand_desc(sid, self.id2desc[sid]):
                if d == '-':
                    continue
                summary.write(d + '\n')
                summary.write('\n')

        print('Starters')
        for s in self.starters:
            attr = self.id2attrs[s]
            print(' {0} - {1} - {2}'.format(self.id2name[s], attr['element'], attr['op']))

        summary.close()
        print('Total spell count = %d' % count)
        if self.blank_count != 0:
            print('*** BLANK SPELLS *** = %d' % self.blank_count)
        
    def processing_summary(self):
        if self.verbose:
            print('Max ID:', self.max_id)
    
def usage():
    print("Usage: %s <options>" % sys.argv[0])
    print("where <options> are:")
    CardGen_OptionDesc()
    print("  --summary   Generate spell summary document")
    sys.exit(2)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],
            CardGen_ShortFlags,
            CardGen_LongFlags + ['summary'])
    except getopt.GetoptError:
        usage()

    #print(CardGen_LongFlags + ['summary'])
    options = CardGen_DefaultOptions
    options['summary'] = False
    options['per-page'] = 1
    for opt,arg in opts:
        if opt in ('--summary'):
            options['summary'] = True
        CardGen_ProcessOption(options, opt, arg)

    options['out-dir'] = 'spell-cards'

    cgen = SpellCardGen(options)
    cgen.generate_cards()
    if options['summary']:
        cgen.gen_spell_summary()
    cgen.processing_summary()

if __name__ == '__main__':
    main()
