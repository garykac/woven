#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from svg import SVG, Style, Node
from inkscape import Inkscape

class SVGCardGen(object):
    OPTIONS = {
	'out': {'type': 'string', 'default': "out", 'desc': "Output directory"},
	'png': {'type': 'bool', 'default': False, 'desc': "Generate PNG output files"},
	'per-page': {'type': 'int', 'default': 1, 'desc': "Set # of cards per page"},
    }
    
    def __init__(self, card_handler, card_data, options):
        self.card_handler = card_handler
        
        self.out_dir = options['out']
        self.svg_out_dir = os.path.join(self.out_dir, 'svg')
        self.png_out_dir = os.path.join(self.out_dir, 'png')
        self.gen_png = options['png']
        
        self.curr_filename = ''
        self.curr_file = 0  # Current file index
        
        self.cards_per_page = 1
        self.curr_card = 0  # Current card index on page

        self.card_width = options['width']
        self.card_height = options['height']

        # Card data to process.
        # This is an array where each element defines a single card.
        self.card_data = card_data

    def __create_svg_file(self):
        self.svg = SVG([self.card_width, self.card_height])

    def __write_svg_file(self, name):
        if not os.path.isdir(self.svg_out_dir):
            os.makedirs(self.svg_out_dir);
        out = os.path.join(self.svg_out_dir, '%s.svg' % name)
        self.svg.write(out)

        if self.gen_png:
            self.__gen_png(name)

    def __start_card_gen(self):
        self.curr_file = -1
        self.curr_card = -1
        self.curr_filename = ''
	
    def __end_card_gen(self):
        if self.curr_filename != '':
            print('Closing', self.curr_filename)
            self.__write_svg_file(self.curr_filename)

    # Generate PNG file.
    def __gen_png(self, name):
        if not os.path.isdir(self.png_out_dir):
            os.makedirs(self.png_out_dir);
        print("Exporting {0:s}.png".format(name))
        Inkscape.export_png(
            os.path.abspath(os.path.join(self.svg_out_dir, '{0:s}.svg'.format(name))),
            os.path.abspath(os.path.join(self.png_out_dir, '{0:s}.png'.format(name))),
            300)

    #
    # PUBLIC METHODS
    #

    def get_svg(self):
        return self.svg
    
    def generate_cards(self):
        self.__start_card_gen()

        for card_data in self.card_data:
            metadata = {
                'file': self.curr_file,
                'id': self.curr_card,
                }
            self._called_pre_card = False
            self._called_post_card = False
            self.card_handler.process_card_data(metadata, card_data)
            if not (self._called_pre_card and self._called_post_card):
                raise Exception("card handler should call both pre_card() and post_card()")

        # Fill out last sheet with blank cards.
        while self.curr_filename != '':
            self.pre_card()
            self.post_card()

        self.__end_card_gen()

    # Creates a new layer and returns the SVG node where the card should be added.
    def pre_card(self):
        if self._called_pre_card:
            raise Exception("pre_card() should only be called once per card")
        
        if self.curr_filename == '':
            self.curr_file += 1
            self.curr_filename = 'out{0:02d}'.format(self.curr_file)
            self.__create_svg_file()
            self.curr_card += 1

        layer = self.svg.add_inkscape_layer('card{0:02d}'.format(self.curr_card),
                                            "Card {0}".format(self.curr_card))

        cut_line = SVG.rect_round(0, 0, 0, self.card_width, self.card_height, 3)
        style = Style()
        style.set('fill', "#ffffff")
        style.set('stroke', "none")
        cut_line.set_style(style)
        SVG.add_node(layer, cut_line)
        
        self._called_pre_card = True
        return layer
	
    def post_card(self):
        if not self._called_pre_card:
            raise Exception("pre_card() should be called before post_card()")
        if self._called_post_card:
            raise Exception("post_card() should only be called once per card")
        
        if self.curr_card == (self.cards_per_page - 1):
            self.__write_svg_file(self.curr_filename)
            self.curr_filename = ''
            self.curr_card = -1
        self._called_post_card = True
