#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Note: Requires the `identify` and `convert` command line tools from ImageMagick.

# TODO: Autogenerate data_texture.py file when building swatches.

import getopt
import os
import re
import subprocess
import sys

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree

VERBOSE = False

MAP_OUTPUT_DIR = "../maps"
MAP_TEMPLATE_DIR = os.path.join(MAP_OUTPUT_DIR, 'templates')

TEXTURE_DIR = "../../third_party/textures"

TEXTURES = {
    # <id>: <swatch-size>
    "g01": 30,  # grey stone (castle/tower, bridge)
    "h02": 40,  # high elevation
    "l01": 50,  # low elevation
    "m01": 45,  # mid elevation
    "r01": 200, # rivers and lakes
    "r02": 200, # rivers and lakes
    "s01": 20,  # star icons
    "t01": 20,  # trees
}

TEXTURE_TYPES = [t[0] for t in TEXTURES.keys()]

def run(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    return result.stdout.decode("utf8")

class TextureBuilder():

    def __init__(self):
        self.swatchCounts = {}
        
    def genTextureSwatches(self, id):
        self.id = id
        self.terrainType = id[0]
        
        self.calcImageSize(os.path.join(TEXTURE_DIR, f"{self.terrainType}/{id}.png"))

        file = os.path.join(MAP_TEMPLATE_DIR, f"texture-{self.terrainType}.svg")

        tree = ElementTree()
        tree.parse(file)

        imageNode = findId(tree.getroot(), f"{self.id}")
        if not imageNode:
            raise Exception(f"Unable to find {self.id} in {file}")
        self.extractImageInfo(imageNode)

        circlesNode = findId(tree.getroot(), f"{self.id}-circles")
        if not imageNode:
            raise Exception(f"Unable to find {self.id}-circles in {file}")
        self.extractCircleInfo(circlesNode)

    def extractImageInfo(self, root):
        for c in root:
            (ns, tag) = splitTag(c.tag)
            if tag == "image":
                self.x = (float)(c.attrib.get("x"))
                self.y = (float)(c.attrib.get("y"))
                self.scaledWidth = (float)(c.attrib.get("width"))
                self.scaledHeight = (float)(c.attrib.get("height"))

    def extractCircleInfo(self, root):
        swatchId = 0
        print(f"Processing {self.id}", end='')

        outputDir = os.path.join(TEXTURE_DIR, f"{self.terrainType}/{self.id}")
        if not os.path.exists(outputDir):
           os.makedirs(outputDir)

        for c in root:
            (ns, tag) = splitTag(c.tag)
            if tag in ["ellipse", "circle"]:
                swatchId += 1
                print(".", flush=True, end='')
                cx = (float)(c.attrib.get("cx"))
                cy = (float)(c.attrib.get("cy"))
                self.genTexture(swatchId, cx, -cy)
        print()

        # Record swatch count.
        self.swatchCounts[self.id] = swatchId

    def genTexture(self, swatchId, cx, cy):
        if VERBOSE:
            print(f"size: {self.width} x {self.height}")
            print(f"Scaled size: {self.scaledWidth} x {self.scaledHeight}")
        scale = self.width / self.scaledWidth
        #            (x,y)               scaledWidth
        #               +-------------------+
        #               |                   |
        #               |  cx,cy            |
        #               |    +              |
        #               |         o---------|-----> x
        #               |         |         |
        #               |         |         |
        #               |         |         |
        #  scaledHeight +-------------------+
        #                         |
        #                         v y
        x = cx - self.x
        y = -cy - self.y

        swatchSize = TEXTURES[self.id]
        width = (int)(swatchSize * scale)
        height = (int)(swatchSize * scale)
        originX = (int)((x - swatchSize/2) * scale)
        originY = (int)((y - swatchSize/2) * scale)

        # If the scale is too large, we'll have larger files than needed.
        # Restrict the overall scale to be 10 (dots-per-mm) which is roughly 254dpi.
        resizeScale = None
        if scale > 10:
            resizeScale = 10 / scale
            if VERBOSE:
                print(f"resizeScale: {resizeScale}")

        if VERBOSE:
            print(f"swatchSize: {swatchSize}; scale: {scale} {width}x{height} @ {originX},{originY}")
        if originX + width > self.width:
            error(f"Swatch {swatchId} off right edge of texture: {originX} + {width} > {self.width}")
        if originY + height > self.height:
            error(f"Swatch {swatchId} off bottom edge of texture: {originY} + {height} > {self.height}")

        id = self.id
        cmd = ["convert"]
        cmd.append(os.path.join(TEXTURE_DIR, f"{self.terrainType}/{id}.png"))
        cmd.extend(["-crop", f"{width}x{height}+{originX}+{originY}"])
        if resizeScale:
            newWidth = width * resizeScale
            newHeight = height * resizeScale
            cmd.extend(["-resize", f"{newWidth}x{newHeight}"])
        cmd.append(os.path.join(TEXTURE_DIR, f"{self.terrainType}/{id}/{id}-{swatchId:02d}.png"))
        result = run(cmd)

    def calcImageSize(self, path):
        cmd = ["identify"]
        cmd.append("-ping")
        cmd.extend(["-format", "%[width]x%[height]\n"])
        cmd.append(path)
        result = run(cmd)
        sizeMatch = re.match(r"^(?P<width>\d+)x(?P<height>\d+)$", result)
        if not sizeMatch:
            self.width = 2000
            self.height = 2000
            return
        
        self.width = (int)(sizeMatch.group("width"))
        self.height = (int)(sizeMatch.group("height"))

    def writeDataFile(self):
        with open("data_texture.py", "w") as fout:
            fout.write("# DO NOT EDIT THIS FILE\n")
            fout.write("# This file is autogenerated by build_texture.py.\n")
            fout.write("\n")

            fout.write("# Texture info.\n")
            fout.write("TEXTURE_INFO = {\n")
            fout.write("    # <id>: <swatch-size>, <num-swatches>\n")
            for t in TEXTURES:
                fout.write(f'    "{t}": [{TEXTURES[t]}, {self.swatchCounts[t]}],\n')
            fout.write("}\n")
            fout.write("\n")

            
            tTypes = {}
            for t in TEXTURE_TYPES:
                tTypes[t] = []
            for t in TEXTURES:
                tTypes[t[0]].append(t)
            fout.write("TEXTURES = {\n")
            for tType in tTypes:
                textures = ', '.join([f'"{x}"' for x in tTypes[tType]])
                fout.write(f'    "{tType}": [{textures}],\n')
            fout.write("}\n")
        
def findId(node, id):
    nId = node.attrib.get("id")
    if nId == id:
        return node
    for child in node:
        r = findId(child, id)
        if r:
            return r
    return None

def splitTag(tag):
    namespace = ''
    m = re.match(r'\{(?P<namespace>.*)\}(?P<tag>.*)', tag)
    if m:
        namespace = m.group("namespace")
        tag = m.group("tag")
    return [namespace, tag]

def error(msg):
    print(f"ERROR: {msg}")
    sys.exit(0)

def main():
    tb = TextureBuilder()
    for t in TEXTURES:
        tb.genTextureSwatches(t)
    tb.writeDataFile()

if __name__ == '__main__':
    main()
