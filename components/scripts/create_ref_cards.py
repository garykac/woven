#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from inkscape import Inkscape, InkscapeActions

REF_DIR = os.path.join('..', 'ref-cards')
PNG_OUTPUT_DIR = os.path.join(REF_DIR, 'png')
PDF_5UP_DIR = os.path.join(REF_DIR, '5up')

def export_monster_parts():
	MONSTER_PARTS = [
		"monster-i",
		"monster-ii",
		"monster-iii",
		"monster-iv",
	]
	for m in MONSTER_PARTS:
		export_svg2png_showlayer("academy-monster", m, f'academy-{m}')

def export_spell_parts():
	SPELL_PARTS = [
		"spell-i",
		"spell-ii",
		"spell-iii",
	]
	for s in SPELL_PARTS:
		export_svg2png_showlayer("spell-cast", s, s)

def export_score_tracks():
	SCORE_TRACK = [
		"track-1p",
		"track-2p",
		"track-3p",
		"track-4p",
	]
	for s in SCORE_TRACK:
		export_svg2png_showlayer("academy-score-track", s, f'academy-score-{s}')

def export_5up_pdfs():
	for x in ["monster", "spell"]:
		export_svg2pdf(f"5up-{x}")

def export_svg2pdf(name):
	print(f"Exporting {name}.pdf")
	actions = InkscapeActions()
	actions.exportFilename(os.path.join(PDF_5UP_DIR, f'{name}.pdf'))
	actions.exportDpi(300)
	actions.exportAreaPage()
	actions.exportDo()
	Inkscape.run_actions(os.path.join(PDF_5UP_DIR, f'{name}.svg'), actions)

def export_svg2png(name):
	print(f"Exporting {name}.png")
	actions = InkscapeActions()
	actions.exportFilename(os.path.join(PNG_OUTPUT_DIR, f'{name}.png'))
	actions.exportDpi(300)
	actions.exportAreaPage()
	actions.exportDo()
	Inkscape.run_actions(os.path.join(REF_DIR, f'{name}.svg'), actions)

def export_svg2png_showlayer(svg, layername, png_out):
	print(f"Exporting {svg} {layername}.png")
	actions = InkscapeActions()
	actions.layerShow(f"{layername}")
	actions.exportFilename(os.path.join(PNG_OUTPUT_DIR, f'{png_out}.png'))
	actions.exportDpi(300)
	actions.exportAreaPage()
	actions.exportDo()
	Inkscape.run_actions(os.path.join(REF_DIR, f'{svg}.svg'), actions)

export_monster_parts()
export_svg2png("academy-monster-all")
export_svg2png("academy-player-aid")
export_score_tracks()
export_spell_parts()
export_5up_pdfs()
