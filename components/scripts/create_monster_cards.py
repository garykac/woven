#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import getopt
import os
import platform
import subprocess
import sys

from data_monster_cards import monster_card_data
from data_monster_cards import monster_card_revision
from data_spell_patterns import spell_card_patterns
from inkscape import Inkscape, InkscapeActions
from svg import SVG, Style, Node
from svg_card_gen import SVGCardGen


MONSTER_DIR = os.path.join('..', 'monster-cards')
CARD_TEMPLATE = os.path.join(MONSTER_DIR, 'monster-card.svg')
PNG_OUTPUT_DIR = os.path.join(MONSTER_DIR, 'png')
PDF_5UP_DIR = os.path.join(MONSTER_DIR, '5up')

elem_map = {
	'a': 'air',
	'e': 'earth',
	'f': 'fire',
	'w': 'water',
}

# Spell attributes
monster_attributes = [
	'element', 'pattern', 'image', 'id', 'attack', 'actions',
]

symbols = [
	'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'm', 'r', 'w', 'y', 'z', 
]

base_attack_map = {
	'*': "attack-base1",
	'**': "attack-base2",
	'***': "attack-base3",
}

attack_map = {
	'*': "action-attack1",
	'**': "action-attack2",
	'***': "action-attack3",
}

attack_hexes = ['center',
				'top', 'bottom', 'top-left', 'top-right', 'bottom-left', 'bottom-right',
				'center-triangle']

# Spell description keys
spell_desc_keys = {
	'cast': {
	},
	'react': {
		'prefix': "Reaction",
	},
	'charged': {
		'prefix': "While charged",
	},
	'sacrifice': {
		'prefix': "Sacrifice charge",
	},
	'note': {
	},
}

# Spell info keys (appear at bottom of card).
spell_info_keys = {
	'prereq': {
		'prefix': "Prereq",
	},
	'target': {
		'prefix': "Target",
	},
	'trigger': {
		'prefix': "Trigger",
	},
	'cost': {
		'prefix': "Cost",
	},
}

OUTPUT_DIR = os.path.join('..', 'monster-cards')
CARD_TEMPLATE = os.path.join(OUTPUT_DIR, 'template', 'monster-template.svg')

