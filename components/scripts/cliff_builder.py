
from map_common import calcSortedId, calcSortedIdFromPair
from ridge_builder import RidgeBuilder

class CliffBuilder(RidgeBuilder):
    def __init__(self, cliffEdges, cliffRidges, cliffEnds, width):
        super().__init__(cliffEdges, cliffRidges, cliffEnds, width)

        # Verify that cliff ends are not along the edge.
        for c in cliffEnds:
            if c in cliffEdges:
                raise Exception(f"Cliff ridge {c}: cannot end a cliff along the tile edge.")

    def _post_analyze(self):
        # Remove all the vertex overrides for the cliff ends so that they end in a point.
        self.logger.log("Cliff post_analyze:")
        self.logger.indent()
        for ridgeInfo in self.ridgeSegmentLoops:
            numRidges = len(ridgeInfo)
            for ir in range(numRidges):
                (seeds, verts) = ridgeInfo[ir]
                ridgeKey = calcSortedIdFromPair(seeds)
                
                # Look for case where loops reverses direction around a cliff end.
                if ridgeKey in self.ridgeEnds:
                    iPrev = (ir + numRidges - 1) % numRidges
                    (prevSeeds, prevVerts) = ridgeInfo[iPrev]
                    prevRidgeKey = calcSortedIdFromPair(prevSeeds)
                    if prevRidgeKey in self.ridgeEnds:
                        # Found the ridge were we just turned around a cliff end.
                        # Remove the vertex override for the last vertex of the cliff.
                        self.logger.log(f"Found cliff end - removing vert {verts[0]}")
                        self._removeVertexOverride(verts[0])
        self.logger.outdent()

    def _regionLoopReverseCheck(self, ridgeKey, currV):
        return ridgeKey in self.reverseRidges
