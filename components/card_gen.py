#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import getopt
import os
import shutil
import subprocess
import sys

def error(msg):
	print '\nERROR: %s\n' % msg
	sys.exit(0)

# Convert points (=1/72 inch) into 90dpi pixels
def pt2px(p):
	return (p * 90.0) / 72.0

# Convert 90dpi pixels into points (=1/72 inch)
def px2pt(px):
	return (px * 72.0) / 90.0

# Convert inches to 90dpi pixels
def in2px(i):
	return i * 90.0

CardGen_ShortFlags = 'v'
CardGen_LongFlags = ['a4', 'clean', 'combine', 'no-border', 'pdf', 'per-page=', 'png', 'verbose']
CardGen_DefaultOptions = {
	'a4': False,
	'clean': False,
	'combine': False,
	'pdf': False,
	'png': False,
	'per-page': 9,
	'no-border': False,
	'verbose': False,
}

def CardGen_ProcessOption(options, opt, arg):
	if opt in ('--a4'):
		options['a4'] = True
	if opt in ('--clean'):
		options['clean'] = True
	if opt in ('--combine'):
		options['combine'] = True
	if opt in ('--pdf'):
		options['pdf'] = True
	if opt in ('--png'):
		options['png'] = True
	if opt in ('--per-page'):
		options['per-page'] = int(arg)
	if opt in ('--no-border'):
		options['no-border'] = True
	if opt in ('-v', '--verbose'):
		options['verbose'] = True

def CardGen_OptionDesc():
	print "  --a4        A4 output (default = letter)"
	print "  --clean     Remove old files"
	print "  --combine   Combine into single PDF file"
	print "  --pdf       Generate PDF output files"
	print "  --png       Generate PNG output files"
	print "  --per-page  Num cards per page: 8 or 9 (default)"
	print "  --no-border Don't draw border around cards"
	print "  --verbose   Verbose output"