class WovenMonsterCards():
	
	def __init__(self, options):
		self.next_id = 0
		self.name2id = {}
		self.pattern_elements = {}
		self.elements = {}
		self.id2name = {}
		self.id2pattern = {}
		self.id2attrs = {}
		self.id2desc = {}
		self.pattern2id = {}
		self.max_id = 0
		self.blank_count = 0
				
		self.valid_elements = ['none', 'air', 'fire', 'earth', 'water']

		# Poker size cards: 2.5" x 3.5" = 225px x 315px = 63.5mm x 88.9mm
		# Bridge size cards: 2.25" x 3.5" = 202.5px x 315px
		# Tarot size cards: 2.75" x 4.75" = 247.5px x 427.5px = 69.85 mm x 120.65
		self.width = 69.85
		self.height = 120.65
		options['width'] = self.width
		options['height'] = self.height
		
		# Set data for SVGCardGen.
		self.card_gen = SVGCardGen(self, options)

		# Initialize card patterns.
		self.card_patterns = spell_card_patterns

		
	#
	# DATA VALIDATION
	#
	
	def pattern_key(self, pattern):
		"""Convert pattern array into a simple string that can be used as a key."""
		return '/'.join([''.join(x.split()) for x in pattern])

	def validate_attrs(self, name, attrs):
		# Ensure all attributes are valid.
		for attr in attrs.keys():
			if not attr in monster_attributes:
				raise Exception(f"{name}: Unknown attribute: {attr}")
			
		if name in self.name2id:
			raise Exception(f"{name}: Spell name already used by spell ID {self.name2id[name]}")

		if not 'element' in attrs:
			raise Exception(f"{name}: Missing 'element' attribute")
		if not attrs['element'] in self.valid_elements:
			raise Exception(f"{name}: Invalid element: {attrs['element']}")
		
		if not 'id' in attrs:
			raise Exception(f"{name}: Missing 'id' attribute")
		if attrs['id'] in self.id2name:
			raise Exception(f"{name} ID {attrs['id']} already used by {self.id2name[attrs['id']]}")
		
		if not 'pattern' in attrs:
			raise Exception(f"{name}: Missing 'pattern' attribute")

	#
	# CARD GENERATION
	#

	def generate_cards(self):
		self.card_gen.generate_cards()

	# Returns an iterator that produces an object for each card.
	# This is a callback used by SVGCardGen
	def card_data(self):
		for card in monster_card_data:  #spell_card_blank_data:
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
		pattern = attrs['pattern']		
		element = attrs['element']

		border_types = ['outer', 'title', 'image', 'vertical', 'action']
		
		image = attrs['image']
		attack = attrs['attack']
		actions = attrs['actions']
		
		# Build list of template ids and then load from svg file.
		svg_ids = []
		svg_ids.extend([f'element-{elem_map[e]}' for e in elem_map])
		svg_ids.extend([f'action-{elem_map[e]}' for e in elem_map])
		svg_ids.extend([f'{n}-border' for n in border_types])
		svg_ids.append('monster-name')
		svg_ids.append(f'clip-image')
		svg_ids.append(f'image-{image}')
		#svg_ids.extend([f'{sym}-clone' for sym in symbols] )
		svg_ids.extend([f'hex-{n}' for n in attack_hexes] )
		svg_ids.extend([f'action-attack{n}' for n in [1,2,3]] )
		svg_ids.extend([f'attack-base{n}' for n in [1,2,3]] )
		svg_ids.append(f'action-plus')
		svg.load_ids(CARD_TEMPLATE, svg_ids)

		# Add Element and category masters (hidden, used for cloning).
		g_masters = SVG.group('masters')
		g_masters.set_style("display:none")
		SVG.add_node(svg_group, g_masters)
		for (e,elem) in elem_map.items():
			svg.add_loaded_element(g_masters, f"element-{elem}")
		#for sym in symbols:
		#	svg.add_loaded_element(g_masters, f"{sym}-clone")

		# Draw spell title.
		title = svg.add_loaded_element(svg_group, 'monster-name')
		SVG.set_text(title, name)

		img = svg.add_loaded_element(svg_group, f"image-{image}")
		clip = svg.get_loaded_path(f"clip-image")
		clipid = svg.add_clip_path(id, clip)
		img.set("clip-path", f"url(#{clipid})")
		
		#g_weak = SVG.group('weakness')
		#SVG.add_node(svg_group, g_weak)
		#self.draw_weaknesses(attrs['weakness'], g_weak)

		g_attack_hex = SVG.group('attack-hex')
		SVG.add_node(svg_group, g_attack_hex)
		self.draw_attack_pattern(svg, g_attack_hex)

		g_pattern_t = SVG.group('pattern_translate')
		SVG.add_node(svg_group, g_pattern_t)
		#g_pattern_t.set_translate_transform(52,76)
		g_pattern_t.set_translate_transform(47,78.7)
		#g_pattern_r = SVG.group('pattern_rotate')
		#SVG.add_node(g_pattern_t, g_pattern_r)
		#g_pattern_r.set_rotate_transform(90)
		self.draw_pattern(title, pattern, element, g_pattern_t)

		g_actions = SVG.group('actions')
		SVG.add_node(svg_group, g_actions)
		self.draw_actions(attack, actions, svg, g_actions)

		g_borders = SVG.group('borders')
		SVG.add_node(svg_group, g_borders)
		for t in border_types:
			svg.add_loaded_element(g_borders, f'{t}-border')

	def draw_attack_pattern(self, svg, svg_group):
		for hex in attack_hexes:
			svg.add_loaded_element(svg_group, f"hex-{hex}")

	def draw_weaknesses(self, weaknesses, svg_group):
		x0 = 3
		y0 = 1.25
		self.draw_weakness_group(x0, y0, weaknesses[0], svg_group)
		y0 += 21.25
		self.draw_weakness_group(x0, y0, weaknesses[1], svg_group)
		   
	def draw_weakness_group(self, x0, y0, weaknesses, svg_group):
		nSym = 0
		for w in weaknesses:
			sym_master = f'#{w}-clone'
			x = nSym % 3
			y = int(nSym / 3)
			sym_clone = SVG.clone(0, sym_master, x0 + x*10, y0 + y*10)
			nSym += 1
			SVG.add_node(svg_group, sym_clone)

	def draw_actions(self, attack, actions, svg, svg_group):
		if attack:
			svg.add_loaded_element(svg_group, base_attack_map[attack])
		svg.add_loaded_element(svg_group, f"action-plus")
		for (e,elem) in elem_map.items():
			svg.add_loaded_element(svg_group, f"action-{elem}")
		for x in range(0, 4):
			g_action = SVG.group(f'action{x}')
			SVG.add_node(svg_group, g_action)
			g_action.set_translate_transform(x*10.8,0)
			if actions[x]:
				action = svg.add_loaded_element(g_action, attack_map[actions[x]])
		
	def draw_pattern(self, monster_name, pattern_raw, element, svg_group):		
		pattern = [x.split() for x in pattern_raw]
		pheight = len(pattern)
		if pheight == 0:
			raise Exception(f"Missing pattern for {monster_name}")
		if pheight > 6:
			raise Exception(f"Pattern too tall for {monster_name}")
		pwidth = len(pattern[0])

		# Size and spacing for each box in pattern.
		box_size = 5.5
		box_spacing = 7

		# Max pattern width that fits on the card.
		max_width = 7
		# Center of pattern area.
		pcenter_x = 0 #(self.width / 2) + 2.8
		# Upper left corner of pattern area
		px0 = pcenter_x - (((max_width-1) * box_spacing) + box_size) / 2
		# Adjust offsets to center the patterns horizontally.
		if pwidth % 2 == 0:
			px0 += box_spacing / 2
			max_width = 6

		# Tall spells need to use larger pattern area.
		max_height = pheight
		pcenter_y = 0
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
						elemaster = f'#element-{element}'
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
						raise Exception(f"Unrecognized pattern symbol: {cell}")

