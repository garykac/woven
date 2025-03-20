#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
import subprocess

INKSCAPE_APP = 'inkscape'
if platform.system() == 'Darwin': # MacOS
    INKSCAPE_APP = '/Applications/Inkscape.app/Contents/MacOS/inkscape'

class Inkscape(object):

    # |svg_path| - Full path to SVG source file
    # |png_path| - Full path to PNG output file
    # |dpi| - DPI for PNG output file
    @staticmethod
    def export_png(svg_path, png_path, *, id=None, dpi=300):
        cmd = [INKSCAPE_APP]
        cmd.append(f"--export-filename={png_path}")
        cmd.append(f"--export-dpi={dpi}")
        cmd.append("--export-text-to-path")
        if id:
            cmd.append(f"--export-id={id}")
        else:
            cmd.append("--export-area-page")
        cmd.append(svg_path)
        subprocess.run(cmd, stdout = subprocess.DEVNULL)

    @staticmethod
    def export_pdf(svg_path, pdf_path, *, dpi=300):
        cmd = [INKSCAPE_APP]
        cmd.append(f"--export-filename={pdf_path}")
        cmd.append(f"--export-dpi={dpi}")
        cmd.append("--export-text-to-path")
        cmd.append("--export-area-page")
        cmd.append(svg_path)
        subprocess.run(cmd, stdout = subprocess.DEVNULL)

    @staticmethod
    def run_actions(svg_path, inkscape_actions):
        cmd = [INKSCAPE_APP]

        actions = ';'.join(inkscape_actions.actions)
        cmd.append(f"--actions={actions}")

        cmd.append(svg_path)
        subprocess.run(cmd, stdout = subprocess.DEVNULL)

class InkscapeActions(object):
    def __init__(self):
        self.actions = []
    
    def addAction(self, action):
        self.actions.append(action)

    def selectById(self, id):
        self.addAction(f"select-by-id:{id}")

    def selectionHide(self):
        self.addAction("selection-hide")

    def layerHide(self, layer_id):
        self.addAction(f"select-clear")
        self.addAction(f"select-by-id:{layer_id}")
        self.addAction(f"object-set-attribute:style, display:none")

    def layerShow(self, layer_id):
        self.addAction(f"select-clear")
        self.addAction(f"select-by-id:{layer_id}")
        self.addAction(f"object-set-attribute:style, display:inline")

    def exportId(self, id):
        self.addAction(f"export-id:{id}")

    def exportFilename(self, filename):
        self.addAction(f"export-filename:{filename}")

    def exportDpi(self, dpi):
        self.addAction(f"export-dpi:{dpi}")

    def exportAreaPage(self):
        self.addAction("export-area-page")

    def exportDo(self):
        self.addAction("export-do")
