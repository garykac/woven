#!/bin/bash
# This script must be run from the spell-cards/9up directory.

INKSCAPE="/Applications/Inkscape.app/Contents/MacOS/inkscape"

for i in $(seq -f "%02g" 1 4)
do
	echo Generating spell PDF page$i 
	$INKSCAPE --export-filename pdf/9up-page$i.pdf --export-dpi=300 --export-text-to-path --export-area-page svg/9up-page$i.svg
done