import copy
import glob
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import random  # Only used to seed numpy random, if needed
import re
import scipy.spatial
import subprocess

from inkscape import Inkscape
from math_utils import (feq, fge, fle, scale, clamp,
                        lerp, lerp_pt, lerp_pt_delta, lerperp,
                        pt_along_line,
                        near, dist, dist_pt_line, line_intersection_t,
                        ptInHex)
from object3d import Object3d
from river_builder import RiverBuilder
from svg import SVG, Group, Style, Node, Path, Text

GENERATE_SVG = True
GENERATE_PLOT = True   # As PNG file.
PLOT_CELL_IDS = True   # Add cell ids to png output file.

ENABLE_SMALL_REGION_CHECK = False

NUM_SIDES = 6

EDGE_TYPES = ['1s', '2f', '2s', '3f', '3s']

# EdgeRegionInfo:
# Each dict entry contains an array of region heights, one per region on this
# side.
# # = number of seeds between the corners
# 's' = self symmetric
# 'f' = forward edge, mirror pairs
# 'r' = reverse edge, auto-calculated from 'f' edge
EDGE_REGION_INFO = {
    '1s': ['l', 'l', 'l'],                     # l - l
    '2f': ['l', 'l', 'l', 'm'],                # l - m, m - h
    '2s': ['m', 'm', 'm', 'm'],                # m - m
    '3f': ['m', 'm', 'h', 'm', 'h'],           # m - h, h - m
    '3s': ['h', 'h', 'm', 'h', 'h'],           # h - h
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
    '3f': ['m', 'm', 'h', '*', 'm', 'h'],      # m - h, h - m
}

# Edge seed info.
# Each dict entry contains an array of seed positions along the edge.
# There are implicit seeds at the 2 ends of the edge.
# Each seed position is:
#   [ offset-along-edge, perpendicular-offset ]
EDGE_SEED_INFO = {
    '1s': [[0.50, 0]],
    '2f': [[0.33, 0.04],  [0.71, -0.03]],
    '2s': [[1/3, 0.04],   [2/3, -0.04]],
    '3f': [[0.26, -0.04], [0.55, 0],      [0.77, 0.03]],
    '3s': [[0.28, -0.05], [0.50, 0],      [0.72, 0.05]],
}

# Minimum seed distance based on terrain type.
# These are also used as weights for each type.
MIN_DISTANCE_L = 0.30 #0.22
MIN_DISTANCE_M = 0.24 #0.19
MIN_DISTANCE_H = 0.20 #0.16

MIN_RIDGE_LEN = 0.08
MIN_RIDGE_LEN_EDGE = 0.04

# Fill colors for regions based on terrain height.
REGION_COLOR = {
    '_': "#ffffff",  # blank
    'l': "#f0eaac",  #"#d9f3b9",  #'#efecc6',  # low
    'm': "#f0ce76",  #'#dcc382',  # medium
    'h': "#e7a311",  #'#d69200',  # high
    'r': "#a2c6ff",  # river/water
    'v': "#be850a",  # very high mountain
}

# Random dist of terrain types based on the corner terrain.
# Exact probs for each cell are interpolated from corners (and center).
TERRAIN_DIST = {
    # hhhhhh:        27 m + 24 h  :   0%  53%  47%
    # mmmhhh:  4 l + 24 m +  9 h  :  11%  65%  24%
    # llmmhm: 10 l + 15 m +  8 h  :  30%  46%  24%
    # llmhhm:  8 l + 13 m + 11 h  :  25%  54%  21%
    # llmhhm: 10 l + 22 m +  5 h  :  27%  59%  14%
    # lllmlm: 23 l +  5 m         :  82%  18%
    # llllll: 16 l +  6 m         :  73%  27%

    # hhhhhh:  6 l + 19 m + 13 h (l center)
    # llllll: 16 l + 12 m +  2 h (h center)
    'l': [ 0.80, 0.20, 0.00 ],
    'h': [ 0.00, 0.50, 0.50 ],
}

# NOTE: Default units for SVG is mm.

STROKE_COLOR = "#000000"
STROKE_WIDTH = 0.3
THICK_STROKE_WIDTH = 0.9

RIVER_WIDTH = 2.0

def calcSortedId(id0, id1):
    if int(id0) < int(id1):
        return f"{id0}-{id1}"
    return f"{id1}-{id0}"

def warning(msg):
    print("WARNING:", msg)

def error(msg):
    print("ERROR:", msg)
    sys.exit(0)

