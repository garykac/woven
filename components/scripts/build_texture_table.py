#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree

MAP_OUTPUT_DIR = "../maps"
MAP_TEMPLATE_DIR = os.path.join(MAP_OUTPUT_DIR, 'templates')

def scanTextureSvg(templateId):
    file = os.path.join(MAP_TEMPLATE_DIR, f"texture-{templateId}.svg")

    tree = ElementTree()
    tree.parse(file)
    circles = findId(tree.getroot(), f"{templateId}-circles")
    extractCircleInfo(circles)

def findId(node, id):
    nId = node.attrib.get("id")
    if nId == id:
        return node
    for child in node:
        r = findId(child, id)
        if r:
            return r
    return None

def extractCircleInfo(root):
    for c in root:
        (ns, tag) = split_tag(c.tag)
        if tag == "ellipse":
            cx = c.attrib.get("cx")
            cy = c.attrib.get("cy")
            print(f"[{cx}, {cy}],")

def split_tag(tag):
    namespace = ''
    m = re.match(r'\{(.*)\}(.*)', tag)
    if m:
        namespace = m.group(1)
        tag = m.group(2)
    return [namespace, tag]

def main():
    scanTextureSvg("h01")

if __name__ == '__main__':
    main()
