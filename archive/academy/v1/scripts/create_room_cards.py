#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from inkscape import Inkscape, InkscapeActions

ROOM_DIR = os.path.join('..', 'room-cards')
CARD_TEMPLATE = os.path.join(ROOM_DIR, 'room-card.svg')
PNG_OUTPUT_DIR = os.path.join(ROOM_DIR, 'png')
PDF_9UP_DIR = os.path.join(ROOM_DIR, '9up')

ROOMS = [
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
	"start",
]

def export_room(r):
	print(f"Exporting {r}")
	actions = InkscapeActions()
	actions.layerShow(f"room-{r}")
	actions.exportFilename(os.path.join(PNG_OUTPUT_DIR, f'{r}.png'))
	actions.exportDpi(300)
	actions.exportAreaPage()
	actions.exportDo()
	Inkscape.run_actions(CARD_TEMPLATE, actions)

def export_rooms():
	for r in ROOMS:
		export_room(r)

def export_all_png():
	print(f"Exporting all.png")
	actions = InkscapeActions()
	actions.exportFilename(os.path.join(ROOM_DIR, f'all.png'))
	actions.exportDpi(300)
	actions.exportAreaPage()
	actions.exportDo()
	Inkscape.run_actions(os.path.join(ROOM_DIR, f'all.svg'), actions)

def export_9up_pdf(name):
	print(f"Exporting {name}")
	actions = InkscapeActions()
	actions.exportFilename(os.path.join(PDF_9UP_DIR, f'{name}.pdf'))
	actions.exportDpi(300)
	actions.exportAreaPage()
	actions.exportDo()
	Inkscape.run_actions(os.path.join(PDF_9UP_DIR, f'{name}.svg'), actions)

def export_9up_pdfs():
	for x in range(1, 3):
		export_9up_pdf(f"9up-page{x}")

export_rooms()
export_all_png()
export_9up_pdfs()
