#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Note: Requires the `identify` and `convert` command line tools from ImageMagick.

import getopt
import os
import re
import subprocess
import sys

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree

MAP_OUTPUT_DIR = "../maps"
MAP_TEMPLATE_DIR = os.path.join(MAP_OUTPUT_DIR, 'templates')

TEXTURE_DIR = "../../third_party/textures"

TEXTURES = {
    # <id>: [ <swatch-size> ]
    "l01": [50],
    "m01": [40],
    "h02": [40],
}

class TextureBuilder():

    def __init__(self, id):
        self.id = id
        self.terrainType = id[0]
        
        self.getImageSize(os.path.join(TEXTURE_DIR, f"{self.terrainType}/{id}.png"))

        
    def genTextureSwatches(self):
        file = os.path.join(MAP_TEMPLATE_DIR, f"texture-{self.terrainType}.svg")

        tree = ElementTree()
        tree.parse(file)

        imageNode = findId(tree.getroot(), f"{self.id}")
        self.extractImageInfo(imageNode)

        circlesNode = findId(tree.getroot(), f"{self.id}-circles")
        self.extractCircleInfo(circlesNode)

    def extractImageInfo(self, root):
        for c in root:
            (ns, tag) = splitTag(c.tag)
            if tag == "image":
                self.x = (float)(c.attrib.get("x"))
                self.y = (float)(c.attrib.get("y"))
                self.scaledHeight = (float)(c.attrib.get("height"))
                self.scaledWidth = (float)(c.attrib.get("width"))
                self.scaledHeight = (float)(c.attrib.get("height"))

    def extractCircleInfo(self, root):
        swatchId = 0
        for c in root:
            (ns, tag) = splitTag(c.tag)
            if tag in ["ellipse", "circle"]:
                swatchId += 1
                print(f"Processing {self.id} - {swatchId}")
                cx = (float)(c.attrib.get("cx"))
                cy = (float)(c.attrib.get("cy"))
                self.genTexture(swatchId, cx, -cy)

    def genTexture(self, swatchId, cx, cy):
        #print(f"size: {self.width} x {self.height}")
        #print(f"Scaled size: {self.scaledWidth} x {self.scaledHeight}")
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

        swatchSize = TEXTURES[self.id][0]
        width = (int)(swatchSize * scale)
        height = (int)(swatchSize * scale)
        originX = (int)((x - swatchSize/2) * scale)
        originY = (int)((y - swatchSize/2) * scale)

        if originX + width > self.width:
            error(f"Swatch {swatchId} off right edge of texture: {originX} + {width} > {self.width}")
        if originY + height > self.height:
            error(f"Swatch {swatchId} off bottom edge of texture: {originY} + {height} > {self.height}")

        id = self.id
        cmd = ["convert"]
        cmd.append(os.path.join(TEXTURE_DIR, f"{self.terrainType}/{id}.png"))
        cmd.extend(["-crop", f"{width}x{height}+{originX}+{originY}"])
        cmd.append(os.path.join(TEXTURE_DIR, f"{self.terrainType}/{id}/{id}-{swatchId:02d}.png"))
        result = subprocess.run(cmd, stdout=subprocess.PIPE)

    def getImageSize(self, path):
        cmd = ["identify"]
        cmd.append("-ping")
        cmd.extend(["-format", "%[width]x%[height]\n"])
        cmd.append(path)
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        sizeMatch = re.match(r"^(?P<width>\d+)x(?P<height>\d+)$", result.stdout.decode("utf8"))
        if not sizeMatch:
            return [0,0]
        
        self.width = (int)(sizeMatch.group("width"))
        self.height = (int)(sizeMatch.group("height"))

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
    args = sys.argv[1:]
    if len(args) != 1:
        error("Missing arg: <texture-id>")
    id = args.pop(0)
    if not id in TEXTURES:
        error("Unknown texture id: <texture-id>")
    
    tb = TextureBuilder(id)
    tb.genTextureSwatches()

if __name__ == '__main__':
    main()