def export_all_png():
	print(f"Exporting all.png")
	actions = InkscapeActions()
	actions.exportFilename(os.path.join(MONSTER_DIR, f'all.png'))
	actions.exportDpi(300)
	actions.exportAreaPage()
	actions.exportDo()
	Inkscape.run_actions(os.path.join(MONSTER_DIR, f'all.svg'), actions)

def export_5up_pdf(name):
	print(f"Exporting {name}")
	actions = InkscapeActions()
	actions.exportFilename(os.path.join(PDF_5UP_DIR, f'{name}.pdf'))
	actions.exportDpi(300)
	actions.exportAreaPage()
	actions.exportDo()
	Inkscape.run_actions(os.path.join(PDF_5UP_DIR, f'{name}.svg'), actions)

def export_5up_pdfs():
	num_pdfs = 5
	for x in range(1, (num_pdfs+1)):
		export_5up_pdf(f"5up-page{x}")

	# gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=temp.pdf ../spell-academy-cards/8up/8up*.pdf
	cmd = ['gs']
	if platform.system() == 'Darwin': # MacOS
		cmd = ['/opt/homebrew/bin/gs']
	cmd.append("-dBATCH")
	cmd.append("-dNOPAUSE")
	cmd.append("-q")
	cmd.append("-sDEVICE=pdfwrite")
	cmd.append(f"-sOutputFile={OUTPUT_DIR}/combined.pdf")

	for x in range(1, (num_pdfs+1)):
		cmd.append(f"{PDF_5UP_DIR}/5up-page{x}.pdf")
	#subprocess.run(cmd, stdout = subprocess.DEVNULL)
	subprocess.run(cmd)

def usage(options):
	print("Usage: %s <options>" % sys.argv[0])
	print("where <options> are:")
	for opt,info in options.items():
		if info['type'] == 'bool':
			print(f" --{opt} {info['desc']}")
		else:
			print(f" --{opt} <arg> {info['desc']}")
	sys.exit(2)

def parse_options():
	option_defs = {}
	option_defs.update(SVGCardGen.OPTIONS)
	option_defs.update({
		'summary': {'type': 'bool', 'default': False, 'desc': "Generate spell summary"},
		'all': {'type': 'bool', 'default': False, 'desc': "Generate combined output files"},
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
				option_flags.append(f"-{opt_info['short']}")
			option_flags.append(f"--{opt_name}")

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
	mgen = WovenMonsterCards(options)
	mgen.generate_cards()

	if options['all']:
		export_all_png()
		export_5up_pdfs()

if __name__ == '__main__':
	main()
