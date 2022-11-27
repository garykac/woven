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
    def __init__(self, type, id=None):
        self.element = Element(type)
        if id == None:
            id = f'node{SVG.next_id()}'
        self.id = id

        self.element.set('id', id)

    def set(self, attr, val):
        self.element.set(attr, str(val))
        
    def set_style(self, style):
        self.element.set('style', str(style))

    def set_transform(self, t):
        self.element.set('transform', t)

    def set_scale_transform(self, x, y):
        self.element.set('transform', f"scale({x},{y})")

    def set_translate_transform(self, x, y):
        self.element.set('transform', f"translate({x} {y})")

class Group(Node):
    def __init__(self, id=None):
        super().__init__('g', id)
        self.children = []

    def add_node(self, node):
        self.children.append(node)
        self.element.append(node.element)
        
class Layer(Group):
    def __init__(self, id=None, label="Layer"):
        super().__init__(id)
        self.element.set('inkscape:label', label)
        self.element.set('inkscape:groupmode', "layer")
    
    def hide(self):
        self.set('style', 'display:none')        

class Style(object):
    def __init__(self, fill=None, stroke=None, strokeWidth=None):
        if fill == None:
            fill = 'none'
        if stroke == None:
            stroke = 'none'
        if strokeWidth == None:
            strokeWidth = '0'
        self.props = {
            'fill': fill,
            'stroke': stroke,
            'stroke-width': str(strokeWidth),
        }

    def get(self, attr):
        return self.props[attr]
    
    def set(self, attr, value):
        self.props[attr] = str(value)

    def set_fill(self, color):
        self.props['fill'] = str(color)

    def set_stroke(self, color, width = 0):
        self.props['stroke'] = str(color)
        self.props['stroke-width'] = str(width)
        
    def __str__(self):
        return ';'.join([k+':'+self.props[k] for k in self.props.keys()])

    def __repr__(self):
        return 'Style=' + self.__str__()

class Path(Node):
    def __init__(self, id=None):
        if id == None:
            id = f'path{SVG.next_id()}'
        super().__init__('path', id)
        self.path = []
        self.currPosition = [0, 0]
    
    def addXY(self, x, y):
        if len(self.path) == 0:
            # First point must be "move" to location.
            self.path.append(['m', x, y])
        else:
            # Subsequent points draw lines from the previous point.
            dx = x - self.currPosition[0]
            dy = y - self.currPosition[1]
            self.path.append(['l', dx, dy])
        self.currPosition = [x, y]
    
    def addPoint(self, pt):
        x, y = pt
        self.addXY(x, y)

    def addPoints(self, pts):
        for pt in pts:
            self.addPoint(pt)
    
    def addCurvePoint(self, c0, c1, pt):
        if len(self.path) == 0:
            raise Exception(f"Must add fixed point before adding curve points")
        (currx, curry) = self.currPosition
        (x, y) = pt
        c0dx = c0[0] - currx
        c0dy = c0[1] - curry
        c1dx = c1[0] - currx
        c1dy = c1[1] - curry
        dx = x - currx
        dy = y - curry
        self.path.append(['c', c0dx, c0dy, c1dx, c1dy, dx, dy])
        self.currPosition = [x, y]

    def end(self):
        path = "m"
        current_type = "l"
        first_point = True
        for pt in self.path:
            type = pt[0]
            if (not first_point) and type != current_type:
                path += f" {type}"
                current_type = type
            first_point = False
            
            if type in ['l', 'm']:
                (x, y) = pt[1:]
                path += f" {x:.6g} {y:.6g}"
            elif type == "c":
                (c0dx, c0dy, c1dx, c1dy, dx, dy) = pt[1:]
                path += f" {c0dx:.6g} {c0dy:.6g} {c1dx:.6g} {c1dy:.6g} {dx:.6g} {dy:.6g}"
            else:
                raise Exception(f"Unsupport path type: {type}")
            
        path += " z"
        self.set('d', path)

    def setPoints(self, pts):
        self.addPoints(pts)
        self.end()
        
