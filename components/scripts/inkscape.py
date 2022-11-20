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
    def export_png(svg_path, png_path, dpi):
        cmd = [INKSCAPE_APP]
        if False:   # deprecated arguments
            cmd.append("--file={0:s}".format(svg_path))
            cmd.append("--export-png={0:s}".format(png_path))
            cmd.append("--without-gui")
        else:
            cmd.append("--export-filename={0:s}".format(png_path))
        cmd.append("--export-dpi={0:d}".format(dpi))
        cmd.append("--export-text-to-path")
        cmd.append("--export-area-page")
        cmd.append(svg_path)
        subprocess.run(cmd, stdout = subprocess.DEVNULL)

    @staticmethod
    def export_pdf(svg_path, pdf_path, dpi):
        cmd = [INKSCAPE_APP]
        cmd.append("--export-filename={0:s}".format(pdf_path))
        cmd.append("--export-dpi={0:d}".format(dpi))
        cmd.append("--export-text-to-path")
        cmd.append("--export-area-page")
        cmd.append(svg_path)
        subprocess.run(cmd, stdout = subprocess.DEVNULL)
