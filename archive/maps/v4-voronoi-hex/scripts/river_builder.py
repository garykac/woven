
from ridge_builder import RidgeBuilder

class RiverBuilder(RidgeBuilder):
    def __init__(self, riverEdges, riverRidges, riverEnds, lakes, width):
        super().__init__(riverEdges, riverRidges, riverEnds, width)

        # Regions that are lakes.
        self.lakes = lakes
        
        self.lakeVertices = {}
        
    def _post_analyze(self):
        pass

    # Return a list of vertices associated with the lakes.
    def _getKnownVertices(self):
        verts = []
        for lake in self.lakes:
            for v in self.sid2region[lake]:
                verts.append(v)
        return verts

    def _regionLoopReverseCheck(self, ridgeKey, currV):
        # Rivers can also end when they reach a lake.
        self.logger.log(f"regionLoopReverseCheck: {ridgeKey} {currV}")
        for lake in self.lakes:
            self.logger.log(f"  checking lake: {lake}: {self.sid2region[lake]}")
            if currV in self.sid2region[lake]:
                self.logger.log(f"found lake {lake} at vertex {currV}")
                self.lakeVertices[currV] = ridgeKey
                return True
        return False