class CardGen(object):
	def __init__(self, options):
		self.gen_pdf = options['pdf']
		self.combine_pdf = options['combine']
		self.gen_png = options['png']
		self.cards_per_page = options['per-page']
		self.no_border = options['no-border']
		self.verbose = options['verbose']

		self.out_dir = options['out-dir']
		self.svg_out_dir = os.path.join(self.out_dir, 'svg')
		self.pdf_out_dir = os.path.join(self.out_dir, 'pdf')
		self.png_out_dir = os.path.join(self.out_dir, 'png')
		
		self.curr_filename = ''
		self.pdf_files = []
		
		self.curr_file = 0
		self.curr_card = 0
		self.out = 0
		self.indent_count = 0
				
		# Poker size cards: 2.5" x 3.5" = 225px x 315px
		# Bridge size cards: 2.25" x 3.5" = 202.5px x 315px
		self.card_width = in2px(2.5)
		self.card_height = in2px(3.5)
		self.card_size = 'poker' # 'bridge'

		# Paper size: Letter = 8.5" x 11" = 765px x 990px = 612pt x 792pt
		self.paper_type = 'letter'
		self.paper_width = in2px(8.5)
		self.paper_height = in2px(11)
		
		if options['a4']:
			# Paper size: A4 = 210mm x 297mm = 744.09449px x 1052.36220px
			self.paper_type = 'a4'
			self.paper_width = 744.09449
			self.paper_height = 1052.36220

		self.card_spacing_col = 0
		self.card_spacing_row = 0
		
		if self.cards_per_page == 18:
			# 12x18 printplaygames 18-up Poker page.
			# https://www.printplaygames.com/prototypes/formatting-guidelines/card-formatting-templates/
			self.paper_type = '12x18'
			self.paper_width = in2px(12)
			self.paper_height = in2px(18)

			# row-spacing = 22.5
			# col-spacing: ;719.99377 - 382.41348 - 44.83316
			self.card_spacing_col = 22.5803
			self.card_spacing_row = 22.5
			
			if self.card_size != 'poker':
				error('18-up must be poker')
		
		if self.cards_per_page == 21:
			# 12x18 printplaygames 21-up Bridge page.
			# https://www.printplaygames.com/prototypes/formatting-guidelines/card-formatting-templates/
			self.paper_type = '12x18'
			self.paper_width = in2px(12)
			self.paper_height = in2px(18)

			# row-spacing = 22.5
			# col-spacing: ;719.99377 - 382.41348 - 44.83316
			self.card_spacing_col = 22.5803
			self.card_spacing_row = 22.5
		
			if self.card_size != 'bridge':
				error('21-up must be bridge')

		# Subclass should override
		self.card_patterns = {}
		self.card_data = []
		
		if options['clean']:
			if os.path.isdir(self.svg_out_dir):
				shutil.rmtree(self.svg_out_dir)
			if self.gen_pdf:
				if os.path.isdir(self.pdf_out_dir):
					shutil.rmtree(self.pdf_out_dir)
			if self.gen_png:
				if os.path.isdir(self.png_out_dir):
					shutil.rmtree(self.png_out_dir)
		
	def write(self, str):
		self.out.write('  ' * self.indent_count)
		self.out.write(str)
	
	def write_raw(self, str):
		self.out.write(str)
	
	def indent(self, count=1):
		self.indent_count += count
	
	def outdent(self, count=1):
		self.indent_count -= count
		
	def __create_svg_file(self, name):
		if not os.path.isdir(self.svg_out_dir):
			os.makedirs(self.svg_out_dir);
		self.out = open(os.path.join(self.svg_out_dir, '%s.svg' % name), "w")
		self.write_svg_header()
		self.write_svg_header_extra()
		self.write_svg_header_layer()

	def __close_svg_file(self, name):
		self.write_svg_footer()
		self.out.close()

		if self.gen_pdf:
			# Generate PDF file.
			if not os.path.isdir(self.pdf_out_dir):
				os.makedirs(self.pdf_out_dir);
			self.pdf_files.append(os.path.abspath(os.path.join(self.pdf_out_dir, '%s.pdf' % name)))
			subprocess.call([
				"/Applications/Inkscape.app/Contents/Resources/bin/inkscape",
				"--file=%s" % os.path.abspath(os.path.join(self.svg_out_dir, '%s.svg' % name)),
				"--export-pdf=%s" % os.path.abspath(os.path.join(self.pdf_out_dir, '%s.pdf' % name)),
				"--export-dpi=300",
				"--export-text-to-path",
				"--without-gui"
				])

		if self.gen_png:
			# Generate PNG file.
			if not os.path.isdir(self.png_out_dir):
				os.makedirs(self.png_out_dir);
			subprocess.call([
				"/Applications/Inkscape.app/Contents/Resources/bin/inkscape",
				"--file=%s" % os.path.abspath(os.path.join(self.svg_out_dir, '%s.svg' % name)),
				"--export-png=%s" % os.path.abspath(os.path.join(self.png_out_dir, '%s.png' % name)),
				"--export-dpi=300",
				"--export-text-to-path",
				"--export-area-page",
				"--without-gui"
				])

	def write_svg_header(self):
		self.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')

		self.write('<svg version="1.1"\n')
		self.indent()
		namespaces = [
			'xmlns:dc="http://purl.org/dc/elements/1.1/"',
			'xmlns:cc="http://creativecommons.org/ns#"',
			'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"',
			#'xmlns:svg="http://www.w3.org/2000/svg"',
			'xmlns="http://www.w3.org/2000/svg"',
			'xmlns:xlink="http://www.w3.org/1999/xlink"',
			'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"',
			'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"',
			]
		for ns in namespaces:
			self.write('%s\n' % ns)
		if self.paper_type == 'a4':
			self.write('height="297mm" width="210mm"\n')
		else:
			self.write('height="%d" width="%d"\n' % (self.paper_height, self.paper_width))
		#self.write('viewBox="0 0 %d %d"\n' % (self.paper_height, self.paper_width))
		self.write('>\n')
		self.outdent()
		self.write('<metadata>\n')
		self.write('<rdf:RDF>\n')
		self.indent()
		self.write('<cc:Work rdf:about="">\n')
		self.write('<dc:format>image/svg+xml</dc:format>\n')
		self.write('<dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage"/>\n')
		self.write('<dc:title/>\n')
		self.write('</cc:Work>\n')
		self.outdent()
		self.write('</rdf:RDF>\n')
		self.write('</metadata>\n')
		self.write('\n')

	def write_svg_header_extra(self):
		# Subclass override
		return

	def write_svg_header_layer(self):
		self.write('<g id="layer1" inkscape:label="Layer 1" inkscape:groupmode="layer">\n')
		self.write('\n')

	def write_svg_footer(self):
		self.write('\n')
		self.write('</g>\n')
		self.write('</svg>\n')

	def start_card_page_transform(self, id):
		# Transform to move the card to the correct position on the page.
		if self.cards_per_page == 9:
			#  +---+---+---+
			#  | 0 | 1 | 2 |
			#  |   |   |   |
			#  +---+---+---+
			#  | 3 | 4 | 5 |
			#  |   |   |   |
			#  +---+---+---+
			#  | 6 | 7 | 8 |
			#  |   |   |   |
			#  *---+---+---+
			rows = 3
			cols = 3
			rotate = False
		elif self.cards_per_page == 8:
			# +----+----+
			# | 3  | 7  |
			# +----+----+
			# | 2  | 6  |
			# +----+----+
			# | 1  | 5  |
			# +----+----+
			# | 0  | 4  |
			# *----+----+
			rows = 2
			cols = 4
			rotate = True
		elif self.cards_per_page == 18:
			# +----+----+----+
			# | 5  | 11 | 17 |
			# +----+----+----+
			# | .  | .  | .  |
			#   .    .    .
			# | .  | .  | .  |
			# +----+----+----+
			# | 0  | 6  | 12 |
			# *----+----+----+
			rows = 3
			cols = 6
			rotate = True
		elif self.cards_per_page == 21:
			# +----+----+----+
			# | 6  | 13 | 20 |
			# +----+----+----+
			# | .  | .  | .  |
			#   .    .    .
			# | .  | .  | .  |
			# +----+----+----+
			# | 0  | 7  | 14 |
			# *----+----+----+
			rows = 3
			cols = 7
			rotate = True
		else:
			error("Invalid number of cards per page: %d" % self.cards_per_page)

		card_x_px = self.card_width
		card_y_px = self.card_height
		card_x = (id % cols)
		card_y = (int(id / cols) - rows)
		dir_x = 1
		dir_y = 1
		if rotate:
			card_x_px = self.card_height
			card_y_px = self.card_width
			card_x = int(id / cols)
			card_y = (id % cols)
			dir_x = 1
			dir_y = -1

		# Bottom-left point of bottom left card on printed page.
		origin0_x = (self.paper_width - (rows * card_x_px) - ((rows-1) * self.card_spacing_row)) / 2
		origin0_y = self.paper_height - ((self.paper_height - (cols * card_y_px) - ((cols-1) * self.card_spacing_col)) / 2)

		# Set origin to top-left of current card.
		origin_x = origin0_x + dir_x * ((card_x * card_x_px) + ((card_x) * self.card_spacing_row))
		origin_y = origin0_y + dir_y * ((card_y * card_y_px) + ((card_y) * self.card_spacing_col))

		if rotate:
			self.write('<g id="card%d" transform="matrix(0,-1,1,0,%f,%f)">\n' % (id, origin_x, origin_y))
		else:
			self.write('<g id="card%d" transform="translate(%f,%f)">\n' % (id, origin_x, origin_y))

		self.indent()

	def end_card_page_transform(self):
		self.outdent()
		self.write('</g>\n')

	# Utilities

	def draw_border(self):
		style = 'fill:#ffffff;fill-opacity:1;stroke:#c0c0c0;stroke-width:0.88582677;stroke-opacity:1'
		self.write('<rect id="c%d-border" x="%.03f" y="%.03f" width="%.03f" height="%.03f" rx="11.25" ry="11.25" style="%s"/>\n' % (self.curr_card, 0, 0, self.card_width, self.card_height, style))

	def start_layer(self, id, label, hidden=False, locked=True):
		tag = '<g inkscape:groupmode="layer" id="%s" inkscape:label="%s" ' % (id, label)
		if hidden:
			tag += 'style="display:none" '
		else:
			tag += 'style="display:inline" '
		if locked:
			tag += 'sodipodi:insensitive="true" '
		tag += '>\n'
		self.write(tag)
		self.indent()
		
	def end_layer(self):
		self.outdent()
		self.write('</g>\n')
	
	def start_group(self, id='', style='', transform=''):
		tag = '<g '
		if id != '':
			tag += 'id="%s" ' % id
		if style != '':
			tag += 'style="%s" ' % style
		if transform != '':
			tag += 'transform="%s" ' % transform
		tag += '>\n'
		self.write(tag)
		self.indent()

	def end_group(self):
		self.outdent()
		self.write('</g>\n')
		
	def draw_path(self, style, path, id='', transform=''):
		tag = '<path style="%s" ' % style
		if id != '':
			tag += 'id="%s" ' % id
		if transform != '':
			tag += 'transform="%s" ' % transform
		tag += 'd="%s" ' % path
		tag += '/>\n'
		self.write(tag)
	
	def draw_clone(self, link, id='', x=0, y=0, transform='', style=''):
		tag = '<use xlink:href="#%s" height="100%%" width="100%%" x="%f" y="%f" ' % (link, x, y)
		if id != '':
			tag += 'id="%s" ' % id
		if transform != '':
			tag += 'transform="%s" ' % transform
		if style != '':
			tag += 'style="%s" ' % style
		tag += '/>\n'
		self.write(tag)

	def draw_rect(self, style, x, y, width, height, id='', r=0, transform=''):
		tag = '<rect x="%f" y="%f" width="%f" height="%f" style="%s" ' % (x, y, width, height, style)
		if r != 0:
			tag += 'ry="%f" ' % r
		if id != '':
			tag += 'id="%s" ' % id
		if transform != '':
			tag += 'transform="%s" ' % transform
		tag += '/>\n'
		self.write(tag)
	
	def draw_circle(self, style, cx, cy, r, id='', transform=''):
		tag = '<circle cx="%f" cy="%f" r="%f" style="%s" ' % (cx, cy, r, style)
		if id != '':
			tag += 'id="%s" ' % id
		if transform != '':
			tag += 'transform="%s" ' % transform
		tag += '/>\n'
		self.write(tag)
	
	def draw_ellipse(self, style, cx, cy, rx, ry, id='', transform=''):
		tag = '<ellipse cx="%f" cy="%f" rx="%f" ry="%f" style="%s" ' % (cx, cy, rx, ry, style)
		if id != '':
			tag += 'id="%s" ' % id
		if transform != '':
			tag += 'transform="%s" ' % transform
		tag += '/>\n'
		self.write(tag)

	def draw_text(self, id, x, y, text, size=18, align='center', style='normal', weight='normal', font='Sans'):
		if align == 'left':
			align = 'start'
			anchor = 'start'
		elif align == 'center':
			anchor = 'middle';
		elif align == 'right':
			align = 'end'
			anchor = 'end'
		if weight == 'bold':
			weight = '900'
			
		if id =='':
			self.write('<text xml:space="preserve"\n')
		else:
			self.write('<text id="%s" xml:space="preserve"\n' % id)
		self.indent()
		self.write('style="font-size:12px;font-style:normal;font-weight:normal;text-align:%s;line-height:125%%;letter-spacing:0px;word-spacing:0px;text-anchor:%s;fill:#000000;fill-opacity:1;stroke:none;font-family:%s"\n' % (align, anchor, font))
		self.write('x="%.3f" y="%.3f"\n' % (x, y))
		self.write('><tspan x="%.03f" y="%.03f"\n' % (x, y))
		self.write('style="font-size:%dpx;font-style:%s;font-variant:normal;font-weight:%s;font-stretch:normal;fill:#000000;fill-opacity:1;font-family:%s"\n' % (size, style, weight, font))
		self.write('>%s</tspan></text>\n' % text)
		self.outdent()
	
	def draw_flow_text(self, rect, text, size=12.5):
		#style = 'fill:#ffffff;fill-opacity:1;stroke:#c0c0c0;stroke-width:0.88582677;stroke-opacity:1'
		#self.write('<rect x="%.03f" y="%.03f" width="%.03f" height="%.03f" style="%s"/>\n' % (rect['x'], rect['y'], rect['width'], rect['height'], style))

		self.indent()
		self.write('<flowRoot xml:space="preserve" id="flowRoot4268"')
		self.write_raw(' style="font-style:normal;font-weight:normal;font-size:%gpx;line-height:125%%;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1">' % size)
		self.write_raw('<flowRegion id="flowRegion4270">')
		self.write_raw('<rect x="%.3g" y="%.3g" width="%.3g" height="%.3g" />' % (rect['x'], rect['y'], rect['width'], rect['height']))
		self.write_raw('</flowRegion>')
		for para in text:
			if para == "-":
				self.write_raw('<flowPara style="font-size:5px"> </flowPara>')
			else:
				self.write_raw('<flowPara>%s</flowPara>' % para)
		self.write_raw('</flowRoot>')
		self.write_raw('\n')
		self.outdent()
		
	def __start_card_gen(self):
		self.curr_file = -1
		self.curr_card = -1
		self.curr_filename = ''
	
	def __end_card_gen(self):
		if self.curr_filename != '':
			if self.verbose:
				print 'Closing', self.curr_filename
			self.__close_svg_file(self.curr_filename)
		
		if self.gen_pdf and self.combine_pdf:
			if self.verbose:
				print 'Combining PDF files...'
			cmd = ["/System/Library/Automator/Combine PDF Pages.action/Contents/Resources/join.py",
				"-o", os.path.join(self.out_dir, 'cards.pdf')] + self.pdf_files
			subprocess.call(cmd)
	
	def generate_cards(self):
		self.__start_card_gen()

		for card_data in self.card_data:
			self.process_card_data(card_data)
			
		while self.curr_filename != '':
			self.process_blank_card()

		self.__end_card_gen()

	def process_card_data(self, card_data):
		# Subclass override.
		# Must call pre_card() and post_card() for each card.
		return

	def process_blank_card(self):
		# Subclass override.
		# Must call pre_card() and post_card() for each card.
		return

	def pre_card(self):
		if self.curr_filename == '':
			self.curr_file += 1
			self.curr_filename = 'out%02d' % self.curr_file
			if self.verbose:
				print 'Opening', self.curr_filename
			self.__create_svg_file(self.curr_filename)
		self.curr_card += 1
	
	def post_card(self):
		if self.curr_card == (self.cards_per_page - 1):
			if self.verbose:
				print 'Closing', self.curr_filename
			self.__close_svg_file(self.curr_filename)
			self.curr_filename = ''
			self.curr_card = -1
