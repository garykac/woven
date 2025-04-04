import copy
import math
import matplotlib.pyplot as plt
import os
import re

from cliff_builder import CliffBuilder
from inkscape import Inkscape, InkscapeActions
from map_common import calcSortedId, calcSortedIdFromPair
from math_utils import (feq, feq_pt, lerp, lerperp, lerp_line, perp_offset, pt_along_line, dist)
from svg import SVG, Filter, Group, Image, Style, Node, Path, Text
from object3d import Object3d
from river_builder import RiverBuilder

from data_texture import TEXTURES, TEXTURE_INFO

NUM_SIDES = 6

TEXTURES_DIR = "../../../third_party/textures"

GENERATE_PLOT = True   # As PNG file.
PLOT_CELL_IDS = True   # Add cell ids to png output file.
DRAW_PUZZLE_BORDER = False

TILE_VERSION = 5

# NOTE: Default units for SVG is mm.

STROKE_WIDTH = 0.3
THICK_STROKE_WIDTH = 1.0
ICON_STROKE_WIDTH = 0.7
ICON_STROKE_WIDTH_MIRROR = 0.5

RIVER_WIDTH = 2.8
CLIFF_WIDTH = 2.0

CLIFF_TOOTH_SPACING = 2.2  # (mm)
CLIFF_TOOTH_WIDTH = 0.8   # (mm)
CLIFF_TOOTH_POINT_WIDTH = 0.05  # (mm)

STROKE_COLOR = "#000000"
STROKE_COLOR_MIRROR = "#ffffff"

# Fill colors for regions based on terrain height.
REGION_COLOR = {
    '_': "#ffffff",  # blank
    'l': "#f0eaac",  #"#d9f3b9",  #'#efecc6',  # low
    'm': "#f0ce76",  #'#dcc382',  # medium
    'h': "#e7a311",  #'#d69200',  # high
    'r': "#a2c6ff",  # river/water
    'c': "#808080",  # cliff
    'v': "#be850a",  # very high mountain
    's': "#eb6eff",  # star/special
    't': "#5ba22d",  # tree
    'x': "#000000",  # annotations
}
REGION_COLOR_MIRROR = {
    '_': "#000000",  # blank
    'l': "#fae470",  # low
    'm': "#e9b530",  # medium
    'h': "#885111",  # high
    'r': "#6286ff",  # river/water
    'c': "#808080",  # cliff
    'v': "#be850a",  # very high mountain
    's': "#eb6eff",  # star/special
    't': "#5ba22d",  # tree
    'x': "#ffffff",  # annotations
}

# Mark where rivers are located on edges using an '*' to note the regions that
# the river flows between.
EDGE_RIVER_INFO = {
    '2f': ['l', '*', 'l', 'l', 'm'],           # l - m, m - h
    '2s': ['m', 'm', '*', 'm', 'm'],           # m - m
}
NEW_EDGE_RIVER_INFO = {
    '1f': ['l', '*', 'l', 'm'],           # l - m, m - l
    '2f': ['m', 'm', '*', 'm', 'h'],      # m - h, h - m
}

# Mark where cliffs are located on edges using an '*' to note the regions that
# are separated by a cliff.
EDGE_CLIFF_INFO = {
    '3f': ['m', 'm', '*', 'h', 'm', 'h'],      # m - h, h - m
}

# Edge puzzle tab info.
# The locations (and type) of the puzzle tabs for interlocking hex tiles.
# Each entry is:
#   [ offset-along-edge, tab-width, tab-height ]
EDGE_PUZZLE_INFO = {
    '0s': [[0.16, 0.05, -0.05], [0.84, 0.05, 0.05]],    # l-l
    '1s': [[0.16, 0.05, -0.05], [0.84, 0.05, 0.05]],    # l-l-l
    '1f': [[0.16, 0.05, -0.05], [0.84, 0.05, 0.05]],    # l-l-l  TODO - needs to be different from 1s
    '2f': [[0.36, 0.05,  0.05]],                        # l-l-l-m
    '2s': [[ 1/3, 0.04,  0.05], [ 2/3, 0.04, -0.05]],   # m-m-m-m
    '3f': [[0.28, 0.03, -0.05], [0.78, 0.03, -0.05]],   # m-m-h-m-h
    '3s': [[0.24, 0.03, -0.05], [0.76, 0.03, 0.05]],    # h-h-m-h-h
}

# Style to use for each type of mark (for the overlay).
OVERLAY_MARK_STYLES = {
    "bridge": "bridge",
    "star": "star",
    "tower": "stone",
    "tree1": "tree",
    "tree2": "tree",
    "tree3": "tree",
    "tree4": "tree",
}

# Dictionary keys:
#   For texture-fill:
#     tex-type: type of texture
#     tex-id: texture image id
#   For non-texture-fill
#     fill: fill color
#   Fill for texture/non-texture
#     stroke: stroke color and style
#   Mirror fill/stroke:
#     mirror-fill: fill color
#     mirror-stroke: stroke color and style
OVERLAY_MARK_STYLE_INFO = {
    "bridge": {
        "tex-type": "g",
        "tex-id": "g01",
        "fill": 'x',
        "stroke": ['x', ICON_STROKE_WIDTH],
        "mirror-fill": '_',
        "mirror-stroke": ['x', ICON_STROKE_WIDTH_MIRROR],
        },
    "stone": {
        "tex-type": "g",
        "tex-id": "g01",
        "fill": '_',
        "stroke": ['x', ICON_STROKE_WIDTH],
        "mirror-fill": 'x',
        "mirror-stroke": [None, ICON_STROKE_WIDTH_MIRROR],
        },
    "star": {
        "tex-type": "s",
        "tex-id": "s01",
        "fill": 's',
        "stroke": ['x', ICON_STROKE_WIDTH],
        "mirror-fill": 's',
        "mirror-stroke": ['x', ICON_STROKE_WIDTH_MIRROR],
        },
    "tree": {
        "tex-type": "t",
        "tex-id": "t01",
        "fill": 't',
        "stroke": ['x', ICON_STROKE_WIDTH],
        "mirror-fill": 't',
        "mirror-stroke": ['x', ICON_STROKE_WIDTH_MIRROR],
        },
}