class Text(Node):
    def __init__(self, id, x, y, text):
        if id == None:
            id = f'text{SVG.next_id()}'
        super().__init__('text', id)
        self.set('x', str(x))
        self.set('y', str(y))
        self.set_style("font-style:normal;font-weight:normal;font-size:4px;font-family:sans-serif;fill:#000000;fill-opacity:1;stroke:none")

        tspan = Element('tspan')
        tspan.set('x', str(x))
        tspan.set('y', str(y))
        tspan.text = text
        self.element.append(tspan)

class SVG(object):
    id_base = 1000
    
    def __init__(self, size):
        self.width = size[0]
        self.height = size[1]
        
        self.idmap = {}

        #ET.register_namespace('', "http://www.w3.org/2000/svg")
        #ET.register_namespace('sodipodi', "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")
        #ET.register_namespace('inkscape', "http://www.inkscape.org/namespaces/inkscape")
        #ET.register_namespace('xlink', "http://www.w3.org/1999/xlink")
        #ET.register_namespace('dc', "http://purl.org/dc/elements/1.1/")
        #ET.register_namespace('cc', "http://creativecommons.org/ns#")
        #ET.register_namespace('rdf', "http://www.w3.org/1999/02/22-rdf-syntax-ns#")

        self.root = Element('svg')
        svg = self.root
        svg.set('version', "1.1")
        svg.set('id', "svg_root")

        # Manually add registered namespaces.
        svg.set('xmlns', "http://www.w3.org/2000/svg")
        svg.set('xmlns:sodipodi', "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")
        svg.set('xmlns:inkscape', "http://www.inkscape.org/namespaces/inkscape")

        # Explicitly add additional namespaces.
        svg.set('xmlns:xlink', "http://www.w3.org/1999/xlink")

        # Width and height of drawing in absolute units (mm).
        svg.set('width', f"{self.width}mm")
        svg.set('height', f"{self.height}mm")

        # The viewbox defines the "user units" for the file.
        # Set the viewbox to be the same as the width,height in mm so that
        # each user unit = 1mm.
        svg.set('viewBox', f"0 0 {self.width} {self.height}")

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
        
    # |path| a Path class
    def add_clip_path(self, path):
        clip = Element("clipPath")
        clippath_id = f"clippath-{SVG.next_id()}"
        clip.set("id", clippath_id)
        clip.append(path.element)
        self.defs.append(clip)
        return clippath_id
        
    def add_inkscape_layer(self, id, label, parent=None):
        layer = Layer(id, label)
        if parent == None:
            self.root.append(layer.element)
        else:
            parent.add_node(layer)
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

    # |elem| The <text> or <flowRoot> element to update.
    # |text| A string or a list of strings with the text to add.
    @staticmethod
    def set_text(elem, text):
        (ns, tag) = SVG.split_tag(elem.tag)
        if tag == 'text':
            if isinstance(text, list):
                text = text[0]
            SVG.__set_single_text(elem, text)
        elif tag == 'flowRoot':
            if not isinstance(text, list):
                text = [text]
            SVG.__set_flow_text(elem, text)
        else:
            raise Exception(f"Unable to set_text for {tag} node")

    # Set the text within an SVG text span:
    #   <text>
    #     <tspan>
    # |elem| The <text> node to update.
    # |text| A string 
    @staticmethod
    def __set_single_text(elem, text):
        for child in elem.iter():
            if SVG.split_tag(child.tag)[1] == 'tspan':
                child.text = text

    # Set blocks of text within an SVG flow text:
    #   <flowRoot>
    #     <flowRegion>
    #     <flowPara>*
    # |elem| The <flowRoot> node to update.
    # |text| A list of strings (one per paragraph)
    @staticmethod
    def __set_flow_text(elem, text):
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
            id = f'use{SVG.next_id()}'
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
            id = f'rect{SVG.next_id()}'
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
            id = f'circle{SVG.next_id()}'
        n = Node('circle', id)
        n.set('cx', str(cx))
        n.set('cy', str(cy))
        n.set('r', str(r))
        return n
