import copy

from logger import Logger

def calcSortedId(id0, id1):
    if int(id0) < int(id1):
        return f"{id0}-{id1}"
    return f"{id1}-{id0}"

class RiverBuilder():
    def __init__(self, riverEdges, riverRidges, lakes):
        # The set of river ridges that extend off the tile, so only 1 vertex links up with
        # other ridges.
        self.riverEdges = riverEdges.copy()

        # The set of all ridges that comprise the rivers on this tile.
        self.riverRidges = riverRidges.copy()

        # Regions that are lakes.
        self.lakes = lakes
        
        self.logger = Logger()
        
        # Build dict of ridge segments that should be rivers.
        self.riverSegments = {}
        for r in riverRidges:
            self.riverSegments[r] = 1

        # Make sure river edges are defined where the tile needs them.
        for redge in riverEdges:
            (s0, s1) = redge.split('-')
            key = calcSortedId(s0, s1)
            if not key in self.riverSegments:
                raise Exception(f"Missing river edge segment {key}")
        
        self.logger.log(f"riverEdges: {riverEdges}")
        self.logger.log(f"riverRidges: {riverRidges}")
        self.logger.log(f"lakes: {lakes}")
    
    def setTileInfo(self, sid2region):
        self.sid2region = sid2region

        self.vid2sids = {}
        for sid in range(1, len(sid2region)):
            for vid in sid2region[sid]:
                if not vid in self.vid2sids:
                    self.vid2sids[vid] = []
                self.vid2sids[vid].append(sid)
 
    def setVerbose(self, v):
        self.logger.setVerbose(v)
    
    def buildRiverInfo(self, vor):
        self._buildRidgeInfo(vor)
        self._buildBankInfo()
        self._buildRegionNeighbors()
    
    def _buildRidgeInfo(self, vor):
        # Build dict of ridge keys ("#-#") -> id, seeds, vertices.
        self.ridgeInfo = {}
        self.v2ridges = {}  # Vertex id -> list of ridges with that vertex.
        n_ridges = len(vor.ridge_points)
        for i in range(0, n_ridges):
            (s0, s1) = vor.ridge_points[i]
            key = calcSortedId(s0, s1)
            if key in self.riverSegments:
                (v0, v1) = vor.ridge_vertices[i]
                self._appendToDictEntry(self.v2ridges, v0, key)
                self._appendToDictEntry(self.v2ridges, v1, key)
                self.ridgeInfo[key] = {
                    'ridge-id': i,
                    'seeds': [s0, s1],
                    'verts': [v0, v1],
                    }

        self.logger.log(f"ridgeInfo:")
        self.logger.indent()
        for key in self.ridgeInfo.keys():
            self.logger.log(f"  {key}: {self.ridgeInfo[key]}")
        self.logger.outdent()

	# Build struct to track river bank regions.
    def _buildBankInfo(self):
        self.bankInfo = {}
        for ridge in self.riverRidges:
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
            self.logger.log(f"  {key}: {self.bankInfo[key]}")
        self.logger.outdent()

    def _buildRegionNeighbors(self):
        self.sid2neighbors = {}    
        for seedId in range(1, len(self.sid2region)):
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
            self.logger.log(f"  {key}: {self.sid2neighbors[key]}")
        self.logger.outdent()

    def _appendToDictEntry(self, d, key, value):
        if not key in d:
            d[key] = []
        d[key].append(value)

    def buildTransitions(self):
        # Start from one of the river edges and build the vertex connections.
        self.riverStarts = []
        self.riverEnds = []
        self.lakeEnds = []  # For rivers that end at a lake.
        # Dictionary of <vertex> -> list-of-vertices
        self.riverTransitions = {}

        # Save original river edges/ridges so they can be restored.
        origRiverEdges = copy.deepcopy(self.riverEdges)
        origRiverRidges = copy.deepcopy(self.riverRidges)
        origV2Ridges = copy.deepcopy(self.v2ridges)

        self.logger.log(f"buildTransitions:")
        self.logger.indent()

        while len(self.riverRidges) != 0:
            # Find a river edge to start.
            currEdge = self.findNextRiverEdge()
            if currEdge == None:
                break

            rInfo = self.ridgeInfo[currEdge]
            self.riverEdges.remove(currEdge)
            self.riverRidges.remove(currEdge)
            
            vStart = self.findUnmatchedRidgeVertex(currEdge)
            self.riverStarts.append(vStart)
            self.logger.log(f"start edge: {currEdge}, off-tile vertex: {vStart}")
            
            lakeCand = self.hasLakeConnection(currEdge, vStart)
            if lakeCand:
                (lakeId, vLake) = lakeCand
                self.logger.log(f"found direct lake match: {lakeId} @ {vLake}")
                self.riverTransitions[vStart] = [vLake]
                self.lakeEnds.append(vLake)
                self.logger.log(f"add transitions: {vStart} -> {vLake}")
                break

            newCandidates = self.findNextCandidates(currEdge, vStart)
            self.riverTransitions[vStart] = copy.copy(newCandidates)
            vCandidates = newCandidates

            self.logger.log(f"add start transitions: {vStart} -> {newCandidates}")

            while len(vCandidates) != 0:
                v = vCandidates.pop(0)
                ridges = self.v2ridges[v]
                self.logger.log(f"candidate from v: {v}, ridges: {ridges}")
                self.logger.indent()
                for r in ridges:
                    lakeCand = self.hasLakeConnection(r, v)
                    if lakeCand:
                        (lakeId, vLake) = lakeCand
                        self.logger.log(f"found lake match: {lakeId} @ {vLake}")
                        self.riverTransitions[v] = [vLake]
                        self.lakeEnds.append(vLake)
                        self.logger.log(f"add lake transitions: {v} -> {vLake}")
                    else:
                        newCandidates = self.findNextCandidates(r, v)
                        self.logger.log(f"ridge: {r}, new v candidates: {newCandidates}")
                        # If there aren't any vertex candidates.
                        if len(newCandidates) == 0:
                            # Check if the current ridge exits the tile.
                            if r in self.riverEdges:
                                verts = copy.copy(self.ridgeInfo[r]['verts'])
                                verts.remove(v)
                                self.riverEnds.append(verts[0])
                                self.riverEdges.remove(r)
                                self.riverTransitions[v] = copy.copy(verts)
                                self.logger.log(f"end river transition: {v} -> (off-tile){verts}")
                        else:
                            self.riverTransitions[v] = copy.copy(newCandidates)
                            vCandidates.extend(copy.copy(newCandidates))
                            self.logger.log(f"add transitions: {v} -> {newCandidates}")
                    self.riverRidges.remove(r)

                self.logger.outdent()
        self.logger.outdent()
        
        # Restore river edges/ridges.
        self.riverEdges = origRiverEdges
        self.riverRidges = origRiverRidges
        self.v2ridges = origV2Ridges

    def findNextRiverEdge(self):
        # Get next available river edge from the |rRidges|.
        # We scan |rRidges| from start each time so that we process the ridges in the
        # order that we specified them in the data file.
        for r in self.riverRidges:
            if r in self.riverEdges:
                return r
        return None
    
    # Given a ridge, find the vertex that is not shared with another ridge.
    # This is typically used for river edges.
    def findUnmatchedRidgeVertex(self, ridge):
        rInfo = self.ridgeInfo[ridge]
        for v in rInfo['verts']:
            if len(self.v2ridges[v]) == 1:
                return v
        return None
    
    # Given a |ridge| and a vertex |vStart| on that ridge, return the set of vertices that
    # have river ridges starting from |vStart|.
    def findNextCandidates(self, ridge, vStart):
        self.logger.log(f"find ridge candidates from {ridge}, starting from {vStart}")
        rInfo = self.ridgeInfo[ridge]
        nextVertCandidates = []
        self.logger.indent()
        for v in rInfo['verts']:
            if v == vStart:
                continue
            self.v2ridges[v].remove(ridge)
            if len(self.v2ridges[v]) != 0:
                nextVertCandidates.append(v)
            self.logger.log(f"removing ridge {ridge} and appending vertex {v}")
        self.logger.outdent()
        return nextVertCandidates

    # Given a |ridge| and a vertex |vStart| on that ridge, return the lake index of a
    # lake (if any) that the ridge connects to.
    def hasLakeConnection(self, ridge, vStart):
        self.logger.log(f"checking lakes from {ridge} starting from {vStart}")
        rInfo = self.ridgeInfo[ridge]
        for v in rInfo['verts']:
            if v == vStart:
                continue
            for lake in self.lakes:
                if v in self.sid2region[lake]:
                    self.v2ridges[v].remove(ridge)
                    return (lake, v)
        return None

    def isRiverEndPoint(self, v):
        if v in self.riverEnds:
            return True
        if v in self.lakeEnds:
            return True
        return False

    def getRiverVertices(self):
        self.logger.log(f"transitions: {self.riverTransitions}")
        rivers = []
        for start in self.riverStarts:
            r = []
            v = start
            while not self.isRiverEndPoint(v):
                r.append(v)
                v = self.riverTransitions[v][0]
            r.append(v)
            rivers.append(r)
        return rivers

    # Each ridge has 2 vertices. Given a ridge and one vertex, return the other vertex.
    def _getRidgeOtherVert(self, ridge, vCurr):
        verts = self.ridgeInfo[ridge]['verts']
        for v in verts:
            if v != vCurr:
                return v
        return None

    def _isRiverAtTileEdge(self, ridge):
        # Rivers can end when they exit a tile edge.
        if ridge in self.riverEdges:
            return True
        # The start edge is removed from |riverEdges|, so we need to check it separately.
        if ridge == self.startEdge:
            return True
        return False

    def _isRiverAtLake(self, v):
        # Rivers can also end when they reach a lake.
        for lake in self.lakes:
            if v in self.sid2region[lake]:
                self.logger.log(f"found lake {lake} at vertex {v}")
                return True
        return False

    # Get the loop of regions that define the outer boundary of the rivers.
    def calcRegionLoop(self):
        self.logger.log(f"calcRegionLoops:")
        self.logger.indent()
        loops = []
        while True:
            # Find a river edge to start.
            self.startEdge = self.findNextRiverEdge()
            if self.startEdge == None:
                break
            vStart = self.findUnmatchedRidgeVertex(self.startEdge)
            self.logger.log(f"start edge: {self.startEdge}, off-tile vertex: {vStart}")

            self.riverEdges.remove(self.startEdge)
            
            # Pick one of the seeds as a stating point.
            (currSeed, oppositeSeed) = self.ridgeInfo[self.startEdge]['seeds']
            currV = self._getRidgeOtherVert(self.startEdge, vStart)

            # Special case - directly from tile edge into a lake.
            if self._isRiverAtLake(currV):
                seedList = [[currSeed, oppositeSeed], [oppositeSeed, currSeed]]
                loops.append(seedList)
                continue

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

                    # Check if we hit the edge of a tile.
                    foundEdge = False
                    if self._isRiverAtTileEdge(ridgeKey):
                        foundEdge = True

                    # Does this neighbor have a river ridge shared with the currSeed or
                    # oppositeSeed?
                    # Check |currSeed| first.
                    if ridgeKey in self.riverRidges:
                        if n in self.sid2neighbors[oppositeSeed]:
                            self.logger.log(f"found opposite-side riverbank neighbor with {n} via {ridgeKey}")
                            oppositeSeed = n
                            found = True

                    # Check |oppositeSeed| if we didn't find a match with |currSeed|.
                    if not found:
                        ridgeKey = calcSortedId(oppositeSeed, n)
                        self.logger.log(f"checking {oppositeSeed} neighbor {n} with {ridgeKey}")
                        # Check ridges that cross the tile edge.
                        if self._isRiverAtTileEdge(ridgeKey):
                            foundEdge = True
                        if ridgeKey in self.riverRidges:
                            self.logger.log(f"found same-side riverbank neighbor with {n} via {ridgeKey}")
                            currSeed = n
                            found = True

                    if found:
                        self.logger.log(f"found {ridgeKey} {currV}")
                        if foundEdge:
                            # Switch to the other side of the river.
                            self.logger.log(f"Edge of tile - switching to other side")
                            self.logger.log(f"adding {currSeed} ({oppositeSeed}) to loop")             
                            seedList.append([currSeed, oppositeSeed])
                            (currSeed, oppositeSeed) = (oppositeSeed, currSeed)
                            # Note: |currV| stays the same since we switched direction.
                            if ridgeKey == self.startEdge:
                                done = True
                            else:
                                self.riverEdges.remove(ridgeKey)
                        else:
                            currV = self._getRidgeOtherVert(ridgeKey, currV)

                        if self._isRiverAtLake(currV):
                            self.logger.log(f"River enters lake - switching to other side")
                            (currSeed, oppositeSeed) = (oppositeSeed, currSeed)
                            self.logger.log(f"new curr {currSeed}; opposite {oppositeSeed}; vertex: {currV}; {ridgeKey}")
                            seedList.append([currSeed, oppositeSeed])
                            # Switch the vertex back since we swapped it above.
                            currV = self._getRidgeOtherVert(ridgeKey, currV)

                        self.logger.outdent()
                        break

                if not found:
                    raise Exception(f"Unable to find match for seed {currSeed} from vertex {currV}")

            loops.append(seedList)

        self.logger.outdent()

        return loops
