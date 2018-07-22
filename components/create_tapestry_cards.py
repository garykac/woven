#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os.path
import re
import subprocess
import sys

from data_tapestry_cards import tapestry_card_data

def error(msg):
	print 'Error: %s' % (msg)
	sys.exit(1)

class Parser():
	"""Build Tapestry Card for BlockChain"""

	def __init__(self, template, basename, pattern, elements, gen_png):
		self.svg_template = template
		self.basename = basename
		self.pattern = pattern
		self.elements = elements

		self.cards_dir = 'tapestry-cards'
		self.svg_out_dir = 'svg_out'
		self.png_out_dir = 'png_out'

		self.gen_png = gen_png
		
		# True if we've found the layer to skip over (and insert a new one).
		self.skipping_layer = False

	def write_box(self, x, y):
		info = [
			[['g4443', 'use4461'], ['g4446', 'use4471']],
			[['g4452', 'use4467'], ['g4449', 'use4463']],
			[['g4455', 'use4469'], ['g4458', 'use4465']],
		]
		ref = info[y][x][0]
		name = info[y][x][1]
		self.outfile.write('<use style="display:inline" x="0" y="0" ')
		self.outfile.write('xlink:href="#%s" ' % ref)
		self.outfile.write('id="%s" ' % name)
		self.outfile.write('transform="translate(240,0)" width="100%" height="100%" />\n')

	def write_element(self, element, x, y):
		info = {
			'a': {
				'ref': 'g4377',  # Ref to master object this is cloned from.
				'name': 'use4389',
				# Offsets from master object to this clone's position.
				'offsets': [
					[[120.52679,-225.32061], [219.52998,-225.32053]],
					[[120.52679,-126.31744], [219.52998,-126.31744]],
					[[120.52679,-27.314263], [219.52998,-27.314263]],
				],
			},
			'f': {
				'ref': 'g4380',
				'name': 'use4387',
				'offsets': [
					[[191.07479,-225.32061], [290.07798,-225.32054]],
					[[191.07479,-126.31744], [291.06946,-126.31744]],
					[[191.07479,-27.314264], [290.07798,-27.314264]],
				],
			},
			'e': {
				'ref': 'g4397',
				'name': 'use4435',
				'offsets': [
					[[263.60575,-225.3206], [362.60894,-225.32053]],
					[[263.60575,-126.31743], [362.60894,-126.31743]],
					[[263.60575,-27.314256], [362.60894,-27.314256]],
				],
			},
			'w': {
				'ref': 'g4391',
				'name': 'use4433',
				'offsets': [
					[[335.14524,-225.32061], [434.14843,-225.32053]],
					[[335.14524,-126.31744], [434.14843,-126.31744]],
					[[335.14524,-27.314263], [434.14843,-27.314263]],
				],
			},
		}
		self.outfile.write('<use style="display:inline" x="0" y="0" ')
		self.outfile.write('xlink:href="#%s" ' % info[element]['ref'])
		self.outfile.write('id="%s" ' % info[element]['name'])
		offsets = info[element]['offsets'][y][x]
		self.outfile.write('transform="matrix(0,1,-1,0,%f,%f)" ' % (offsets[0], offsets[1]))
		self.outfile.write('width="100%" height="100%" />\n')

	def insert_layer(self):
		# Layer has already been opened, we're just adding content.
		# Opened with : <g inkscape:groupmode="layer" id="layer5"
		self.outfile.write('inkscape:label="Inserted Card" style="display:inline">\n')

		for x in [0,1]:
			for y in [0,1,2]:
				if self.pattern[y][x] == 'X':
					self.write_box(x, y)
				else:
					element_index = int(self.pattern[y][x]) - 1
					self.write_element(self.elements[element_index], x, y)

		# Close out layer and open a new one so that the next layer merges cleanly.
		self.outfile.write('</g><g inkscape:groupmode="layer" id="layer6"\n')
		
	# Process an entire line from the file.
	def process_line(self, line):
		# SVG is written back to front, so END (lower) comes before START (higher layer).
		m = re.match(r'^.*inkscape:label="CARD INSERT END".*/><g.*$', line)
		if m:
			self.skipping_layer = True
			self.insert_layer()

		m = re.match(r'^.*inkscape:label="CARD INSERT BEGIN".*/><g.*$', line)
		if m:
			self.skipping_layer = False

		if not self.skipping_layer:
			self.outfile.write(line)

	def process(self):

		template_path = os.path.join(self.cards_dir, self.svg_template)
		if not os.path.isfile(template_path):
			error('File "%s" doesn\'t exist' % template_path)

		try:
			self.infile = open(template_path, 'r')
		except IOError as e:
			error('Unable to open "%s" for reading: %s' % (template_path, e))

		svg_out_path = os.path.join(self.cards_dir, self.svg_out_dir)
		if not os.path.isdir(svg_out_path):
			os.makedirs(svg_out_path)
		svg_relpath = os.path.join(svg_out_path, '%s.svg' % self.basename)

		try:
			self.outfile = open(svg_relpath, 'w')
		except IOError as e:
			error('Unable to open "%s" for writing: %s' % (svg_relpath, e))

		for line in self.infile:
			self.process_line(line)

		self.infile.close()

		self.outfile.flush()
		os.fsync(self.outfile.fileno())
		self.outfile.close()
	
		if self.gen_png:
			(svg_path, svg_name) = os.path.split(svg_relpath)
			(base_path, svg_dir) = os.path.split(svg_path)
			(base_name, ext) = os.path.splitext(svg_name)
			png_name = base_name + '.png'
			png_dir = os.path.join(base_path, self.png_out_dir)
			if not os.path.isdir(png_dir):
				os.makedirs(png_dir)
			png_path = os.path.join(png_dir, png_name)

			subprocess.call([
				"/Applications/Inkscape.app/Contents/Resources/bin/inkscape",
				"--file=%s" % os.path.abspath(svg_relpath),
				"--export-png=%s" % os.path.abspath(png_path),
				"--export-dpi=300",
				"--export-text-to-path",
				"--export-area-page",
				"--without-gui"
				])

