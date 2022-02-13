import getopt
import glob
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.spatial
import subprocess
import sys

from math_utils import (feq, fge, fle, scale,
                        lerp, lerp_pt, lerp_pt_delta, lerperp,
                        near, dist, dist_pt_line, ptInHex)
from svg import SVG, Style, Node, Path

GENERATE_SVG = True
GENERATE_PLOT = True
ANIM_SUBDIR = "anim"
ENABLE_SMALL_REGION_CHECK = False

NUM_SIDES = 6

EDGE_TYPES = ['1s', '2s', '2f', '3s', '3f', '4s']

# EdgeRegionInfo:
# Each dict entry contains an array of region heights, one per region on this
# side.
EDGE_REGION_INFO = {
    '1s': ['l', 'l', 'l'],
    '2s': ['l', 'l', 'l', 'l'],
    '2f': ['l', 'l', 'm', 'm'],  # +reversed
    '3s': ['m', 'm', 'm', 'm', 'm'],
    '3f': ['m', 'm', 'h', 'h', 'h'],  # +reversed
    '4s': ['h', 'h', 'm', 'm', 'h', 'h'],
}

# Edge seed info.
# Each dict entry contains an array of seed positions along the edge.
# Each seed position is:
#   [ offset-along-edge, perpendicular-offset ]
EDGE_SEED_INFO = {
    '1s': [[1/2, 0]],
    '2s': [[1/3, 0.03],   [2/3, -0.03]],
    '2f': [[0.35, 0.02],  [0.70, -0.03]],  # +reversed
    '3s': [[1/4, -0.03],  [2/4, 0],      [3/4, 0.03]],
    '3f': [[0.30, 0.02],  [0.55, 0],     [0.75, -0.03]],  # +reversed
    '4s': [[0.24, -0.02], [0.44, 0.02],  [0.56, -0.02],    [0.76, 0.02]],
}

# Minimum seed distance based on terrain type.
MIN_DISTANCE_L = 0.22
MIN_DISTANCE_M = 0.19
MIN_DISTANCE_H = 0.16

# Fill colors for regions based on terrain height.
REGION_STYLE = {
    'l': '#efecc6',
    'm': '#dcc382',
    'h': '#d69200',
}

