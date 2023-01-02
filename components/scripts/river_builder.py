
from ridge_builder import RidgeBuilder

class RiverBuilder(RidgeBuilder):
    def __init__(self, riverEdges, riverRidges, lakes, width):
        super().__init__(riverEdges, riverRidges, width)

        # Regions that are lakes.
        self.lakes = lakes
        
    def _post_analyze(self):
        pass

    def _regionLoopReverseCheck(self, ridgeKey, currV):
        # Rivers can also end when they reach a lake.
        for lake in self.lakes:
            if currV in self.sid2region[lake]:
                self.logger.log(f"found lake {lake} at vertex {currV}")
                return True
        return False
