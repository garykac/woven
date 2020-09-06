#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

INKSCAPE_APP = 'inkscape'

class Inkscape(object):

    # |svg_path| - Full path to SVG source file
    # |png_path| - Full path to PNG output file
    # |dpi| - DPI for PNG output file
    @staticmethod
    def export_png(svg_path, png_path, dpi):
        subprocess.run([
            INKSCAPE_APP,
            "--file={0:s}".format(svg_path),
            "--export-png={0:s}".format(png_path),
            "--export-dpi={0:d}".format(dpi),
            "--export-text-to-path",
            "--export-area-page",
            "--without-gui"
        ], stdout = subprocess.DEVNULL)
