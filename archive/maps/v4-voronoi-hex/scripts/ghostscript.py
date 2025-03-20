#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

GHOSTSCRIPT_APP = 'gs'

class GhostScript(object):

    # |pdfOutput| - Combined PDF output file
    # |pddfFiles| - List of PDFs to combine
    @staticmethod
    def combine_pdfs(pdfOutput, pdfFiles):
        cmd = [GHOSTSCRIPT_APP]
        cmd.append("-dBATCH")
        cmd.append("-dNOPAUSE")
        cmd.append("-q")
        cmd.append("-sDEVICE=pdfwrite")
        cmd.append(f"-sOutputFile={pdfOutput}")
        for f in pdfFiles:
	        cmd.append(f)
        subprocess.run(cmd, stdout = subprocess.DEVNULL)