class VoronoiHexTilePlotter():
    def __init__(self, tile):
        self.tile = tile
        self.options = tile.options
        
        # Random number generator state
        self.rng = tile.rng
        
        self.size = tile.size
        self.vHex = tile.vHex
        self.xMax = tile.xMax

        # Voronoi object has following attributes:
        # .points : array of seed values used to create the Voronoi
        # .point_region : mapping from seed index to region index
        # .vertices : array of Voronoi vertices
        # .regions : array of regions, where each region is an array of Voronoi
        #     indices
        # Ridges are the line segments that comprise the Voronoi diagram:
        # .ridge_points : array of seed index pairs associated with each ridge
        #     [ [s0, s1], [s2, s3], ... ]
        # .ridge_vertices : array of vertex index pairs associated with each
        #     ridge
        #     [ [v0, v1], [v2, v3], ... ]
        self.vor = tile.vor

        # Calculated voronoi vertices.
        self.vertices = tile.vertices

        # np.array of x,y coords.
        self.seeds = tile.seeds
        # Total number of active seeds (ignore external seeds)
        self.numActiveSeeds = tile.numActiveSeeds
        # Mapping seed id -> region (array of vertex ids)
        self.sid2region = tile.sid2region
        self.sid2clippedRegion = tile.sid2clippedRegion
        # Mapping seed id -> terrain type.
        self.seed2terrain = tile.seed2terrain

        # Edge pattern for tile.
        self.edgeTypes = tile.edgeTypes

        # Mapping edge type -> seed location along the edge
        self.edgeSeedInfo = tile.edgeSeedInfo
        # Mapping edge type -> terrain for each region along the edge
        self.edgeRegionInfo = tile.edgeRegionInfo

        # Explicit terrain/river data (loaded from file).
        self.riverData = tile.riverData
        self.cliffData = tile.cliffData
        self.overlayData = tile.overlayData

        self.riverBuilder = None
        self.vertexOverrideRiver = {}
        self.cliffBuilder = None
        self.vertexOverrideCliff = {}
                
        self.calcReversedEdges()

    def calcReversedEdges(self):
        # Calculate data for reversed edges ('r') from the forward ('f') edges.
        for type in self.tile.singleEdgeTypes:
            if type[-1] == 'f':
                newType = type[:-1] + 'r'
                if type in EDGE_RIVER_INFO:
                    EDGE_RIVER_INFO[newType] = EDGE_RIVER_INFO[type][::-1]
                if type in EDGE_CLIFF_INFO:
                    EDGE_CLIFF_INFO[newType] = EDGE_CLIFF_INFO[type][::-1]
                if type in EDGE_PUZZLE_INFO:
                    newEdgePuzzleInfo = []
                    for si in reversed(EDGE_PUZZLE_INFO[type]):
                        offset, tabWidth, tabHeight = si
                        newEdgePuzzleInfo.append([1.0-offset, tabWidth, -tabHeight])
                    EDGE_PUZZLE_INFO[newType] = newEdgePuzzleInfo
            if type[-1] == 's':
                if type in EDGE_PUZZLE_INFO:
                    # Verify the symmetry.
                    first, second = EDGE_PUZZLE_INFO[type]
                    if not feq(first[0], 1.0 - second[0]):
                        raise Exception(f"Puzzle tab offsets for {type} are not symmetric: {first[0]} and {second[0]}")
                    if not feq(first[1], second[1]):
                        raise Exception(f"Puzzle tab widths for {type} do not match: {first[2]} and {second[2]}")
                    if not feq(first[2], -second[2]):
                        raise Exception(f"Puzzle tab heights for {type} are not compatible: {first[3]} and {second[3]}")

    def getTerrainFillColor(self, type):
        if type is None:
            return None
        if self.mirror:
            return REGION_COLOR_MIRROR[type]
        return REGION_COLOR[type]

    def getStrokeColor(self):
        if type is None:
            return None
        if self.mirror:
            return STROKE_COLOR_MIRROR
        return STROKE_COLOR
        
    def plotTile(self, plotId):
        fig = plt.figure(figsize=(8,8))
        self.plotClippedRegions()
        if plotId:
            self.plotBadEdges()
            self.plotTooCloseSeedsLayer()
            self.plotInscribedCircles()
        self.plotRegionIds()
        self.writePlotOutput(fig, plotId)

    def plotClippedRegions(self):
        for sid in range(0, self.numActiveSeeds):
            vids = self.sid2clippedRegion[sid]
            terrain_type = self.seed2terrain[sid]
            color = self.getTerrainFillColor(terrain_type)
            self.plotRegion(vids, color)

    def plotBadEdges(self):
        if len(self.tile.badEdges) == 0:
            return
        
        for bei in self.tile.badEdges:
            badEdge = self.tile.badEdges[bei]
            vid0, vid1, rid = badEdge[0]
            self.plotBadVertex(self.vertices[vid0])
            self.plotBadVertex(self.vertices[vid1])

    def plotTooCloseSeedsLayer(self):
        if len(self.tile.tooClose) == 0:
            return

        for spair in self.tile.tooClose:
            s0, s1 = spair
            self.plotBadVertex(self.seeds[s0])
            self.plotBadVertex(self.seeds[s1])
    
    def plotBadVertex(self, v):
        circle = plt.Circle(v, 1, color="r")
        plt.gca().add_patch(circle)

    def plotInscribedCircles(self):
        for sid in range(0, self.numActiveSeeds):
            polyCenter, polyRadius = self.tile.regionCircles[sid]
            if polyRadius < self.tile.minInscribedCircleRadius:
                circle = plt.Circle(polyCenter, polyRadius, color="#80000080")
                plt.gca().add_patch(circle)
    
    def plotRegionIds(self):
        for sid in range(0, self.numActiveSeeds):
            center = self.seeds[sid]
            if PLOT_CELL_IDS:
                # Shift center point over so the id is drawn centered over the seed point.
                xOffset = 1.4
                if sid >= 10:
                    xOffset *= 2
                plt.text(center[0]-xOffset, center[1]-1.5, f"{sid}")

    def writePlotOutput(self, fig, plotId):
        if not self.options['write_output']:
            return

        outdir_pngid = self.getPngIdOutputDir()
        name = self.tile.calcBaseFilename()

        if plotId is None:
            out_pngid = os.path.join(outdir_pngid, f"{name}.png")
        else:
            outdir_pngid = os.path.join(outdir_pngid, self.options['anim_subdir'])
            if not os.path.isdir(outdir_pngid):
                os.makedirs(outdir_pngid);
            out_pngid = os.path.join(outdir_pngid, f"{name}-{plotId:03d}")
            plt.text(-self.size, -self.size, plotId)

        plt.axis("off")
        plt.xlim([x * self.size for x in [-1, 1]])
        plt.ylim([y * self.size for y in [-1, 1]])
        if GENERATE_PLOT:
            plt.savefig(out_pngid, bbox_inches='tight')
        plt.close(fig)

    def plot(self, plotId=None):
        self.mirror = False
        self._plot(True, plotId)
        if self.options['mirror']:
            self.mirror = True
            saveTextureFillMode = self.options['texture-fill']
            self.options['texture-fill'] = False

            self._plot(False)

            self.options['texture-fill'] = saveTextureFillMode

    def _plot(self, doPlot, plotId=None):
        self.svg = SVG([215.9, 279.4])  #SVG([210, 297])
        if doPlot:
            self.plotTile(plotId)

        # Build list of template ids and then load from svg file.
        svg_ids = []
        for obj in ['bridge', 'star', 'tree1', 'tree2', 'tree3', 'tree4', 'tower']:
            svg_ids.append(f"obj-{obj}")
        svg_ids.append("tile-id")
        self.svg.load_ids(self.options['map_obj_template'], svg_ids)

        self.addInnerGlowFilter("filterInnerGlowH", 2.5, "rgb(217,104,14)")
        self.addInnerGlowFilter("filterInnerGlowM", 2.5, "rgb(220,174,16)")
        self.addInnerGlowFilter("filterInnerGlowL", 2.5, "rgb(219,217,86)")
        self.addInnerGlowFilter("filterInnerGlowR", 2.0, "rgb(111,161,232)")

        layer = self.svg.add_inkscape_layer('layer', "Layer")
        layer.set_transform("translate(107.95 120) scale(1, -1)")
        self.layer = layer

        self.analyzeSpecialRidges()

        # Draw layers back to front.
        
        # Copy background fill from stroke color.
        backgroundFill = Style(fill=self.getStrokeColor())
        self.drawHexTileBorder("background", "Tile Background", backgroundFill)

        self.drawClippedRegionLayer()

        self.drawRoundedRegionFillLayer()

        self.drawRoundedRegionStrokeLayer()
        
        self.drawRegionLayer()
        self.drawUnmodifiedRegionLayer()

        self.drawSeedLayer()
        self.drawCentroidLayer()
        self.drawSeedExclusionZoneLayer()
        self.drawMarginExclusionZoneLayer()

        self.drawBadEdgeLayer()
        self.drawTooCloseSeedsLayer()
        self.drawInscribedCirclesLayer()

        self.drawTileId()

        self.drawAnnotationsLayer()
        self.drawEdgeAnnotationsLayer()

        self.drawRiverLayer()
        self.drawCliffLayer()
        
        self.drawOverlayLayer()

        self.drawRegionIdLayer()

        stroke = Style("none", self.getStrokeColor(), STROKE_WIDTH)
        border_layer = self.drawHexTileBorder("border", "Border", stroke)
        if self.options['bleed']:
            border_layer.hide()
        
        self.drawHexTilePuzzleBorder()

        self.drawRegistrationMarksLayer()
        
        self.writeSvgOutput()

    def addInnerGlowFilter(self, name, blur, rgb):
        filter = Filter(name, 0.41051782, 0.41554717, 0.16543989, 0.17009096)
        filter.add_op("feFlood", {'flood-opacity':"1", 'flood-color':rgb, 'result':"flood"})
        filter.add_op("feComposite", {'in':"flood", 'in2':"SourceGraphic", 'operator':"out", 'result':"composite1"})
        filter.add_op("feGaussianBlur", {'in':"composite1", 'stdDeviation':blur, 'result':"blur"})
        filter.add_op("feOffset", {'dx':"0", 'dy':"0", 'result':"offset"})
        filter.add_op("feComposite", {'in':"offset", 'in2':"SourceGraphic", 'operator':"atop", 'result':"composite2"})
        self.svg.add_filter(filter)

    def analyzeSpecialRidges(self):
        # Scan the tile edges to determine if a river is required.
        # Build a list of tile edges that have a river exit: |riverEdges|.
        self.riverEdges = []
        self.cliffEdges = []
        seedIdCorner = 0
        seedIdEdge = 6
        for e in self.edgeTypes:
            eInfo = self.edgeRegionInfo[e]
            numEdgeRegions = len(eInfo) - 2  # Ignore first/last since those are corners.
            
            if e in EDGE_RIVER_INFO:
                rInfo = EDGE_RIVER_INFO[e]
                edge = self._findSpecialEdge(rInfo, seedIdCorner, seedIdEdge, numEdgeRegions)
                self.riverEdges.append(edge)
            if e in EDGE_CLIFF_INFO:
                rInfo = EDGE_CLIFF_INFO[e]
                edge = self._findSpecialEdge(rInfo, seedIdCorner, seedIdEdge, numEdgeRegions)
                self.cliffEdges.append(edge)

            seedIdCorner += 1
            seedIdEdge += numEdgeRegions

        if len(self.riverEdges) != 0 and self.riverData:
            # Build a clean list of ridge segments that should be rivers and extract
            # river ends.
            rRidges = []
            rRidgeEnds = []
            for r in self.riverData:
                if not r:
                    continue
                if r[-1] == '*':
                    rRidges.append(r[:-1])
                    rRidgeEnds.append(r[:-1])
                else:
                    rRidges.append(r)

            lakes = []
            if self.overlayData and "lake" in self.overlayData:
                lakes = [int(lake) for lake in self.overlayData['lake'] if lake]
            
            rb = RiverBuilder(self.riverEdges, rRidges, rRidgeEnds, lakes, RIVER_WIDTH)
            rb.setTileInfo(self.tile.sid2region)
            rb.buildRidgeInfo(self.vor)
            self.vertexOverrideRiver = rb.analyze()
            self.riverBuilder = rb

        if self.cliffData:
            # Build a clean list of ridge segments that should be cliffs and extract the
            # cliff ends.
            rRidges = []
            rRidgeEnds = []
            for r in self.cliffData:
                if not r:
                    continue
                if r[-1] == '*':
                    rRidges.append(r[:-1])
                    rRidgeEnds.append(r[:-1])
                else:
                    rRidges.append(r)

            if len(rRidges) != 0:
                cb = CliffBuilder(self.cliffEdges, rRidges, rRidgeEnds, CLIFF_WIDTH)
                cb.setTileInfo(self.tile.sid2region)
                cb.buildRidgeInfo(self.vor)
                self.vertexOverrideCliff = cb.analyze()
                self.cliffBuilder = cb

    def _findSpecialEdge(self, rInfo, seedIdCorner, seedIdEdge, numEdgeRegions):
        regions = [seedIdCorner]
        regions += list(range(seedIdEdge, seedIdEdge + numEdgeRegions))
        regions += [(seedIdCorner + 1) % 6]
        edgeIndex = rInfo.index('*')
        r0 = regions[edgeIndex - 1]
        r1 = regions[edgeIndex]
        return calcSortedId(r0, r1)
    
    def drawHexTileBorder(self, id, layer_name, style):
        layer_border = self.svg.add_inkscape_layer(id, layer_name, self.layer)
        if DRAW_PUZZLE_BORDER:
            p = self.calcPuzzleBorder()
        else:
            p = Path()
            p.addPoints(self.vHex)
            p.end()
        p.set_style(style)
        SVG.add_node(layer_border, p)
        return layer_border

    def drawClippedRegionLayer(self):
        layer_region_clip = self.svg.add_inkscape_layer(
            'region-clip', "Region Clipped", self.layer)
        if self.mirror:
            layer_region_clip.set_scale_transform(-1, 1)
        layer_region_clip.hide()

        gClip = SVG.group('clipped-regions')
        SVG.add_node(layer_region_clip, gClip)

        for sid in range(0, self.numActiveSeeds):
            vids = self.sid2clippedRegion[sid]
            id = f"clippedregion-{sid}"
            terrain_type = self.seed2terrain[sid]
            color = self.getTerrainFillColor(terrain_type)
            self.plotRegion(vids, color)
            self.drawUnmodifiedRegion(id, sid, vids, color, gClip)

    def drawRoundedRegionFillLayer(self):
        layer_region_rounded = self.svg.add_inkscape_layer(
            f"region-rounded-fill", f"Region Rounded Fill", self.layer)
        if self.mirror:
            layer_region_rounded.set_scale_transform(-1, 1)

        group_region_rounded = SVG.group('region-rounded-fill-group')
        SVG.add_node(layer_region_rounded, group_region_rounded)
        if DRAW_PUZZLE_BORDER or not self.options['bleed']:
            clippath_id = self.addHexTileClipPath()
            group_region_rounded.set("clip-path", f"url(#{clippath_id})")

        for sid in range(0, self.numActiveSeeds):
            terrainType = self.seed2terrain[sid]
            if self.options['texture-fill']:
                # Choose a random texture for this terrain.
                if not terrainType in TEXTURES:
                    continue
                texId = TEXTURES[terrainType][0]

                # Choose a random swatch from the texture.
                (swatchSize, numSwatches) = TEXTURE_INFO[texId]
                swatchId = self.rng.randint(numSwatches) + 1
                
                # Random texture rotation angle.
                angle = self.rng.randint(360)

                region = self.calcTexturedRegionNode(sid, terrainType, texId, swatchId, angle)
            else:
                id = f"roundedregionfill-{sid}"
                vids = self.sid2region[sid]
                region = self.calcRoundedRegionPath(id, sid, vids)

                color = self.getTerrainFillColor(terrainType)
                style = Style(color, None)
                region.set_style(style)

            SVG.add_node(group_region_rounded, region)

    def calcTexturedRegionNode(self, sid, terrainType, texId, swatchId, rotateAngle):
        if not terrainType in ['l', 'm', 'h']:
            raise Exception(f"Unexpected terrain type {terrainType}")
        
        id = f"rregion-{sid}"
        vids = self.sid2region[sid]
        path = self.calcRoundedRegionPath(id, sid, vids)
        texturedPathOps = {
            'pathClip': path,
            'textureType': terrainType,
            'textureId': texId,
            'textureSwatchId': swatchId,
            'textureRotateAngle': rotateAngle,
            'textureOffsetXY': self.vor.points[sid],
            'pathInnerGlow': terrainType.upper(),
        }
        return self.calcTexturedPathNode(id, texturedPathOps)

    # |ops| contains the options for the textured path:
    # Path options:
    #   pathClip - the path used for clipping the texture
    #   pathRotateAngle - rotation applied after clipping
    #   pathOffsetXY - the offset to apply after clipping
    #   pathInnerGlow - inner glow filter suffix to apply: H, M, L, R or C
    #      Filter name is "filterInnerGlow" + suffix
    # Texture options:
    #   textureType - texture type: h, m, l, r or c
    #   textureId - texture id: x##, where x is textureType and ## is 2-digit number
    #   textureSwatchId - the swatch id to use from the texture
    #   textureRotateAngle - texture rotation angle applied before clipping
    #   textureOffsetXY - texture offset applied before clipping
    def calcTexturedPathNode(self, id, ops):

        if not self.options['texture-fill']:
            raise Exception("Texture fill is disabled.")

        # Use groups to isolate the clip region from the image transforms/filters.
        # +-gGlow with inner glow filter
        # +-gTransPath - translate the clipped path
        # +-gRotateTex - rotate the clipped path
        # +-gClip - clip the texture
        # +-gTransTex - translate the texture to move it to the path
        # +-gRotateTex - rotate the texture
        # +-texture swatch
                
        # Add a new copy of the texture swatch.
        textureType = ops['textureType']
        texId = ops['textureId']
        swatchId = ops['textureSwatchId']
        textureName = f"{textureType}/{texId}/{texId}-{swatchId:02}.png"
        texPath = os.path.join(TEXTURES_DIR, textureName)
        (swatchSize, numSwatches) = TEXTURE_INFO[texId]
        s = swatchSize
        texture = Image(f"tex-{id}-{texId}-{swatchId:02}", texPath, -s/2, -s/2, s, s)
        texture.set_scale_transform(1, -1)
        childNode = texture

        # Rotate the texture.
        rotateAngle = ops.get('textureRotateAngle', None)
        if not rotateAngle is None:
            gRotateTex = Group(f"gRotateTex-{id}")
            gRotateTex.set_transform(f"rotate({rotateAngle})")
            SVG.add_node(gRotateTex, childNode)
            childNode = gRotateTex

        # Move the center of the texture sample to the specified point.
        offsetTexture = ops.get('textureOffsetXY', None)
        if not offsetTexture is None:
            gTransTex = Group(f"gTransTex-{id}")
            gTransTex.set_translate_transform(offsetTexture[0], offsetTexture[1])
            SVG.add_node(gTransTex, childNode)
            childNode = gTransTex

        # Clip the texture to the path.
        gClip = Group(f"gclip-{id}")
        clipid = self.svg.add_clip_path(id, ops['pathClip'])
        gClip.set("clip-path", f"url(#{clipid})")
        SVG.add_node(gClip, childNode)
        childNode = gClip

        # Rotate the clipped path.
        rotateAngle = ops.get('pathRotateAngle', None)
        if not rotateAngle is None:
            gRotatePath = Group(f"gRotatePath-{id}")
            gRotatePath.set_transform(f"rotate({rotateAngle})")
            SVG.add_node(gRotatePath, childNode)
            childNode = gRotatePath

        # Translate the clipped path.
        offsetPath = ops.get('pathOffsetXY', None)
        if not offsetPath is None:
            gTransPath = Group(f"gTransPath-{id}")
            gTransPath.set_translate_transform(offsetPath[0], offsetPath[1])
            SVG.add_node(gTransPath, childNode)
            childNode = gTransPath

        # Add inner glow to enhance border.
        glowType = ops.get('pathInnerGlow', None)
        if not glowType is None:
            gGlow = Group(f"gglow-{id}")
            gGlow.set_style(f"filter:url(#filterInnerGlow{glowType})")
            SVG.add_node(gGlow, childNode)
            childNode = gGlow
        
        return childNode

    def drawRoundedRegionStrokeLayer(self):
        layer_region_rounded = self.svg.add_inkscape_layer(
            f"region-rounded-stroke", f"Region Rounded Stroke", self.layer)
        if self.mirror:
            layer_region_rounded.set_scale_transform(-1, 1)

        group_region_rounded = SVG.group('region-rounded-stroke-group')
        SVG.add_node(layer_region_rounded, group_region_rounded)
        if DRAW_PUZZLE_BORDER or not self.options['bleed']:
            clippath_id = self.addHexTileClipPath()
            group_region_rounded.set("clip-path", f"url(#{clippath_id})")

        for sid in range(0, self.numActiveSeeds):
            vids = self.sid2region[sid]
            id = f"roundedregionstroke-{sid}"

            path = self.calcRoundedRegionPath(id, sid, vids)

            style = Style(None, self.getStrokeColor(), THICK_STROKE_WIDTH)
            path.set_style(style)
            SVG.add_node(group_region_rounded, path)

    def drawRegionLayer(self):
        layer_region = self.svg.add_inkscape_layer('region', "Region", self.layer)
        if self.mirror:
            layer_region.set_scale_transform(-1, 1)
        layer_region.hide()

        for sid in range(0, self.numActiveSeeds):
            rid = self.vor.point_region[sid]
            id = f"region-{sid}"
            self.drawRegion(id, sid, self.vor.regions[rid], self.getTerrainFillColor('_'), layer_region)

    def drawUnmodifiedRegionLayer(self):
        layer_region = self.svg.add_inkscape_layer('unmod-region', "Unmodified Region", self.layer)
        if self.mirror:
            layer_region.set_scale_transform(-1, 1)
        layer_region.hide()

        for sid in range(0, self.numActiveSeeds):
            rid = self.vor.point_region[sid]
            id = f"unmodregion-{sid}"
            self.drawUnmodifiedRegion(id, sid, self.vor.regions[rid], self.getTerrainFillColor('_'), layer_region)

    def drawSeedLayer(self):
        layer_seeds = self.svg.add_inkscape_layer('seeds', "Seeds", self.layer)
        if self.mirror:
            layer_seeds.set_scale_transform(-1, 1)
        layer_seeds.hide()

        black_fill = Style(fill=self.getStrokeColor())
        for sid in range(0, self.numActiveSeeds):
            center = self.seeds[sid]
            id = f"seed-{sid}"
            self._drawCircle(id, center, 1.0, black_fill, layer_seeds)

    def drawCentroidLayer(self):
        layer_centroids = self.svg.add_inkscape_layer('centroids', "Centroids", self.layer)
        if self.mirror:
            layer_centroids.set_scale_transform(-1, 1)
        layer_centroids.hide()

        black_fill = Style(fill="#008080")
        for sid in range(0, self.numActiveSeeds):
            center = self.tile.calcCentroid(sid)
            id = f"centroid-{sid}"
            self._drawCircle(id, center, 1.0, black_fill, layer_centroids)

    def drawSeedExclusionZoneLayer(self):
        layer_seed_ex = self.svg.add_inkscape_layer(
            'seed_exclusion', "Seed Exclusion", self.layer)
        if self.mirror:
            layer_seed_ex.set_scale_transform(-1, 1)
        layer_seed_ex.hide()

        fill = Style(fill="#800000")
        fill.set('fill-opacity', 0.15)

        for sid in range(0, self.numActiveSeeds):
            center = self.vor.points[sid]
            radius = self.tile.seed2minDistance[sid]
            id = f"seed-ex-{sid}"
            self._drawCircle(id, center, radius, fill, layer_seed_ex)

    def drawMarginExclusionZoneLayer(self):
        layer_margin_ex = self.svg.add_inkscape_layer(
            'margin_exclusion', "Margin Exclusion", self.layer)
        if self.mirror:
            layer_margin_ex.set_scale_transform(-1, 1)
        layer_margin_ex.hide()

        fill = Style(fill="#000080")
        fill.set('fill-opacity', 0.15)

        for mz in self.tile.edgeMarginZone:
            center, radius = mz
            self._drawCircle(None, center, radius, fill, layer_margin_ex)

    def drawBadEdgeLayer(self):
        if len(self.tile.badEdges) == 0:
            return
        
        layer_bad_edges = self.svg.add_inkscape_layer(
            'bad-edges', "Bad Edges", self.layer)
        if self.mirror:
            layer_bad_edges.set_scale_transform(-1, 1)

        for bei in self.tile.badEdges:
            badEdge = self.tile.badEdges[bei]
            vid0, vid1, rid = badEdge[0]
            self.drawBadVertex(self.vertices[vid0], layer_bad_edges)
            self.drawBadVertex(self.vertices[vid1], layer_bad_edges)

    def drawTooCloseSeedsLayer(self):
        if len(self.tile.tooClose) == 0:
            return

        layer_too_close = self.svg.add_inkscape_layer(
            'too-close', "Too Close Seeds", self.layer)
        if self.mirror:
            layer_too_close.set_scale_transform(-1, 1)

        for spair in self.tile.tooClose:
            s0, s1 = spair
            p = Path()
            p.setPoints([self.seeds[s] for s in [s0,s1]])
            p.set_style(Style(None, "#800000", "0.5px"))
            SVG.add_node(layer_too_close, p)
            
            self.drawBadVertex(self.seeds[s0], layer_too_close)
            self.drawBadVertex(self.seeds[s1], layer_too_close)
    
    def drawInscribedCirclesLayer(self):
        layer_circles = self.svg.add_inkscape_layer(
            'circles', "Inscribed Circles", self.layer)
        if self.mirror:
            layer_circles.set_scale_transform(-1, 1)
        layer_circles.hide()
        
        fill = Style(fill="#008000")
        fill.set('fill-opacity', 0.15)
        black_fill = Style(fill=self.getStrokeColor())

        for sid in self.tile.regionCircles:
            center, radius = self.tile.regionCircles[sid]
            id = f"incircle-{sid}"
            self._drawCircle(id, center, radius, fill, layer_circles)

            id = f"incircle-ctr-{sid}"
            self._drawCircle(id, center, '0.5', black_fill, layer_circles)
    
    def drawTileId(self):
        id = self.options['id']
        if id:
            layer_id = self.svg.add_inkscape_layer(
                'tile-id', "Tile Id", self.layer)
            layer_id.set_scale_transform(1, -1)

            g = SVG.group('tile-id-group')
            SVG.add_node(layer_id, g)
            
            pattern = self.options['pattern']
            patternInfo = self.tile.patternMirror[pattern]
            mirrorPattern = patternInfo[0]
            rotate = patternInfo[1]
            mirrorId = patternInfo[2]

            if self.mirror:
                # Rotate the id to the appropriate corner for the mirrored side.
                g.set_rotate_transform(-60 * rotate)
                if pattern != mirrorPattern:
                    id = mirrorId

            id_text = self.svg.add_loaded_element(g, 'tile-id')
            id_text.set('transform', f"translate(0 {-self.size+8})")
            SVG.set_text(id_text, f"{id:03d}")

    def drawAnnotationsLayer(self):
        self.layer_text = self.svg.add_inkscape_layer(
            'annotations', "Annotations", self.layer)
        self.layer_text.set_scale_transform(1, -1)

        # Reset number of annotation lines.
        self.numLines = 0
        
        if self.options['id']:
            id = self.options['id']
            self.numLines -= 1
            self._addAnnotationText(f"id: {id}")

        self._addAnnotationText(f"size: {self.size:g}")
        if self.options['seed']:
            self._addAnnotationText(f"rng seed {self.options['seed']}")
        else:
            self._addAnnotationText("rng seed RANDOM")

        pattern = self.options['pattern']
        self._addAnnotationText(f"pattern {pattern} (v{TILE_VERSION})")
        self._addAnnotationText(f"seed attempts: {self.tile.seedAttempts}")
        self._addAnnotationText(f"seed distance: "
                f"l {self.tile.minDistanceL:.03g}; "
                f"m {self.tile.minDistanceM:.03g}; "
                f"h {self.tile.minDistanceH:.03g}")

        center = "AVG"
        if self.options['center']:
            center = self.options['center']
        self._addAnnotationText(f"center: ({center}) {self.tile.centerWeight / self.size:.03g}")

        self._addAnnotationText(f"min ridge length: {int(100*self.tile.minRidgeLengthScale)}%; at edge: x{int(100*self.tile.minRidgeLengthEdgeScale)}%")
        self._addAnnotationText(f"edge margin exclusion zone scale: {self.tile.edgeMarginScale:.02g}")
        self._addAnnotationText(f"iterations: {self.tile.iteration-1}")
        self._addAnnotationText(f"adjustments: side {self.tile.adjustmentSide:.03g}, neighbor {self.tile.adjustmentNeighbor:.03g}")
        self._addAnnotationText(f"closeness: {self.tile.closeThreshold:.03g}, adjust {self.tile.adjustmentTooClose:.03g}")

        # Add 15mm circle (for mana size).
        self._drawCircle('mana', [50,110], '7.5',
                         Style(fill="#000000"), self.layer_text)
        SVG.add_node(self.layer_text, Text(None, 44, 122, "15mm"))
        
        # Add terrain swatches.
        y_start = 90
        for type in ['v', 'h', 'm', 'l', 'r']:
            color = self.getTerrainFillColor(type)
            r = SVG.rect(0, 75, y_start, 15, 6)
            r.set_style(Style(color, self.getStrokeColor(), STROKE_WIDTH))
            SVG.add_node(self.layer_text, r)

            label = Text(None, 70, y_start + 4.5, type.upper())
            SVG.add_node(self.layer_text, label)
            y_start += 10
      
    def _addAnnotationText(self, text):
        t = Text(None, -92, 90 + 5.5 * self.numLines, text)
        SVG.add_node(self.layer_text, t)
        self.numLines += 1
    
    def drawEdgeAnnotationsLayer(self):
        layer_edge_annotations = self.svg.add_inkscape_layer(
            'edge-annotations', "Edge Annotations", self.layer)
        if self.mirror:
            layer_edge_annotations.set_scale_transform(-1, -1)
        else:
            layer_edge_annotations.set_scale_transform(1, -1)
        if not self.options['show-seed-ids']:
            layer_edge_annotations.hide()

        # Add corner terrain labels.
        for i in range(0, self.tile.numSides):
            t = self.options['pattern'][i]
            label = Text(None, -1.5, -(self.size + 5), t.upper())
            if i != 0:
                label.set_transform(f"rotate({60 * i})")
            SVG.add_node(layer_edge_annotations, label)

        # Add edge terrain labels.
        for i in range(0, self.tile.numSides):
            g = Group(None)
            g.set_transform(f"rotate({30 + i * 60})")
            SVG.add_node(layer_edge_annotations, g)
            edgeType = self.tile.edgeTypes[i]
            seedPattern = self.edgeSeedInfo[edgeType]
            for j in range(0, len(seedPattern)):
                t, perp_t = seedPattern[j]
                x = lerp(-self.size/2, self.size/2, t)

                type = self.edgeRegionInfo[edgeType][j+1]
                label = Text(None, x - 1.5, -(self.xMax + 6), type.upper())
                SVG.add_node(g, label)

        # Add river info.
        for i in range(0, self.tile.numSides):
            edgeType = self.edgeTypes[i]
            if edgeType in EDGE_RIVER_INFO:
                g = Group(None)
                g.set_transform(f"rotate({30 + i * 60})")
                SVG.add_node(layer_edge_annotations, g)

                rIndex = EDGE_RIVER_INFO[edgeType].index('*')
                seedPattern = self.edgeSeedInfo[edgeType]
                x = self._calcEdgeFeatureOffset(rIndex, seedPattern)

                fillColor = self.getTerrainFillColor('r')
                r = SVG.rect(0, x-1.5, -self.xMax -8, 3, 8)
                r.set_style(Style(fillColor, self.getStrokeColor(), STROKE_WIDTH))
                SVG.add_node(g, r)

                label = Text(None, x - 1.5, -(self.xMax + 10), "R")
                SVG.add_node(g, label)

        # Add cliff info.
        for i in range(0, self.tile.numSides):
            edgeType = self.edgeTypes[i]
            if edgeType in EDGE_CLIFF_INFO:
                g = Group(None)
                g.set_transform(f"rotate({30 + i * 60})")
                SVG.add_node(layer_edge_annotations, g)

                rIndex = EDGE_CLIFF_INFO[edgeType].index('*')
                seedPattern = self.edgeSeedInfo[edgeType]
                x = self._calcEdgeFeatureOffset(rIndex, seedPattern)

                fillColor = self.getTerrainFillColor('c')
                r = SVG.rect(0, x-1.5, -self.xMax -8, 3, 8)
                r.set_style(Style(fillColor, self.getStrokeColor(), STROKE_WIDTH))
                SVG.add_node(g, r)

                label = Text(None, x - 1.5, -(self.xMax + 10), "X")
                SVG.add_node(g, label)

    def _calcEdgeFeatureOffset(self, rIndex, seedPattern):
        # EDGE_RIVER_INFO: [ 'l' '*' 'l' 'l' 'm' ]
        #    edgeSeedInfo:    -       x   x   -
        # For the seed info, the first/last are implicit: (0.0 1.0) and these's no
        # entry for the river.
        beforeIndex = rIndex - 2
        before = 0
        if beforeIndex != -1:
            before = seedPattern[rIndex-2][0]

        afterIndex = rIndex - 1
        after = 1
        if afterIndex < len(seedPattern):
            after = seedPattern[rIndex-1][0]

        # The edge feature is located between the 2 regions.
        t = (before + after) / 2
        return lerp(-self.size/2, self.size/2, t)
      
    def drawRiverLayer(self):
        if not self.riverBuilder:
            return

        layer_river = self.svg.add_inkscape_layer('river', "River", self.layer)
        if self.mirror:
            layer_river.set_scale_transform(-1, 1)

        group_river = SVG.group('river-group')
        SVG.add_node(layer_river, group_river)
        if DRAW_PUZZLE_BORDER or not self.options['bleed']:
            clippath_id = self.addHexTileClipPath()
            group_river.set("clip-path", f"url(#{clippath_id})")

        rivers = self.riverBuilder.getRidgeVertices()
        p = Path()
        for river in rivers:
            p.resetMove()
            numVerts = len(river)
            verts = []
            for i in range(numVerts):
                (sid, vid) = river[i]
                verts.append(self.getVertexForRegion(vid, sid))

            self.addRoundedVerticesToPath(p, verts)

        # Add lakes to path so they can share the same water texture.
        if self.overlayData and "lake" in self.overlayData:
            for lake_sid in self.overlayData['lake']:
                if not lake_sid:
                    continue

                self.addLakeToPath(p, int(lake_sid), self.riverBuilder.lakeVertices)
        
        p.end()
        pBorder = copy.deepcopy(p)

        if self.options['texture-fill']:
            texturedPathOps = {
                'pathClip': p,
                'textureType': "r",
                'textureId': "r01",
                'textureSwatchId': 1,
                'textureRotateAngle': 45,
                'pathInnerGlow': "R",
            }
            node = self.calcTexturedPathNode("texriver", texturedPathOps)
            SVG.add_node(group_river, node)
        else:
            style_river = Style(self.getTerrainFillColor('r'), None)
            style_river.set("stroke-linecap", "round")
            style_river.set("stroke-linejoin", "round")
            p.set_style(style_river)
            SVG.add_node(group_river, p)

        style_river_border = Style(None, self.getStrokeColor(), THICK_STROKE_WIDTH)
        style_river_border.set("stroke-linecap", "round")
        style_river_border.set("stroke-linejoin", "round")
        pBorder.set_style(style_river_border)
        SVG.add_node(group_river, pBorder)

    def drawCliffLayer(self):
        if not self.cliffBuilder:
            return

        layer_cliff = self.svg.add_inkscape_layer('cliff', "Cliff", self.layer)
        if self.mirror:
            layer_cliff.set_scale_transform(-1, 1)

        group_cliff = SVG.group('cliff-group')
        SVG.add_node(layer_cliff, group_cliff)
        if DRAW_PUZZLE_BORDER or not self.options['bleed']:
            clippath_id = self.addHexTileClipPath()
            group_cliff.set("clip-path", f"url(#{clippath_id})")

        cliffs = self.cliffBuilder.getRidgeVertices()
        for cliff in cliffs:
            p = Path()
            numVerts = len(cliff)
            for i in range(numVerts):
                vInfo = cliff[i]
                (sid, vid) = vInfo
                v = self.getVertexForRegion(vid, sid)

                prev = (i + numVerts - 1) % numVerts
                next = (i + 1) % numVerts
                vPrevInfo = cliff[prev]
                vNextInfo = cliff[next]
                vPrev = self.getVertexForRegion(vPrevInfo[1], vPrevInfo[0])
                vNext = self.getVertexForRegion(vNextInfo[1], vNextInfo[0])

                # Cliffs end in a single point, so don't add curves at that point.
                # Detect this because we get 2 identical points in a row.
                if feq_pt(v, vPrev) or feq_pt(v, vNext):
                    p.addPoint(v)
                else:
                    # Add a small curve for this vertex.
                    self.addCurvePoints(p, vPrev, v, vNext)

            p.end(False)
            pBorder = copy.deepcopy(p)

            style_cliff = Style(self.getTerrainFillColor('c'), None)
            p.set_style(style_cliff)
            SVG.add_node(group_cliff, p)
            
            style_cliff_border = Style(None, self.getStrokeColor(), THICK_STROKE_WIDTH)
            style_cliff_border.set("stroke-linecap", "round")
            style_cliff_border.set("stroke-linejoin", "round")
            pBorder.set_style(style_cliff_border)
            SVG.add_node(group_cliff, pBorder)

        # Draw fill lines for the cliff.
        for cliffLoop in self.cliffBuilder.getRidgeSegmentLoops():
            ridgeInfo = []
            lastRidgeKey = None
            # Convert the loop into a single list of regions that bound the ridge.
            for seg in cliffLoop:
                (seeds, verts) = seg
                ridgeKey = calcSortedIdFromPair(seeds)
                if ridgeKey == lastRidgeKey:
                    break
                lastRidgeKey = ridgeKey
                ridgeInfo.append([seeds, verts])

            terrainOrder = ['l', 'm', 'h']
            p = Path()
            numSegments = len(ridgeInfo)
            for iSeg in range(numSegments):
                seg = ridgeInfo[iSeg]
                (seeds, verts) = seg
                v = []
                terrain = []
                for seedId in seeds:
                    terrain.append(self.seed2terrain[seedId])
                    for vertexId in verts:
                        v.append(self.getVertexForRegion(vertexId, seedId))
                line0 = [v[0], v[1]]
                line1 = [v[2], v[3]]
                # Force line0 to be the region with higher elevation.
                if (not terrain[0] in terrainOrder) or (not terrain[1] in terrainOrder):
                    raise Exception(f"Terrain not defined for seeds {seeds}")
                if terrainOrder.index(terrain[1]) > terrainOrder.index(terrain[0]):
                    line0, line1 = line1, line0
                if iSeg != 0:
                    self._drawCornerRidgeTooth(p, prevLine0, prevLine1, line0, line1)
                self._drawRidgeTeeth(p, line0, line1)
                prevLine0 = line0
                prevLine1 = line1
            p.end()
            style_cliff_pattern = Style(self.getStrokeColor())
            p.set_style(style_cliff_pattern)
            SVG.add_node(group_cliff, p)

    def _drawCornerRidgeTooth(self, path, prev0, prev1, line0, line1):
        # Create tooth at the start point of line0/line1, using prev0/prev1 for reference.
        #                          +
        #                     0   /
        #                    e   /    
        #                   n   /    
        #                  i   /       +
        #                 l   /       /
        #                    +       /  1
        #   prev0       pt0 / |     /  e
        #  +-----------+---*   ,   /  n
        #               \      '  /  i
        #                 \    | /  l
        #                   \   +
        #  +-----------------+-*
        #   prev1               pt1
        #
        # Line at higher elevation (with wider part of tooth):
        #   prev0 - line0, connected by pt0
        # Line at lower elevation (with narrower part of tooth):
        #   prev1 - line1, connected by pt1
        # Rather than connect pt0 to pt1, we want a tooth-shaped connection so it is wider
        # at the top (the prev0/line0 side), and narrower at the bottom (prev1/side1).
        pt0 = line0[0]
        pt1 = line1[0]
        path.movePoint(pt0)
        path.addPoint(pt_along_line(pt0, line0[1], CLIFF_TOOTH_WIDTH))
        path.addPoint(pt_along_line(pt1, line1[1], CLIFF_TOOTH_POINT_WIDTH))
        path.addPoint(pt1)
        path.addPoint(pt_along_line(pt1, prev1[0], CLIFF_TOOTH_POINT_WIDTH))
        path.addPoint(pt_along_line(pt0, prev0[0], CLIFF_TOOTH_WIDTH))
    
    def _drawRidgeTeeth(self, path, lineA, lineB):
        lenA = dist(lineA[0], lineA[1])
        lenB = dist(lineB[0], lineB[1])
        minLength = min(lenA, lenB)
        numTeeth = int(minLength / CLIFF_TOOTH_SPACING)
        for i in range(numTeeth):
            self._drawRidgeTooth(path, lineA, lineB, (i+1) / (numTeeth+1))

    def _drawRidgeTooth(self, path, lineA, lineB, t):
        ptA = lerp_line(lineA, t)
        ptB = lerp_line(lineB, t)
        A = perp_offset([ptA, ptB], CLIFF_TOOTH_WIDTH)
        B = perp_offset([ptB, ptA], CLIFF_TOOTH_POINT_WIDTH)
        first = True
        for b in B:
            if first:
                path.moveXY(b[0], b[1])
            else:
                path.addXY(b[0], b[1])
            first = False
        for a in A:
            path.addXY(a[0], a[1])
    
    def drawOverlayLayer(self):
        self.layer_overlay = self.svg.add_inkscape_layer(
            'overlay', "Overlay", self.layer)
        if self.mirror:
            self.layer_overlay.set_scale_transform(-1, -1)
        else:
            self.layer_overlay.set_scale_transform(1, -1)

        if not self.overlayData:
            return

        if "bridge" in self.overlayData:
            for bridge in self.overlayData['bridge']:
                if bridge:
                    m = re.match(r"^(\d+\-\d+)(\((\d\d)\%\))?$", bridge)
                    # The position of the bridge on the ridge. By default this is on
                    # the midpoint, but it can be shifted over.
                    position = 0.50
                    if m:
                        seedIds = m.group(1)
                        if m.group(2):
                            position = float(m.group(3))/100.0
                    else:
                        raise Exception(f"Unrecognized bridge data: {bridge}")

                    # Place the  bridge at the midpoint of the ridge between the regions.
                    (startId, endId) = seedIds.split('-')
                    ptStart = self.seeds[int(startId)]
                    ptEnd = self.seeds[int(endId)]
                    rTheta = math.atan2(-(ptEnd[1] - ptStart[1]), ptEnd[0] - ptStart[0])
                    pathRotate = 90 + (rTheta * 180 / math.pi);
                    
                    edge_vertices = self.getEdgeRidgeVertices(startId, endId)
                    center = lerp(edge_vertices[0], edge_vertices[1], position)

                    x = center[0]
                    y = -center[1]
                    self.addMark(f"{startId}-{endId}", "bridge", x, y, pathRotate, 0, self.layer_overlay)

        if "tree" in self.overlayData:
            self.handleMarkData("tree", "t1")

        if "mark" in self.overlayData:
            self.handleMarkData("mark", "star")

    def handleMarkData(self, type, default):
        id = 0
        for mark in self.overlayData[type]:
            id += 1
            if mark:
                # <cell-id> '-' <mark-type> '(' <x-offset> <y-offset> ')'
                m = re.match(r"^(\d+)(\-([a-z0-9-]+))?(\(([\d.-]+ [\d.-]+)\))?$", mark)
                if m:
                    sid = m.group(1)
                    markType = None
                    if m.group(2):
                        markType = m.group(3)
                    offset = None
                    if m.group(4):
                        offset = m.group(5).split(' ')
                else:
                    raise Exception(f"Unrecognized {type} data: {mark}")

                if markType is None:
                    markType = default
                
                if type == "tree":
                    # Expand "t1" into "tree1".
                    m2 = re.match(r"t([1-4])", markType)
                    if not m2:
                        raise Exception(f"Invalid tree tyoe: {markType}")
                    markType = f"tree{m2.group(1)}"

                center = self.seeds[int(sid)]
                x = center[0]
                y = -center[1]
                if offset:
                    x += float(offset[0])
                    y -= float(offset[1])

                pathRotate = 0
                texRotate = self.rng.randint(360)
                self.addMark(f"{sid}-{id}", markType, x, y, pathRotate, texRotate, self.layer_overlay)

    def addMark(self, id, type, x, y, pathRotate, texRotate, parent):
        style = OVERLAY_MARK_STYLES[type]
        styleInfo = OVERLAY_MARK_STYLE_INFO[style]

        if self.mirror:
            fillColorId = styleInfo["mirror-fill"]
            fillColor = self.getTerrainFillColor(fillColorId)
            strokeColorId, strokeSize = styleInfo["mirror-stroke"]
            strokeColor = self.getTerrainFillColor(strokeColorId)
        else:
            if self.options['texture-fill']:
                icon = self.svg.get_loaded_path(f"obj-{type}")
                texId = styleInfo["tex-id"]
                texType = styleInfo["tex-type"]
                (swatchSize, numSwatches) = TEXTURE_INFO[texId]
                swatchId = self.rng.randint(numSwatches) + 1

                texturedPathOps = {
                    'pathClip': icon,
                    'pathRotateAngle': pathRotate,
                    'pathOffsetXY': [x,y],
                    'textureType': texType,
                    'textureId': texId,
                    'textureSwatchId': swatchId,
                    'textureRotateAngle': texRotate,
                }
                node = self.calcTexturedPathNode(f"{id}-{type}", texturedPathOps)
                SVG.add_node(parent, node)
            
                fillColor = None
            else:
                fillColorId = styleInfo["fill"]
                fillColor = self.getTerrainFillColor(fillColorId)
            strokeColorId, strokeSize = styleInfo["stroke"]
            strokeColor = self.getTerrainFillColor(strokeColorId)

        icon = self.svg.get_loaded_path(f"obj-{type}")
        style_icon_border = Style(fillColor, strokeColor, strokeSize)
        style_icon_border.set("stroke-linecap", "round")
        style_icon_border.set("stroke-linejoin", "round")
        icon.set_style(style_icon_border)

        # Move icon border to the correct location.
        gTrans = Group(f"gtransborder-{id}-{type}")
        transform = f"translate({x} {y}) rotate({pathRotate})"
        gTrans.set('transform', transform)
        SVG.add_node(gTrans, icon)

        SVG.add_node(parent, gTrans)

    # Given an edge defined by the 2 seeds, return the 2 ridge vertices of the edge.
    def getEdgeRidgeVertices(self, sid0, sid1):
        edgeToFind = calcSortedId(sid0, sid1)
        n_ridges = len(self.vor.ridge_points)
        for i in range(0, n_ridges):
            (s0, s1) = self.vor.ridge_points[i]
            key = calcSortedId(s0, s1)
            if key == edgeToFind:
                return [self.vertices[i] for i in self.vor.ridge_vertices[i]]
        return None

    def drawRegionIdLayer(self):
        layer_region_ids = self.svg.add_inkscape_layer(
            'region_ids', "Region Ids", self.layer)
        if self.mirror:
            layer_region_ids.set_scale_transform(-1, -1)
        else:
            layer_region_ids.set_scale_transform(1, -1)
        if not self.options['show-seed-ids']:
            layer_region_ids.hide()

        for sid in range(0, self.numActiveSeeds):
            center = self.seeds[sid]
            text = f"{sid}"
            t = Text(None, center[0]-1.4, -center[1], text)
            SVG.add_node(layer_region_ids, t)

    def drawHexTilePuzzleBorder(self):
        layer_puzzle = self.svg.add_inkscape_layer("puzzle", "Puzzle Border", self.layer)
        if self.mirror:
            layer_puzzle.set_scale_transform(-1, 1)
        if not self.options['bleed']:
            layer_puzzle.hide()

        p = self.calcPuzzleBorder()
        p.set_style(Style("none", self.getStrokeColor(), STROKE_WIDTH))
        SVG.add_node(layer_puzzle, p)
        
    def addPuzzleBorderClipPath(self):
        p = self.calcPuzzleBorder()
        return self.svg.add_clip_path(None, p)

    def calcPuzzleBorder(self):
        HOOK_SIZE = 0.005
        # Calculate seeds along hex edges
        vertices = []
        for i0 in range(0, NUM_SIDES):
            i1 = (i0 + 1) % NUM_SIDES
            edgeType = self.edgeTypes[i0]
            puzzlePattern = EDGE_PUZZLE_INFO[edgeType]

            startPt = self.vHex[i0]
            endPt = self.vHex[i1]
            vertices.append(startPt)
            for j in range(0, len(puzzlePattern)):
                t, tabWidth, tabHeight = puzzlePattern[j]
                vertices.append(lerp(startPt, endPt, t - tabWidth + HOOK_SIZE))
                vertices.append(lerperp(startPt, endPt, t - tabWidth -HOOK_SIZE, tabHeight))
                vertices.append(lerperp(startPt, endPt, t + tabWidth +HOOK_SIZE, tabHeight))
                vertices.append(lerp(startPt, endPt, t + tabWidth - HOOK_SIZE))

            # End point will be added by next tile edge.
            #vertices.append(endPt)

        p = Path()
        self.addRoundedVerticesToPath(p, vertices, 0.3)
        p.end()
        return p
    
    def drawRegistrationMarksLayer(self):
        layerRegMarks = self.svg.add_inkscape_layer("regmarks", "Registration Marks", self.layer)
        if not self.options['bleed']:
            layerRegMarks.hide()

        yMax = self.tile.size
        xMax = self.xMax
        blackFill = Style(fill="#000000")
        for offset in [1.3, 1.4, 1.5]:
            self._drawCircle(None, [xMax * offset, 0], 2.0, blackFill, layerRegMarks)
            self._drawCircle(None, [xMax * -offset, 0], 2.0, blackFill, layerRegMarks)
            self._drawCircle(None, [0, yMax * offset], 2.0, blackFill, layerRegMarks)
            self._drawCircle(None, [0, yMax * -offset], 2.0, blackFill, layerRegMarks)

    def _drawCircle(self, id, center, radius, fill, layer):
        circle = SVG.circle(id, center[0], center[1], radius)
        circle.set_style(fill)
        SVG.add_node(layer, circle)

    def writeSvgOutput(self):
        if not self.options['write_output']:
            return

        outdir_pngid = self.getPngIdOutputDir()
        name = self.tile.calcBaseFilename()
        if self.mirror:
            name += "r"

        outdir_svg = self.getSvgOutputDir()
        out_svg = os.path.join(outdir_svg, '%s.svg' % name)
        self.svg.write(out_svg)

        if self.options['export-pdf']:
            outdir_pdf = self.getPdfOutputDir()
            out_pdf = os.path.join(outdir_pdf, '%s.pdf' % name)
            Inkscape.export_pdf(
                os.path.abspath(out_svg),
                os.path.abspath(out_pdf))

        if self.options['export-png']:
            outdir_png = self.getPngOutputDir()
            out_png = os.path.join(outdir_png, f"{name}.png")

            actions = InkscapeActions()

            # Hide the "annotations" layer.
            actions.selectById("annotations")
            actions.selectionHide()

            # Export only the hex tile
            actions.exportId("border")

            actions.exportFilename(out_png)
            actions.exportDo()

            Inkscape.run_actions(
                os.path.abspath(out_svg),
                actions)

    def getPngOutputDir(self):
        out_dir = self.options['outdir_png']
        return self.makeDir(out_dir)

    def getPngIdOutputDir(self):
        out_dir = self.options['outdir_png_id']
        return self.makeDir(out_dir)

    def getSvgOutputDir(self):
        out_dir = self.options['outdir_svg']
        return self.makeDir(out_dir)

    def getPdfOutputDir(self):
        out_dir = self.options['outdir_pdf']
        return self.makeDir(out_dir)

    def makeDir(self, directory):
        if not os.path.isdir(directory):
            os.makedirs(directory);
        return directory

    def drawBadVertex(self, v, layer):
        circle = SVG.circle(0, v[0], v[1], '1')
        circle.set_style(Style(fill="#800000"))
        SVG.add_node(layer, circle)

    def getVertexForRegion(self, vid, sid):
        if vid in self.vertexOverrideRiver:
            overrides = self.vertexOverrideRiver[vid]
            if sid in overrides:
                return overrides[sid]
        if vid in self.vertexOverrideCliff:
            overrides = self.vertexOverrideCliff[vid]
            if sid in overrides:
                return overrides[sid]
        return self.vertices[vid]

    # Plot voronoi region given a list of vertex ids.
    def plotRegion(self, vids, color):
        if len(vids) == 0:
            return
        vertices = [self.vertices[i] for i in vids]
        plt.fill(*zip(*vertices), facecolor=color, edgecolor="black")

    # Draw voronoi region in the SVG file, given a list of vertex ids.
    def drawRegion(self, id, sid, vids, colorFill, layer):
        if len(vids) == 0:
            return
        vertices = [self.getVertexForRegion(i, sid) for i in vids]
        
        p = Path() if id == None else Path(id)
        p.addPoints(vertices)
        p.end()
        p.set_style(Style(colorFill, self.getStrokeColor(), STROKE_WIDTH))
        SVG.add_node(layer, p)

    # Draw voronoi region in the SVG file, given a list of vertex ids.
    def drawUnmodifiedRegion(self, id, sid, vids, color, layer):
        if len(vids) == 0:
            return
        vertices = [self.vertices[i] for i in vids]
        
        p = Path() if id == None else Path(id)
        p.addPoints(vertices)
        p.end()
        p.set_style(Style(color, self.getStrokeColor(), STROKE_WIDTH))
        SVG.add_node(layer, p)

    # Calc voronoi region path with rounded points, given a list of vertex ids.
    # Use |addToPath| to add this region to an existing path.
    def calcRoundedRegionPath(self, id, sid, vids):
        if len(vids) == 0:
            return
        
        p = Path() if id == None else Path(id)

        verts = [self.getVertexForRegion(vid, sid) for vid in vids]
        self.addRoundedVerticesToPath(p, verts)

        p.end()
        return p

    def addRoundedVerticesToPath(self, path, verts, curveOffset=0.5):
        # Build rounded path from the vertices.
        path.resetMove()
        nVerts = len(verts)
        for i in list(range(0, nVerts)):
            v = verts[i]
            iPrev = (i + nVerts - 1) % nVerts
            iNext = (i + 1) % nVerts
            
            # Add a small curve for this vertex.
            vPrev = verts[iPrev]
            vNext = verts[iNext]
            self.addCurvePoints(path, vPrev, v, vNext, curveOffset)

    # |curveOffset| dist from vertex to off-curve control point (in mm)
    def addCurvePoints(self, path, vPrev, v, vNext, curveOffset=0.5):
        #   vPrev *
        #          \
        #           \
        #            \
        #             \
        #      prev_pt +
        #               \
        #             c0 +
        #                 \    c1  next_pt
        #                  *----+----+-----------*
        #                v                      vNext
        #
        # * = actual vertices of the region: vPrev, v, vNext
        # + = calculated vertices of the curved corner:
        #     prev_pt, next_pt and the 2 off-curve control points: c0, c1
        # Note: The points for the curve are calculated using an absolute distance
        # from the current vertex along the line to the neighboring vertices.
        ptOffset = 3 * curveOffset  # (mm)

        prev_pt = pt_along_line(v, vPrev, ptOffset)
        path.addPoint(prev_pt)

        curve0_pt = pt_along_line(v, vPrev, curveOffset)
        curve1_pt = pt_along_line(v, vNext, curveOffset)
        next_pt = pt_along_line(v, vNext, ptOffset)
        path.addCurvePoint(curve0_pt, curve1_pt, next_pt)

    def addLakeToPath(self, path, lakeId, lakeVertices):
        vids = self.sid2region[lakeId]
        if len(vids) == 0:
            return

        # Pre-calc the list of vertices for this lake.
        # Find all the places where rivers meet the lake since we need to expand those
        # vertices into 2 separate vertices.        
        newVerts = []
        nVerts = len(vids)
        for i in list(range(0, nVerts)):
            iPrev = (i + nVerts - 1) % nVerts
            iNext = (i + 1) % nVerts

            vid = vids[i]
            vidPrev = vids[iPrev]
            vidNext = vids[iNext]
            
            # Get the current vertex from the POV of the neighbors. If they are not the
            # same, then that means a river is entering the lake at that point and we
            # need to add 2 vertices (for the left/right bank).
            # |sidPrev| is the sid of the neighbor that shares the previous vertex.
            # |sidNext| is the sid of the neighbor that shares the next vertex.
            sidPrev = self.findNeighborId(lakeId, vidPrev, vid)
            sidNext = self.findNeighborId(lakeId, vid, vidNext)
            v0 = self.getVertexForRegion(vid, sidPrev)
            v1 = self.getVertexForRegion(vid, sidNext)
            if not feq_pt(v0, v1):
                newVerts.append(v0)
                newVerts.append(v1)
            else:
                newVerts.append(v0)
        
        self.addRoundedVerticesToPath(path, newVerts)

    # Find the neighbor of |sid| with the shared ridge |vid0| to |vid1|.
    def findNeighborId(self, sid, vid0, vid1):
        rb = self.riverBuilder
        for sidNeighbor in rb.sid2neighbors[sid]:
            vids = self.sid2region[sidNeighbor]
            if vid0 in vids and vid1 in vids:
                return sidNeighbor
        raise Exception(f"Unable to find neighbor of {sid} with vertices {vid0} and {vid1}.")

    def addHexTileClipPath(self):
        if DRAW_PUZZLE_BORDER:
            return self.addPuzzleBorderClipPath()

        p = Path()
        p.addPoints(self.vHex)
        p.end()
        return self.svg.add_clip_path(None, p)

    #
    # 3D tile generation (for rendering in Blender)
    #
    
    def calcRegion3d(self, obj, sid):
        r = self.sid2clippedRegion[sid]
        nVertices = len(r)
        SCALE = 1
        heights = {
            '_': 10,
            'l': 10,
            'm': 15,
            'h': 20,
        }
        x0, y0 = self.options['origin']
        for vid in r:
            v = self.vertices[vid]
            obj.add3dVertex([x0 + v[0] * SCALE, y0 + v[1] * SCALE, 0])

            height = heights[self.seed2terrain[sid]]
            obj.add3dVertex([x0 + v[0] * SCALE, y0 + v[1] * SCALE, height * SCALE])
        obj.addFace([(2 * x) + 1 for x in range(0, nVertices)])
        obj.addFace(reversed([(2 * x) + 2 for x in range(0, nVertices)]))
        for f in range(0, nVertices-1):
            obj.addFace([(2 * f) + x for x in [1, 2, 4, 3]])
        obj.addFace([2, 1, 2*nVertices-1, 2*nVertices])
        obj.writeGroup(f"s{sid}")

    # Import generated obj file into Blender X-Forward, Z-Up
    def writeObject3d(self):
        obj = Object3d()

        out_dir = self.getObjOutputDir()
        name = self.tile.calcBaseFilename()
        outfile = os.path.join(out_dir, '%s.obj' % name)
        obj.open(outfile)
        
        self._writeObject3d(obj)

        if self.options['calc_neighbor_edges']:
            self.writeNeighborEdges(obj)

        obj.close()

    def calcNeighborOffset(self, colrow):
        col, row = colrow
        hexGap = 1.002  # Include a small gap between the hex tiles.
        dx = self.xMax * hexGap
        dy = 1.5 * self.size * hexGap

        # Odd rows are shifted over to the right:
        #    ,+,   ,+,   ,+,   ,+,   ,+,
        #  +'   `+'   `+'   `+'   `+'   `+
        #  |     |     | 0,2 | 1,2 | 2,2 |     = Row 2
        #  +,   ,+,   ,+,   ,+,   ,+,   ,+,
        #    `+'   `+'   `+'   `+'   `+'   `+
        #     |     |     | 0,1 | 1,1 | 2,1 |  = Row 1
        #    ,+,   ,+,   ,*,   ,+,   ,+,   ,+
        #  +'   `+'   `*'   `+'   `+'   `+
        #  |-2,0 |-1,0 | 0,0 | 1,0 | 2,0 |     = Row 0
        #  +,   ,+,   ,*,   ,*,   ,+,   ,+
        #    `+'   `+'   `*'   `+'   `+'   `+
        #     |     |     | 0,-1| 1,-1| 2,-1|  = Row -1
        #    ,+,   ,+,   ,+,   ,+,   ,+,   ,+
        #  +'   `+'   `+'   `+'   `+'   `+'
        #  |     |     | 0,-2| 1,-2| 2,-2|     = Row -2
        #  +,    +,   ,+,   ,+,   ,+,   ,+
        #    `+'   `+'   `+'   `+'   `+'
        #    -2    -1     0     1     2
        x0 = col * 2 * dx
        y0 = row * dy
        if row % 2 == 1:
            x0 += dx
        return [x0, y0]
        
    def writeNeighborEdges(self, obj):
        # Generate neighboring edges for 3d output.
        # 6 neighbors, going clockwise from top-right
        n_coord = [[0,1], [1,0], [0,-1], [-1,-1], [-1,0], [-1,1]]
        neighbors = [self.calcNeighborOffset(rc) for rc in n_coord]
        neighborEdge = [3, 4, 5, 0, 1, 2]
        seedOrig = self.options['seed']
        patternOrig = self.options['pattern']
        
        # The main tile (T0) needs a neighboring tile that matches each edge.
        #
        # The edges that extend out from each corner of the main tile (e.g., AG) must
        # match between adjacent neighbors (T1 and T6 in this case), or else the region in
        # that corner won't match along that edge.
        #
        #                _+_           _+_
        #            _,-'   `-,_ G _,-' M `-,_
        #          +'           `+'           `+
        #          |             |           N |
        #          |     T6      |     T1      |
        #        L |   (-1,1)    |    (0,1)    | H
        #         _+_           _+_           _+_
        #     _,-'   `-,_   _,-' A `-,_   _,-'   `-,_
        #   +'           `+'           `+'           `+
        #   |             | F         B |             |
        #   |     T5      |     T0      |     T2      |
        #   |   (-1,0)    | E  (0,0)  C |    (1,0)    |
        #   +,           ,+,           ,+,           ,+
        #     `-,_   _,-'   `-,_ D _,-'   `-,_   _,-'
        #         `+'           `+'           `+'
        #        K |             |             | I
        #          |     T4      |     T3      |
        #          |   (-1,-1)   |    (0,-1)   |
        #          +,           ,+,           ,+
        #            `-,_   _,-' J `-,_   _,-'
        #                `+'           `+'
        #
        # For neighboring tile T1, which needs to match AB in the main tile, we choose
        # G = M = A and H = N = B.
        # The value for G must be shared with T6, and H shared with T2.
        # The values for M and N aren't relevant, but they must be consistent with
        # G and H (for example, you can't have 'h' and 'l' corners next to each other).
        # So, for simplicity, we choose M and N to mirror the opposite edge since those
        # are guaranteed to be appropriate choices. Hence, M = A and N = B.
        for i in range(0, len(neighbors)):
            n = neighbors[i]
            options = self.options.copy()
            options['origin'] = n
            options['_neighbor_tile'] = True
            options['load'] = None
            options['write_output'] = False
            options['verbose_iteration'] = False
            # Only export the opposite edge on the neighboring tile.
            options['_export_3d_edge'] = (i + 3) % self.tile.numSides
            # Give each neighbor a different seed to ensure that there is no repetition.
            options['seed'] = seedOrig + (i+1)

            # Calculate edge pattern for this edge's neighboring tile.
            edgeStart = patternOrig[i]
            edgeEnd = patternOrig[(i+1) % self.tile.numSides]
            pattern = edgeStart + edgeEnd * 3 + edgeStart * 2
            if i != 0:
                pattern = pattern[-i:] + pattern[0:self.tile.numSides-i]
            options['pattern'] = pattern
            options['_allow_non_canonical_pattern'] = True

            edgeTile = VoronoiHexTile(options)
            edgeTile.init()
            edgeTile.generate()
            while edgeTile.update():
                edgeTile.generate()
            edgeTile.__writeObject3d(obj)

    def _writeObject3d(self, obj):
        sid = self.options['_export_3d_edge']
        if sid == None:
            for sid in range(0, self.numActiveSeeds):
                self.calcRegion3d(obj, sid)
            return

        # Export just the specified edge regions.
        # First corner.
        self.calcRegion3d(obj, sid)
        # Middle regions.
        firstSeed = sum(self.nSeedsPerEdge[:sid])
        nEdgeSeeds = self.nSeedsPerEdge[sid]
        for j in range(firstSeed, firstSeed + nEdgeSeeds):
            self.calcRegion3d(obj, self.tile.numSides + j)
        # End corner.
        self.calcRegion3d(obj, (sid+1) % self.tile.numSides)

