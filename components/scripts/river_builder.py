import copy

def calcSortedId(id0, id1):
    if int(id0) < int(id1):
        return f"{id0}-{id1}"
    return f"{id1}-{id0}"

class RiverBuilder():
    def __init__(self, riverEdges, riverRidges):
        # The set of river ridges that extend off the tile, so only 1 vertex links up with
        # other ridges.
        self.riverEdges = riverEdges

        # The set of all ridges that comprise the rivers on this tile.
        self.riverRidges = riverRidges

        self.verbose = False
        
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
        	print(self.ridgeInfo)

    def _appendToDictEntry(self, d, key, value):
        if not key in d:
            d[key] = []
        d[key].append(value)

    def buildTransitions(self):
        # Start from one of the river edges and build the vertex connections.
        self.riverStarts = []
        self.riverEnds = []
        # Dictionary of <vertex> -> list-of-vertices
        self.riverTransitions = {}

        while len(self.riverRidges) != 0:
            # Find a river edge to start.
            currEdge = self.findNextRiverEdge()
            if currEdge == None:
                break

            rInfo = self.ridgeInfo[currEdge]
            self.riverEdges.remove(currEdge)
            self.riverRidges.remove(currEdge)
            
            startV = self.findUnmatchedRidgeVertex(currEdge)
            self.riverStarts.append(startV)
            
            newCandidates = self.findNextCandidates(currEdge, startV)
            self.riverTransitions[startV] = copy.copy(newCandidates)
            vCandidates = newCandidates

            while len(vCandidates) != 0:
                v = vCandidates.pop(0)
                ridges = self.v2ridges[v]
                for r in ridges:
                    newCandidates = self.findNextCandidates(r, v)
                    if len(newCandidates) == 0:
                        if r in self.riverEdges:
                            verts = copy.copy(self.ridgeInfo[r]['verts'])
                            verts.remove(v)
                            self.riverEnds.append(verts[0])
                            self.riverEdges.remove(r)
                            self.riverTransitions[v] = copy.copy(verts)
                    else:
                        self.riverTransitions[v] = copy.copy(newCandidates)
                        vCandidates.extend(copy.copy(newCandidates))
                    self.riverRidges.remove(r)

    def findNextCandidates(self, ridge, v):
        rInfo = self.ridgeInfo[ridge]
        nextVertCandidates = []
        for v in rInfo['verts']:
            self.v2ridges[v].remove(ridge)
            if len(self.v2ridges[v]) != 0:
                nextVertCandidates.append(v)
        return nextVertCandidates

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
    
    def getRiverVertices(self):
        rivers = []
        for start in self.riverStarts:
            r = []
            v = start
            while not v in self.riverEnds:
                r.append(v)
                # TODO: Add support for tiles with 1 edge river (eg. with a lake)
                if len(self.riverTransitions[v]) == 0:
                    return []
                v = self.riverTransitions[v][0]
            r.append(v)
            rivers.append(r)
        return rivers
        
