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

from data_effect_cards import effect_card_data
from data_effect_cards import effect_card_revision

class EffectCardGen(CardGen):
	def __init__(self, options):
		CardGen.__init__(self, options)

		self.card_data = effect_card_data

	def process_card_data(self, card_data):
		die_rolls = card_data[0]
		event_info = card_data[1]

		self.pre_card()
		if self.verbose:
			print self.curr_file, self.curr_card
		self.draw_card(self.curr_card, die_rolls, event_info)
		self.post_card()

	def draw_card(self, id, die_rolls, event_info):
		self.start_card_page_transform(id)

		if not self.no_border:
			self.draw_border()
		
		self.draw_d4(die_rolls[0])
		self.draw_d6(die_rolls[1])
		self.draw_d8(die_rolls[2])

		self.draw_fire(event_info[0])
		self.draw_air(event_info[1])
		self.draw_water(event_info[2])
		self.draw_earth(event_info[3])
				
		self.end_card_page_transform()
	
	# Element Drawing
	
	def draw_fire(self, info):
		self.draw_clone('element-fire', transform="matrix(1.5,0,0,1.5,-1.624999,-468)")
		rect = { 'x': 27+36, 'y': 138-120, 'width': 121, 'height': 54 }
		if len(info) == 1:
			rect['y'] += 10
		self.draw_flow_text(rect, info)
		
	def draw_air(self, info):
		self.draw_clone('element-air', transform="matrix(1.5,0,0,1.5,-1.447551,-410.56458)")
		rect = { 'x': 27+36, 'y': 138-62, 'width': 121, 'height': 54 }
		if len(info) == 1:
			rect['y'] += 10
		self.draw_flow_text(rect, info)
	
	def draw_water(self, info):
		self.draw_clone('element-water', transform="matrix(1.5,0,0,1.5,-1.447551,-353.12914)")
		rect = { 'x': 27+36, 'y': 138-5, 'width': 121, 'height': 54 }
		if len(info) == 1:
			rect['y'] += 10
		self.draw_flow_text(rect, info)

	def draw_earth(self, info):
		self.draw_clone('element-earth', transform="matrix(1.5,0,0,1.5,-1.447551,-295.69372)")
		rect = { 'x': 27+36, 'y': 138+52, 'width': 121, 'height': 54 }
		if len(info) == 1:
			rect['y'] += 10
		self.draw_flow_text(rect, info)

	# Dice Drawing
	
	def draw_d4(self, value):
		pips = [[], [0], [2, 3], [1, 2, 3], [0, 1, 2, 3]]
		pips_xy = [
			[41.252983, 282.409],  # Center
			[41.252983, 271.75272],  # Top
			[50.481609, 287.73718],  # Bottom Right
			[32.024311, 287.73718],  # Bottom Left
		]

		outline_fill = 'fill:#ffffff'
		pip_fill = 'fill:#000000'
		if value < 0:
			value *= -1
			outline_fill = 'fill:#000000'
			pip_fill = 'fill:#ffffff'

		self.start_group(id='d4')

		outline_style = outline_fill + ";fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:3.79999995;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
		path = "m 65.354984,296.47689 -48.204025,0 24.102013,-41.74591 z"
		self.draw_path(outline_style, path, id='d4-outline')

		pip_style = pip_fill + ";fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
		for pip_index in pips[value]:
			x = pips_xy[pip_index][0]
			y = pips_xy[pip_index][1]
			self.draw_circle(pip_style, x, y, 4)

		self.end_group()
		
	def draw_d6(self, value):
		pips = [[], [4], [0,8], [0,4,8], [0,2,6,8], [0,2,4,6,8], [0,2,3,5,6,8]]
		pips_xy = [
			[89.849571, 264.43292],  # Row 1
			[101.02069, 264.43292],
			[112.19181, 264.43292],
			[89.849571, 275.60406],  # Row 2
			[101.02069, 275.60406],
			[112.19181, 275.60406],
			[89.849571, 286.77518],  # Row 3
			[101.02069, 286.77518],
			[112.19181, 286.77518],
		]

		outline_fill = 'fill:#ffffff'
		pip_fill = 'fill:#000000'
		if value < 0:
			value *= -1
			outline_fill = 'fill:#000000'
			pip_fill = 'fill:#ffffff'

		self.start_group(id='d6')

		outline_style = outline_fill + ";fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:3.79999995;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
		self.draw_rect(outline_style, x=79.908501, y=254.49185, width=42.224377, height=42.224377, r=5.5179586, id='d6-outline')

		pip_style = pip_fill + ";fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
		for pip_index in pips[value]:
			x = pips_xy[pip_index][0]
			y = pips_xy[pip_index][1]
			self.draw_circle(pip_style, x, y, 4.2410717)

		self.end_group()
		
	def draw_d8(self, value):
		pips = [[], [4], [1,7], [1,4,7], [1,2,6,7], [1,2,4,6,7], [1,2,3,5,6,7], [1,2,3,4,5,6,7], [0,1,2,3,5,6,7,8]]
		pips_xy = [
			[160.78839, 260.78104],  # Row 1      *
			[153.37691, 268.19254],  # Row 2    *   *
			[168.19989, 268.19254],
			[145.96542, 275.60403],  # Row 3  *   *   *
			[160.78839, 275.60403],
			[175.61139, 275.60403],
			[153.37691, 283.01553],  # Row 4    *   *
			[168.19989, 283.01553],
			[160.78839, 290.42703],  # Row 5      *
		]

		outline_fill = 'fill:#ffffff'
		pip_fill = 'fill:#000000'
		if value < 0:
			value *= -1
			outline_fill = 'fill:#000000'
			pip_fill = 'fill:#ffffff'

		self.start_group(id='d8')

		outline_style = outline_fill + ";fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:3.79999995;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
		path = "M137.83342 271.70225C137.83342 271.70225 156.88663 252.64904 156.88663 252.64904C159.04822 250.48745 162.52861 250.48745 164.6902 252.64904C164.6902 252.64904 183.74342 271.70225 183.74342 271.70225C185.90501 273.86384 185.90501 277.34423 183.74342 279.50582C183.74342 279.50582 164.6902 298.55904 164.6902 298.55904C162.52861 300.72063 159.04822 300.72063 156.88663 298.55904C156.88663 298.55904 137.83342 279.50583 137.83342 279.50583C135.67183 277.34424 135.67183 273.86384 137.83342 271.70225C137.83342 271.70225 137.83342 271.70225 137.83342 271.70225"
		self.draw_path(outline_style, path, id='d8-outline')

		pip_style = pip_fill + ";fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
		for pip_index in pips[value]:
			x = pips_xy[pip_index][0]
			y = pips_xy[pip_index][1]
			self.draw_circle(pip_style, x, y, 4.0374999)

		self.end_group()
		
	# Utilities

	def write_svg_header_extra(self):
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

def usage():
	print "Usage: %s <options>" % sys.argv[0]
	print "where <options> are:"
	CardGen_OptionDesc()
	sys.exit(2)

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:],
			CardGen_ShortFlags,
			CardGen_LongFlags + ['summary'])
	except getopt.GetoptError:
		usage()

	print CardGen_LongFlags + ['summary']
	options = CardGen_DefaultOptions
	options['summary'] = False
	for opt,arg in opts:
		if opt in ('--summary'):
			options['summary'] = True
		CardGen_ProcessOption(options, opt, arg)

	options['out-dir'] = 'effect-cards'
			
	cgen = EffectCardGen(options)
	cgen.generate_cards()

if __name__ == '__main__':
	main()
