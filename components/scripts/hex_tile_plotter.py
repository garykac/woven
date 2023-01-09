import copy
import math
import matplotlib.pyplot as plt
import os
import re

from cliff_builder import CliffBuilder
from inkscape import Inkscape, InkscapeActions
from map_common import calcSortedId, calcSortedIdFromPair
from math_utils import (feq_pt, lerp, lerp_line, perp_offset, pt_along_line, dist)
from svg import SVG, Filter, Group, Image, Style, Node, Path, Text
from object3d import Object3d
from river_builder import RiverBuilder

from data_texture import TEXTURES, TEXTURE_INFO

TEXTURES_DIR = "../../../third_party/textures"

GENERATE_PLOT = True   # As PNG file.
PLOT_CELL_IDS = True   # Add cell ids to png output file.

# NOTE: Default units for SVG is mm.

STROKE_COLOR = "#000000"
STROKE_WIDTH = 0.3
THICK_STROKE_WIDTH = 1.0
ICON_STROKE_WIDTH = 0.7

RIVER_WIDTH = 2.8
CLIFF_WIDTH = 2.0

# Fill colors for regions based on terrain height.
REGION_COLOR = {
    '_': "#ffffff",  # blank
    'l': "#f0eaac",  #"#d9f3b9",  #'#efecc6',  # low
    'm': "#f0ce76",  #'#dcc382',  # medium
    'h': "#e7a311",  #'#d69200',  # high
    'r': "#a2c6ff",  # river/water
    'c': "#ffffff",  # cliff
    'v': "#be850a",  # very high mountain
}

# Mark where rivers are located on edges using an '*' to note the regions that
# the river flows between.
EDGE_RIVER_INFO = {
    '2f': ['l', '*', 'l', 'l', 'm'],           # l - m, m - h
    '2s': ['m', 'm', '*', 'm', 'm'],           # m - m
}

# Mark where cliffs are located on edges using an '*' to note the regions that
# are separated by a cliff.
EDGE_CLIFF_INFO = {
    '3f': ['m', 'm', '*', 'h', 'm', 'h'],      # m - h, h - m
}

