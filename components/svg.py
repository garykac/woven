#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import re

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import XML

class Node(object):
    def __init__(self, type, id):
        self.element = Element(type)
        self.id = id

        self.element.set('id', id)

    def set(self, attr, val):
        self.element.set(attr, str(val))
        
    def set_style(self, style):
        self.element.set('style', str(style))

class Group(Node):
    def __init__(self, id):
        super().__init__('g', id)
        self.children = []

    def add_node(self, node):
        self.children.append(node)
        self.element.append(node.element)
        
class Layer(Group):
    def __init__(self, id, label):
        super().__init__(id)
        self.element.set('inkscape:label', label)
        self.element.set('inkscape:groupmode', "layer")

class Style(object):
    def __init__(self):
        self.props = {
            'fill': 'none',
            'stroke': 'none',
        }

    def get(self, attr):
        return self.props[attr]
    
    def set(self, attr, value):
        self.props[attr] = str(value)

    def __str__(self):
        return ';'.join([k+':'+self.props[k] for k in self.props.keys()])

    def __repr__(self):
        return 'Style=' + self.__str__()
    
class SVG(object):
    id_base = 1000
    
    def __init__(self, size):
        self.width = size[0]
        self.height = size[1]
        
        self.idmap = {}

        ET.register_namespace('', "http://www.w3.org/2000/svg")
        ET.register_namespace('sodipodi', "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")
        ET.register_namespace('inkscape', "http://www.inkscape.org/namespaces/inkscape")
        ET.register_namespace('xlink', "http://www.w3.org/1999/xlink")
        ET.register_namespace('dc', "http://purl.org/dc/elements/1.1/")
        ET.register_namespace('cc', "http://creativecommons.org/ns#")
        ET.register_namespace('rdf', "http://www.w3.org/1999/02/22-rdf-syntax-ns#")

        self.root = Element('svg')
        svg = self.root
        svg.set('version', "1.1")
        svg.set('id', "svg_root")
 
        # 2.5" x 3.5" poker
        svg.set('width', "{0}mm".format(self.width))
        svg.set('height', "{0}mm".format(self.height))

        # The viewbox defines the "user units" for the file.
        # Set each user unit = 1mm.
        svg.set('viewBox', "0 0 {0} {1}".format(self.width, self.height))

        self.defs = SubElement(svg, 'defs')

        # sodipodi:namedview
        # metadata

    @staticmethod
    def next_id():
        SVG.id_base += 1
        return SVG.id_base
    
    def load_ids(self, file, ids):
        tree = ElementTree()
        tree.parse(file)
        root = tree.getroot()
        # Scan all elements in tree order.
        for elem in root.iter():
            id = elem.get('id')
            if id in ids:
                self.idmap[id] = elem

    def write(self, outfile):
        tree = ElementTree(self.root)
        tree.write(outfile, encoding="UTF-8", xml_declaration=True)

    def add_filter_string(self, filter_str):
        filter = XML(filter_str)
        self.defs.append(filter)
        
    def add_inkscape_layer(self, id, label):
        layer = Layer(id, label)
        self.root.append(layer.element)
        return layer

    def add_loaded_element(self, parent, id):
        elem = copy.deepcopy(self.idmap[id])
        parent.element.append(elem)
        return elem

    @staticmethod
    def add_node(parent, child):
        p = parent.element
        c = child.element
        p.append(c)
        
    @staticmethod
    def split_tag(tag):
        namespace = ''
        m = re.match(r'\{(.*)\}(.*)', tag)
        if m:
            namespace = m.group(1)
            tag = m.group(2)
        return [namespace, tag]

    # Set the text within an SVG text span:
    #   <text>
    #     <tspan>
    @staticmethod
    def set_text(elem, text):
        if SVG.split_tag(elem.tag)[1] != 'text':
            return
        for child in elem.iter():
            if SVG.split_tag(child.tag)[1] == 'tspan':
                child.text = text

    # Set blocks of text within an SVG flow text:
    #   <flowRoot>
    #     <flowRegion>
    #     <flowPara>*
    # Given a |text| array, each string in the array is given a separate paragraph.
    @staticmethod
    def set_flow_text(elem, text):
        if SVG.split_tag(elem.tag)[1] != 'flowRoot':
            return

        # Find <flowPara> to use as a template.
        flowpara = None
        for child in elem.iter():
            if SVG.split_tag(child.tag)[1] == 'flowPara':
                flowpara = child
        if flowpara == None:
            return

        # Remove the flowpara, we'll use it as a template for all the paragraphs.
        elem.remove(flowpara)

        for para in text:
            p = copy.deepcopy(flowpara)
            if para == "-":
                p.text = " "
            else:
                p.text = para
            elem.append(p)
    
    @staticmethod
    def group(id):
        g = Group(id)
        return g

    @staticmethod
    def clone(id, xlink, x, y):
        if id == 0:
            id = 'use{0}'.format(SVG.next_id())
        n = Node('use', id)
        n.set('xlink:href', str(xlink))
        n.set('width', "100%")
        n.set('height', "100%")
        n.set('x', str(x))
        n.set('y', str(y))
        return n
        
    @staticmethod
    def rect(id, x, y, width, height):
        if id == 0:
            id = 'rect{0}'.format(SVG.next_id())
        n = Node('rect', id)
        n.set('x', str(x))
        n.set('y', str(y))
        n.set('width', str(width))
        n.set('height', str(height))
        return n
        
    @staticmethod
    def rect_round(id, x, y, width, height, rx, ry=None):
        if ry == None:
            ry = rx
        n = SVG.rect(id, x, y, width, height)
        n.set('rx', str(rx))
        n.set('ry', str(ry))
        return n
        
    @staticmethod
    def circle(id, cx, cy, r):
        if id == 0:
            id = 'circle{0}'.format(SVG.next_id())
        n = Node('circle', id)
        n.set('cx', str(cx))
        n.set('cy', str(cy))
        n.set('r', str(r))
        return n
        
    