def process_card(basename, pattern, elements, gen_png):
	parser = Parser('template-mpc.svg', basename, pattern, elements, gen_png)
	parser.process()

def usage():
	print "Usage: %s <options>" % sys.argv[0]
	print "where <options> are:"
	print "  --png   Generate PNG output files"
	sys.exit(2)

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:],
			'p',
			['png'])
	except getopt.GetoptError:
		usage()

	gen_png = False
	for opt,arg in opts:
		if opt in ('-p', '--png'):
			gen_png = True

	id = 1
	for card in tapestry_card_data:
		print card['name']
		p = card['pattern']
		# Patterns are interleaved to make the raw data easier to read.
		# Patterns are also rotated relative to the SVG output:
		# Coords:       Front                Back
		#         (1,0) (1,1) (1,2)    (2,0) (1,0) (0,0)
		#         (0,0) (0,1) (0,2)    (2,1) (1,1) (0,1)
		front_pattern = [[p[2][0], p[0][0]], [p[2][2], p[0][2]], [p[2][4], p[0][4]]]
		back_pattern = [[p[1][4], p[3][4]], [p[1][2], p[3][2]], [p[1][0], p[3][0]]]
		for elements in card['elements']:
			name = '%02d-%s-%s' % (id, card['name'], elements)
			print 'Processing card', id, 'front:', front_pattern, elements
			process_card('t%s-front' % name, front_pattern, elements, gen_png)
			print 'Processing card', id, 'back:', back_pattern, elements
			process_card('t%s-back' % name, back_pattern, elements, gen_png)
			id += 1

if __name__ == '__main__':
	main()
