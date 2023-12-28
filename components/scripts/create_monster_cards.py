#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from inkscape import Inkscape, InkscapeActions

MONSTER_DIR = os.path.join('..', 'monster-cards')
CARD_TEMPLATE = os.path.join(MONSTER_DIR, 'monster-card.svg')
PNG_OUTPUT_DIR = os.path.join(MONSTER_DIR, 'png')
PDF_5UP_DIR = os.path.join(MONSTER_DIR, '5up')

MONSTERS = [
	"heba",
	"mfed",
	"rgda",
	"rmcb",
	"wgfb",
	"whdc",
	"ygec",
	"yrhf",
	"ywma",
	"zfca",
	"zmhg",
	"zwre",
	"zydb",
]

def export_monster(m):
	print(f"Exporting {m}")
	actions = InkscapeActions()
	actions.layerShow(f"monster-{m}")
	actions.exportFilename(os.path.join(PNG_OUTPUT_DIR, f'{m}.png'))
	actions.exportDpi(300)
	actions.exportAreaPage()
	actions.exportDo()

	Inkscape.run_actions(CARD_TEMPLATE, actions)

def export_monsters():
	for m in MONSTERS:
		export_monster(m)

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
	for x in range(1, 4):
		export_5up_pdf(f"5up-page{x}")

#export_monsters()
#export_all_png()
export_5up_pdfs()
