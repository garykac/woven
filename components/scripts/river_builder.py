import copy

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
        
        self.verbose = False
        self.log_indent = 0
        
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
        
        if self.verbose:
            self.log(f"riverEdges: {riverEdges}")
            self.log(f"riverRidges: {riverRidges}")
            self.log(f"lakes: {lakes}")
    
    def setTileInfo(self, sid2region):
        self.sid2region = sid2region
 
    def log(self, msg):
        if self.verbose:
            print(f"{'  ' * self.log_indent}{msg}")

    def logindent(self, n):
        self.log_indent += n
    
    def buildRidgeInfo(self, vor):
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
        if self.verbose:
            self.log(f"ridgeInfo:")
            self.logindent(1)
            for key in self.ridgeInfo.keys():
                self.log(f"  {key}: {self.ridgeInfo[key]}")
            self.logindent(-1)

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

        self.log(f"buildTransitions:")
        self.logindent(1)

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
            self.log(f"start edge: {currEdge}, off-tile vertex: {vStart}")
            
            lakeCand = self.hasLakeConnection(currEdge, vStart)
            if lakeCand:
                (lakeId, vLake) = lakeCand
                self.log(f"found direct lake match: {lakeId} @ {vLake}")
                self.riverTransitions[vStart] = [vLake]
                self.lakeEnds.append(vLake)
                self.log(f"add transitions: {vStart} -> {vLake}")
                break

            newCandidates = self.findNextCandidates(currEdge, vStart)
            self.riverTransitions[vStart] = copy.copy(newCandidates)
            vCandidates = newCandidates

            self.log(f"add start transitions: {vStart} -> {newCandidates}")

            while len(vCandidates) != 0:
                v = vCandidates.pop(0)
                ridges = self.v2ridges[v]
                self.log(f"candidate from v: {v}, ridges: {ridges}")
                self.logindent(1)
                for r in ridges:
                    lakeCand = self.hasLakeConnection(r, v)
                    if lakeCand:
                        (lakeId, vLake) = lakeCand
                        self.log(f"found lake match: {lakeId} @ {vLake}")
                        self.riverTransitions[v] = [vLake]
                        self.lakeEnds.append(vLake)
                        self.log(f"add lake transitions: {v} -> {vLake}")
                    else:
                        newCandidates = self.findNextCandidates(r, v)
                        self.log(f"ridge: {r}, new v candidates: {newCandidates}")
                        # If there aren't any vertex candidates.
                        if len(newCandidates) == 0:
                            # Check if the current ridge exits the tile.
                            if r in self.riverEdges:
                                verts = copy.copy(self.ridgeInfo[r]['verts'])
                                verts.remove(v)
                                self.riverEnds.append(verts[0])
                                self.riverEdges.remove(r)
                                self.riverTransitions[v] = copy.copy(verts)
                                self.log(f"end river transition: {v} -> (off-tile){verts}")
                        else:
                            self.riverTransitions[v] = copy.copy(newCandidates)
                            vCandidates.extend(copy.copy(newCandidates))
                            self.log(f"add transitions: {v} -> {newCandidates}")
                        self.riverRidges.remove(r)

                self.logindent(-1)
        self.logindent(-1)

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
        self.log(f"find ridge candidates from {ridge}, starting from {vStart}")
        rInfo = self.ridgeInfo[ridge]
        nextVertCandidates = []
        self.logindent(1)
        for v in rInfo['verts']:
            if v == vStart:
                continue
            self.v2ridges[v].remove(ridge)
            if len(self.v2ridges[v]) != 0:
                nextVertCandidates.append(v)
            self.log(f"removing ridge {ridge} and appending vertex {v}")
        self.logindent(-1)
        return nextVertCandidates

    # Given a |ridge| and a vertex |vStart| on that ridge, return the lake index of a
    # lake (if any) that the ridge connects to.
    def hasLakeConnection(self, ridge, vStart):
        self.log(f"checking lakes from {ridge} starting from {vStart}")
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
        self.log(f"transitions: {self.riverTransitions}")
        rivers = []
        for start in self.riverStarts:
            r = []
            v = start
            while not self.isRiverEndPoint(v):
                r.append(v)
                # TODO: Add support for tiles with 1 edge river (eg. with a lake)
                if len(self.riverTransitions[v]) == 0:
                    return []
                v = self.riverTransitions[v][0]
            r.append(v)
            rivers.append(r)
        return rivers
