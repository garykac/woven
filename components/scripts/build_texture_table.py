#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getopt
import os
import re
import sys

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree

MAP_OUTPUT_DIR = "../maps"
MAP_TEMPLATE_DIR = os.path.join(MAP_OUTPUT_DIR, 'templates')

def scanTextureSvg(templateId):
    terrainType = templateId[0]
    file = os.path.join(MAP_TEMPLATE_DIR, f"texture-{terrainType}.svg")

    tree = ElementTree()
    tree.parse(file)
    circles = findId(tree.getroot(), f"{templateId}-circles")
    extractCircleInfo(templateId, circles)

def findId(node, id):
    nId = node.attrib.get("id")
    if nId == id:
        return node
    for child in node:
        r = findId(child, id)
        if r:
            return r
    return None

def extractCircleInfo(id, root):
    print(f"{id.upper()}_TEXTURE_OFFSETS = [")
    for c in root:
        (ns, tag) = split_tag(c.tag)
        if tag == "ellipse":
            cx = (float)(c.attrib.get("cx"))
            cy = (float)(c.attrib.get("cy"))
            print(f"    [{cx}, {-cy}],")
    print(f"]")

def split_tag(tag):
    namespace = ''
    m = re.match(r'\{(.*)\}(.*)', tag)
    if m:
        namespace = m.group(1)
        tag = m.group(2)
    return [namespace, tag]

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print("Missing arg: <texture-id>")
        sys.exit(0)
    id = args.pop(0)
    scanTextureSvg(id)

if __name__ == '__main__':
    main()
