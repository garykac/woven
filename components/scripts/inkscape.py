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