class VoronoiHexTile():
    def __init__(self, options):
        self.options = options
        
        self.size = self.options['size']
        self.xMax = (math.sqrt(3) * self.size) / 2

        self.initEdgePattern(self.options['pattern'])
        
        # This is used to position the exterior seeds around the outside of the
        # tile. These seed regions constrain the regions in the hex tile and
        # allow us to ignore the outer edges (that go off to infinity).
        self.outerScale = 1.4

        self.seeds = None

        self.startCornerSeed = 0
        self.endCornerSeed = 0
        self.startEdgeSeed = 0
        self.endEdgeSeed = 0
        self.numActiveSeeds = 0

        # Number of candidates to generate and check around a seed before
        # giving up and marking the seed as complete.
        self.seedAttempts = 20
        
        # Min distance between 2 seed points.        
        self.minSeedDistance = 0.22 * self.size  # 2
        #self.minSeedDistance = 0.19 * self.size  # 3
        #self.minSeedDistance = 0.18 * self.size  # 4

        # The edgeMarginZone is a set of circles along the edge between the
        # seeds. They define an exclusion zone between the seeds so that the
        # voronoi vertex does not fall outside the hex tile boundary.
        self.edgeMarginZone = None
        # Margin scale of 1.0 means that voronoi ridges that cross the hex tile
        # edge can end exactly at the tile edge (which we don't want). Use a
        # value > 1.0 to enforce min length for these ridge segments.
        self.edgeMarginScale = 1.1

        # Min distance between 2 voronoi vertices along a ridge.
        self.minRidgeLength = 0.07 * self.size
        # Min ridge length along tile edge.
        self.minRidgeLengthEdge = 0.04 * self.size

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
        #     [ [ s0, s1], [s2, s3], ... ]
        # .ridge_vertices : array of vertex index pairs associated with each
        #     ridge
        #     [ [ v0, v1], [v2, v3], ... ]
        self.vor = None

        # Calculated voronoi vertices.
        self.vertices = None
        
        self.iteration = 0
        self.maxIterations = self.options['iter']

        # Adjustments to apply when we need to move a seed.
        # Each type of adjustment has a slightly different value so that if a
        # seed is being adjusted in multiple ways, it will still make progress
        # toward a goal.
        self.adjustmentSide = 0.011
        self.adjustmentNeighbor = -0.009
        self.adjustmentGrow = -0.005  # -0.006
        self.adjustmentShrink = 0.005

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

        self.rng = np.random.RandomState(self.options['seed'])

    def initEdgePattern(self, patternString):
        self.edgeTypes = patternString.split('-')
        if len(self.edgeTypes) != NUM_SIDES:
            print("Invalid pattern", patternString)
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
                error("Edge patterns don't connect: {0:s} ({1}) and {2:s} ({3})"
                        .format(edge, '-'.join(edgeRegionTypes),
                                edgeNext, '-'.join(edgeNextRegionTypes)))
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
            # Add info for middle regions (trim off corners at front/back).
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
        print("Center weight;", self.centerWeight)

    def init(self):
        self.initFixedSeeds()
        self.initEdgeMarginZone()
        self.initInteriorSeeds()
        self.initExteriorSeeds()

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
        
        # Calculate seeds along hex edges
        vertices = []
        for i0 in range(0, NUM_SIDES):
            i1 = (i0 + 1) % NUM_SIDES
            edgeType = self.edgeTypes[i0]
            seedPattern = EDGE_SEED_INFO[edgeType]
            for j in range(0, len(seedPattern)):
                t, perp_t = seedPattern[j]
                vertices.append(lerperp(self.vHex[i0], self.vHex[i1],
                                        t, perp_t))
        self.vEdgeSeeds = np.array(vertices)

    # Initialize the margin exclusion zones.
    # These zone prevent seeds from getting too close to the tile boundary where
    # they would cause voronoi ridges that are too small, or cause the region to
    # be clipped by the hex boundary.
    def initEdgeMarginZone(self):
        seeds = [self.vHex[0]]
        for i0 in range(0, NUM_SIDES):
            firstSeed = sum(self.nSeedsPerEdge[:i0])
            nEdgeSeeds = self.nSeedsPerEdge[i0]
            for j in range(firstSeed, firstSeed + nEdgeSeeds):
                seeds.append(self.vEdgeSeeds[j])
            i1 = (i0 + 1) % NUM_SIDES
            seeds.append(self.vHex[i1])
        
        # Create edge margin points between the seeds.
        marginPoints = []
        for i in range(0, len(seeds)-1):
            pt = lerp_pt(seeds[i], seeds[i+1], 0.5)
            size = self.edgeMarginScale * 0.5 * dist(seeds[i], seeds[i+1])
            marginPoints.append([pt, size])

        self.edgeMarginZone = marginPoints

    # Generate the interior seed points.
    def initInteriorSeeds(self):
        startSeeds = np.concatenate((self.vHex, self.vEdgeSeeds))

        # Calc mininum seed distance based on seed location.
        seed2minDistance = []
        for i in range(0, len(startSeeds)):
            seed2minDistance.append(self.calcSeedDistance(startSeeds[i]))

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
                if not ptInHex(self.size, seed[0], seed[1]):
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
                seed2minDistance.append(self.calcSeedDistance(seed))

        self.vInteriorSeeds = np.array(newSeeds)
        self.seed2minDistance = seed2minDistance

    # Calc the min seed distance based on the current seed location in the hex
    # tile. Seeds in higher density regions will have a smaller distance than
    # those in low density regions.
    # Assumes hexagon is centered at 0,0
    def calcSeedDistance(self, baseSeed):
        x, y = baseSeed
        # Find the triangle (in the hex) where the seed is located and compute
        # the barycentric coordinates of that point within the triangle. These
        # coordinates will be used as weights to calculate the min distance.
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
                # Seed is within current triangle, calculate weight.
                edgeType = self.nSeedsPerEdge[tri]
                w1 = self.cornerWeight[self.cornerType[tri]]
                w2 = self.cornerWeight[self.cornerType[tri_next]]
                w3 = self.centerWeight
                weight = a * w1 + b * w2 + c * w3
                return weight
        error("Unable to calculate seed distance for {0}".format(baseSeed))
        return 0
        
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

    def calcEdgeId(self, vid0, vid1):
        if vid0 < vid1:
            return "{0:d}-{1:d}".format(vid0, vid1)
        return "{0:d}-{1:d}".format(vid1, vid0)

    # Add a new vertex to the voronoi graph. This is used when clipping the
    # regions along the edge of the tile.
    def addVertex(self, v):
        # Check to see of we've added this vertex already.
        key = "{0:.6g}-{1:.6g}".format(v[0], v[1])
        if key in self.newVertices:
            return self.newVertices[key]
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

    # Calculate the 2 regions on either side of each vertex vid0-vid1.
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

    def calcAdjustment(self, sid, vMod, lerp_t):
        # Calc seed id in the interior seed array.
        sid -= self.startInteriorSeed
        if sid < 0:
            return

        v = self.vInteriorSeeds[sid]
        if not sid in self.adjustments:
            self.adjustments[sid] = [0,0]
        dx, dy = lerp_pt_delta(v, vMod, lerp_t)
        self.adjustments[sid][0] += dx
        self.adjustments[sid][1] += dy

    # Calculate all regions with clipping.
    def calcClippedRegions(self):
        self.sid2region = {}
        for sid in range(0, NUM_SIDES):
            rid = self.vor.point_region[sid]
            vids = self.calcCornerVertices(sid, rid)
            self.sid2region[sid] = vids
        for i0 in range(0, NUM_SIDES):
            i1 = (i0 + 1) % NUM_SIDES
            sid = NUM_SIDES + sum(self.nSeedsPerEdge[:i0])

            # Calc array of seed positions for this edge, including the corners:
            # [ 0, seeds..., 1 ]
            edgeType = self.edgeTypes[i0]
            seedPattern = EDGE_SEED_INFO[edgeType]
            edgeSeeds = [0]
            for p in seedPattern:
                edgeSeeds.append(p[0])
            edgeSeeds.append(1)

            for j in range(0, len(seedPattern)):
                rid = self.vor.point_region[sid + j]
                t0 = lerp(edgeSeeds[j], edgeSeeds[j+1], 0.5)
                t1 = lerp(edgeSeeds[j+1], edgeSeeds[j+2], 0.5)
                vids = self.calcEdgeVertices(i0, i1, rid, t0, t1)
                self.sid2region[sid+j] = vids

        for sid in range(self.startInteriorSeed, self.endInteriorSeed):
            rid = self.vor.point_region[sid]
            self.sid2region[sid] = self.vor.regions[rid]

    def calcCornerVertices(self, sid, rid):
        # Calc prev and next hex corner.
        sid_prev = (sid + NUM_SIDES - 1) % NUM_SIDES
        sid_next = (sid + 1) % NUM_SIDES

        # Calc |t| for each edge lerp, when starting from |sid|. 
        edgeType_prev = self.edgeTypes[sid_prev]
        edgeType = self.edgeTypes[sid]
        edgeDiv_prev = 0.5 * (1.0 - EDGE_SEED_INFO[edgeType_prev][-1][0])
        edgeDiv = 0.5 * EDGE_SEED_INFO[edgeType][0][0]

        return self.__calcEdgeVertices(rid, sid, sid_prev, sid_next,
                                       edgeDiv_prev, edgeDiv)

    def calcEdgeVertices(self, sid0, sid1, rid, t_ccw, t_cw):
        return self.__calcEdgeVertices(rid, sid0, sid1, sid1, t_ccw, t_cw)

    def __calcEdgeVertices(self, rid, sid, sid_prev, sid_next, t_ccw, t_cw):
        r = self.vor.regions[rid]
        verts = []
        # True if we need to generate the tile boundary for this region.
        genTileBounds = True
        internal = False
        for rindex in range(0, len(r)):
            vid = r[rindex]
            v = self.vertices[vid]
            if ptInHex(self.size, v[0], v[1]):
                verts.append(vid)
                internal = True
            elif genTileBounds:
                # Set to false so we don't generate the tile boundary twice.
                genTileBounds = False

                # Assume we're generating edge vertices in ccw order.
                # Note that the order of the vertices in the region (as returned
                # by the voronoi library) is not consistent, so we need to
                # determine which way we are moving around the polygon.
                startCcw = True
                ccw = lerp_pt(self.seeds[sid], self.seeds[sid_prev], t_ccw)
                cw = lerp_pt(self.seeds[sid], self.seeds[sid_next], t_cw)

                # Find closest internal vertex.
                if internal:
                    # i-1 is safe since we saw at least 1 internal vertex at this
                    # point.
                    v2 = self.vertices[r[rindex-1]]

                    # Swap direction if the region vertices are CW.
                    if dist(v2, cw) < dist(v2, ccw):
                        startCcw = False
                else:
                    # Look ahead to find next internal vertex. There must be at
                    # least one because we haven't seen any yet.
                    rindex2 = rindex+1
                    v2 = self.vertices[r[rindex2]]
                    while not ptInHex(self.size, v2[0], v2[1]):
                        rindex2 += 1
                        v2 = self.vertices[r[rindex2]]

                    # Swap direction if the region vertices are CCW.
                    if dist(v2, ccw) < dist(v2, cw):
                        startCcw = False

                if not startCcw:
                    cw, ccw = ccw, cw

                verts.append(self.addVertex(ccw))
                # Hex corners have an extra point in the middle.
                if sid_prev != sid_next:
                    verts.append(self.addVertex(self.seeds[sid]))
                verts.append(self.addVertex(cw))
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
                if vid0 >= self.firstNewVertex and vid1 >= self.firstNewVertex:
                    continue
                if vid0 >= self.firstNewVertex or vid1 >= self.firstNewVertex:
                    minDistance = self.minRidgeLengthEdge

                if near(v0, v1, minDistance):
                    edgeInfo = [vid0, vid1, sid]
                    edgeId = self.calcEdgeId(vid0, vid1)
                    if not edgeId in self.badEdges:
                        self.badEdges[edgeId] = []
                    self.badEdges[edgeId].append(edgeInfo)

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
                        if vid >= self.firstNewVertex:
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
        self.firstNewVertex = len(self.vertices)

        self.analyze()
        
        self.printIteration(self.iteration if self.iteration > 0 else "START")
        if self.options['anim']:
            self.plot(self.iteration)
        self.iteration += 1
        
    def printIteration(self, i):
        print("Iteration", i, end='')
        print(" -", len(self.badEdges), "bad edges", end='')

        if ENABLE_SMALL_REGION_CHECK:
            min = self.minCircle
            max = self.maxCircle
            if min and max:
                print(" - {0:d} {1:.5g} {2:d} {3:.5g}"
                      .format(min, self.regionCircles[min][1],
                              max, self.regionCircles[max][1]), end='')
                print(" - ratio {0:.5g}".format(self.circleRatio), end='')
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
            self.seed2minDistance.append(self.calcSeedDistance(self.seeds[i]))

        self.calcClippedRegions()

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
        if ENABLE_SMALL_REGION_CHECK:
            self.findSmallRegions()

    def update(self):
        if self.iteration > self.maxIterations:
            return False
        hasChanges = False
        self.adjustments = {}

        # Move seed toward short edge to make it longer.
        # |badEdges| is an array of bad edges:
        #   Each bad edge is an array identifying the 2 regions:
        #     [vertex-id0, vertex-id1, seed1-id], [vid0, vid1, seed2-id]
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

        # If there's too much difference between the largest and smallest circle,
        # adjust the regions that surround the min and max regions.
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
        
        newInterior = self.vInteriorSeeds.copy()
        for sid in range(0, len(self.vInteriorSeeds)):
            if sid in self.adjustments:
                newInterior[sid][0] += self.adjustments[sid][0]
                newInterior[sid][1] += self.adjustments[sid][1]
        self.vInteriorSeeds = np.array(newInterior)

        return hasChanges

    def plot(self, plotId=None):
        self.svg = SVG([210, 297])
        fig = plt.figure(figsize=(8,8))

        layer = self.svg.add_inkscape_layer('layer', "Layer")
        layer.set_transform("translate(105 148.5) scale(1, -1)")

        stroke = Style("none", "#000000", "1px")
        black_fill = Style("#000000", "none", "1px")
        
        # Draw clipped regions.
        layer_region_clip = self.svg.add_inkscape_layer(
            'region-clip', "Region Clipped", layer)
        for sid in range(0, self.numActiveSeeds):
            vids = self.sid2region[sid]
            id = "clipregion-{0:d}".format(sid)
            color = "#ffffff"
            if sid < len(self.seed2terrain):
                terrain_type = self.seed2terrain[sid]
                color = REGION_STYLE[terrain_type]
            self.plotRegion(vids, color)
            self.drawRegion(id, vids, color, layer_region_clip)

        # Plot regions and seeds.
        layer_region = self.svg.add_inkscape_layer('region', "Region", layer)
        layer_region.hide()
        layer_seeds = self.svg.add_inkscape_layer('seeds', "Seeds", layer)
        layer_seeds.hide()
        for sid in range(0, self.numActiveSeeds):
            rid = self.vor.point_region[sid]
            id = "region-{0:d}".format(sid)
            self.drawRegion(id, self.vor.regions[rid], "#ffffff", layer_region)

            center = self.seeds[sid]
            id = "seed-{0:d}".format(sid)
            plotCircle(id, center, '1', black_fill, layer_seeds)

        # Plot seed exclusion zones.
        layer_seed_ex = self.svg.add_inkscape_layer(
            'seed_exclusion', "Seed Exclusion", layer)
        layer_seed_ex.hide()
        fill = Style("#800000", "none", "1px")
        fill.set('fill-opacity', 0.15)
        for sid in range(0, self.numActiveSeeds):
            center = self.vor.points[sid]
            radius = self.seed2minDistance[sid]
            id = "seed-ex-{0:d}".format(sid)
            plotCircle(id, center, radius, fill, layer_seed_ex)

        # Plot edge margin exclusion zones.
        layer_margin_ex = self.svg.add_inkscape_layer(
            'margin_exclusion', "Margin Exclusion", layer)
        layer_margin_ex.hide()
        fill = Style("#000080", "none", "1px")
        fill.set('fill-opacity', 0.15)
        for mz in self.edgeMarginZone:
            center, radius = mz
            plotCircle(0, center, radius, fill, layer_margin_ex)
        
        if len(self.badEdges) != 0:
            layer_bad_edges = self.svg.add_inkscape_layer(
                'bad-edges', "Bad Edges", layer)
            for bei in self.badEdges:
                badEdge = self.badEdges[bei]
                vid0, vid1, rid = badEdge[0]
                self.plotVertex(self.vertices[vid0], layer_bad_edges)
                self.plotVertex(self.vertices[vid1], layer_bad_edges)

        # Plot inscribed circles for each region.
        if ENABLE_SMALL_REGION_CHECK:
            layer_circles = self.svg.add_inkscape_layer(
                'circles', "Inscribed Circles", layer)
            layer_circles.hide()
            fill = Style("#008000", "none", "1px")
            fill.set('fill-opacity', 0.15)
            for sid in self.regionCircles:
                center, radius = self.regionCircles[sid]
                id = "incircle-{0:d}".format(sid)
                plotCircle(id, center, radius, fill, layer_circles)

                id = "incircle-ctr-{0:d}".format(sid)
                plotCircle(id, center, '0.5', black_fill, layer_circles)
            if self.circleRatio > self.circleRatioThreshold:
                for c in [self.minCircle, self.maxCircle]:
                    center, radius = self.regionCircles[c]
                    circle = plt.Circle(center, radius, color="#80000080")
                    plt.gca().add_patch(circle)
            
        self.plotHexTileBorder(layer, stroke)
        
        out_dir = self.options['out']
        if self.options['seed'] == None:
            name = "hex"
        else:
            name = "hex-{0:d}".format(self.options['seed'])
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir);

        if plotId == None:
            out = os.path.join(out_dir, '%s.svg' % name)
            if GENERATE_SVG:
                self.svg.write(out)

            out = os.path.join(out_dir, '%s.png' % name)
        else:
            out_dir = os.path.join(out_dir, ANIM_SUBDIR)
            if not os.path.isdir(out_dir):
                os.makedirs(out_dir);
            out = os.path.join(out_dir, '{0:s}-{1:03d}'.format(name, plotId))
            plt.text(-self.size, -self.size, plotId)

        plt.axis("off")
        plt.xlim([x * self.size for x in [-1, 1]])
        plt.ylim([y * self.size for y in [-1, 1]])
        if GENERATE_PLOT:
            plt.savefig(out, bbox_inches='tight')
        plt.close(fig)

    def plotVertex(self, v, layer):
        circle = plt.Circle(v, 1, color="r")
        plt.gca().add_patch(circle)

        circle = SVG.circle(0, v[0], v[1], '2')
        circle.set_style(Style("#800000", "none", "1px"))
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
        p.set_style(Style(color, "#000000", "1px"))
        SVG.add_node(layer, p)

    def plotHexTileBorder(self, layer, style):
        p = Path()
        p.addPoints(self.vHex)
        p.end()
        p.set_style(style)
        SVG.add_node(layer, p)

    def cleanupAnimation(self):
        out_dir = os.path.join(self.options['out'], ANIM_SUBDIR)
        anim_pngs = os.path.join(out_dir, '*.png')
        for png in glob.glob(anim_pngs):
            os.remove(png)

    def exportAnimation(self):
        anim_dir = os.path.join(self.options['out'], ANIM_SUBDIR)
        cmd = ["convert"]
        cmd.extend(["-delay", "15"])
        cmd.extend(["-loop", "0"])
        cmd.append(os.path.join(anim_dir, "hex-*"))

        base = "hex"
        if self.options['seed'] != None:
            base = "hex-{0:d}".format(self.options['seed'])
        last_file = "{0:s}-{1:03d}.png".format(base, self.iteration-1)
        cmd.extend(["-delay", "100"])
        cmd.append(os.path.join(anim_dir, last_file))

        anim_file = os.path.join(self.options['out'], "{0:s}.gif".format(base))
        cmd.append(anim_file)

        subprocess.run(cmd)
        
