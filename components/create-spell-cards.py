#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os
import subprocess
import sys

from spell_card_data import spell_card_data

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

class CardGen(object):
	def __init__(self, options):
		self.gen_pdf = options['pdf']
		self.combine_pdf = options['combine']
		self.cards_per_page = options['per-page']

		self.out_dir = 'spell-cards'
		self.svg_out_dir = os.path.join(self.out_dir, 'svg')
		self.pdf_out_dir = os.path.join(self.out_dir, 'pdf')
		
		self.pdf_files = []
		
		self.curr_file = 0
		self.curr_card = 0
		self.out = 0
		self.indent_count = 0
		
		self.name2id = {}
		self.pattern_elements = {}
		self.elements = {}
		self.categories = {}
		self.id2name = {}
		self.max_id = 0
		
		# Poker size cards: 2.5" x 3.5"
		# Bridge size cards: 2.25" x 3.5" = 202.5px x 315px
		self.card_width = in2px(2.25)
		self.card_height = in2px(3.5)

		# Paper size: Letter = 8.5" x 11" = 765px x 990px = 612pt x 792pt
		self.paper_type = 'letter'
		self.paper_width = in2px(8.5)
		self.paper_height = in2px(11)
		
		if options['a4']:
			# Paper size: A4 = 210mm x 297mm = 744.09449px x 1052.36220px
			self.paper_type = 'a4'
			self.paper_width = 744.09449
			self.paper_height = 1052.36220

		self.valid_elements = ['none', 'air', 'fire', 'earth', 'water']
		self.valid_categories = ['astral', 'attack', 'defend', 'move', 'tendril', 'tapestry', 'terrain']

	def write(self, str):
		self.out.write('  ' * self.indent_count)
		self.out.write(str)
	
	def write_raw(self, str):
		self.out.write(str)
	
	def indent(self, count=1):
		self.indent_count += count
	
	def outdent(self, count=1):
		self.indent_count -= count
		
	def write_header(self):
		namespaces = [
			'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"',
			'xmlns="http://www.w3.org/2000/svg"',
			'xmlns:cc="http://creativecommons.org/ns#"',
			'xmlns:xlink="http://www.w3.org/1999/xlink"',
			'xmlns:dc="http://purl.org/dc/elements/1.1/"',
			'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"',
			'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"',
			]
		self.write('<svg version="1.1"')
		if self.paper_type == 'a4':
			self.write(' height="297mm" width="210mm"')
		else:
			self.write(' height="%dpt" width="%dpt"' % (px2pt(self.paper_height), px2pt(self.paper_width)))
		self.write(' %s>\n' % ' '.join(namespaces))
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

		self.write('<g inkscape:label="Icon Masters" inkscape:groupmode="layer" style="display:none">\n')

		self.write('<g id="element-water" transform="matrix(0.33568916,0,0,0.31348783,-44.537788,309.84728)" style="display:inline;filter:url(#filter9446)">\n')
		self.write('<path sodipodi:nodetypes="ccccccccccc" inkscape:connector-curvature="0" id="path8407" d="m 216.17966,66.561481 c -1.5117,0.245633 -3.1675,1.500335 -4.62784,1.955201 -4.49775,1.925116 -9.05232,1.674803 -13.80832,0.540821 -2.12278,-0.375275 -5.32978,-1.191672 -7.43587,-1.591486 -5.85396,-0.506675 -10.5059,2.585118 -14.99395,6.014542 -1.4384,1.355103 -0.024,2.901987 1.93712,2.65801 2.26464,-0.665698 5.0678,-1.014101 7.29982,-2.39671 2.81804,-1.398042 6.96422,-2.08651 10.03167,-0.830718 5.22123,1.560223 9.98052,2.194805 15.34157,0.806822 3.14588,-0.718653 5.14146,-2.094221 7.64699,-4.167305 1.25145,-1.416861 0.49345,-3.14775 -1.39119,-2.989177 z" style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#00007e;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />\n')
		self.write('<path sodipodi:nodetypes="cccccccccc" inkscape:connector-curvature="0" id="path8409" d="m 224.21149,79.164167 c -3.12271,-0.08421 -3.5103,1.883595 -7.88451,1.956941 -5.33478,0.444095 -8.88015,-0.974771 -14.18696,-1.280536 -7.01949,-0.677004 -14.71165,3.567569 -21.10815,5.409683 -1.68954,1.02507 0.1228,3.231431 2.0916,3.402099 1.75093,-0.0063 2.3243,0.412596 4.03219,0.07782 5.28968,-1.691086 8.684,-5.974404 14.1641,-5.291836 5.52858,0.544071 12.97732,3.078023 18.50994,1.869614 1.75091,-0.74805 3.3381,-1.841409 4.59247,-3.21858 0.89156,-1.443524 1.48689,-2.977774 -0.21068,-2.925207 z" style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#00007e;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />\n')
		self.write('<path sodipodi:nodetypes="cccccccccc" inkscape:connector-curvature="0" id="path8411" d="m 227.94003,90.184189 c -2.30667,0.25193 -5.55002,2.748345 -7.90913,2.884383 -4.39755,0.64283 -9.96594,-0.89292 -14.3607,-1.029109 -7.44154,-0.197688 -11.58941,3.367015 -18.49294,5.782161 -1.74596,0.925703 0.05,2.180286 2.0056,2.464466 1.59957,0.1379 4.15708,-0.89902 5.67568,-1.269645 4.12399,-1.468379 7.77185,-2.633032 12.1793,-2.023285 5.82477,1.088337 9.57118,1.627599 15.28231,0.658956 1.86369,-0.574648 3.65164,-2.550727 5.32809,-3.484689 1.51676,-1.318484 2.30214,-4.043109 0.29179,-3.983238 z" style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#00007e;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />\n')
		self.write('</g>\n')

		self.write('<g id="element-earth" style="display:inline;filter:url(#filter9446)" transform="matrix(0.33568916,0,0,0.31348783,-78.199398,278.79309)">\n')
		self.write('<path sodipodi:nodetypes="ccccc" inkscape:connector-curvature="0" id="path9283" d="m 301.64648,186.74023 c -1.76614,1.2025 -3.89969,5.27677 -5.24414,9.6875 -1.04233,2.81351 3.17744,4.37762 4.22071,1.56446 0.53628,-3.64672 2.38966,-8.29867 2.38966,-8.29867 0.55702,-1.43946 0.17605,-2.89237 -1.36623,-2.95329 z" style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#004c00;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />\n')
		self.write('<path sodipodi:nodetypes="ccccc" inkscape:connector-curvature="0" id="path9285" d="m 309.29842,188.25454 c -1.24188,0.0183 -2.23406,1.25387 -2.2168,2.49576 l -0.64354,11.39006 c -0.043,3.04273 4.32852,0.68309 4.28548,-2.35964 -0.29494,-2.45976 0.61166,-7.70971 -1.42514,-11.52618 z" style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#004c00;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />\n')
		self.write('<path sodipodi:nodetypes="cccscc" inkscape:connector-curvature="0" id="path9287" d="m 314.91657,186.89588 c -1.70622,0.0862 -1.73256,0.89494 -0.83938,2.35126 0,0 3.40403,6.16758 4.58385,10.02881 1.50948,2.66303 6.25738,2.19611 4.72719,-1.22432 -1.82336,-4.07574 -6.40721,-10.03075 -6.40721,-10.03075 -0.42196,-0.73326 -1.21953,-1.1679 -2.06445,-1.125 z" style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#004c00;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />\n')
		self.write('<path sodipodi:nodetypes="ccccccccc" inkscape:connector-curvature="0" id="path9237" d="m 288.19561,168.1501 c -0.7353,0.0173 -4.2044,3.28883 -4.61093,3.90178 -2.30582,3.47722 -3.83023,5.43548 -6.3757,9.2489 -1.66453,2.49592 1.43507,3.06269 3.1006,0.56744 1.9411,-2.908 6.43135,-8.02229 7.85383,-8.52656 0,0 4.67526,3.61461 6.2249,4.50133 2.60888,1.51447 5.6142,-0.0586 2.98907,-1.54466 0.35219,0.202 -2.26884,-1.88692 -3.32123,-3.25973 -1.48005,-1.84578 -4.05702,-4.20408 -5.86054,-4.8885 z" style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#004c00;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />\n')
		self.write('<path sodipodi:nodetypes="ccscccccscccccsccccc" inkscape:connector-curvature="0" id="path9239" d="m 309.00977,161.41602 c -0.50305,0.0252 -0.98309,0.21846 -1.36329,0.54882 -2.42687,2.10718 -4.33784,5.49414 -6.32862,8.70899 -1.98533,3.20605 -5.75777,8.47897 -6.28787,9.27599 -5.32818,5.98219 -7.41497,11.69385 -13.75049,18.4131 -1.96094,2.27083 2.08885,2.53082 4.04979,0.25999 6.29262,-7.29089 7.89517,-9.709 12.80292,-15.14496 0.0733,-0.0816 2.60744,-2.95705 3.63339,-4.44276 0.91183,-1.36599 1.14455,-2.9044 3.05667,-5.99222 1.30051,-2.10017 2.81587,-4.68505 4.01367,-5.31886 1.54953,1.70978 3.96352,4.03035 6.13378,8.89088 1.82198,2.59687 5.06443,6.47082 5.6005,7.2741 1.66466,2.55908 5.31742,7.21734 5.65912,7.8935 1.35263,2.67911 1.93897,-1.17403 1.01441,-4.38894 -0.71242,-1.40972 -1.23105,-3.38885 -2.90205,-5.95769 -1.671,-2.56883 -3.78371,-4.55609 -4.2171,-5.33305 l -1.73355,-2.93075 c -1.49462,-3.57419 -4.04795,-4.91858 -7.31691,-10.62724 -0.42092,-0.73477 -1.21871,-1.17102 -2.06445,-1.1289 z" style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#004c00;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" />\n')
		self.write('</g>\n')

		self.write('<path style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#860000;fill-opacity:0.9745098;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;filter:url(#filter9446);color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" d="m 349.83863,15.938294 c -0.64354,0.69716 0.0714,2.14763 0.0714,2.14763 0,0 0.55185,2.37214 0.75843,4.54618 0.20659,2.17404 -0.0378,3.98798 -0.17022,5.27121 -0.21324,2.06596 -1.95026,5.96682 -3.28642,8.1392 -1.33616,2.17237 -2.19347,4.3801 -2.30243,7.06973 -0.0223,0.55126 0.17044,1.61314 0.25358,2.13246 -1.50437,1.76498 -3.13649,2.63382 -4.67579,3.09375 -2.07253,0.61947 -5.30101,2.30797 -8.08852,5.06277 -2.22249,2.19641 -3.11159,4.23435 -3.85907,7.06451 -0.74749,2.83017 -1.21306,5.15441 -0.93594,7.23275 0,0 0.0289,2.43353 0.77968,3.1307 1.01893,0.21451 2.55503,-0.95753 2.55503,-0.95753 3.1676,-2.40708 6.08306,-4.67688 8.56877,-5.48761 2.70803,-0.88325 5.56997,-0.59913 7.42537,0.003 2.43757,0.79138 5.07675,0.43601 7.63086,-0.15625 1.75956,-0.40802 2.93739,-1.34497 4.23186,-2.5433 1.72356,1.41363 2.77621,1.68436 4.00821,2.68074 1.51302,1.22367 3.25735,2.36974 5.94352,3.11842 2.80535,0.78189 6.01463,0.84546 8.99219,0.42773 2.97755,-0.41773 5.70224,-1.19564 7.63867,-2.9707 0,0 1.66343,-1.23799 1.50254,-1.93515 -0.37564,-0.63882 -2.02436,-1.32074 -2.02436,-1.32074 0,0 -1.83025,-0.75564 -3.88996,-1.97265 -2.05971,-1.21704 -3.65008,-3.3477 -5.02999,-4.65331 -1.6333,-1.54536 -2.06831,-3.62018 -2.78284,-5.72362 -0.71077,-2.09239 -1.60086,-4.78144 -4.34961,-6.69727 -1.31692,-0.91786 -2.59747,-1.70064 -3.96875,-2.23828 -0.32734,-1.50008 -0.31121,-2.89988 -0.13507,-4.43879 0.53962,-2.8161 -0.28736,-6.5882 -1.27327,-9.29702 -1.04011,-2.85773 -3.1895,-4.33553 -4.58319,-5.89194 -1.48506,-1.65845 -3.56485,-3.46995 -5.66733,-4.31095 0,0 -1.29946,-0.5793 -3.33733,-0.52567 z m 4.47715,5.8549 c 0.49831,0.41112 2.0104,1.44244 2.76207,2.24067 1.75757,1.86644 3.23372,4.53046 3.54048,6.51195 0.29872,1.92953 -0.0507,3.63254 -0.25797,5.44286 -0.13334,1.16501 0.018,2.45375 0.46432,3.68571 -0.35581,0.0206 -1.24569,0.0523 -1.61292,0.10547 -1.22544,0.17753 -2.52004,0.53511 -3.91601,1.0586 -2.89087,1.01546 -0.65882,1.6327 2.26266,1.3309 2.28051,-0.12522 4.42276,1.08875 5.83067,1.76026 1.15057,0.54878 3.03142,1.93023 3.60063,2.93387 1.1089,1.95521 2.59211,4.33643 2.8076,5.40292 0.39023,1.93127 1.10468,3.78826 3.15006,6.35682 1.84431,2.31606 4.20223,3.10458 6.46617,4.44765 -0.20222,0.66695 -2.03074,1.21656 -2.6028,1.29682 -2.44038,0.34237 -5.07212,-0.23197 -6.85484,-1.21479 -1.94759,-1.07371 -3.25658,-1.07108 -4.89236,-2.17717 -1.07414,-0.72632 -2.53248,-1.23412 -3.28269,-2.75364 0.98947,-2.31732 2.06345,-4.4314 2.4563,-6.69028 0.62494,-3.03096 -2.32705,-0.0432 -3.59738,2.26218 -1.34951,3.05746 -3.53484,5.4073 -6.82388,6.57601 -2.1296,0.75672 -3.95716,0.0463 -5.93421,-0.38116 -1.97703,-0.42738 -4.74167,-0.90022 -8.32812,0.26953 -2.4664,0.80443 -5.70038,1.727 -8.04512,4.49157 -0.25626,-1.42864 0.43116,-2.88637 0.64648,-3.58163 0.70802,-2.2861 2.74177,-4.59831 4.09035,-5.93107 2.05301,-2.02892 4.61944,-2.63372 6.74442,-3.26887 1.57061,-0.46945 2.24348,-0.43339 3.87832,-1.88578 1.19767,2.07265 2.88979,3.78446 4.89649,5.16406 2.47255,1.69995 1.89499,-1.16784 -0.48289,-3.93651 -1.55071,-1.80557 -2.11148,-3.38258 -2.33316,-7.31418 -0.11303,-2.00463 0.81831,-4.20231 2.09537,-6.27861 1.65628,-2.4555 3.0526,-4.61973 3.40006,-7.986 0.20849,-2.6641 0.40821,-6.10123 -0.1281,-7.93816 z" id="element-fire" inkscape:connector-curvature="0" sodipodi:nodetypes="ccssssccsscccssscssscccssssccssccccsscsccsssscssscccscscssscccssccc" transform="matrix(0.33568916,0,0,0.31348783,-96.660538,322.39616)" />\n')

		self.write('<path style="color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#303030;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;filter:url(#filter9446);color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate" d="m 266.01465,20.022074 c -2.16402,-0.8284 -3.9519,-0.99856 -5.87013,-0.70145 -3.36627,0.52139 -8.04819,1.60863 -11.79423,3.41656 -4.04421,1.95184 -4.97919,3.43786 -8.29607,5.40439 -3.09009,1.83206 -6.21891,3.10498 -8.67834,5.89178 -1.22481,1.38784 -0.14531,2.45627 0.58855,2.20785 4.04323,-1.36867 5.96167,-3.07787 8.41835,-4.65429 2.26034,-1.45044 1.4983,0.1591 5.6097,-2.75252 3.60063,-2.54991 4.31189,-2.96395 6.19587,-3.35206 1.03959,-0.46928 2.11768,-0.9525 3.39564,-1.38115 2.99741,-0.81841 3.38181,-0.58783 7.11477,-0.27515 3.05917,0.25624 6.21552,1.46472 7.57776,2.84244 1.53658,1.55403 4.78665,1.8127 7.75363,8.15531 1.21998,2.60799 1.59561,5.29271 1.34571,7.95703 0.2661,2.05534 1.43491,2.82674 -0.012,9.04492 -1.07426,3.88605 -4.08337,7.53559 -7.94532,9.23828 -4.51384,1.99011 -9.72023,2.33631 -14.19921,1.19727 -4.31442,-1.0972 -8.99174,-5.00508 -9.89255,-9.17996 -0.87827,-4.07043 -1.564,-7.60679 -1.72857,-10.84153 0.35166,-3.99309 4.22352,-3.90769 7.63791,-6.6723 2.33727,-1.00332 3.9923,-2.663 7.20288,-2.663 2.74945,0.40006 5.69059,2.15451 6.7562,4.08005 2.28373,2.31721 3.32408,5.31496 2.61025,9.13339 0.10873,1.92351 -3.15649,5.13369 -5.04286,5.48368 -2.3545,0.43684 -5.31298,-1.52296 -6.77567,-2.25803 -1.39611,-0.4218 -1.30359,-1.00344 -0.72586,-3.17402 0.69608,-1.05513 2.00902,-1.71771 2.80422,-2.24703 0.9617,-0.64015 1.03664,-1.9396 0.76954,-2.98852 -0.58508,-0.87154 -1.16457,-1.48311 -2.57907,-1.0196 -0.96592,0.31652 -2.75435,0.51256 -3.16951,0.92221 -0.67499,0.65674 -2.52925,1.72885 -3.04126,2.48143 -0.48514,1.75438 0.50199,3.68043 0.68579,5.1875 0.23726,1.7865 1.20702,3.84658 3.24415,4.86328 3.07144,1.53291 6.88351,2.30295 9.25093,2.18613 2.89121,-0.3233 8.55766,-2.89879 8.61644,-9.00849 -0.15355,-2.8792 -1.67895,-8.6497 -3.74823,-12.44325 -2.10401,-3.85721 -5.08264,-5.50215 -9.30932,-5.47107 -2.15208,0.19742 -5.2721,0.46643 -9.80439,3.24208 -5.2349,2.09616 -6.0427,2.96843 -9.65488,7.17711 -2.35407,2.74279 -0.29937,7.74981 -0.29937,7.74981 1.66337,3.75798 0.85898,4.20056 2.50553,8.56764 2.1542,5.71353 6.96147,9.97412 12.49609,11.24024 4.47407,1.0235 15.01795,-0.8329 17.30471,-1.39255 6.49182,-1.58879 8.63642,-4.62508 10.53125,-12.54688 1.25967,-5.26636 0.30251,-9.82479 0.0778,-11.65157 -0.2849,-2.31648 -1.0879,-6.15195 -1.72646,-7.85819 -1.46974,-3.56177 -6.22726,-7.07122 -10.05997,-10.5856 -3.56795,-3.18868 -2.76595,-1.2604 -6.14044,-2.55217 z" id="element-air" inkscape:connector-curvature="0" sodipodi:nodetypes="csssssssccsssccssscccccsccscscccsccsccsssssssccsc" transform="matrix(0.33568916,0,0,0.31348783,-64.127898,322.50497)" />\n')

		self.write('</g>\n')

		self.write('<g id="layer1" inkscape:label="Layer 1" inkscape:groupmode="layer">\n')
		self.write('\n')

	def write_footer(self):
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
			# Bottom-left point of bottom left card on page.
			origin0_x = (self.paper_width - (3 * self.card_width)) / 2
			origin0_y = self.paper_height - ((self.paper_height - (3 * self.card_height)) / 2)
			# Set origin to top-left of current card.
			origin_x = origin0_x + (id % 3) * self.card_width
			origin_y = origin0_y + (int(id / 3) - 3) * self.card_height
			self.write('<g id="card%d" transform="translate(%f,%f)">\n' % (id, origin_x, origin_y))
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
			# Bottom-left point of bottom left card on page (ignoring rotation).
			origin0_x = (self.paper_width - (2 * self.card_height)) / 2
			origin0_y = self.paper_height - ((self.paper_height - (4 * self.card_width)) / 2)
			# Set origin to top-left of current card and add rotate transformation.
			origin_x = origin0_x + int(id / 4) * self.card_height
			origin_y = origin0_y - (id % 4) * self.card_width
			self.write('<g id="card%d" transform="matrix(0,-1,1,0,%f,%f)">\n' % (id, origin_x, origin_y))
		else:
			error("Invalid number of cards per page: %d" % self.cards_per_page)

		self.indent()

	def end_card_page_transform(self):
		self.outdent()
		self.write('</g>\n')
	
	def draw_card(self, id, pattern, card):
		name = card[0]
		attrs = card[1]
		desc = card[2]
		self.validate_attrs(name, attrs)
		self.record_attrs(name, attrs)
		self.validate_pattern(name, pattern)
		
		pe_tag = self.pattern_key(pattern) + '-' + attrs['element']
		if pe_tag in self.pattern_elements:
			error('Pattern for "%s" already used for "%s"' % (name, self.pattern_elements[pe_tag]))
		self.pattern_elements[pe_tag] = name

		self.start_card_page_transform(id)

		self.draw_border()
		self.draw_title(name)
		self.draw_id(attrs['id'])
		if 'starter' in attrs:
			self.draw_starter()
		
		self.draw_pattern(pattern, attrs['element'])

		self.draw_desc(desc)
		
		self.end_card_page_transform()
	
	def draw_border(self):
		style = 'fill:#ffffff;fill-opacity:1;stroke:#c0c0c0;stroke-width:0.88582677;stroke-opacity:1'
		self.write('<rect id="c%d-border" x="%.03f" y="%.03f" width="%.03f" height="%.03f" rx="11.25" ry="11.25" style="%s"/>\n' % (self.curr_card, 0, 0, self.card_width, self.card_height, style))

	def draw_title(self, title):
		id = "c%d-title" % self.curr_card
		self.draw_text(id, self.card_width / 2, 30, title, 18, align='center', weight='bold', font='Arial Narrow')
		
	def draw_id(self, spell_id):
		card_id = "c%d-spell-id" % self.curr_card
		self.draw_text(card_id, self.card_width / 2, self.card_height-15, str(spell_id), 10, align='center', style='italic', font='Georgia')

	def draw_starter(self):
		id = "c%d-starter" % self.curr_card
		self.draw_text(id, self.card_width / 2, self.card_height-25, "STARTER", 10, align='center', style='italic', font='Georgia')

	def draw_desc(self, desc):
		width = 155
		height = 160
		bottom_margin = 25
		x = (self.card_width - width) / 2
		y = self.card_height - bottom_margin - height
		rect = { 'x': x, 'y': y, 'width': width, 'height': height }
		self.draw_flow_text(rect, desc, size=10)
	
	def draw_pattern(self, pattern_raw, element):
		style_empty = 'opacity:1;fill:#e0e0e0;fill-opacity:1;stroke:none;stroke-width:0;stroke-linecap:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1'
		style_box = 'opacity:1;fill:none;fill-opacity:1;stroke:#000000;stroke-width:2;stroke-linecap:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1'
		
		pattern = [x.split() for x in pattern_raw]
		gheight = len(pattern)
		gwidth = len(pattern[0])

		offset = 26
		px0 = 13.25
		py0 = 46
		clone_x0 = 0
		clone_y0 = -280
		if gwidth % 2 == 0:
			px0 += offset / 2
			clone_x0 += offset / 2
			max_width = 6
		else:
			max_width = 7
		if gheight %2 == 0:
			py0 += offset / 2
			clone_y0 += offset / 2
			max_height = 2
		else:
			py0 = 46
			max_height = 3

		dot_x0 = px0 + 10
		dot_y0 = py0 + 10

		x_begin = int((max_width - gwidth) / 2)
		x_end = x_begin + gwidth
		y_begin = int((max_height - gheight) / 2)
		y_end = y_begin + gheight
		
		self.indent()
		for iy in xrange(0, max_height):
			for ix in xrange(0, max_width):
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
		
	
	# Spell
	
	def validate_pattern(self, name, pattern):
		first_row = True
		num_cols = 0
		for row in pattern:
			cols = row.split()
			if first_row:
				num_cols = len(cols)
				first_row = False
			if len(cols) != num_cols:
				error(name + ": Mismatch number of columns in pattern")
		
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
			error(name + ': ID ' + str(attrs['id']) + ' already used by "' + self.id2name[attrs['id']] +'"')
		
	def record_attrs(self, name, attrs):
		id = attrs['id']
		self.name2id[name] = id
		self.id2name[id] = name
		if id > self.max_id:
			self.max_id = id

		spell_name = "%s (%d)" % (name, id) 

		element = attrs['element']
		if not element in self.elements:
			self.elements[element] = []
		self.elements[element].append(id)

		for cat in attrs['category'].split(','):
			if not cat in self.categories:
				self.categories[cat] = []
			self.categories[cat].append(id)
		
	def pattern_key(self, pattern):
		"""Convert pattern array into a simple string that can be used as a key."""
		return '/'.join([''.join(x.split()) for x in pattern])

	# Utilities

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
			self.write_raw('<flowPara>%s</flowPara>' % para)
		self.write_raw('</flowRoot>')
		self.write_raw('\n')
		self.outdent()
		
	def create_svg_file(self, name):
		if not os.path.isdir(self.svg_out_dir):
			os.makedirs(self.svg_out_dir);
		self.out = open(os.path.join(self.svg_out_dir, '%s.svg' % name), "w")
		self.write_header()

	def close_svg_file(self, name):
		self.write_footer()
		self.out.close()

		if self.gen_pdf:
			# Generate PDF file.
			if not os.path.isdir(self.pdf_out_dir):
				os.makedirs(self.pdf_out_dir);
			self.pdf_files.append('pdf/%s.pdf' % name)
			subprocess.call([
				"/Applications/Inkscape.app/Contents/Resources/bin/inkscape",
				"--file=%s" % os.path.abspath(os.path.join(self.svg_out_dir, '%s.svg' % name)),
				"--export-pdf=%s" % os.path.abspath(os.path.join(self.pdf_out_dir, '%s.pdf' % name)),
				"--export-dpi=300",
				"--export-text-to-path",
				"--without-gui"
				])

	def gen_cards(self):
		self.curr_file = -1
		self.curr_card = -1
		filename = ''
		for card_pattern in spell_card_data:
			pattern = card_pattern[0]

			for card in card_pattern[1]:
				if filename == '':
					self.curr_file += 1
					filename = 'out%02d' % self.curr_file
					self.create_svg_file(filename)
				self.curr_card += 1
				
				print self.curr_file, self.curr_card, card[0]
				self.draw_card(self.curr_card, pattern, card)

				if self.curr_card == (self.cards_per_page - 1):
					self.close_svg_file(filename)
					filename = ''
					self.curr_card = -1

		if filename != '':
			self.close_svg_file(filename)
		
		if self.gen_pdf and self.combine_pdf:
			cmd = ["/System/Library/Automator/Combine PDF Pages.action/Contents/Resources/join.py",
				"-o", os.path.join(self.out_dir, 'cards.pdf')] + self.pdf_files
			subprocess.call(cmd)

	def gen_summary(self):
		print 'Element Summary:'
		for e in self.valid_elements:
			print ' ', e
			print '   ', self.elements[e]
			print '   Total spells:', len(self.elements[e])

		print 'Category Summary:'
		for c in self.valid_categories:
			print ' ', c
			print '   ', self.categories[c]

		print 'Max ID:', self.max_id
	

def usage():
	print "Usage: %s <options>" % sys.argv[0]
	print "where <options> are:"
	print "  --pdf       Generate PDF output files"
	print "  --combine   Combine into single PDF file"
	print "  --per-page  Num cards per page: 8 or 9 (default)"
	print "  --a4        A4 output (default = letter)"
	sys.exit(2)

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:],
			'p',
			['pdf', 'per-page=', 'combine', 'a4', 'summary'])
	except getopt.GetoptError:
		usage()

	options = {
		'pdf': False,
		'per-page': 9,
		'combine': False,
		'a4': False,
		'summary': False,
	}
	for opt,arg in opts:
		if opt in ('-p', '--pdf'):
			options['pdf'] = True
		if opt in ('--per-page'):
			options['per-page'] = int(arg)
		if opt in ('--combine'):
			options['combine'] = True
		if opt in ('--a4'):
			options['a4'] = True
		if opt in ('--summary'):
			options['summary'] = True
			
	cgen = CardGen(options)
	cgen.gen_cards()
	if options['summary']:
		cgen.gen_summary()

if __name__ == '__main__':
	main()