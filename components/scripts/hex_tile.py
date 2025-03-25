import copy
import glob
import math
import numpy as np
import os
import random  # Only used to seed numpy random, if needed
import scipy.spatial
import subprocess

from data_tile_pattern_ids import TILE_PATTERN_IDS
from hex_tile_plotter import VoronoiHexTilePlotter
from map_common import calcSortedId
from math_utils import (feq, fge, fle, scale, clamp,
                        lerp, lerp_pt, lerp_pt_delta, lerperp,
                        near, dist, dist_pt_line, line_intersection_t,
                        isClockwise, area,
                        ptInHex)

NUM_SIDES = 6

SINGLE_EDGE_TYPES = ['1s', '2f', '2s', '3f', '3s']
NEW_SINGLE_EDGE_TYPES = ['0s', '1f', '1s', '2f', '2s']

# EdgeRegionInfo:
# Each dict entry contains an array of region heights, one per region on this
# side.
# # = number of seeds between the corners
# 's' = self symmetric
# 'f' = forward edge, mirror pairs
# 'r' = reverse edge, not listed here since they are auto-calculated from 'f' edge
EDGE_REGION_INFO = {
    '1s': ['l', 'l', 'l'],                     # l - l
    '2f': ['l', 'l', 'l', 'm'],                # l - m, m - h
    '2s': ['m', 'l', 'l', 'm'],                # m - m
    '3f': ['m', 'm', 'h', 'm', 'h'],           # m - h, h - m
    '3s': ['h', 'h', 'm', 'h', 'h'],           # h - h
}
NEW_EDGE_REGION_INFO = {
    '0s': ['l', 'l'],                          # l - l
    '1f': ['l', 'l', 'm'],                     # l - m, m - l
    '1s': ['m', 'm', 'm'],                     # m - m
    '2f': ['m', 'm', 'm', 'h'],                # m - h
    '2s': ['h', 'm', 'm', 'h'],                # h - h
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
NEW_EDGE_SEED_INFO = {
    '0s': [],
    '1f': [[0.58, 0.05]],
    '1s': [[0.50, 0]],
    '2f': [[0.42, 0.04],  [0.77, -0.03]],
    '2s': [[1/3, 0.04],   [2/3, -0.04]],
}

# Minimum seed distance based on terrain type.
# These are also used as weights for each type.
MIN_DISTANCE_L = 0.30 #0.38 #0.30 #0.22
MIN_DISTANCE_M = 0.24 #0.29 #0.24 #0.19
MIN_DISTANCE_H = 0.20 #0.24 #0.20 #0.16

# Scale applied to min seed distance.
MIN_RIDGE_LEN_SCALE = 0.45
# Scale applied to standard min ridge len.
MIN_RIDGE_LEN_EDGE_SCALE = 0.5

# Min allowed radius for circle inscribed within region.
# Should be at least 7.5 so that 15mm diameter pieces fit well in the region.
MIN_INSCRIBED_CIRCLE_RADIUS = 8

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

class VoronoiHexTile():
    def __init__(self, options):
        self.options = options
        self.debug = options['debug']

        self.numSides = NUM_SIDES
        self.size = self.options['size']
        self.xMax = (math.sqrt(3) * self.size) / 2

        self.singleEdgeTypes = SINGLE_EDGE_TYPES
        
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

        self.edgeSeedInfo = EDGE_SEED_INFO
        self.edgeRegionInfo = EDGE_REGION_INFO
        self.minDistanceL = MIN_DISTANCE_L
        self.minDistanceM = MIN_DISTANCE_M
        self.minDistanceH = MIN_DISTANCE_H

        self.minInscribedCircleRadius = MIN_INSCRIBED_CIRCLE_RADIUS
        
        # Min distance between 2 voronoi vertices along a ridge.
        # This scale is applied to the minDistance for the seeds for this ridge.
        self.minRidgeLengthScale = MIN_RIDGE_LEN_SCALE
        self.minRidgeLengthEdgeScale = MIN_RIDGE_LEN_EDGE_SCALE

        # Voronoi object has following attributes:
        # .points : array of seed values used to create the Voronoi
        # .point_region : mapping from seed index to region index
        #     -1 for seeds that don't have a corresponding region.
        # .vertices : array of Voronoi vertices
        # .regions : array of regions, where each region is an array of Voronoi
        #     indices. The Voronoi index will be -1 for vertices outside the Voronoi
        #     diagram (out to infinity).
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
        # seed is being adjusted in multiple ways, it's more likely to make progress
        # toward a goal.
        
        # Move seeds toward or away from an edge to make it longer.
        self.adjustmentSide = 0.011
        self.adjustmentNeighbor = -0.009

        # Move neighboring seeds closer or further to make inscribed circle
        # smaller or larger.
        self.adjustmentGrow = -0.003  # -0.006
        self.adjustmentShrink = 0.003

        # Move seeds away when they are too close.
        self.closeThreshold = 0.90
        self.adjustmentTooClose = -0.013
        
        # Move seeds toward their centroid when relaxing the entire voronoi graph.
        self.centroidRelax = 0.001

        # Explicit terrain/river data (loaded from file).
        self.terrainData = None
        self.riverData = None
        self.cliffData = None
        self.overlayData = None
        
        # Calculate data for reversed edges ('r') from the forward ('f') edges.
        for type in self.singleEdgeTypes:
            if type[-1] == 'f':
                newType = type[:-1] + 'r'
                self.edgeRegionInfo[newType] = self.edgeRegionInfo[type][::-1]
                newSeedInfo = []
                for si in reversed(self.edgeSeedInfo[type]):
                    offset, perp_offset = si
                    newSeedInfo.append([1.0-offset, -perp_offset])
                self.edgeSeedInfo[newType] = newSeedInfo
            # Verify that symmetric edges are actually symmetric.
            if type[-1] == 's':
                nSeeds = len(self.edgeSeedInfo[type])
                if (nSeeds % 2) == 1:
                    # The middle seed (if present) must be at [0.5 0].
                    midIndex = int(nSeeds / 2)
                    sInfo = self.edgeSeedInfo[type][midIndex]
                    if not (feq(sInfo[0], 0.5) and feq(sInfo[1], 0)):
                        raise Exception(f"Middle edge seed for {type} musst be at [0.5,0.0] instead of {sInfo}")
                if nSeeds > 1:
                    first = sInfo = self.edgeSeedInfo[type][0]
                    last = sInfo = self.edgeSeedInfo[type][-1]
                    if not feq(first[0], 1.0 - last[0]):
                        raise Exception(f"Seed offsets for {type} are not symmetric: {first[0]} and {last[0]}")
                    if not feq(first[1], -last[1]):
                        raise Exception(f"Seed perpendcular offsets for {type} do not match: {first[1]} and {last[1]}")
        
        # Calculate the pattern mirror map.
        # Corner ids for:
        #           ,0,             ,0,
        #  Front  5'   `1   Back  1'   `5
        #         |     |         |     |
        #         4,   ,2         2,   ,4
        #           `3'             `3'
        self.patternMirror = {}
        for t in TILE_PATTERN_IDS:
            rev = t[0] + t[5:0:-1]
            canonPattern, rotate, pId = self.findCanonicalEdgePattern(rev)
            self.patternMirror[t] = [canonPattern, rotate, pId]

    def setTerrainData(self, data):
        self.terrainData = data
        
    def setRiverData(self, data):
        self.riverData = data
        
    def setCliffData(self, data):
        self.cliffData = data
        
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
            raise Exception(f"Invalid pattern: {pattern}")

        # Build mapping from corner to edge pattern.
        self.corner2edge = {}
        for eri in self.edgeRegionInfo:
            info = self.edgeRegionInfo[eri]
            edge = info[0] + info[-1]
            self.corner2edge[edge] = eri
        #print(self.corner2edge)
        
        # Convert corner pattern ("llllll") -> edge pattern (2s-2s-2s-2s-2s-2s).
        self.edgeTypes = []
        for i in range(0, NUM_SIDES):
            i2 = (i + 1) % NUM_SIDES
            corners = pattern[i] + pattern[i2]
            if not corners in self.corner2edge:
                raise Exception(f"Invalid adjacent corners: {pattern[i]} and {pattern[i2]}")
            self.edgeTypes.append(self.corner2edge[corners])
        #print(self.edgeTypes)

        self.nSeedsPerEdge = [len(self.edgeSeedInfo[x]) for x in self.edgeTypes]

        # Verify that each edge pattern is consistent with its neighbors.
        self.cornerType = []
        for i in range(0, NUM_SIDES):
            edge = self.edgeTypes[i]
            edgeNext = self.edgeTypes[(i+1) % NUM_SIDES]
            # Make sure last region type of this edge matches the first type of
            # the next.
            edgeRegionTypes = self.edgeRegionInfo[edge]
            edgeNextRegionTypes = self.edgeRegionInfo[edgeNext]
            if edgeRegionTypes[-1] != edgeNextRegionTypes[0]:
                edgeTypes = '-'.join(edgeRegionTypes)
                edgeNextTypes = '-'.join(edgeNextRegionTypes)
                raise Exception(f"Edge patterns don't connect: {edge} ({edgeTypes}) and {edgeNext} ({edgeNextTypes})")
            self.cornerType.append(edgeRegionTypes[0])

        # Verify that the pattern is in its canonical form.
        if self.options['_allow_non_canonical_pattern'] == False:
            if not pattern in TILE_PATTERN_IDS:
                cPattern = self.findCanonicalEdgePattern(pattern)
                if cPattern:
                    p, rot, id = cPattern
                    raise Exception(f"Non canonical pattern. Use {p} ({TILE_PATTERN_IDS[p]}) instead of {pattern}.")
                raise Exception("Invalid pattern: {pattern}")
                    
        # Record the terrain type for each region along the edge of the tile.
        self.seed2terrain = []
        # Add the 6 corners.
        for e in self.edgeTypes:
            eInfo = self.edgeRegionInfo[e]
            self.seed2terrain.append(eInfo[0])
        # Add the seeds for each edge.
        for e in self.edgeTypes:
            eInfo = self.edgeRegionInfo[e]
            # Add info for middle regions (trim off first/last values since we've already
            # added the corners).
            for ei in eInfo[1:-1]:
                self.seed2terrain.append(ei)

        self.cornerWeight = {
            'l': self.minDistanceL * self.size,
            'm': self.minDistanceM * self.size,
            'h': self.minDistanceH * self.size,
        }

        if self.options['center'] == None:
            # Calculate center as average of all corner weights.
            self.centerWeight = (
                sum([self.cornerWeight[i] for i in self.cornerType]) / NUM_SIDES)
        else:
            self.centerWeight = self.cornerWeight[self.options['center']]
        if self.options['verbose']:
            print("Center weight:", self.centerWeight)

    # Return the canonical form of the pattern and rotation offset if it exists.
    # The rotation offset identifies the start index of the canonical form of the pattern.
    def findCanonicalEdgePattern(self, pattern):
        # Try to find the canonical form.
        for p in TILE_PATTERN_IDS:
            for i in range(0, NUM_SIDES):
                rotatedPattern = p[i:] + p[:i]
                if pattern == rotatedPattern:
                    return [p, i, TILE_PATTERN_IDS[p]]
        return None
    
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
            seedPattern = self.edgeSeedInfo[edgeType]
            #print(seedPattern)
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

        #print(self.vHex)
        #print(self.vEdgeSeeds)
        # Build temp seeds so that it can be used for the rest of the seed
        # initialization.
        if self.vEdgeSeeds.size:
            self.seeds = np.concatenate((self.vHex, self.vEdgeSeeds))
        else:
            self.seeds = self.vHex

    # Initialize the margin exclusion zones.
    # These zones prevent seeds from getting too close to the tile boundary where
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
        if self.vEdgeSeeds.size:
            startSeeds = np.concatenate((self.vHex, self.vEdgeSeeds))
        else:
            startSeeds = self.vHex

        # Calc mininum seed distance based on seed location.
        seed2minDistance = []
        for i in range(0, len(startSeeds)):
            seed2minDistance.append(self.calcSeedWeight(startSeeds[i]))

        activeSeedIds = [x for x in range(0, len(startSeeds))]
        allSeeds = startSeeds.tolist()
        newSeeds = []
        
        # Force a seed at the center
        if (self.options['center-seed']):
            seed = [0,0]
            activeSeedIds.append(len(allSeeds))
            allSeeds.append(seed)
            newSeeds.append(seed)
            seed2minDistance.append(self.calcSeedWeight(seed))

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
                        numAttempts -= 1
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
            raise Exception(f"Terrain for seeds generated out of order: {sid}")

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
        t = 1 - ((w - self.minDistanceH) / (self.minDistanceL - self.minDistanceH))

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
        raise Exception(f"Unable to calculate seed distance for {x},{y}")
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
        if not sid0 in self.sid2clippedRegion:
            return []
        vids = self.sid2clippedRegion[sid0]
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

    def calcMinRidgeLengthForSeed(self, sid):
        return self.seed2minDistance[sid] * self.minRidgeLengthScale
    
    # Calc the min ridge length for the edge defined by the 2 vertices.
    # This is the average of the min ridge length for the seeds on either side of the
    # edge.
    def calcMinRidgeLength(self, vid0, vid1):
        return 0.08 * self.size
        # Get the seed ids for the seeds on either side of this edge.
        sids = [x[1] for x in self.calcSideRegions(vid0, vid1)]
        rlen = 0
        for sid in sids:
            rlen += self.calcMinRidgeLengthForSeed(sid)
        rlen /= 2  # Calc average of the values for the 2 seeds.
        return rlen

    # Calc adjustment of |sid| to move it toward |vMod| by |lerp_t|.
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

    # Calculate mapping from seed-id to array of vertices (ordered clockwise).
    def calcSid2Region(self):
        self.sid2region = {}
        for sid in range(0, self.endInteriorSeed):
            rid = self.vor.point_region[sid]
            self.sid2region[sid] = self.vor.regions[rid]
            if not self.isClockwise(sid):
                self.sid2region[sid] = self.vor.regions[rid][::-1]

    # Calculate mapping from seed-id to array of (clockwise) vertices with clipping.
    def calcSid2ClippedRegion(self):
        self.sid2clippedRegion = {}
        for sid in range(0, NUM_SIDES):
            rid = self.vor.point_region[sid]
            if self.debug == sid:
                print(f"Calc clip region for corner {sid}")
            vids = self.calcCornerVertices(sid, rid)
            self.sid2clippedRegion[sid] = vids
        for i0 in range(0, NUM_SIDES):
            i1 = (i0 + 1) % NUM_SIDES
            sid0 = NUM_SIDES + sum(self.nSeedsPerEdge[:i0])
            
            # Calc array of seed positions for this edge, including the corners:
            # [ 0, seeds..., 1 ]
            edgeType = self.edgeTypes[i0]
            seedPattern = self.edgeSeedInfo[edgeType]
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
                self.sid2clippedRegion[sid] = vids

        for sid in range(self.startInteriorSeed, self.endInteriorSeed):
            rid = self.vor.point_region[sid]
            self.sid2clippedRegion[sid] = self.vor.regions[rid]
            if not self.isClockwise(sid):
                self.sid2clippedRegion[sid] = self.vor.regions[rid][::-1]

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

    def calcCentroid(self, sid):
        verts = self._getRegionVertices(sid)

        area2 = 0.0
        cx = 0.0
        cy = 0.0
        numVerts = len(verts)
        for i in range(0, numVerts):
            # Formula for the centroid of a polygon
            #               n-1
            #        1     ,---
            # c  = ------   >     ( x  + x   ) (x  y     -  x    y  )
            #  x    6 A    '---      i    i+1    i  i+1      i+1  i
            #               n=0
            #
            #               n-1
            #        1     ,---
            # c  = ------   >     ( y  + y   ) (x  y     -  x    y  )
            #  y    6 A    '---      i    i+1    i  i+1      i+1  i
            #               n=0
            #
            # where A is the area:
            #           n-1
            #      1   ,---
            # A = ---   >     (x  y     -  x    y  )
            #      2   '---     i  i+1      i+1  i
            #           n=0
            # Note that the list of vertices wraps around so x[i+1] equals x[0].
            (xi, yi) = verts[i]
            (xi_1, yi_1) = verts[(i+1) % numVerts]
            t = (xi * yi_1) - (xi_1 * yi)
            area2 += t
            cx += (xi + xi_1) * t
            cy += (yi + yi_1) * t
        
        area = 0.5 * area2
        cx /= 6 * area
        cy /= 6 * area
        return [cx, cy]

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
        #edgeT_prev = 0.5 * (1.0 - self.edgeSeedInfo[edgeType_prev][-1][0])
        #edgeT = 0.5 * self.edgeSeedInfo[edgeType][0][0]

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

    def _getRegionVertices(self, sid):
        rid = self.vor.point_region[sid]
        vids = self.vor.regions[rid]
        return [self.vertices[vid] for vid in vids]

    # Return true if the points are in clockwise order.
    def isClockwise(self, sid):
        verts = self._getRegionVertices(sid)
        return isClockwise(verts)

    def area(self, sid):
        verts = self._getRegionVertices(sid)
        return area(verts)

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
            raise Exception(f"calculating clipped region for {sid}")

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
            r = self.sid2clippedRegion[sid]
            for rindex in range(0, len(r)):
                vid0 = r[rindex]
                vid1 = r[(rindex + 1) % len(r)]
                v0 = self.vertices[vid0]
                v1 = self.vertices[vid1]

                # Determin min edge length.
                minDistance = self.calcMinRidgeLength(vid0, vid1)
                # Ignore edges along the hex tile boundary (we can't adjust them).
                if self.isEdgeVertex(vid0) and self.isEdgeVertex(vid1):
                    continue
                # If this is one of the edges that is clipped by the hex tile
                # boundary, then scale down the min edge length (by 1/2).
                if self.isEdgeVertex(vid0) or self.isEdgeVertex(vid1):
                    # Scale min ridge len for ridges that cross the tile edge.
                    minDistance *= self.minRidgeLengthEdgeScale

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
    # Calculate the radius of the largest inscribed circle for each region.
    # Flag regions with a radius that is below the threshold.
    def findSmallRegions(self):
        self.regionCircles = {}
        self.tooSmallCircles = []
        self.minCircle = None
        self.maxCircle = None
    
        minCircleRadius = 0
        maxCircleRadius = 0
        for sid in range(0, self.endInteriorSeed):
            r = self.sid2region[sid]
            polyCenter = []
            polyRadius = 0

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

            if polyRadius < self.minInscribedCircleRadius:
                self.tooSmallCircles.append([sid, polyCenter, polyRadius])

    # Calculate and analyze the voronoi graph from the set of seed points.
    def generate(self):
        if self.vEdgeSeeds.size:
            self.seeds = np.concatenate((self.vHex, self.vEdgeSeeds))
        else:
            self.seeds = self.vHex
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

        self.analyze()
        
        if self.options['verbose_iteration']:
            self.printIteration(self.iteration if self.iteration > 0 else "START")
        if self.options['anim']:
            self.plot(self.iteration)
        self.iteration += 1
        
    def printIteration(self, i):
        print("Iteration", i, end='')
        print(" -", len(self.badEdges), "bad edges", end='')

        nTooClose = len(self.tooClose)
        if nTooClose > 0:
            print(" -", nTooClose, "seed pairs are too close", end='')
        
        nTooSmall = len(self.tooSmallCircles)
        if nTooSmall > 0:
            print(" -", nTooSmall, "regions are too small", end='')

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

        self.calcSid2Region()
        self.calcSid2ClippedRegion()

        # Ensure each region has a terrain type.
        for sid in range(len(self.seed2terrain), self.numActiveSeeds):
            self.calcTerrainType(sid)

        # Verify that all voronoi vertices are shared by 3 seed regions.
        # Note ignoring regions along outer edge which will have some vertices
        # shared by only 1 or 2 regions.
        # Note that this uses the vertices from the clipped regions.
        self.vid2sids = {}
        for sid in range(0, self.numActiveSeeds):
            for vid in self.sid2clippedRegion[sid]:
                if not vid in self.vid2sids:
                    self.vid2sids[vid] = []
                self.vid2sids[vid].append(sid)
        for k,v in self.vid2sids.items():
            if len(v) > 3:
                raise Exception("Vertex shared by more than 3 regions:", k, v)
        
        self.findBadEdges()
        self.findSmallRegions()
        self.findTooClose()

    def update(self):
        if self.iteration > self.maxIterations:
            self.successfulTileGeneration = False
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
            
        # Adjust regions that are too small.
        for smallCircleInfo in self.tooSmallCircles:
            sid, polyCenter, polyRadius = smallCircleInfo
            neighbors = self.calcNeighboringRegions(sid)

            if self.debug == sid:
                print(f"Region {sid} is too small (r={polyRadius}).")

            # Calc distance to each neighbor.
            dClosest = 1000
            dFurthest = 0
            for n in neighbors:
                d = dist(self.seeds[sid], self.seeds[n])
                if d > dFurthest:
                    dFurthest = d
                    sidFurthest = n
                if d < dClosest:
                    dClosest = d
                    sidClosest = n

            # Move the furthest neighbor closer and the closest one further to reshape
            # the region.
            self.calcAdjustment(sidFurthest, self.seeds[sid], self.adjustmentShrink)
            self.calcAdjustment(sidClosest, self.seeds[sid], self.adjustmentGrow)

            hasChanges = True

        # If we're making any adjustments, then relax the entire voronoi graph by moving
        # the seeds closer to their centroid.
        if hasChanges:
            for sid in range(0, self.numActiveSeeds):
                centroid = self.calcCentroid(sid)
                self.calcAdjustment(sid, centroid, self.centroidRelax)
                if self.debug == sid:
                    print(f"relaxing {sid} from {self.seeds[sid]} to {centroid} @ {self.centroidRelax}")
            
        # Apply the adjustments.
        newInterior = self.vInteriorSeeds.copy()
        numAdjustments = 0
        for sid in range(0, len(self.vInteriorSeeds)):
            if sid in self.adjustments:
                numAdjustments += 1
                if self.debug == sid:
                    print(f"Adjusting {sid} by {self.adjustments[sid]}")
                newInterior[sid][0] += self.adjustments[sid][0]
                newInterior[sid][1] += self.adjustments[sid][1]
        self.vInteriorSeeds = np.array(newInterior)

        if hasChanges and numAdjustments == 0:
            # This could happen when the only adjustable seeds are along the tile edge.
            raise Exception("Unable to make further adjustments")

        if not hasChanges:
            self.successfulTileGeneration = True
        return hasChanges

    def isEdgeVertex(self, vid):
        return vid >= self.firstEdgeVertex and vid < self.lastEdgeVertex

    def plot(self, plotId=None):
        plotter = VoronoiHexTilePlotter(self)
        plotter.plot(plotId)

    def calcBaseFilename(self):
        id = self.options['id']
        if id:
            return f"hex-{id:03d}"

        id = TILE_PATTERN_IDS[self.options['pattern']]
        suffix = ""
        if self.options['seed']:
            suffix = f"-{self.options['seed']}"
        return f"hex-{id:03d}{suffix}"

    def cleanupAnimation(self):
        out_dir = os.path.join(self.options['outdir_png_id'], self.options['anim_subdir'])
        anim_pngs = os.path.join(out_dir, '*.png')
        for png in glob.glob(anim_pngs):
            os.remove(png)

    def exportAnimation(self):
        anim_dir = os.path.join(self.options['outdir_png_id'], self.options['anim_subdir'])
        cmd = ["convert"]
        cmd.extend(["-delay", "15"])
        cmd.extend(["-loop", "0"])
        cmd.append(os.path.join(anim_dir, "hex-*"))

        base = self.calcBaseFilename()
        last_file = f"{base}-{self.iteration-1:03d}.png"
        cmd.extend(["-delay", "100"])
        cmd.append(os.path.join(anim_dir, last_file))

        anim_file = os.path.join(self.options['outdir_png_id'], f"{base}.gif")
        cmd.append(anim_file)

        subprocess.run(cmd)