def plotCircle(id, center, radius, fill, layer):
    circle = SVG.circle(id, center[0], center[1], radius)
    circle.set_style(fill)
    SVG.add_node(layer, circle)

def error(msg):
    print("ERROR:", msg)
    sys.exit(0)

OPTIONS = {
    'anim': {'type': 'bool', 'default': False,
             'desc': "Generate animation plots"},
    'center': {'type': 'string', 'default': None,
               'desc': "Terrain type for center of tile: l, m, h"},
    'iter': {'type': 'int', 'default': 25,
             'desc': "Max iterations"},
    'pattern': {'type': 'string', 'default': "2-2-2-2-2-2",
                'desc': "Edge pattern"},
    'seed': {'type': 'int', 'default': None,
             'desc': "Random seed"},
    'size': {'type': 'int', 'default': 80,
             'desc': "Size of hex side (mm)"},
}

def usage():
    print("python create-map.py <options>")
    for o in OPTIONS:
        opt = OPTIONS[o]
        print("  ", o, end=' ')
        if opt['type'] == 'int':
            print("<int>", end=' ')
        elif opt['type'] == 'string':
            print("<str>", end=' ')
        print("-", opt['desc'])
    sys.exit(0)

def parse_options():
    option_defs = {}
    option_defs.update(OPTIONS)
    short_opts = ""
    long_opts = []
    for opt,info in option_defs.items():
        if 'short' in info:
            short_opts += info['short']
            if info['type'] != 'bool':
                short_opts += ':'
        long_opt = opt
        if info['type'] != 'bool':
            long_opt += '='
        long_opts.append(long_opt)

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        usage()

    options = {}
    for opt,info in option_defs.items():
        options[opt] = info['default']
    options['out'] = "map-out"

    for opt,arg in opts:
        # Build list of short and fullname for this option.
        for opt_name, opt_info in option_defs.items():
            option_flags = []
            if 'short' in opt_info:
                option_flags.append('-{0}'.format(opt_info['short']))
            option_flags.append('--{0}'.format(opt_name))

            # If matches this option.
            if opt in option_flags:
                type = opt_info['type']
                if type == 'bool':
                    options[opt_name] = True
                elif type == 'int':
                    options[opt_name] = int(arg)
                else:
                    options[opt_name] = str(arg)

    return options

def main():
    options = parse_options()
    
    v = VoronoiHexTile(options)
    v.init()

    if options['anim']:
        v.cleanupAnimation()

    v.generate()
    while v.update():
        v.generate()
    v.plot()

    if options['anim']:
        v.exportAnimation()

if __name__ == '__main__':
    main()