# Textures to use for each type of mark (for the overlay).
OVERLAY_MARK_TEXTURES = {
    "bridge": "g01",
    "star": "s01",
    "tower": "g01",
    "tree1": "t01",
    "tree2": "t01",
    "tree3": "t01",
    "tree4": "t01",
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
                
        # Reset number of annotation lines.
        self.numLines = 0

        # Calculate data for reversed edges ('r') from the forward ('f') edges.
        for type in self.tile.singleEdgeTypes:
            if type[-1] == 'f':
                newType = type[:-1] + 'r'
                if type in EDGE_RIVER_INFO:
                    EDGE_RIVER_INFO[newType] = EDGE_RIVER_INFO[type][::-1]
                if type in EDGE_CLIFF_INFO:
                    EDGE_CLIFF_INFO[newType] = EDGE_CLIFF_INFO[type][::-1]

    def getTerrainStyle(self, type):
        if self.options['bw']:
            return REGION_COLOR['_']
        return REGION_COLOR[type]

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
            color = self.getTerrainStyle(terrain_type)
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
        self.svg = SVG([215.9, 279.4])  #SVG([210, 297])
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
        self.addInnerGlowFilter("filterInnerGlowC", 2.0, "rgb(200,200,200)")

        layer = self.svg.add_inkscape_layer('layer', "Layer")
        layer.set_transform("translate(107.95 120) scale(1, -1)")
        self.layer = layer

        stroke = Style("none", "#000000", STROKE_WIDTH)
        black_fill = Style(fill="#000000")

        self.analyzeSpecialRidges()

        # Draw layers back to front.
        
        self.drawHexTileBorder("background", "Tile Background", black_fill)

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

        self.drawTerrainLabelsLayer()

        self.drawRiverLayer()
        self.drawCliffLayer()
        
        self.drawOverlayLayer()

        self.drawRegionIdLayer()

        self.drawHexTileBorder("border", "Border", stroke)
        
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
        p = Path()
        p.addPoints(self.vHex)
        p.end()
        p.set_style(style)
        SVG.add_node(layer_border, p)

    def drawClippedRegionLayer(self):
        layer_region_clip = self.svg.add_inkscape_layer(
            'region-clip', "Region Clipped", self.layer)
        gClip = SVG.group('clipped-regions')
        SVG.add_node(layer_region_clip, gClip)
        layer_region_clip.hide()

        for sid in range(0, self.numActiveSeeds):
            vids = self.sid2clippedRegion[sid]
            id = f"clippedregion-{sid}"
            terrain_type = self.seed2terrain[sid]
            color = self.getTerrainStyle(terrain_type)
            self.plotRegion(vids, color)
            self.drawUnmodifiedRegion(id, sid, vids, color, gClip)

    def drawRoundedRegionFillLayer(self):
        layer_region_rounded = self.svg.add_inkscape_layer(
            f"region-rounded-fill", f"Region Rounded Fill", self.layer)
        group_region_rounded = SVG.group('region-rounded-fill-group')
        SVG.add_node(layer_region_rounded, group_region_rounded)
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

                color = self.getTerrainStyle(terrainType)
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
        group_region_rounded = SVG.group('region-rounded-stroke-group')
        SVG.add_node(layer_region_rounded, group_region_rounded)
        clippath_id = self.addHexTileClipPath()
        group_region_rounded.set("clip-path", f"url(#{clippath_id})")

        for sid in range(0, self.numActiveSeeds):
            vids = self.sid2region[sid]
            id = f"roundedregionstroke-{sid}"

            path = self.calcRoundedRegionPath(id, sid, vids)

            style = Style(None, STROKE_COLOR, THICK_STROKE_WIDTH)
            path.set_style(style)
            SVG.add_node(group_region_rounded, path)

    def drawRegionLayer(self):
        layer_region = self.svg.add_inkscape_layer('region', "Region", self.layer)
        layer_region.hide()

        for sid in range(0, self.numActiveSeeds):
            rid = self.vor.point_region[sid]
            id = f"region-{sid}"
            self.drawRegion(id, sid, self.vor.regions[rid], "#ffffff", layer_region)

    def drawUnmodifiedRegionLayer(self):
        layer_region = self.svg.add_inkscape_layer('unmod-region', "Unmodified Region", self.layer)
        layer_region.hide()

        for sid in range(0, self.numActiveSeeds):
            rid = self.vor.point_region[sid]
            id = f"unmodregion-{sid}"
            self.drawUnmodifiedRegion(id, sid, self.vor.regions[rid], "#ffffff", layer_region)

    def drawSeedLayer(self):
        layer_seeds = self.svg.add_inkscape_layer('seeds', "Seeds", self.layer)
        layer_seeds.hide()

        black_fill = Style(fill="#000000")
        for sid in range(0, self.numActiveSeeds):
            center = self.seeds[sid]
            id = f"seed-{sid}"
            self._drawCircle(id, center, 1.0, black_fill, layer_seeds)

    def drawCentroidLayer(self):
        layer_centroids = self.svg.add_inkscape_layer('centroids', "Centroids", self.layer)
        layer_centroids.hide()

        black_fill = Style(fill="#008080")
        for sid in range(0, self.numActiveSeeds):
            center = self.tile.calcCentroid(sid)
            id = f"centroid-{sid}"
            self._drawCircle(id, center, 1.0, black_fill, layer_centroids)

    def drawSeedExclusionZoneLayer(self):
        layer_seed_ex = self.svg.add_inkscape_layer(
            'seed_exclusion', "Seed Exclusion", self.layer)
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
        layer_margin_ex.hide()

        fill = Style(fill="#000080")
        fill.set('fill-opacity', 0.15)

        for mz in self.tile.edgeMarginZone:
            center, radius = mz
            self._drawCircle(0, center, radius, fill, layer_margin_ex)

    def drawBadEdgeLayer(self):
        if len(self.tile.badEdges) == 0:
            return
        
        layer_bad_edges = self.svg.add_inkscape_layer(
            'bad-edges', "Bad Edges", self.layer)
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
        layer_circles.hide()
        
        fill = Style(fill="#008000")
        fill.set('fill-opacity', 0.15)
        black_fill = Style(fill="#000000")

        for sid in self.tile.regionCircles:
            center, radius = self.tile.regionCircles[sid]
            id = f"incircle-{sid}"
            self._drawCircle(id, center, radius, fill, layer_circles)

            id = f"incircle-ctr-{sid}"
            self._drawCircle(id, center, '0.5', black_fill, layer_circles)
    
    def drawTileId(self):
        id = self.options['id']
        if id:
            self.layer_text = self.svg.add_inkscape_layer(
                'tile-id', "Tile Id", self.layer)
            self.layer_text.set_transform("scale(1,-1)")

            id_text = self.svg.add_loaded_element(self.layer_text, 'tile-id')
            id_text.set('transform', f"translate(0 {-self.size+8})")
            SVG.set_text(id_text, f"{id:03d}")

    def drawAnnotationsLayer(self):
        self.layer_text = self.svg.add_inkscape_layer(
            'annotations', "Annotations", self.layer)
        self.layer_text.set_transform("scale(1,-1)")

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
        self._addAnnotationText(f"pattern {pattern}")
        self._addAnnotationText(f"seed attempts: {self.tile.seedAttempts}")
        self._addAnnotationText(f"seed distance: "
                f"l {self.tile.minDistanceL:.03g}; "
                f"m {self.tile.minDistanceM:.03g}; "
                f"h {self.tile.minDistanceH:.03g}")

        center = "AVG"
        if self.options['center']:
            center = self.options['center']
        self._addAnnotationText(f"center: ({center}) {self.tile.centerWeight / self.size:.03g}")

        self._addAnnotationText(f"min ridge length: {self.tile.minRidgeLength:.02g}; at edge: {self.tile.minRidgeLengthEdge:.02g}")
        self._addAnnotationText(f"edge margin exclusion zone scale: {self.tile.edgeMarginScale:.02g}")
        self._addAnnotationText(f"iterations: {self.tile.iteration-1}")
        self._addAnnotationText(f"adjustments: side {self.tile.adjustmentSide:.03g}, neighbor {self.tile.adjustmentNeighbor:.03g}")
        self._addAnnotationText(f"closeness: {self.tile.closeThreshold:.03g}, adjust {self.tile.adjustmentTooClose:.03g}")

    def _addAnnotationText(self, text):
        t = Text(None, -92, 90 + 5.5 * self.numLines, text)
        SVG.add_node(self.layer_text, t)
        self.numLines += 1
    
    def drawTerrainLabelsLayer(self):
        # Add corner terrain labels.
        for i in range(0, self.tile.numSides):
            t = self.options['pattern'][i]
            label = Text(None, -1.5, -(self.size + 2), t.upper())
            if i != 0:
                label.set_transform(f"rotate({60 * i})")
            SVG.add_node(self.layer_text, label)

        # Add edge terrain labels.
        for i in range(0, self.tile.numSides):
            g = Group(None)
            g.set_transform(f"rotate({30 + i * 60})")
            SVG.add_node(self.layer_text, g)
            edgeType = self.tile.edgeTypes[i]
            seedPattern = self.edgeSeedInfo[edgeType]
            for j in range(0, len(seedPattern)):
                t, perp_t = seedPattern[j]
                x = lerp(-self.size/2, self.size/2, t)

                type = self.edgeRegionInfo[edgeType][j+1]
                label = Text(None, x - 1.5, -(self.xMax + 3), type.upper())
                SVG.add_node(g, label)

        # Add river info.
        for i in range(0, self.tile.numSides):
            edgeType = self.edgeTypes[i]
            if edgeType in EDGE_RIVER_INFO:
                g = Group(None)
                g.set_transform(f"rotate({30 + i * 60})")
                SVG.add_node(self.layer_text, g)

                rIndex = EDGE_RIVER_INFO[edgeType].index('*')
                seedPattern = self.edgeSeedInfo[edgeType]
                x = self._calcEdgeFeatureOffset(rIndex, seedPattern)

                color = self.getTerrainStyle('r')
                r = SVG.rect(0, x-1.5, -self.xMax -8, 3, 8)
                r.set_style(Style(color, STROKE_COLOR, STROKE_WIDTH))
                SVG.add_node(g, r)

                label = Text(None, x - 1.5, -(self.xMax + 10), "R")
                SVG.add_node(g, label)

        # Add cliff info.
        for i in range(0, self.tile.numSides):
            edgeType = self.edgeTypes[i]
            if edgeType in EDGE_CLIFF_INFO:
                g = Group(None)
                g.set_transform(f"rotate({30 + i * 60})")
                SVG.add_node(self.layer_text, g)

                rIndex = EDGE_CLIFF_INFO[edgeType].index('*')
                seedPattern = self.edgeSeedInfo[edgeType]
                x = self._calcEdgeFeatureOffset(rIndex, seedPattern)

                color = self.getTerrainStyle('c')
                r = SVG.rect(0, x-1.5, -self.xMax -8, 3, 8)
                r.set_style(Style(color, STROKE_COLOR, STROKE_WIDTH))
                SVG.add_node(g, r)

                label = Text(None, x - 1.5, -(self.xMax + 10), "X")
                SVG.add_node(g, label)

        # Add 15mm circle (for mana size).
        self._drawCircle('mana', [50,110], '7.5',
                         Style(fill="#000000"), self.layer_text)
        
        # Add terrain swatches.
        y_start = 90
        for type in ['v', 'h', 'm', 'l', 'r']:
            color = self.getTerrainStyle(type)
            r = SVG.rect(0, 75, y_start, 15, 6)
            r.set_style(Style(color, STROKE_COLOR, STROKE_WIDTH))
            SVG.add_node(self.layer_text, r)

            label = Text(None, 70, y_start + 4.5, type.upper())
            SVG.add_node(self.layer_text, label)
            y_start += 10
      
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
        group_river = SVG.group('river-group')
        SVG.add_node(layer_river, group_river)
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
                'textureId': "r02",
                'textureSwatchId': 1,
                'textureRotateAngle': 45,
                'pathInnerGlow': "R",
            }
            node = self.calcTexturedPathNode("texriver", texturedPathOps)
            SVG.add_node(group_river, node)
        else:
            style_river = Style(REGION_COLOR['r'], None)
            style_river.set("stroke-linecap", "round")
            style_river.set("stroke-linejoin", "round")
            p.set_style(style_river)
            SVG.add_node(group_river, p)

        style_river_border = Style(None, STROKE_COLOR, THICK_STROKE_WIDTH)
        style_river_border.set("stroke-linecap", "round")
        style_river_border.set("stroke-linejoin", "round")
        pBorder.set_style(style_river_border)
        SVG.add_node(group_river, pBorder)

    def drawCliffLayer(self):
        if not self.cliffBuilder:
            return

        layer_cliff = self.svg.add_inkscape_layer('cliff', "Cliff", self.layer)
        group_cliff = SVG.group('cliff-group')
        SVG.add_node(layer_cliff, group_cliff)
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

            style_cliff = Style(REGION_COLOR['c'], None)
            style_cliff.set("filter", "url(#filterInnerGlowC)")
            p.set_style(style_cliff)
            SVG.add_node(group_cliff, p)
            
            style_cliff_border = Style(None, STROKE_COLOR, THICK_STROKE_WIDTH)
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
                self._drawRidgeTeeth(p, line0, line1, iSeg == 0, iSeg == numSegments - 1)
            p.end()
            style_cliff_pattern = Style(STROKE_COLOR)
            p.set_style(style_cliff_pattern)
            SVG.add_node(group_cliff, p)

    def _drawRidgeTeeth(self, path, lineA, lineB, firstSegment, lastSegment):
        TOOTH_SPACING = 2.2  # (mm)
        lenA = dist(lineA[0], lineA[1])
        lenB = dist(lineB[0], lineB[1])
        minLength = min(lenA, lenB)
        if not firstSegment:
            self._drawRidgeTooth(path, lineA, lineB, 0)
        numTeeth = int(minLength / TOOTH_SPACING)
        for i in range(numTeeth):
            self._drawRidgeTooth(path, lineA, lineB, (i+1) / (numTeeth+1))
        if not lastSegment:
            self._drawRidgeTooth(path, lineA, lineB, 1)

    def _drawRidgeTooth(self, path, lineA, lineB, t):
        TOOTH_WIDTH = 0.8   # (mm)
        TOOTH_POINT_WIDTH = 0.05  # (mm)
        ptA = lerp_line(lineA, t)
        ptB = lerp_line(lineB, t)
        A = perp_offset([ptA, ptB], TOOTH_WIDTH)
        B = perp_offset([ptB, ptA], TOOTH_POINT_WIDTH)
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
        self.layer_overlay.set_scale_transform(1, -1)

        if not self.overlayData:
            return

        if "bridge" in self.overlayData:
            for bridge in self.overlayData['bridge']:
                if bridge:
                    m = re.match(r"^(\d+\-\d+)$", bridge)
                    if m:
                        seedIds = m.group(1)
                    else:
                        raise Exception(f"Unrecognized bridge data: {bridge}")

                    # Place the  bridge at the midpoint of the ridge between the regions.
                    (startId, endId) = seedIds.split('-')
                    ptStart = self.seeds[int(startId)]
                    ptEnd = self.seeds[int(endId)]
                    rTheta = math.atan2(-(ptEnd[1] - ptStart[1]), ptEnd[0] - ptStart[0])
                    degTheta = 90 + (rTheta * 180 / math.pi);
                    edge_vertices = self.getEdgeRidgeVertices(startId, endId)
                    center = lerp(edge_vertices[0], edge_vertices[1], 0.5)

                    if self.options['texture-fill']:
                        type = 'bridge'
                        sidPair = f"{startId}-{endId}"
                        texId = OVERLAY_MARK_TEXTURES[type]
                        texType = texId[0]
                        (swatchSize, numSwatches) = TEXTURE_INFO[texId]
                        swatchId = self.rng.randint(numSwatches) + 1
                        icon = self.svg.get_loaded_path(f"obj-{type}")

                        texturedPathOps = {
                            'pathClip': icon,
                            'pathRotateAngle': degTheta,
                            'pathOffsetXY': [center[0], -center[1]],
                            'textureType': texType,
                            'textureId': texId,
                            'textureSwatchId': swatchId,
                        }
                        node = self.calcTexturedPathNode(f"{sidPair}-{type}", texturedPathOps)
                        SVG.add_node(self.layer_overlay, node)

                        icon = self.svg.get_loaded_path(f"obj-{type}")
                        style_icon_border = Style(None, STROKE_COLOR, ICON_STROKE_WIDTH)
                        style_icon_border.set("stroke-linecap", "round")
                        style_icon_border.set("stroke-linejoin", "round")
                        icon.set_style(style_icon_border)

                        # Move icon border to the correct location.
                        gTrans = Group(f"gtransborder-{sidPair}-{type}")
                        transform = f"translate({center[0]} {-center[1]}) rotate({degTheta})"
                        gTrans.set('transform', transform)
                        SVG.add_node(gTrans, icon)

                        SVG.add_node(self.layer_overlay, gTrans)
                    else:
                        icon = self.svg.add_loaded_element(self.layer_overlay, 'obj-bridge')
                        transform = f"translate({center[0]} {-center[1]}) rotate({degTheta})"
                        icon.set('transform', transform)

        if "mark" in self.overlayData:
            id = 0
            for mark in self.overlayData['mark']:
                id += 1
                if mark:
                    # <type> '-' <cell-id> '(' <x-offset> <y-offset> ')'
                    m = re.match(r"^([a-z0-9-]+)\-(\d+)(\(([\d.-]+ [\d.-]+)\))?$", mark)
                    if m:
                        type = m.group(1)
                        sid = m.group(2)
                        offset = None
                        if m.group(3):
                            offset = m.group(4).split(' ')
                    else:
                        raise Exception(f"Unrecognized mark data: {mark}")

                    center = self.seeds[int(sid)]
                    x = center[0]
                    y = -center[1]
                    if offset:
                        x += float(offset[0])
                        y -= float(offset[1])

                    if self.options['texture-fill']:
                        icon = self.svg.get_loaded_path(f"obj-{type}")

                        texId = OVERLAY_MARK_TEXTURES[type]
                        texType = texId[0]
                        (swatchSize, numSwatches) = TEXTURE_INFO[texId]
                        swatchId = self.rng.randint(numSwatches) + 1
                        rotateAngle = self.rng.randint(360)

                        texturedPathOps = {
                            'pathClip': icon,
                            'pathOffsetXY': [x,y],
                            'textureType': texType,
                            'textureId': texId,
                            'textureSwatchId': swatchId,
                            'textureRotateAngle': rotateAngle,
                        }
                        node = self.calcTexturedPathNode(f"{sid}-{type}-{id}", texturedPathOps)
                        SVG.add_node(self.layer_overlay, node)
        
                        icon = self.svg.get_loaded_path(f"obj-{type}")
                        style_icon_border = Style(None, STROKE_COLOR, ICON_STROKE_WIDTH)
                        style_icon_border.set("stroke-linecap", "round")
                        style_icon_border.set("stroke-linejoin", "round")
                        icon.set_style(style_icon_border)

                        # Move icon border to the correct location.
                        gTrans = Group(f"gtransborder-{sid}-{type}-{id}")
                        gTrans.set_translate_transform(x, y)
                        SVG.add_node(gTrans, icon)

                        SVG.add_node(self.layer_overlay, gTrans)
                    else:
                        icon = self.svg.add_loaded_element(self.layer_overlay, f"obj-{type}")
                        icon.set('transform', f"translate({x} {y})")

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
        if not self.options['show-seed-ids']:
            layer_region_ids.hide()
        layer_region_ids.set_transform("scale(1,-1)")
        for sid in range(0, self.numActiveSeeds):
            center = self.seeds[sid]
            text = f"{sid}"
            t = Text(None, center[0]-1.4, -center[1], text)
            SVG.add_node(layer_region_ids, t)

    def _drawCircle(self, id, center, radius, fill, layer):
        circle = SVG.circle(id, center[0], center[1], radius)
        circle.set_style(fill)
        SVG.add_node(layer, circle)

    def writeSvgOutput(self):
        if not self.options['write_output']:
            return

        outdir_pngid = self.getPngIdOutputDir()
        name = self.tile.calcBaseFilename()

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
    def drawRegion(self, id, sid, vids, color, layer):
        if len(vids) == 0:
            return
        vertices = [self.getVertexForRegion(i, sid) for i in vids]
        
        p = Path() if id == None else Path(id)
        p.addPoints(vertices)
        p.end()
        p.set_style(Style(color, STROKE_COLOR, STROKE_WIDTH))
        SVG.add_node(layer, p)

    # Draw voronoi region in the SVG file, given a list of vertex ids.
    def drawUnmodifiedRegion(self, id, sid, vids, color, layer):
        if len(vids) == 0:
            return
        vertices = [self.vertices[i] for i in vids]
        
        p = Path() if id == None else Path(id)
        p.addPoints(vertices)
        p.end()
        p.set_style(Style(color, STROKE_COLOR, STROKE_WIDTH))
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

    def addRoundedVerticesToPath(self, path, verts):
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
            self.addCurvePoints(path, vPrev, v, vNext)

    # Find the neighbor of |sid| with the shared ridge |vid0| to |vid1|.
    def findNeighborId(self, sid, vid0, vid1):
        rb = self.riverBuilder
        for sidNeighbor in rb.sid2neighbors[sid]:
            vids = self.sid2region[sidNeighbor]
            if vid0 in vids and vid1 in vids:
                return sidNeighbor
        raise Exception(f"Unable to find neighbor of {sid} with vertices {vid0} and {vid1}.")

    def addCurvePoints(self, path, vPrev, v, vNext):
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
        PT_OFFSET = 1.5  # (mm)
        CURVE_PT_OFFSET = 0.5  # (mm)

        prev_pt = pt_along_line(v, vPrev, PT_OFFSET)
        path.addPoint(prev_pt)

        curve0_pt = pt_along_line(v, vPrev, CURVE_PT_OFFSET)
        curve1_pt = pt_along_line(v, vNext, CURVE_PT_OFFSET)
        next_pt = pt_along_line(v, vNext, PT_OFFSET)
        path.addCurvePoint(curve0_pt, curve1_pt, next_pt)

    def addHexTileClipPath(self):
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

