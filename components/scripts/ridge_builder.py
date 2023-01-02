import copy

from logger import Logger
from map_common import calcSortedId, calcSortedIdFromPair
from math_utils import lerp_line, dist_pt_line, line_intersection_t, parallel_lines, isClockwise

# Bases class for handling special voronoi ridges.
class RidgeBuilder():
    def __init__(self, ridgeEdges, ridges, ridgeEnds, width):
        # The set of ridges that extend off the tile, so only 1 vertex links up with
        # other ridges.
        self.ridgeEdges = ridgeEdges

        # The set of all ridges that comprise this kind of special ridge on this tile.
        self.ridges = ridges

        # Ridges that end in the middle of the tile. Currently only used for cliffs.
        self.ridgeEnds = ridgeEnds
        
        # The set of ridges at the end of a ridge sequence, where we will loop around
        # to process the other direction.
        self.reverseRidges = self.ridgeEdges.copy() + self.ridgeEnds.copy()

        self.ridgeWidth = width

        self.logger = Logger()
        
        # Build dict of ridge segments that should be rivers.
        self.ridgeSegments = {}
        for r in ridges:
            self.ridgeSegments[r] = 1

        # Make sure river edges are defined where the tile needs them.
        for redge in ridgeEdges:
            (s0, s1) = redge.split('-')
            key = calcSortedId(s0, s1)
            if not key in self.ridgeSegments:
                raise Exception(f"Missing ridge edge segment {key}")
        
    def setTileInfo(self, sid2region):
        self.sid2region = sid2region

        self.vid2sids = {}
        for sid in range(len(sid2region)):
            for vid in sid2region[sid]:
                if not vid in self.vid2sids:
                    self.vid2sids[vid] = []
                self.vid2sids[vid].append(sid)
 
    def setVerbose(self, v):
        self.logger.setVerbose(v)
    
    def buildRidgeInfo(self, vor):
        self.logger.log(f"ridges: {self.ridges}")
        self.logger.log(f"ridgeEdges: {self.ridgeEdges}")
        self.logger.log(f"ridgeEnds: {self.ridgeEnds}")

        self._buildRidgeInfo(vor)
        self._buildBankInfo()
        self._buildRegionNeighbors()
    
    def _buildRidgeInfo(self, vor):
        self.vor = vor
        # Build dict of ridge keys ("#-#") -> id, seeds, vertices.
        self.ridgeInfo = {}
        self.v2ridges = {}  # Vertex id -> list of ridges with that vertex.
        n_ridges = len(vor.ridge_points)
        for i in range(0, n_ridges):
            (s0, s1) = vor.ridge_points[i]
            key = calcSortedId(s0, s1)
            if key in self.ridgeSegments:
                (vid0, vid1) = vor.ridge_vertices[i]
                self._appendToDictEntry(self.v2ridges, vid0, key)
                self._appendToDictEntry(self.v2ridges, vid1, key)
                self.ridgeInfo[key] = {
                    'ridge-id': i,
                    'seed-ids': [s0, s1],
                    'vertex-ids': [vid0, vid1],
                    }

        self.logger.log(f"ridgeInfo:")
        self.logger.indent()
        for key in self.ridgeInfo.keys():
            self.logger.log(f"{key}: {self.ridgeInfo[key]}")
        self.logger.outdent()

    def _appendToDictEntry(self, d, key, value):
        if not key in d:
            d[key] = []
        d[key].append(value)

	# Build struct to track river bank regions.
    def _buildBankInfo(self):
        self.bankInfo = {}
        for ridge in self.ridges:
            (s0, s1) = [int(x) for x in ridge.split('-')]
            if not s0 in self.bankInfo:
                self.bankInfo[s0] = []
            self.bankInfo[s0].append(s1)
            if not s1 in self.bankInfo:
                self.bankInfo[s1] = []
            self.bankInfo[s1].append(s0)

        self.logger.log(f"bankInfo:")
        self.logger.indent()
        for key in self.bankInfo.keys():
            self.logger.log(f"{key}: {self.bankInfo[key]}")
        self.logger.outdent()

    def _buildRegionNeighbors(self):
        self.sid2neighbors = {}    
        for seedId in range(len(self.sid2region)):
            vids = self.sid2region[seedId]
            sids = []
            for vid in vids:
                for sid in self.vid2sids[vid]:
                    if sid != seedId and not sid in sids:
                        sids.append(sid)
            self.sid2neighbors[seedId] = sids

        self.logger.log(f"sid2neighbors:")
        self.logger.indent()
        for key in self.sid2neighbors.keys():
            self.logger.log(f"{key}: {self.sid2neighbors[key]}")
        self.logger.outdent()

    def _findNextRidgeEdge(self):
        # Get next available ridge edge from the |ridges|.
        # We scan |ridges| from start each time so that we process the ridges in the
        # order that we specified them in the data file.
        for r in self.ridges:
            if r in self.reverseRidges:
                return r
        return None
    
    # Given a ridge, find the vertex that is not shared with another ridge.
    # This is typically used for river edges.
    def _findUnmatchedRidgeVertex(self, ridge):
        rInfo = self.ridgeInfo[ridge]
        for v in rInfo['vertex-ids']:
            if len(self.v2ridges[v]) == 1:
                return v
        return None
    
    # Each ridge has 2 vertices. Given a ridge and one vertex, return the other vertex.
    def _getRidgeOtherVert(self, ridge, vCurr):
        verts = self.ridgeInfo[ridge]['vertex-ids']
        for v in verts:
            if v != vCurr:
                return v
        return None

    def _isRidgeAtEnd(self, ridge):
        if ridge in self.reverseRidges:
            return True
        # The start edge is removed from |reverseRidges|, so we need to check it separately.
        if ridge == self.startEdge:
            return True
        return False

    def _regionLoopReverseCheck(self, ridgeKey, currV):
        # Subclass should override to handle special situations where the ridge ends and
        # _calcRegionLoops needs to change direction to handle the other side.
        pass

    # Get the loop of regions that define the outer boundary of the rivers.
    # Each region in the loop is identified by its seed-id and the seed-id of the
    # region on the opposite side of the river. These 2 seeds define the river ridge.
    # 
    # For example,
    #                 a         b         c
    #                 |         |         |
    #             1   |    2    |    3    |   4
    #              . .|. . . . .|. . . . .|. .
    #              .  |         |         |  .
    #     - - - -d====e====f----g----h----i----j- - - -
    #            : .       #         |       . :
    #       5    : .  6    #    7    |    8  . :    9
    #            : .       #         |       . :
    #            : .       #         |       . :
    #     - - - -k----l----m====n----o----p----q- - - -
    #              .  |         #         |  .
    #              . .|. . . . .#. . . . .|. .
    #            10   |   11    #   12    |   13
    #                 |         #         |
    #                 r         s         t
    # The river:
    #   d e f m n s
    # would have a region loop of:
    #    1 ( 6)    2 ( 6)    7 ( 6)    7 (11)   12 (11)
    #   11 (12)   11 ( 7)    6 ( 7)    6 ( 2)    6 ( 1)
    # where a (b) means a = seed-id, and b = opposite seed-id
    def _calcRegionLoops(self):
        self.logger.log(f"calcRegionLoops:")
        self.logger.indent()

        self.regionLoops = []
        while True:
            # Find a river edge to start.
            self.startEdge = self._findNextRidgeEdge()
            if self.startEdge == None:
                break
            vStart = self._findUnmatchedRidgeVertex(self.startEdge)
            self.logger.log(f"start edge: {self.startEdge}, off-tile vertex: {vStart}")

            self.reverseRidges.remove(self.startEdge)
            
            # Pick one of the seeds as a stating point.
            (currSeed, oppositeSeed) = self.ridgeInfo[self.startEdge]['seed-ids']
            currV = self._getRidgeOtherVert(self.startEdge, vStart)

            # Special case - directly from tile edge into a lake.
            # Note that cliff edges are not allowed to end immediately.
            if self._regionLoopReverseCheck("", currV):
                seedList = [[currSeed, oppositeSeed], [oppositeSeed, currSeed]]
                self.logger.log("direct from edge into lake")
                self.regionLoops.append(seedList)
                continue

            seedList = self._calcRegionLoop(self.startEdge, currV)
            self.regionLoops.append(seedList)

        self.logger.outdent()

    def _calcRegionLoop(self, startRidge, currV):
        (currSeed, oppositeSeed) = self.ridgeInfo[startRidge]['seed-ids']

        # Keep of list of seeds that have already been added.
        seedList = []
        
        done = False
        while not done:
            self.logger.log(f"curr seed: {currSeed}; vertex: {currV}")
            self.logger.indent()

            self.logger.log(f"adding {currSeed} ({oppositeSeed}) to loop")             
            seedList.append([currSeed, oppositeSeed])
            
            # Check the neighbors of the current vertex for a region that shares the
            # riverbank.
            found = False
            for n in self.vid2sids[currV]:
                if n == oppositeSeed or n == currSeed:
                    continue

                ridgeKey = calcSortedId(currSeed, n)
                self.logger.log(f"checking {currSeed} neighbor {n} with {ridgeKey}")

                # Check if we hit the end of a ridge sequence.
                foundEnd = False
                if self._isRidgeAtEnd(ridgeKey):
                    foundEnd = True

                # Does this neighbor have a ridge shared with the currSeed or
                # oppositeSeed?
                # Check |currSeed| first.
                if ridgeKey in self.ridges:
                    if n in self.sid2neighbors[oppositeSeed]:
                        self.logger.log(f"found opposite-side riverbank neighbor with {n} via {ridgeKey}")
                        oppositeSeed = n
                        found = True

                # Check |oppositeSeed| if we didn't find a match with |currSeed|.
                if not found:
                    ridgeKey = calcSortedId(oppositeSeed, n)
                    self.logger.log(f"checking {oppositeSeed} neighbor {n} with {ridgeKey}")
                    # Check ridges that cross the tile edge.
                    if self._isRidgeAtEnd(ridgeKey):
                        foundEnd = True
                    if ridgeKey in self.ridges:
                        self.logger.log(f"found same-side riverbank neighbor with {n} via {ridgeKey}")
                        currSeed = n
                        found = True

                if found:
                    self.logger.log(f"found {ridgeKey} {currV}")
                    if foundEnd:
                        # Switch to the other side of the river.
                        self.logger.log(f"Edge of tile - switching to other side")
                        self.logger.log(f"adding {currSeed} ({oppositeSeed}) to loop")             
                        seedList.append([currSeed, oppositeSeed])
                        (currSeed, oppositeSeed) = (oppositeSeed, currSeed)
                        # Note: |currV| stays the same since we switched direction.
                        if ridgeKey == self.startEdge:
                            done = True
                        else:
                            self.reverseRidges.remove(ridgeKey)
                    else:
                        currV = self._getRidgeOtherVert(ridgeKey, currV)

                    if self._regionLoopReverseCheck(ridgeKey, currV):
                        seedList.append([currSeed, oppositeSeed])
                        self.logger.log(f"Reversing ridge processing - switching to other side")
                        (currSeed, oppositeSeed) = (oppositeSeed, currSeed)
                        self.logger.log(f"new curr {currSeed}; opposite {oppositeSeed}; vertex: {currV}; {ridgeKey}")
                        # Switch the vertex back since we swapped it above.
                        currV = self._getRidgeOtherVert(ridgeKey, currV)

                    self.logger.outdent()
                    break

            if not found:
                raise Exception(f"Unable to find match for seed {currSeed} from vertex {currV}")
        
        return seedList

        
    # Calculate the line parallel to the ridge between |seedA| and |seedB|.
    # The parallel line should be distance |dist| away from the ridge.
    # Since there are 2 parallel lines that satisfy this condition, choose
    # the one closest to |seedA|.
    def _findInsetRidgeVertices(self, seedA, seedB, dist):
        ridgeKey = calcSortedId(seedA, seedB)
        (v0, v1) = self.ridgeInfo[ridgeKey]['vertex-ids']
        ridge = [self.vor.vertices[v0], self.vor.vertices[v1]]
        
        # Setting |dist| to 0 is only used by the unittests to make it easier to
        # verify the results.
        if dist == 0:
            return ridge

        # Calculate the 2 parallel ridges.
        (paraRidge1, paraRidge2) = parallel_lines(ridge, dist)

        # Determine which one is closer to |seedA|.
        ptA = self.vor.points[seedA]
        distA1 = dist_pt_line(ptA, paraRidge1)
        distA2 = dist_pt_line(ptA, paraRidge2)
        if distA1 < distA2:
            return paraRidge1
        return paraRidge2

    def _getRidgeVertexIds(self, seeds):
        (seedA, seedB) = seeds
        ridgeKey = calcSortedId(seedA, seedB)
        (v0, v1) = self.ridgeInfo[ridgeKey]['vertex-ids']
        return [v0, v1]  # Return a copy

    def _getInsetRidgeVerts(self, seedPair):
        (seedId, seedOpposite) = seedPair
        return self._findInsetRidgeVertices(seedId, seedOpposite, self.ridgeWidth / 2)

    def _calcInsetRidgeSegments(self, loopRegions):
        self.logger.log("_calcInsetRidgeSegments:")
        self.logger.indent()
        ridgeSegments = []
        numRegions = len(loopRegions)
        for rIndex in range(numRegions):
            (seedId, seedOpposite) = loopRegions[rIndex]
            self.logger.log(f"Seeds: {seedId} ({seedOpposite})")
            self.logger.indent()
            insetRidgeVerts = self._getInsetRidgeVerts(loopRegions[rIndex])
            self.logger.log(f"inset ridge: {insetRidgeVerts}")

            rIndexNext = (rIndex + 1) % numRegions
            rIndexPrev = (rIndex + numRegions - 1) % numRegions

            # Order the vertices to match the direction that we're
            # looping around the river.
            firstVertId = None
            lastVertId = None
            vids = self._getRidgeVertexIds(loopRegions[rIndex])
            vidsNext = self._getRidgeVertexIds(loopRegions[rIndexNext])
            # Calc vert in next ridge that is not in the current ridge.
            nextRidgeNewVertId = [x for x in vidsNext if not x in vids]

            self.logger.log(f"vert ids: {vids}")

            if len(nextRidgeNewVertId) == 0:
                # If the next ridge entirely overlaps with the current ridge, then
                # this is river edge (that exits the tile). So we'll need to check
                # the previous ridge to determine the correct order.
                vidsPrev = self._getRidgeVertexIds(loopRegions[rIndexPrev])
                prevRidgeNewVertId = [x for x in vidsPrev if not x in vids]
                if len(prevRidgeNewVertId) == 0:
                    # This means that the next ridge is the same as the previous ridge.
                    # This can happen with a single-ridge river. Force clockwise order.
                    # Create a triangle with seed + the 2 ridge points to check.
                    tri = [self.vor.points[seedId],
                        self.vor.vertices[vids[0]],
                        self.vor.vertices[vids[1]]]
                    if isClockwise(tri):
                        firstVertId = vids[0]
                        lastVertId = vids[1]
                    else:
                        firstVertId = vids[1]
                        lastVertId = vids[0]
                else:
                    # Find vertex shared with the previous ridge.
                    vidsPrev.remove(prevRidgeNewVertId[0])
                    firstVertId = vidsPrev[0]
                    lastVertId = [x for x in vids if x != firstVertId][0]
            else:
                # Find vertex shared with the next ridge.
                vidsNext.remove(nextRidgeNewVertId[0])
                lastVertId = vidsNext[0]
                # First vertex of this ridge is the one not shared with the next ridge.
                firstVertId = [x for x in vids if x != lastVertId][0]

            if vids[0] != firstVertId:
                insetRidgeVerts = insetRidgeVerts[::-1]
                self.logger.log(f"swapping vertex order: {insetRidgeVerts}")
            
            ridgeKey = calcSortedIdFromPair(loopRegions[rIndex])

            # Calc intersection point with the previous ridge (unless coming from edge).
            prevRidgeKey = calcSortedIdFromPair(loopRegions[rIndexPrev])
            if prevRidgeKey != ridgeKey:
                prevRidgeVerts = self._getInsetRidgeVerts(loopRegions[rIndexPrev])
                (t, tPrev) = line_intersection_t(insetRidgeVerts, prevRidgeVerts, True)
                pt = lerp_line(insetRidgeVerts, t)
                self._addVertexOverride(firstVertId, seedId, pt)
            else:
                self._addVertexOverride(firstVertId, seedId, insetRidgeVerts[0])

            # Calc intersection point with the next ridge (unless going into edge).
            nextRidgeKey = calcSortedIdFromPair(loopRegions[rIndexNext])
            if nextRidgeKey != ridgeKey:
                nextRidgeVerts = self._getInsetRidgeVerts(loopRegions[rIndexNext])
                (t, tPrev) = line_intersection_t(insetRidgeVerts, nextRidgeVerts, True)
                pt = lerp_line(insetRidgeVerts, t)
                self._addVertexOverride(lastVertId, seedId, pt)
            else:
                self._addVertexOverride(lastVertId, seedId, insetRidgeVerts[1])

            self.logger.outdent()

            ridgeSegments.append([[seedId, seedOpposite], [firstVertId, lastVertId]])
        self.logger.outdent()
        return ridgeSegments

    def _calcRidgeSegmentLoops(self):
        self.ridgeSegmentLoops = []
        self.vertexOverride = {}
        for loop in self.regionLoops:
            self.ridgeSegmentLoops.append(self._calcInsetRidgeSegments(loop))

    def _addVertexOverride(self, vid, sid, vert):
        if not vid in self.vertexOverride:
            self.vertexOverride[vid] = {}
        vidOverride = self.vertexOverride[vid]
        vidOverride[sid] = vert

    # Remove all overrides for the given vertex.    
    def _removeVertexOverride(self, vid):
        del self.vertexOverride[vid]

    def _getVertexForRegion(self, vid, sid):
        if vid in self.vertexOverride:
            overrides = self.vertexOverride[vid]
            if sid in overrides:
                return overrides[sid]
        return self.vor.vertices[vid]

    def analyze(self):
        self._calcRegionLoops()
        self._calcRidgeSegmentLoops()
        self._post_analyze()
        return self.vertexOverride

    def _post_analyze(self):
        # Subclass should override if needed
        pass

    def getRidgeVertices(self):
        self.logger.log("getRidgeVertices:")
        self.logger.indent()
        ridges = []
        for ridgeSegments in self.ridgeSegmentLoops:
            ridge = []
            numSegments = len(ridgeSegments)
            for iSeg in range(numSegments):
                seg = ridgeSegments[iSeg]
                self.logger.log(f"{seg}")
                (seeds, insetRidge) = seg
                (seedId, seedOpposite) = seeds

                iSegPrev = (iSeg + numSegments - 1) % numSegments
                segPrev = ridgeSegments[iSegPrev]
                (seedsPrev, insetRidgePrev) = segPrev

                # If we match the previous ridge, then we need to emit both vertices.
                if calcSortedIdFromPair(seeds) == calcSortedIdFromPair(seedsPrev):
                    ridge.append([seedId, insetRidge[0]])
                
                # Emit the 2nd vertex.
                ridge.append([seedId, insetRidge[1]])
            ridges.append(ridge)
        self.logger.outdent()
        self.logger.log(f"{ridges}")
        return ridges