class VoronoiHexTile():
    def __init__(self, options):
        self.options = options
        self.debug = options['debug']

        self.size = self.options['size']
        self.xMax = (math.sqrt(3) * self.size) / 2

        # This is used to position the exterior seeds around the outside of the
        # tile. These seed regions constrain the regions in the hex tile and
        # allow us to ignore the outer edges (that go off to infinity).
        self.outerScale = 1.4

        # np.array of x,y coords.
        self.seeds = None

        # Useful indices into |self.seeds|.
        self.startCornerSeed = 0      # First corner seed (always 0)
        self.endCornerSeed = 0        # Last corner seed +1 (always 6 for hex)
        self.startEdgeSeed = 0        # First edge seed (always 6 for hex)
        self.endEdgeSeed = 0
        self.startInteriorSeed = 0    # First interior seed
        self.endInteriorSeed = 0
        self.numActiveSeeds = 0       # Total number of active seeds (ignore external seeds)

        # Number of candidates to generate and check around a seed before
        # giving up and marking the seed as complete.
        self.seedAttempts = 20
        
        # The edgeMarginZone is a set of circles along the edge between the
        # seeds. They define an exclusion zone between the seeds so that the
        # voronoi vertex does not fall outside the hex tile boundary.
        self.edgeMarginZone = None
        # Margin scale of 1.0 means that voronoi ridges that cross the hex tile
        # edge can end exactly at the tile edge (which we don't want). Use a
        # value > 1.0 to enforce min length for these ridge segments.
        self.edgeMarginScale = 1.1

        # Min distance between 2 voronoi vertices along a ridge.
        self.minRidgeLength = MIN_RIDGE_LEN * self.size
        # Min ridge length along tile edge.
        self.minRidgeLengthEdge = MIN_RIDGE_LEN_EDGE * self.size

        # Circle ratio threshold.
        # Maximum allowed ratio between largest and smallest inscribed circles.
        self.circleRatioThreshold = 1.51
        
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
        self.vor = None

        # Calculated voronoi vertices.
        self.vertices = None

        # Used to track new vertices that are added to the voronoi regions, for example,
        # to clip regions along the edge.
        # |newVertices| is a dictionary of vertices that we've already added so we don't
        # add the same vertex multiple times.
        self.newVertices = None
        # Index into |vertices| of the first edge vertex that we added.
        self.firstEdgeVertex = 0
        self.lastEdgeVertex = 0
        
        self.iteration = 0
        self.maxIterations = self.options['iter']

        # Adjustments to apply when we need to move a seed.
        # Each type of adjustment has a slightly different value so that if a
        # seed is being adjusted in multiple ways, it will still make progress
        # toward a goal.
        # Move seeds toward or away from an edge to make it longer.
        self.adjustmentSide = 0.011
        self.adjustmentNeighbor = -0.009
        # Move neighboring seeds closer or further to make inscribed circle
        # smaller or larger.
        self.adjustmentGrow = -0.005  # -0.006
        self.adjustmentShrink = 0.005
        # Move seeds away when they are too close.
        self.closeThreshold = 0.90
        self.adjustmentTooClose = -0.013

        # Explicit terrain/river data (loaded from file).
        self.terrainData = None
        self.riverData = None
        self.overlayData = None

        # Calculate data for reversed edges ('r') from the forward ('f') edges.
        for type in EDGE_TYPES:
            if type[-1] == 'f':
                newType = type[:-1] + 'r'
                EDGE_REGION_INFO[newType] = EDGE_REGION_INFO[type][::-1]
                newSeedInfo = []
                for si in reversed(EDGE_SEED_INFO[type]):
                    offset, perp_offset = si
                    newSeedInfo.append([1.0-offset, -perp_offset])
                EDGE_SEED_INFO[newType] = newSeedInfo

                if type in EDGE_RIVER_INFO:
                    EDGE_RIVER_INFO[newType] = EDGE_RIVER_INFO[type][::-1]
                if type in EDGE_CLIFF_INFO:
                    EDGE_CLIFF_INFO[newType] = EDGE_CLIFF_INFO[type][::-1]
        
    def setTerrainData(self, data):
        self.terrainData = data
        
    def setRiverData(self, data):
        self.riverData = data
        
    def setOverlayData(self, data):
        self.overlayData = data
        
    def init(self):
        self.initEdgePattern(self.options['pattern'])

        if self.options['seed'] == None:
            self.options['seed'] = random.randint(0,5000)
        if self.options['verbose']:
            print("Seed:", self.options['seed'])
        self.rng = np.random.RandomState(self.options['seed'])

        self.initFixedSeeds()
        self.initEdgeMarginZone()
        self.initInteriorSeeds()
        self.initExteriorSeeds()

    def initEdgePattern(self, pattern):
        if len(pattern) != NUM_SIDES:
            error(f"Invalid pattern: {pattern}")

        # Build mapping from corner to edge pattern.
        self.corner2edge = {}
        for eri in EDGE_REGION_INFO:
            info = EDGE_REGION_INFO[eri]
            edge = info[0] + info[-1]
            self.corner2edge[edge] = eri

        # Convert corner pattern ("llllll") -> edge pattern (2s-2s-2s-2s-2s-2s).
        self.edgeTypes = []
        for i in range(0, NUM_SIDES):
            i2 = (i + 1) % NUM_SIDES
            corners = pattern[i] + pattern[i2]
            self.edgeTypes.append(self.corner2edge[corners])

        self.nSeedsPerEdge = [len(EDGE_SEED_INFO[x]) for x in self.edgeTypes]

        # Verify that each edge pattern is consistent with its neighbors.
        self.cornerType = []
        for i in range(0, NUM_SIDES):
            edge = self.edgeTypes[i]
            edgeNext = self.edgeTypes[(i+1) % NUM_SIDES]
            # Make sure last region type of this edge matches the first type of
            # the next.
            edgeRegionTypes = EDGE_REGION_INFO[edge]
            edgeNextRegionTypes = EDGE_REGION_INFO[edgeNext]
            if edgeRegionTypes[-1] != edgeNextRegionTypes[0]:
                edgeTypes = '-'.join(edgeRegionTypes)
                edgeNextTypes = '-'.join(edgeNextRegionTypes)
                error(f"Edge patterns don't connect: {edge} ({edgeTypes}) and {edgeNext} ({edgeNextTypes})")
            self.cornerType.append(edgeRegionTypes[0])

        # Record the terrain type for each region along the edge of the tile.
        self.seed2terrain = []
        # Add the 6 corners.
        for e in self.edgeTypes:
            eInfo = EDGE_REGION_INFO[e]
            self.seed2terrain.append(eInfo[0])
        # Add the seeds for each edge.
        for e in self.edgeTypes:
            eInfo = EDGE_REGION_INFO[e]
            # Add info for middle regions (trim off first/last values since we've already
            # added the corners).
            for ei in eInfo[1:-1]:
                self.seed2terrain.append(ei)

        self.cornerWeight = {
            'l': MIN_DISTANCE_L * self.size,
            'm': MIN_DISTANCE_M * self.size,
            'h': MIN_DISTANCE_H * self.size,
        }

        if self.options['center'] == None:
            # Calculate center as average of all corner weights.
            self.centerWeight = (
                sum([self.cornerWeight[i] for i in self.cornerType]) / NUM_SIDES)
        else:
            self.centerWeight = self.cornerWeight[self.options['center']]
        if self.options['verbose']:
            print("Center weight:", self.centerWeight)

    # Initialize the fixed seeds along the edge of the hex tile.
    def initFixedSeeds(self):
        size = self.size
        xHex = self.xMax
        yHex = size/2

        # Hexagon vertices, starting at top and going around clockwise.
        self.vHex = np.array([
            [0, size], [xHex, yHex], [xHex, -yHex],
            [0, -size], [-xHex, -yHex], [-xHex, yHex],
            ])
        dbg_id = self.debug
        if dbg_id >= 0 and dbg_id < NUM_SIDES:
            print(f"Initializing corner seed {dbg_id}: {self.vHex[dbg_id]}")

        # Construct a list of adjacent edge regions for convenience later.
        # Each entry is a pair of seed ids identifying the 2 adjacent regions
        # for this seed: [ ccw, cw ]
        self.edgeAdjacent = {
            0: [],  # Init first seed so that we can append easily.
        }

        # Calculate seeds along hex edges
        vertices = []
        for i0 in range(0, NUM_SIDES):
            i1 = (i0 + 1) % NUM_SIDES
            edgeType = self.edgeTypes[i0]
            seedPattern = EDGE_SEED_INFO[edgeType]
            prev_sid = i0
            for j in range(0, len(seedPattern)):
                t, perp_t = seedPattern[j]
                vertices.append(lerperp(self.vHex[i0], self.vHex[i1],
                                        t, perp_t))
                sid = NUM_SIDES-1 + len(vertices)
                self.edgeAdjacent[prev_sid].append(sid)
                self.edgeAdjacent[sid] = [prev_sid]
                prev_sid = sid

                if dbg_id == sid:
                    print(f"Initializing edge seed {dbg_id}: {vertices[-1]}")

            self.edgeAdjacent[prev_sid].append(i1)
            if i1 == 0:
                self.edgeAdjacent[i1].insert(0, prev_sid)
            else:
                self.edgeAdjacent[i1] = [prev_sid]
        self.vEdgeSeeds = np.array(vertices)

        # Build temp seeds so that it can be used for the rest of the seed
        # initialization.
        self.seeds = np.concatenate((self.vHex, self.vEdgeSeeds))

    # Initialize the margin exclusion zones.
    # These zone prevent seeds from getting too close to the tile boundary where
    # they would cause voronoi ridges that are too small, or cause the region to
    # be clipped by the hex boundary.
    def initEdgeMarginZone(self):
        marginPoints = []
        for i0 in range(0, NUM_SIDES):
            sids = [i0]
            firstSeed = sum(self.nSeedsPerEdge[:i0])
            nEdgeSeeds = self.nSeedsPerEdge[i0]
            for j in range(firstSeed, firstSeed + nEdgeSeeds):
                sids.append(NUM_SIDES + j)
            i1 = (i0 + 1) % NUM_SIDES
            sids.append(i1)

            for i in range(0, len(sids)-1):
                # For the center of the margin exclusion zone, we can't just use
                # the midpoint between the two edge seeds; we have to calculate
                # the circle (based on the distance between the two seeds) and
                # then slide the circle along the voronoi ridge to place the
                # center on the tile edge.
                #
                #                   ridge line
                #       seed0 +       /
                #                    /
                #                   + <- midpoint between seeds 
                #                  /
                #   tile edge ----a-------+ seed1
                #                /         \
                #
                # Center of circle for margin zone must be at 'a'.
                #
                # This is important when the edge seeds lie outside the hex
                # because otherwise the margin zone will be too small (too far
                # outside the hex) and it will allow internal seeds to be placed
                # too close to the edge.
                t = self.calcEdgeRidgeIntersection(i0, i1, sids[i], sids[i+1])
                pt = lerp_pt(self.seeds[i0], self.seeds[i1], t)
                size = (self.edgeMarginScale * 0.5
                        * dist(self.seeds[sids[i]], self.seeds[sids[i+1]]))
                marginPoints.append([pt, size])
        
        self.edgeMarginZone = marginPoints

    # Generate the interior seed points.
    def initInteriorSeeds(self):
        startSeeds = np.concatenate((self.vHex, self.vEdgeSeeds))

        # Calc mininum seed distance based on seed location.
        seed2minDistance = []
        for i in range(0, len(startSeeds)):
            seed2minDistance.append(self.calcSeedWeight(startSeeds[i]))

        activeSeedIds = [x for x in range(0, len(startSeeds))]
        allSeeds = startSeeds.tolist()
        newSeeds = []
        while len(activeSeedIds) > 0:
            # Choose a random active seed.
            i = self.rng.randint(len(activeSeedIds))
            sid = activeSeedIds[i]
            found = False
            numAttempts = self.seedAttempts
            minSeed = seed2minDistance[sid]
            while not found and numAttempts > 0:
                seed = self.calcRandomSeedBridson(
                    allSeeds[sid], minSeed, 2 * minSeed)
                if not ptInHex(self.size, seed):
                    seed = None
                    continue
                # Also not too close the the edge margin region.
                for mz in self.edgeMarginZone:
                    pt, radius = mz
                    if near(pt, seed, radius):
                        seed = None
                        break
                if not seed:
                    continue
                    
                # Make sure it's no too close to any existing seeds.
                for sid2 in range(0, len(allSeeds)):
                    s = allSeeds[sid2]
                    if near(s, seed, seed2minDistance[sid2]):
                        seed = None
                        numAttempts -= 1
                        break
                if not seed:
                    continue

                found = True
                
            if seed == None:
                activeSeedIds.pop(i)
            else:
                activeSeedIds.append(len(allSeeds))
                allSeeds.append(seed)
                newSeeds.append(seed)
                seed2minDistance.append(self.calcSeedWeight(seed))

        self.vInteriorSeeds = np.array(newSeeds)
        self.seed2minDistance = seed2minDistance

    def calcTerrainType(self, sid):
        # Record terrain type for this seed so that we don't regenerate new
        # terrain for each iteration.
        if len(self.seed2terrain) != sid:
            error(f"Terrain for seeds generated out of order: {sid}")

        # If we have terrain data loaded from a file, use that.
        if self.terrainData:
            type = self.terrainData[sid]
            if type != '':
                self.seed2terrain.append(type)
                return type
        
        if not self.options['random-terrain-fill']:
            self.seed2terrain.append('_')
            return '_'
            
        w = self.calcSeedWeight(self.seeds[sid])
        w /= self.size
        
        # Convert weight to a range from 0 ('l') to 1 ('h').
        t = 1 - ((w - MIN_DISTANCE_H) / (MIN_DISTANCE_L - MIN_DISTANCE_H))

        # Interpolate the probs for each type based on the cell's weight.
        l_terrain = TERRAIN_DIST['l']
        h_terrain = TERRAIN_DIST['h']
        l_prob = clamp(lerp(l_terrain[0], h_terrain[0], t), 0, 1)
        m_prob = clamp(lerp(l_terrain[1], h_terrain[1], t), 0, 1)
        h_prob = clamp(lerp(l_terrain[2], h_terrain[2], t), 0, 1)

        probs = [l_prob, m_prob, h_prob]
        type = self.rng.choice(['l', 'm', 'h'], p = probs)

        self.seed2terrain.append(type)

        return type
        
    # Calc the min seed distance based on the current seed location in the hex
    # tile. Seeds in higher density regions will have a smaller distance than
    # those in low density regions.
    def calcSeedWeight(self, baseSeed):
        x, y = baseSeed
        a, b, c, sid0, sid1 = self.calcHexTriWeights(x, y)
        
        # Seed is within current triangle, calculate weight.
        w1 = self.cornerWeight[self.cornerType[sid0]]
        w2 = self.cornerWeight[self.cornerType[sid1]]
        w3 = self.centerWeight
        weight = a * w1 + b * w2 + c * w3
        return weight

    # Assumes hexagon is centered at 0,0
    def calcHexTriWeights(self, x, y):
        # Find the triangle (in the hex) where the point is located and compute
        # the barycentric coordinates of that point within the triangle. These
        # coordinates will be used as weights for that point.
        #
        # Given a point x,y, in barycentric coords:
        #   x = a * x1 + b * x2 + c * x3
        #   y = a * y1 + b * y2 + c * y3
        #   a + b + c = 1
        # Where (x1,y1), (x2,y2) and (x3,y3) are the points (P1,P2,P3) defining
        # the triangle and a,b,c are the weights that define the point.
        #
        # a,b,c can be calculated:
        #   a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3))
        #         / ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))
        #   b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3))
        #         / ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))
        #   c = 1 - a - b
        # 
        #                   0
        #                  _+_
        #              _,-' : `-,_
        #     5    _,-'     :     `-,_    1
        #        +:      5  :  0      :+
        #        | `-,_     :     _,-' |
        #        |     `-,_ : _,-'     |
        #        |   4     :+:     1   |
        #        |     _,-' : `-,_     |
        #        | _,-'     :     `-,_ |
        #        +:      3  :  2      :+
        #     4    `-,_     :     _,-'    2
        #              `-,_ : _,-'
        #                  `+'
        #                   3
        for tri in range(0, NUM_SIDES):
            tri_next = (tri + 1) % NUM_SIDES
            x1,y1 = self.vHex[tri]
            x2,y2 = self.vHex[tri_next]

            # Using P3 = (0,0) for the shared center of the hexagon, this
            # simplifies to:
            #   denom = ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))
            #         = ((y2 - 0) * (x1 - 0) + (0 - x2) * (y1 - 0))
            #         = (y2 * x1) - (x2 * y1)
            #   a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denom
            #     = ((y2 - 0) * (x - 0) + (0 - x2) * (y - 0)) / denom
            #     = ((y2 * x) - (x2 * y)) / denom
            #   b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denom
            #     = ((0 - y1) * (x - 0) + (x1 - 0) * (y - 0)) / denom
            #     = ((x1 * y) - (y1 * x)) / denom
            #   c = 1 - a - b
            denom = (y2 * x1) - (x2 * y1)
            a = ((y2 * x) - (x2 * y)) / denom
            b = ((x1 * y) - (y1 * x)) / denom
            c = 1 - a - b

            # Normally, we need to confirm that a,b,c are all within [0,1], but
            # because we know the point is within the hexagon, we can eliminate
            # some checks. Note that if the seed is along an edge between 2
            # triangles, it doesn't matter which triangle we choose since the
            # weighted-distance will be the same either way. So we just take the
            # first match.
            # Note: Some of the edge seeds are actually slightly outside the
            # hexagon (so that |c| is < 0), but this is OK.
            if fge(a, 0) and fge(b, 0) and fle(c, 1):
                return (a, b, c, tri, tri_next)
        error(f"Unable to calculate seed distance for {x},{y}")
        return None
        
    # Generate a random x,y point within a ring (defined by |r0| and |r1|) around
    # the given |baseSeed|.
    def calcRandomSeedBridson(self, baseSeed, r0, r1):
        x0, y0 = baseSeed
        angle = self.rng.uniform(0, math.tau)
        r = self.rng.uniform(r0, r1)
        x = x0 + r * math.cos(angle)
        y = y0 + r * math.sin(angle)
        return [x, y]
            
    # Calculate boundary seeds around outside of hex.
    # These seeds constrain the voronoi regions by providing boundaries for the
    # regions along the edges, which allows us to ignore unbounded regions.
    def initExteriorSeeds(self):
        vertices = []
        for i0 in range(0, NUM_SIDES):
            i1 = (i0 + 1) % NUM_SIDES
            vertices.append(scale(self.vHex[i0], self.outerScale))
            nBoundarySeeds = self.nSeedsPerEdge[i0] + 1
            for j in range(0, nBoundarySeeds):
                vertices.append(
                    scale(lerp_pt(self.vHex[i0], self.vHex[i1],
                                  (j+1) / (nBoundarySeeds + 1)),
                          self.outerScale))
        self.vOutsideSeeds = np.array(vertices)

    # Add a new vertex to the voronoi graph. This is used when clipping the
    # regions along the edge of the tile.
    # Return the index of the new vertex.
    def addEdgeVertex(self, v):
        # Check to see of we've added this vertex already.
        key = self._calcVertexKey(v)
        if key in self.newVertices:
            return self.newVertices[key]
        id = self._addNewVertex(v, key)
        self.lastEdgeVertex = id + 1
        return id

    def add3dVertex(self, v):
        # Check to see of we've added this vertex already.
        key = self._calcVertexKey(v)
        if key in self.newVertices:
            return self.newVertices[key]
        return self._addNewVertex(v, key)

    def _calcVertexKey(self, v):
        return f"{v[0]:.6g}-{v[1]:.6g}"

    def _addNewVertex(self, v, key):
        id = len(self.vertices)
        self.vertices.append(v)
        self.newVertices[key] = id
        return id

    # Calculate the set of regions (seed ids) that surround the given region.
    def calcNeighboringRegions(self, sid0):
        if not sid0 in self.sid2region:
            return []
        vids = self.sid2region[sid0]
        sids = []
        for vid in vids:
            for sid in self.vid2sids[vid]:
                if sid != sid0 and not sid in sids:
                    sids.append(sid)
        return sids

    # Calculate the 2 regions on either side of the edge defined by vertices vid0-vid1.
    # Return array of [vid, sid] for the 2 vertices, ignoring the regions that
    # are common to both vertices.
    def calcSideRegions(self, vid0, vid1):
        sides = []
        for sid in self.vid2sids[vid0]:
            if not sid in self.vid2sids[vid1]:
                sides.append([vid0, sid])
        for sid in self.vid2sids[vid1]:
            if not sid in self.vid2sids[vid0]:
                sides.append([vid1, sid])
        return sides

    # Given an edge defined by the 2 seeds, return the 2 ridge vertices of the edge.
    def getEdgeRidgeVertices(self, sid0, sid1):
        edgeToFind = f"{sid0}-{sid1}"
        n_ridges = len(self.vor.ridge_points)
        for i in range(0, n_ridges):
            (s0, s1) = self.vor.ridge_points[i]
            if s1 < s0:
                s0,s1 = s1,s0
            key = f"{s0}-{s1}"
            if key == edgeToFind:
                return [self.vertices[i] for i in self.vor.ridge_vertices[i]]
        return None

    def calcAdjustment(self, sid, vMod, lerp_t):
        # Don't adjust the fixed seeds along the edge.
        if sid < self.startInteriorSeed:
            return
        sid_orig = sid

        # Calc seed id in the interior seed array.
        sid -= self.startInteriorSeed

        v = self.vInteriorSeeds[sid]
        if not sid in self.adjustments:
            self.adjustments[sid] = [0,0]
        dx, dy = lerp_pt_delta(v, vMod, lerp_t)
        self.adjustments[sid][0] += dx
        self.adjustments[sid][1] += dy
        if self.debug == sid_orig:
            print(f"Adjusting {sid_orig} by ({dx}, {dy})")

    # Calculate all regions with clipping.
    def calcClippedRegions(self):
        self.sid2region = {}
        for sid in range(0, NUM_SIDES):
            rid = self.vor.point_region[sid]
            if self.debug == sid:
                print(f"Calc clip region for corner {sid}")
            vids = self.calcCornerVertices(sid, rid)
            self.sid2region[sid] = vids
        for i0 in range(0, NUM_SIDES):
            i1 = (i0 + 1) % NUM_SIDES
            sid0 = NUM_SIDES + sum(self.nSeedsPerEdge[:i0])
            
            # Calc array of seed positions for this edge, including the corners:
            # [ 0, seeds..., 1 ]
            edgeType = self.edgeTypes[i0]
            seedPattern = EDGE_SEED_INFO[edgeType]
            edgeSeeds = [0]
            for p in seedPattern:
                edgeSeeds.append(p[0])
            edgeSeeds.append(1)

            for j in range(0, len(seedPattern)):
                sid = sid0 + j
                rid = self.vor.point_region[sid]
                if self.debug == sid:
                    print(f"Calc clip region for edge {sid}")

                adjSeeds = self.edgeAdjacent[sid]

                t0 = self.calcEdgeRidgeIntersection(
                    i0, i1, sid, adjSeeds[0])
                t1 = self.calcEdgeRidgeIntersection(
                    i0, i1, sid, adjSeeds[1])

                #t0 = lerp(edgeSeeds[j], edgeSeeds[j+1], 0.5)
                #t1 = lerp(edgeSeeds[j+1], edgeSeeds[j+2], 0.5)
                vids = self.calcEdgeVertices(sid, rid, i0, i1, t0, t1)
                self.sid2region[sid] = vids

        for sid in range(self.startInteriorSeed, self.endInteriorSeed):
            rid = self.vor.point_region[sid]
            self.sid2region[sid] = self.vor.regions[rid]
            if not self.isClockwise(sid):
                self.sid2region[sid] = self.vor.regions[rid][::-1]

    # sid_c0 - seed id of start corner
    # sid_c1 - seed id of end corner
    # sid_e0 - seed id of first edge seed
    # sid_e1 - seed id of second edge seed
    # Returns t, the position of the intersection between the two corner seeds
    #   (sid_c0 and sid_c1).
    def calcEdgeRidgeIntersection(self, sid_c0, sid_c1, sid_e0, sid_e1):
        c0 = self.seeds[sid_c0]
        c1 = self.seeds[sid_c1]
        # Seeds for the prev/next region along the edge.
        pt_e0 = self.seeds[sid_e0]
        pt_e1 = self.seeds[sid_e1]

        # Calc points along perpendicular bisector (= voronoi ridge between
        # these 2 seeds).
        dx,dy = lerp_pt_delta(pt_e0, pt_e1, 0.5)
        # First pt is midpoint between seeds.
        mid = [pt_e0[0] + dx, pt_e0[1] + dy]
        # Arbitrary second pt on perpendicular bisector.
        pb = [mid[0] - dy, mid[1] + dx]

        # Calc intersection |t| along edge (from corner to corner).
        t1, t2 = line_intersection_t([c0, c1], [mid, pb])
        return t1

    # sid - seed id of corner vertex
    # rid - region id
    # Returns an array of vertex indices for the corner region.
    def calcCornerVertices(self, sid, rid):
        # Calc prev and next hex corner seed ids.
        sid_cprev = (sid + NUM_SIDES - 1) % NUM_SIDES
        sid_cnext = (sid + 1) % NUM_SIDES

        # Calc |t| for each edge lerp, when starting from |sid|. 
        edgeType_prev = self.edgeTypes[sid_cprev]
        edgeType = self.edgeTypes[sid]

        # If the edge seeds are all exactly on the edge, then we can calculate
        # the edge-ridge intersection as the midpoint between the seeds.
        # However, because we're adding a perpendicular offset to the edge
        # seeds, we can't take this shortcut and we need to calculate the
        # intersection between the voronoi ridge and the tile edge.
        #edgeT_prev = 0.5 * (1.0 - EDGE_SEED_INFO[edgeType_prev][-1][0])
        #edgeT = 0.5 * EDGE_SEED_INFO[edgeType][0][0]

        adjSeeds = self.edgeAdjacent[sid]

        edgeT_prev = self.calcEdgeRidgeIntersection(
            sid, sid_cprev, sid, adjSeeds[0])
        edgeT = self.calcEdgeRidgeIntersection(
            sid, sid_cnext, sid, adjSeeds[1])

        return self.__calcEdgeVertices(sid, rid, sid, sid_cprev, sid_cnext,
                                       edgeT_prev, edgeT)

    # sid - seed if for this region
    # sid0 - first corner sid for the edge containing this region
    # sid1 - second corner sid for the edge containing this region
    # Returns an array of vertex indices for the edge region.
    def calcEdgeVertices(self, sid, rid, sid0, sid1, t_ccw, t_cw):
        return self.__calcEdgeVertices(sid, rid, sid0, sid1, sid1, t_ccw, t_cw)

    # Calculate 2x signed area of the region.
    def __signedArea2(self, sid):
        rid = self.vor.point_region[sid]
        pts = self.vor.regions[rid]

        # Algorithm:
        #   Calculate the signed area.
        #   Sum (x2 - x1)(y2 + y1) for each segment.
        # Positive = clockwise, Negative = counter-clockwise.
        #   Divide by 2 to get area.
        # Example:
        #  5 +
        #    |
        #  4 +              ,C,
        #    |            ,'   `,
        #  3 +          ,'       `,
        #    |        ,'           `,
        #  2 +       A - - - - - - - B
        #    |
        #  1 +
        #    |
        #  0 +---+---+---+---+---+---+---+---+
        #    0   1   2   3   4   5   6   7   8
        #  A = (2,2)  B = (6,2)  C = (4,4)
        # For [A, B, C]:
        #   Calc A->B, B->C and C->A
        #   = (6-2)(2+2) + (4-6)(4+2) + (2-4)(2+4)
        #   = 16 + -12 + -12
        #   = -8 (counter-clockwise)
        # For [A, C, B]:
        #   Calc A->C, C->B and B->A
        #   = (4-2)(4+2) + (6-4)(2+4) + (2-6)(2+2)
        #   = 12 + 12 + -16
        #   = 8 (clockwise)
        # Area = 8 / 2 = 4
        area2 = 0.0
        for i in range(0, len(pts)):
            pt1 = self.vertices[pts[i]]
            pt2 = self.vertices[pts[(i+1) % len(pts)]]
            area2 += (pt2[0] - pt1[0]) * (pt2[1] + pt1[1])
        # The sign of area2 indicates the direction of the points.
        # The actual area can be obtained by dividing |area2| by 2.
        return area2

    # Return true if the points are in clockwise order.
    def isClockwise(self, sid):
        # No need to divide by 2 since we don't need the area, just the sign.
        return fge(self.__signedArea2(sid), 0.0)

    def area(self, sid):
        # Divide the absolute value by 2 to get the area.
        return abs(self.__signedArea2(sid)) / 2;

    # sid - seed id for the region being calculated
    # rid - region id
    # sid0 - seed id of start corner
    # sid_cprev - seed id of end corner for prev (ccw) dir
    # sid_cnext - seed id of end corner for next (cw) dir
    # t_ccw - percentage from start to end corner for ccw
    # t_cw - percentage from start to end corner for cw
    #
    # sid0, _prev and _next are the seeds that are used as reference points to
    # calculate the vertices. t_ccw and t_cw are used to determine how far along
    # the vertex lines between the start (sid0) and end (_prev or _next).
    #
    # For corners, sid0 is the same as sid.
    #                   sid
    #                  sid0
    #        t_ccw      _+_     t_cw
    #              \_,-'   `-,_/
    # sid_prev  _,-'           `-,_  sid_next
    #         +'                   `+
    #         |                     |
    #
    # For edges, the vertices are always between start and the same end, so
    # sid_prev and sid_next are the same.
    #
    #              t_ccw    t_cw     sid_prev 
    #     sid0       |       |       sid_next
    #         +----------+----------+
    #        /          sid          \
    #       /                         \
    def __calcEdgeVertices(self, sid, rid, sid0, sid_cprev, sid_cnext,
                           t_ccw, t_cw):
        debug = False
        if self.debug == sid:
            debug = True

        regions = self.vor.regions[rid]
        if debug: print("  original vertex order", regions)
        if self.isClockwise(sid):
            r = regions[:]
        else:
            r = regions[::-1]
        if debug: print("  clockwise vertex order", r)

        # Rotate the region vertices so that all the internal vertices are at
        # the beginning of the array.
        # Rotate left until we have an internal vertex at the front.
        done = False
        while not done:
            v = self.vertices[r[0]]
            if ptInHex(self.size, v):
                done = True
            else:
                r = r[1:] + r[0:1]
        # Rotate right until there isn't an internal vertex at the end.
        done = False
        while not done:
            v = self.vertices[r[-1]]
            if not ptInHex(self.size, v):
                done = True
            else:
                r = r[-1:] + r[:-1]
        if debug: print("  rotated vertex order", r)

        # Count number of internal vertices.
        numInternal = sum([1 if ptInHex(self.size, self.vertices[vid]) else 0
                           for vid in r])
        if debug: print("  # of internal vertices", numInternal)
        
        verts = []
        # Write out internal vertices.
        for rindex in range(0, numInternal):
            vid = r[rindex]
            v = self.vertices[vid]
            if debug: print(f"  vertex {vid} : {v}")
            verts.append(vid)
            if debug: print(f"    appending internal: {vid}")

        # Write tile boundary.
        # Assume we're generating edge vertices in ccw order.
        # Note that the order of the vertices in the region (as returned
        # by the voronoi library) is not consistent, so we need to
        # determine which way we are moving around the polygon.
        startCcw = True
        ccw = lerp_pt(self.seeds[sid0], self.seeds[sid_cprev], t_ccw)
        cw = lerp_pt(self.seeds[sid0], self.seeds[sid_cnext], t_cw)
        if debug:
            print("     assume ccw")
            print(f"     ccw {ccw} from {sid0} and {sid_cprev} @ {t_ccw:.03g}%")
            print(f"      cw {cw} from {sid0} and {sid_cnext} @ {t_cw:.03g}%")

        # Determine which tile boundary point is closest to the last internal
        # vertex.
        vFirstIn = self.vertices[r[0]]
        vLastIn = self.vertices[r[numInternal-1]]
        if debug:
            print(f"     check dist to first/last internal {vFirstIn} {vLastIn}")
            print(f"       first dist to cw: {dist(vFirstIn, cw)}")
            print(f"       first dist to ccw: {dist(vFirstIn, ccw)}")
            print(f"       last dist to cw: {dist(vLastIn, cw)}")
            print(f"       last dist to ccw: {dist(vLastIn, ccw)}")

        # Swap direction if the region vertices are CW.
        if dist(vFirstIn, ccw) < dist(vLastIn, ccw):
            startCcw = False
            if debug: print("    swap direction to cw")

        # Double-check direction by checking the cw point.
        startCcwCheck = dist(vFirstIn, cw) < dist(vLastIn, cw)
        if numInternal != 1 and startCcw != startCcwCheck:
            warning(f"calculating clipped region for {sid}")

        if not startCcw:
            cw, ccw = ccw, cw

        verts.append(self.addEdgeVertex(ccw))
        if debug: print(f"    adding new vertex {ccw}")

        # Hex corners have an extra point in the middle.
        if sid_cprev != sid_cnext:
            verts.append(self.addEdgeVertex(self.seeds[sid0]))
            if debug: print(f"    adding new vertex (corner) {self.seeds[sid0]}")

        verts.append(self.addEdgeVertex(cw))
        if debug: print(f"    adding new vertex {cw}")
        return verts

    # Find any voronoi edges that are too small.
    def findBadEdges(self):
        self.badEdges = {}
        for sid in range(0, self.numActiveSeeds):
            r = self.sid2region[sid]
            for rindex in range(0, len(r)):
                vid0 = r[rindex]
                vid1 = r[(rindex + 1) % len(r)]
                v0 = self.vertices[vid0]
                v1 = self.vertices[vid1]

                # If this is one of the edges that is clipped by the hex
                # boundary, then enforce a smaller min edge
                minDistance = self.minRidgeLength
                if self.isEdgeVertex(vid0) and self.isEdgeVertex(vid1):
                    continue
                if self.isEdgeVertex(vid0) or self.isEdgeVertex(vid1):
                    minDistance = self.minRidgeLengthEdge

                if near(v0, v1, minDistance):
                    edgeInfo = [vid0, vid1, sid]
                    edgeId = calcSortedId(vid0, vid1)
                    if not edgeId in self.badEdges:
                        self.badEdges[edgeId] = []
                    self.badEdges[edgeId].append(edgeInfo)

    # Find seeds that have drifted too close to neighboring seeds.
    def findTooClose(self):
        self.tooClose = []
        for sid in range(0, self.numActiveSeeds):
            minDist = self.closeThreshold * self.seed2minDistance[sid]
            for n_sid in self.calcNeighboringRegions(sid):
                s0 = self.seeds[sid]
                s1 = self.seeds[n_sid]
                if near(s0, s1, minDist):
                    self.tooClose.append([sid, n_sid])
                    if self.debug == sid or self.debug == n_sid:
                        print("Seeds", sid, n_sid, "are close")

    # Find any regions that are too small.
    def findSmallRegions(self):
        self.regionCircles = {}
        self.circleRatio = 0
        self.minCircle = None
        self.maxCircle = None
    
        minCircleRadius = 0
        maxCircleRadius = 0
        for sid in range(0, self.endInteriorSeed):
            r = self.sid2region[sid]
            polyCenter = []
            polyRadius = 0

            # Handle corner and edge regions.
            if sid < self.endEdgeSeed:
                if sid < self.endCornerSeed:
                    # Center is the corner seed.
                    polyCenter = self.seeds[sid]
                elif sid < self.endEdgeSeed:
                    # Find the 2 vertices that were added during clipping. This
                    # will be the outer edge.
                    v = []
                    for vid in r:
                        if self.isEdgeVertex(vid):
                            v.append(vid)
                    # Midpoint of outer edge is center.
                    polyCenter = lerp_pt(self.vertices[v[0]],
                                         self.vertices[v[1]], 0.5)
                # Calc min distance from v to each edge of original polygon.
                dist = -1
                for rv0 in range(0, len(r)):
                    rv1 = (rv0 + 1) % len(r)
                    edge = [self.vertices[r[rv0]], self.vertices[r[rv1]]]
                    d = dist_pt_line(polyCenter, edge)
                    # Ignore if d == 0 because that means that the center vertex
                    # is on the line (which means it's an outer edge).
                    if not feq(d, 0) and (dist == -1 or d < dist):
                        dist = d
                polyRadius = dist

            # Handle internal regions.
            else:
                # Create voronoi for this polygon to use as a seleton.
                polySeeds = []
                for rv0 in range(0, len(r)):
                    rv1 = (rv0 + 1) % len(r)
                    vid0 = r[rv0]
                    vid1 = r[rv1]
                    mid = lerp_pt(self.vertices[vid0], self.vertices[vid1], 0.5)
                    polySeeds.append(mid)
                polyVoro = scipy.spatial.Voronoi(polySeeds)

                for v in polyVoro.vertices:
                    # Calc min distance from v to each edge of original polygon.
                    dist = -1
                    for rv0 in range(0, len(r)):
                        rv1 = (rv0 + 1) % len(r)
                        edge = [self.vertices[r[rv0]], self.vertices[r[rv1]]]
                        d = dist_pt_line(v, edge)
                        if dist == -1 or d < dist:
                            dist = d
                    # Record vertex with largest min distance
                    if len(polyCenter) == 0 or dist > polyRadius:
                        polyCenter = v
                        polyRadius = dist

            self.regionCircles[sid] = [polyCenter, polyRadius]
            if self.minCircle == None or polyRadius < minCircleRadius:
                self.minCircle = sid
                minCircleRadius = polyRadius
            if self.maxCircle == None or polyRadius > maxCircleRadius:
                self.maxCircle = sid
                maxCircleRadius = polyRadius
        self.circleRatio = maxCircleRadius / minCircleRadius

    # Calculate and analyze the voronoi graph from the set of seed points.
    def generate(self):
        self.seeds = np.concatenate((self.vHex, self.vEdgeSeeds))
        if len(self.vInteriorSeeds) > 0:
            self.seeds = np.append(self.seeds, self.vInteriorSeeds, 0)
        self.seeds = np.append(self.seeds, self.vOutsideSeeds, 0)

        # Record offsets into the seed array.
        self.startCornerSeed = 0
        self.endCornerSeed = len(self.vHex)
        self.startEdgeSeed = self.endCornerSeed
        self.endEdgeSeed = self.endCornerSeed + len(self.vEdgeSeeds)
        self.startInteriorSeed = self.endEdgeSeed
        self.endInteriorSeed = self.endEdgeSeed + len(self.vInteriorSeeds)

        # Calc number of seeds on tile, ignoring the outside seeds.
        self.numActiveSeeds = (len(self.vHex)
                               + len(self.vEdgeSeeds)
                               + len(self.vInteriorSeeds))

        self.vor = scipy.spatial.Voronoi(self.seeds)

        # Make a copy of the generated vertices so that we can add new
        # vertices along the tile boundary.
        self.vertices = [vid for vid in self.vor.vertices]
        self.newVertices = {}
        self.firstEdgeVertex = len(self.vertices)
        self.lastEdgeVertex = self.firstEdgeVertex + 1

        # Reset number of annotation lines.
        self.numLines = 0

        self.analyze()
        
        self.printIteration(self.iteration if self.iteration > 0 else "START")
        if self.options['anim']:
            self.plot(self.iteration)
        self.iteration += 1
        
    def printIteration(self, i):
        if self.options['verbose_iteration']:
            print("Iteration", i, end='')
            print(" -", len(self.badEdges), "bad edges", end='')

            nTooClose = len(self.tooClose)
            if nTooClose > 0:
                print(" -", nTooClose, "seed pairs are too close", end='')
            
            if ENABLE_SMALL_REGION_CHECK:
                min = self.minCircle
                max = self.maxCircle
                if min and max:
                    print(f" - {min} {self.regionCircles[min][1]:.5g} {max} {self.regionCircles[max][1]:.5g}", end='')
                    print(f" - ratio {self.circleRatio:.5g}", end='')
                if self.circleRatio > self.circleRatioThreshold:
                    print(" - adj min/max", end='')

            print()
        
    def analyze(self):
        # Create a dict to map from region id to seed id.
        self.rid2sid = {}
        for sid in range(0, len(self.vor.point_region)):
            rid = self.vor.point_region[sid]
            self.rid2sid[rid] = sid

        # Recalculate the min seed distance for each seed.
        self.seed2minDistance = []
        for i in range(0, self.numActiveSeeds):
            self.seed2minDistance.append(self.calcSeedWeight(self.seeds[i]))

        self.calcClippedRegions()

        # Ensure each region has a terrain type.
        for sid in range(len(self.seed2terrain), self.numActiveSeeds):
            self.calcTerrainType(sid)

        # Verify that all voronoi vertices are shared by 3 seed regions.
        # Note ignoring regions along outer edge which will have some vertices
        # shared by only 1 or 2 regions.
        self.vid2sids = {}
        for sid in range(0, self.numActiveSeeds):
            for vid in self.sid2region[sid]:
                if not vid in self.vid2sids:
                    self.vid2sids[vid] = []
                self.vid2sids[vid].append(sid)
        for k,v in self.vid2sids.items():
            if len(v) > 3:
                print("Error - vertex shared by more than 3 regions:", k, v)
        
        self.findBadEdges()
        self.findSmallRegions()
        self.findTooClose()

    def update(self):
        if self.iteration > self.maxIterations:
            return False
        hasChanges = False
        self.adjustments = {}

        # Move seed toward short edge to make it longer.
        # |badEdges| is an array of bad edges:
        #   Each bad edge is an array identifying the 2 regions:
        #     [vertex-id0, vertex-id1, seed1-id], [vid0, vid1, seed2-id]
        #
        # For a bad (too short) edge:
        # 
        #            \       side        /
        #             \       v         /
        #  <-neighbor  +---------------+  neighbor->
        #             /       ^         \ 
        #            /       side        \ 
        #
        # Seeds for the side regions are moved closer.
        # Seeds for the neighboring regions are moved away.
        for bei in self.badEdges:
            badEdge = self.badEdges[bei]
            vid0, vid1, sid0 = badEdge[0]
            if len(badEdge) < 2:
                print("Matching edge not found for", sid0, vid0, vid1)
                continue
            sid1 = badEdge[1][2]

            # Calc mid-point of bad edge
            mid = lerp_pt(self.vertices[vid0], self.vertices[vid1], 0.5)
            
            # Nudge seed points on either side of the edge closer.
            for sid in [sid0, sid1]:
                self.calcAdjustment(sid, mid, self.adjustmentSide)

            # Nudge seeds points for neighboring regions away.
            sides = self.calcSideRegions(vid0, vid1)
            for s in sides:
                vid, sid = s
                self.calcAdjustment(sid, self.vertices[vid],
                                    self.adjustmentNeighbor)
            hasChanges = True

        # Adjust seeds that are too close.
        for seed_pair in self.tooClose:
            s0, s1 = seed_pair
            # s1 is too close to s0 and should be moved away slightly.
            self.calcAdjustment(s1, self.seeds[s0], self.adjustmentTooClose)
            # Adjust both seeds to handle case where s1 is fixed.
            self.calcAdjustment(s0, self.seeds[s1], self.adjustmentTooClose)
            if self.debug == s0 or self.debug == s1:
                print(f"Seed {s1} is being pushed away from {s0}")
            hasChanges = True
            
        if ENABLE_SMALL_REGION_CHECK:
            # If there's too much difference between the largest and smallest
            # circle, adjust the regions that surround the min and max regions.
            if self.circleRatio > self.circleRatioThreshold:
                # Move neighboring regions slightly away from the small region.
                for sid in self.calcNeighboringRegions(self.minCircle):
                    self.calcAdjustment(sid, self.seeds[self.minCircle],
                                        self.adjustmentGrow)
                # Move neighboring regions slightly away from the small region.
                for sid in self.calcNeighboringRegions(self.maxCircle):
                    self.calcAdjustment(sid, self.seeds[self.maxCircle],
                                        self.adjustmentShrink)
                hasChanges = True

        # Apply the adjustments.
        newInterior = self.vInteriorSeeds.copy()
        for sid in range(0, len(self.vInteriorSeeds)):
            if sid in self.adjustments:
                if self.debug == sid:
                    print(f"Adjusting {sid} by {self.adjustments[sid]}")
                newInterior[sid][0] += self.adjustments[sid][0]
                newInterior[sid][1] += self.adjustments[sid][1]
        self.vInteriorSeeds = np.array(newInterior)

        return hasChanges

    def getTerrainStyle(self, type):
        if self.options['bw']:
            return REGION_COLOR['_']
        return REGION_COLOR[type]

    def isEdgeVertex(self, vid):
        return vid >= self.firstEdgeVertex and vid < self.lastEdgeVertex

    def plot(self, plotId=None):
        self.svg = SVG([215.9, 279.4])  #SVG([210, 297])
        fig = plt.figure(figsize=(8,8))

        # Build list of template ids and then load from svg file.
        svg_ids = []
        for obj in ['bridge', 'star', 'tree1', 'tree2', 'tree3', 'tree4', 'tower']:
            svg_ids.append(f"obj-{obj}")
        svg_ids.append("tile-id")
        self.svg.load_ids(self.options['map_obj_template'], svg_ids)

        layer = self.svg.add_inkscape_layer('layer', "Layer")
        layer.set_transform("translate(107.95 120) scale(1, -1)")
        self.layer = layer

        stroke = Style("none", "#000000", STROKE_WIDTH)
        black_fill = Style(fill="#000000")

        self.calcUpdatedRegions()

        # Draw layers back to front.
        
        self.drawHexTileBorder("background", "Tile Background", black_fill)

        self.drawClippedRegionLayer()

        self.drawRoundedRegionLayer("fill", "Fill")
        self.drawLakeOverlayLayer()

        self.drawRoundedRegionLayer("stroke", "Stroke")
        
        self.drawRegionLayer()

        self.drawSeedLayer()
        self.drawSeedExclusionZoneLayer()
        self.drawMarginExclusionZoneLayer()
        self.drawBadEdgeLayer()
        self.drawTooCloseSeedsLayer()
        self.drawInscribedCirclesLayer()

        self.drawTileId()

        self.drawAnnotations()

        self.drawTerrainLabels()

        self.drawRivers()
        
        self.drawOverlay()

        self.drawRegionIdLayer()

        self.drawHexTileBorder("border", "Border", stroke)
        
        self.writeOutput(fig, plotId)

    # Calc updated regions that have been adjusted by rivers.
    def calcUpdatedRegions(self):
        self.sid2updatedRegion = copy.deepcopy(self.sid2region)

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
        gClip = SVG.group('clip')
        SVG.add_node(layer_region_clip, gClip)
        layer_region_clip.hide()

        for sid in range(0, self.numActiveSeeds):
            vids = self.sid2region[sid]
            id = f"clipregion-{sid}"
            color = "#ffffff"
            terrain_type = self.seed2terrain[sid]
            color = self.getTerrainStyle(terrain_type)
            self.plotRegion(vids, color)
            self.drawRegion(id, vids, color, gClip)

    def drawRoundedRegionLayer(self, idSuffix, desc):
        layer_region_rounded = self.svg.add_inkscape_layer(
            f"region-rounded-{idSuffix}", f"Region Rounded {desc}", self.layer)

        for sid in range(0, self.numActiveSeeds):
            vids = self.sid2region[sid]
            id = f"roundedregion{idSuffix}-{sid}"
            
            if idSuffix == "fill":
                terrain_type = self.seed2terrain[sid]
                color = self.getTerrainStyle(terrain_type)
                style = Style(color, None)
                stroke = False
            else:
                style = Style(None, STROKE_COLOR, THICK_STROKE_WIDTH)
                stroke = True
            self.drawRoundedRegion(id, vids, style, layer_region_rounded, isStroke=stroke)

    def drawLakeOverlayLayer(self):
        if not self.overlayData:
            return
        if not "lake" in self.overlayData:
            return

        self.layer_lakes = self.svg.add_inkscape_layer(
            'lakes', "Lakes", self.layer)
        #self.layer_lakes.set_scale_transform(1, -1)

        for lake_seed_id in self.overlayData['lake']:
            if lake_seed_id:
                rid = self.vor.point_region[int(lake_seed_id)]
                id = f"lake-{lake_seed_id}"
                style = Style(REGION_COLOR['r'], None)
                self.drawRoundedRegion(id, self.vor.regions[rid], style, self.layer_lakes)

    def drawRegionLayer(self):
        layer_region = self.svg.add_inkscape_layer('region', "Region", self.layer)
        layer_region.hide()

        for sid in range(0, self.numActiveSeeds):
            rid = self.vor.point_region[sid]
            id = f"region-{sid}"
            self.drawRegion(id, self.vor.regions[rid], "#ffffff", layer_region)

    def drawSeedLayer(self):
        layer_seeds = self.svg.add_inkscape_layer('seeds', "Seeds", self.layer)
        layer_seeds.hide()

        black_fill = Style(fill="#000000")
        for sid in range(0, self.numActiveSeeds):
            center = self.seeds[sid]
            id = f"seed-{sid}"
            self._drawCircle(id, center, 1.0, black_fill, layer_seeds)

    def drawSeedExclusionZoneLayer(self):
        layer_seed_ex = self.svg.add_inkscape_layer(
            'seed_exclusion', "Seed Exclusion", self.layer)
        layer_seed_ex.hide()

        fill = Style(fill="#800000")
        fill.set('fill-opacity', 0.15)

        for sid in range(0, self.numActiveSeeds):
            center = self.vor.points[sid]
            radius = self.seed2minDistance[sid]
            id = f"seed-ex-{sid}"
            self._drawCircle(id, center, radius, fill, layer_seed_ex)

    def drawMarginExclusionZoneLayer(self):
        layer_margin_ex = self.svg.add_inkscape_layer(
            'margin_exclusion', "Margin Exclusion", self.layer)
        layer_margin_ex.hide()

        fill = Style(fill="#000080")
        fill.set('fill-opacity', 0.15)

        for mz in self.edgeMarginZone:
            center, radius = mz
            self._drawCircle(0, center, radius, fill, layer_margin_ex)

    def drawBadEdgeLayer(self):
        if len(self.badEdges) == 0:
            return
        
        layer_bad_edges = self.svg.add_inkscape_layer(
            'bad-edges', "Bad Edges", self.layer)
        for bei in self.badEdges:
            badEdge = self.badEdges[bei]
            vid0, vid1, rid = badEdge[0]
            self.plotBadVertex(self.vertices[vid0], layer_bad_edges)
            self.plotBadVertex(self.vertices[vid1], layer_bad_edges)

    def drawTooCloseSeedsLayer(self):
        if len(self.tooClose) == 0:
            return

        layer_too_close = self.svg.add_inkscape_layer(
            'too-close', "Too Close Seeds", self.layer)
        for spair in self.tooClose:
            s0, s1 = spair
            p = Path()
            p.setPoints([self.seeds[s] for s in [s0,s1]])
            p.set_style(Style(None, "#800000", "0.5px"))
            SVG.add_node(layer_too_close, p)
            
            self.plotBadVertex(self.seeds[s0], layer_too_close)
            self.plotBadVertex(self.seeds[s1], layer_too_close)
    
    def drawInscribedCirclesLayer(self):
        layer_circles = self.svg.add_inkscape_layer(
            'circles', "Inscribed Circles", self.layer)
        layer_circles.hide()
        
        fill = Style(fill="#008000")
        fill.set('fill-opacity', 0.15)
        black_fill = Style(fill="#000000")

        for sid in self.regionCircles:
            center, radius = self.regionCircles[sid]
            id = f"incircle-{sid}"
            self._drawCircle(id, center, radius, fill, layer_circles)

            id = f"incircle-ctr-{sid}"
            self._drawCircle(id, center, '0.5', black_fill, layer_circles)
        if ENABLE_SMALL_REGION_CHECK:
            if self.circleRatio > self.circleRatioThreshold:
                for c in [self.minCircle, self.maxCircle]:
                    center, radius = self.regionCircles[c]
                    circle = plt.Circle(center, radius, color="#80000080")
                    plt.gca().add_patch(circle)
    
    def drawTileId(self):
        if self.options['id']:
            self.layer_text = self.svg.add_inkscape_layer(
                'tile-id', "Tile Id", self.layer)
            self.layer_text.set_transform("scale(1,-1)")

            id = self.options['id']
            id_text = self.svg.add_loaded_element(self.layer_text, 'tile-id')
            id_text.set('transform', f"translate(0 {-self.size+8})")
            SVG.set_text(id_text, f"{id:03d}")

    def drawAnnotations(self):
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
        pNum = self.calcNumericPattern()
        self._addAnnotationText(f"pattern {pNum} / {pattern}")
        self._addAnnotationText(f"seed attempts: {self.seedAttempts}")
        self._addAnnotationText(f"seed distance: l {MIN_DISTANCE_L:.03g}; m {MIN_DISTANCE_M:.03g}; h {MIN_DISTANCE_H:.03g}")

        center = "AVG"
        if self.options['center']:
            center = self.options['center']
        self._addAnnotationText(f"center: ({center}) {self.centerWeight / self.size:.03g}")

        self._addAnnotationText(f"min ridge length: {MIN_RIDGE_LEN:.02g}; at edge: {MIN_RIDGE_LEN_EDGE:.02g}")
        self._addAnnotationText(f"edge margin exclusion zone scale: {self.edgeMarginScale:.02g}")
        self._addAnnotationText(f"iterations: {self.iteration-1}")
        self._addAnnotationText(f"adjustments: side {self.adjustmentSide:.03g}, neighbor {self.adjustmentNeighbor:.03g}")
        self._addAnnotationText(f"closeness: {self.closeThreshold:.03g}, adjust {self.adjustmentTooClose:.03g}")

    def _addAnnotationText(self, text):
        t = Text(None, -92, 90 + 5.5 * self.numLines, text)
        SVG.add_node(self.layer_text, t)
        self.numLines += 1
    
    def drawTerrainLabels(self):
        # Add corner terrain labels.
        for i in range(0, NUM_SIDES):
            t = self.options['pattern'][i]
            label = Text(None, -1.5, -(self.size + 2), t.upper())
            if i != 0:
                label.set_transform(f"rotate({60 * i})")
            SVG.add_node(self.layer_text, label)

        # Add edge terrain labels.
        for i in range(0, NUM_SIDES):
            g = Group(None)
            g.set_transform(f"rotate({30 + i * 60})")
            SVG.add_node(self.layer_text, g)
            edgeType = self.edgeTypes[i]
            seedPattern = EDGE_SEED_INFO[edgeType]
            for j in range(0, len(seedPattern)):
                t, perp_t = seedPattern[j]
                x = lerp(-self.size/2, self.size/2, t)

                type = EDGE_REGION_INFO[edgeType][j+1]
                label = Text(None, x - 1.5, -(self.xMax + 3), type.upper())
                SVG.add_node(g, label)

        # Add river info.
        for i in range(0, NUM_SIDES):
            edgeType = self.edgeTypes[i]
            if edgeType in EDGE_RIVER_INFO:
                g = Group(None)
                g.set_transform(f"rotate({30 + i * 60})")
                SVG.add_node(self.layer_text, g)

                rIndex = EDGE_RIVER_INFO[edgeType].index('*')
                seedPattern = EDGE_SEED_INFO[edgeType]
                x = self._calcEdgeFeatureOffset(rIndex, seedPattern)

                color = self.getTerrainStyle('r')
                r = SVG.rect(0, x-1.5, -self.xMax -8, 3, 8)
                r.set_style(Style(color, STROKE_COLOR, STROKE_WIDTH))
                SVG.add_node(g, r)

                label = Text(None, x - 1.5, -(self.xMax + 10), "R")
                SVG.add_node(g, label)

        # Add cliff info.
        for i in range(0, NUM_SIDES):
            edgeType = self.edgeTypes[i]
            if edgeType in EDGE_CLIFF_INFO:
                g = Group(None)
                g.set_transform(f"rotate({30 + i * 60})")
                SVG.add_node(self.layer_text, g)

                rIndex = EDGE_CLIFF_INFO[edgeType].index('*')
                seedPattern = EDGE_SEED_INFO[edgeType]
                x = self._calcEdgeFeatureOffset(rIndex, seedPattern)

                color = self.getTerrainStyle('r')
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
        #  EDGE_SEED_INFO:    -       x   x   -
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
      
    def drawRivers(self):
        # There are 2 layers for the rivers: the black border and the blue river fill.
        # This is so that all the borders are behind all of the river fills.
        self.layer_river_border = self.svg.add_inkscape_layer(
            'river-border', "River Border", self.layer)
        self.group_river_border = SVG.group('river-border-group')
        SVG.add_node(self.layer_river_border, self.group_river_border)
        clippath_id = self.addHexTileClipPath()
        self.group_river_border.set("clip-path", f"url(#{clippath_id})")
        self.style_river_border = Style(None, STROKE_COLOR,
                                   RIVER_WIDTH + 2 * STROKE_WIDTH)
        self.style_river_border.set("stroke-linecap", "round")
        self.style_river_border.set("stroke-linejoin", "round")

        self.layer_river = self.svg.add_inkscape_layer('river', "River", self.layer)
        self.group_river = SVG.group('river-group')
        SVG.add_node(self.layer_river, self.group_river)
        clippath_id = self.addHexTileClipPath()
        self.group_river.set("clip-path", f"url(#{clippath_id})")
        self.style_river = Style(None, REGION_COLOR['r'], RIVER_WIDTH)
        self.style_river.set("stroke-linecap", "round")
        self.style_river.set("stroke-linejoin", "round")

        rivers = self._calcRiverVertices()
        for r in rivers:
            p = Path()
            for vid in r:
                p.addPoint(self.vertices[vid])
            p.end(False)
            p2 = copy.deepcopy(p)

            p.set_style(self.style_river_border)
            SVG.add_node(self.group_river_border, p)

            p2.set_style(self.style_river)
            SVG.add_node(self.group_river, p2)
        
    def _calcRiverVertices(self):
        # Scan the tile edges to determine if a river is required.
        # Build a list of tile edges that have a river exit: |riverEdges|.
        riverEdges = []
        seedIdCorner = 0
        seedIdEdge = 6
        for e in self.edgeTypes:
            eInfo = EDGE_REGION_INFO[e]
            numEdgeRegions = len(eInfo) - 2  # Ignore first/last since those are corners.
            
            if e in EDGE_RIVER_INFO:
                rInfo = EDGE_RIVER_INFO[e]
                regions = [seedIdCorner]
                regions += list(range(seedIdEdge, seedIdEdge + numEdgeRegions))
                regions += [(seedIdCorner + 1) % 6]
                riverIndex = rInfo.index('*')
                r0 = regions[riverIndex-1]
                r1 = regions[riverIndex]
                riverEdges.append(calcSortedId(r0,r1))
            seedIdCorner += 1
            seedIdEdge += numEdgeRegions

        # Exit if this tile has no tile edges with rivers.
        if len(riverEdges) == 0:
            return []

        if self.riverData:
            # Build a clean list of ridge segments that should be rivers.
            rRidges = [r for r in self.riverData if r]

            r = RiverBuilder(riverEdges, rRidges)
            r.buildRidgeInfo(self.vor)
            r.buildTransitions()
            
            return r.getRiverVertices()
        return []

    def drawOverlay(self):
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
                        cells = m.group(1)
                    else:
                        raise Exception(f"Unrecognized bridge data: {bridge}")

                    (start, end) = cells.split('-')
                    ptStart = self.seeds[int(start)]
                    ptEnd = self.seeds[int(end)]
                    rTheta = math.atan2(-(ptEnd[1] - ptStart[1]), ptEnd[0] - ptStart[0])
                    degTheta = 90 + (rTheta * 180 / math.pi);
                    edge_vertices = self.getEdgeRidgeVertices(start, end)
                    center = lerp(edge_vertices[0], edge_vertices[1], 0.5)
                    icon = self.svg.add_loaded_element(self.layer_overlay, 'obj-bridge')
                    
                    transform = f"translate({center[0]} {-center[1]}) rotate({degTheta})"
                    icon.set('transform', transform)

        if "mark" in self.overlayData:
            for mark in self.overlayData['mark']:
                if mark:
                    # <type> '-' <cell-id> '(' <x-offset> <y-offset> ')'
                    m = re.match(r"^([a-z0-9-]+)\-(\d+)(\(([\d.-]+ [\d.-]+)\))?$", mark)
                    if m:
                        type = m.group(1)
                        cell = m.group(2)
                        offset = None
                        if m.group(3):
                            offset = m.group(4).split(' ')
                    else:
                        raise Exception(f"Unrecognized star data: {mark}")

                    center = self.seeds[int(cell)]
                    icon = self.svg.add_loaded_element(self.layer_overlay, f"obj-{type}")
                    x = center[0]
                    y = -center[1]
                    if offset:
                        x += float(offset[0])
                        y -= float(offset[1])
                    icon.set('transform', f"translate({x} {y})")

    def drawRegionIdLayer(self):
        layer_region_ids = self.svg.add_inkscape_layer(
            'region_ids', "Region Ids", self.layer)
        if not self.options['show-seed-ids']:
            layer_region_ids.hide()
        layer_region_ids.set_transform("scale(1,-1)")
        for sid in range(0, self.numActiveSeeds):
            center = self.seeds[sid]
            text = f"{sid}"
            if PLOT_CELL_IDS:
                plt.text(center[0]-1.4, center[1]-1.5, text)
            t = Text(None, center[0]-1.4, -center[1], text)
            SVG.add_node(layer_region_ids, t)

    def _drawCircle(self, id, center, radius, fill, layer):
        circle = SVG.circle(id, center[0], center[1], radius)
        circle.set_style(fill)
        SVG.add_node(layer, circle)

    def writeOutput(self, fig, plotId):
        if self.options['write_output']:
            outdir_png = self.getPngOutputDir()
            name = self.calcBaseFilename()
            if plotId == None:
                if GENERATE_SVG:
                    outdir_svg = self.getSvgOutputDir()
                    out_svg = os.path.join(outdir_svg, '%s.svg' % name)
                    self.svg.write(out_svg)

                    outdir_pdf = self.getPdfOutputDir()
                    out_pdf = os.path.join(outdir_pdf, '%s.pdf' % name)
                    Inkscape.export_pdf(
                        os.path.abspath(out_svg),
                        os.path.abspath(out_pdf))

                out_png = os.path.join(outdir_png, '%s.png' % name)
            else:
                outdir_png = os.path.join(outdir_png, self.options['anim_subdir'])
                if not os.path.isdir(outdir_png):
                    os.makedirs(outdir_png);
                out_png = os.path.join(outdir_png, f"{name}-{plotId:03d}")
                plt.text(-self.size, -self.size, plotId)

            plt.axis("off")
            plt.xlim([x * self.size for x in [-1, 1]])
            plt.ylim([y * self.size for y in [-1, 1]])
            if GENERATE_PLOT:
                plt.savefig(out_png, bbox_inches='tight')
            plt.close(fig)

    def getPngOutputDir(self):
        out_dir = self.options['outdir_png']
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

    def calcNumericPattern(self):
        altPattern = {
            'l': '1',
            'm': '2',
            'h': '3',
        }
    
        pattern = self.options['pattern']
        return ''.join([altPattern[i] for i in pattern])
        
    def calcBaseFilename(self):
        name = "hex"
        if self.options['id'] != None:
            name = f"hex-{self.options['id']:03d}"
        elif self.options['seed'] != None:
            pNum = self.calcNumericPattern()
            name = f"hex-{pNum}-{self.options['seed']}"
        return name

    def plotBadVertex(self, v, layer):
        circle = plt.Circle(v, 1, color="r")
        plt.gca().add_patch(circle)

        circle = SVG.circle(0, v[0], v[1], '1')
        circle.set_style(Style(fill="#800000"))
        SVG.add_node(layer, circle)

    # Plot voronoi region given a list of vertex ids.
    def plotRegion(self, vids, color):
        if len(vids) == 0:
            return
        vertices = [self.vertices[i] for i in vids]
        plt.fill(*zip(*vertices), facecolor=color, edgecolor="black")

    # Draw voronoi region in the SVG file, given a list of vertex ids.
    def drawRegion(self, id, vids, color, layer):
        if len(vids) == 0:
            return
        vertices = [self.vertices[i] for i in vids]
        
        p = Path() if id == None else Path(id)
        p.addPoints(vertices)
        p.end()
        p.set_style(Style(color, STROKE_COLOR, STROKE_WIDTH))
        SVG.add_node(layer, p)

    # Draw voronoi region with rounded points in the SVG file, given a list of vertex ids.
    def drawRoundedRegion(self, id, vids, style, layer, isStroke = False):
        if len(vids) == 0:
            return
        num_verts = len(vids)
        
        iv = list(range(0, num_verts))

        # The first vertex of the region to draw.
        firstVertex = 0
        # The number of vertices at the end to skip (only for strokes).
        numSkipVertices = 0
        # True if we should automatically connect the last vertex to the first.
        closePath = True
        
        # If this is an edge region, then we:
        # * Don't want to round off the vertices along the edge.
        # * Don't want to close off the segment corresponding to the edge
        #   (Because we don't want a fat stroke along that edge).
        isEdgeRegion = False
        numEdgeVertices = 0
        for i in range(0, num_verts):
            if self.isEdgeVertex(vids[i]):
                isEdgeRegion = True
                numEdgeVertices += 1

        if isEdgeRegion and isStroke:
            closePath = False

            # Rotate vertex indices until the last edge vertex is in the first position.
            # Scenarios (edge vertices in parentheses)
            #    2 edge vertex:
            #      (0) -  1  -  2  -  3  - (4)   : -
            #      (0) - (1) -  2  -  3  -  4    : rotate 1
            #       0  - (1) - (2) -  3  -  4    : rotate 2
            #       0  -  1  - (2) - (3) -  4    : rotate 3
            #       0  -  1  -  2  - (3) - (4)   : rotate 4
            #    3 edge vertex:
            #      (0) -  1  -  2  - (3) - (4)   : -
            #      (0) - (1) -  2  -  3  - (4)   : rotate 1
            #      (0) - (1) - (2) -  3  -  4    : rotate 2
            #       0  - (1) - (2) - (3) -  4    : rotate 3
            #       0  -  1  - (2) - (3) - (4)   : rotate 4
            while not (self.isEdgeVertex(vids[iv[0]]) and not self.isEdgeVertex(vids[iv[1]])):
                iv = iv[1:] + iv[:1]
            
            # Remove the last vertex from the stroke if we have 3 edge vertices.
            if numEdgeVertices == 3:
                iv.pop()
                
        p = Path() if id == None else Path(id)
        for i in iv:
            vid = vids[i]
            v = self.vertices[vid]

            # We don't want to round the vertices along the edge of the tile. We can
            # identify these edge vertices easily because they are the ones that we
            # added to the end of the vertex list during clipping.
            if self.isEdgeVertex(vid):
                p.addPoint(v)
            else:
                # Add a small curve for this vertex.
                prev = (i + num_verts - 1) % num_verts
                next = (i + num_verts + 1) % num_verts

                # v[prev] *
                #          \
                #           \
                #            \
                #             \
                #      prev_pt +
                #               \
                #             c0 +
                #                 \    c1  next_pt
                #                  *----+----+-----------*
                #                v[i]                  v[next]
                #
                # * = actual vertices of the region: v[prev], v[i], v[next]
                #     Note: v[prev] is shorthand for self.vertices[vids[prev]]
                # + = calculated vertices of the curved corner:
                #     prev_pt, next_pt and the 2 off-curve control points: c0, c1
                # Note: The points for the curve are calculated using an absolute distance
                # from the current vertex along the line to the neighboring vertices.
                PT_OFFSET = 1.5  # (mm)
                CURVE_PT_OFFSET = 0.5  # (mm)

                prev_pt = pt_along_line(v, self.vertices[vids[prev]], PT_OFFSET)
                p.addPoint(prev_pt)

                curve0_pt = pt_along_line(v, self.vertices[vids[prev]], CURVE_PT_OFFSET)
                curve1_pt = pt_along_line(v, self.vertices[vids[next]], CURVE_PT_OFFSET)
                next_pt = pt_along_line(v, self.vertices[vids[next]], PT_OFFSET)
                p.addCurvePoint(curve0_pt, curve1_pt, next_pt)

        p.end(closePath)
        p.set_style(style)
        SVG.add_node(layer, p)

    def addHexTileClipPath(self):
        p = Path()
        p.addPoints(self.vHex)
        p.end()
        return self.svg.add_clip_path(p)

    def cleanupAnimation(self):
        out_dir = os.path.join(self.options['outdir_png'], self.options['anim_subdir'])
        anim_pngs = os.path.join(out_dir, '*.png')
        for png in glob.glob(anim_pngs):
            os.remove(png)

    def exportAnimation(self):
        anim_dir = os.path.join(self.options['outdir_png'], self.options['anim_subdir'])
        cmd = ["convert"]
        cmd.extend(["-delay", "15"])
        cmd.extend(["-loop", "0"])
        cmd.append(os.path.join(anim_dir, "hex-*"))

        base = self.calcBaseFilename()
        last_file = f"{base}-{self.iteration-1:03d}.png"
        cmd.extend(["-delay", "100"])
        cmd.append(os.path.join(anim_dir, last_file))

        anim_file = os.path.join(self.options['outdir_png'], f"{base}.gif")
        cmd.append(anim_file)

        subprocess.run(cmd)

    def writeTileData(self):
        center = self.options['center']
        if center == None:
            center = "AVG"
        print(f"TERRAIN,{self.options['pattern']},{self.options['seed']},{center},", end='')

        while len(self.seed2terrain) <= 100:
            self.seed2terrain.append('')
        terrain = ','.join(self.seed2terrain)
        print(terrain)

    #
    # 3D tile generation (for rendering in Blender)
    #
    
    def calcRegion3d(self, obj, sid):
        r = self.sid2region[sid]
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
        name = self.calcBaseFilename()
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
            options['_export_3d_edge'] = (i + 3) % NUM_SIDES
            # Give each neighbor a different seed to ensure that there is no repetition.
            options['seed'] = seedOrig + (i+1)

            # Calculate edge pattern for this edge's neighboring tile.
            edgeStart = patternOrig[i]
            edgeEnd = patternOrig[(i+1) % NUM_SIDES]
            pattern = edgeStart + edgeEnd * 3 + edgeStart * 2
            if i != 0:
                pattern = pattern[-i:] + pattern[0:NUM_SIDES-i]
            options['pattern'] = pattern
            
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
            self.calcRegion3d(obj, NUM_SIDES + j)
        # End corner.
        self.calcRegion3d(obj, (sid+1) % NUM_SIDES)
