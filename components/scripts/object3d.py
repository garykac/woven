
class Object3d():
    def __init__(self):
        self.reset()
	
    def reset(self):
        self.vertices = []
        self.numVertices = 0

        self.faces = []
        self.numFaces = 0

    def open(self, outfile):
        self.fout = open(outfile, "w")

    def close(self):
        self.fout.close()
        
    def addVertex(self, v):
        self.vertices.append(v)
        self.numVertices += 1
        return self.numVertices

    def addFace(self, f):
        self.faces.append(f)
        self.numFaces += 1
        return self.numFaces

    def writeGroup(self, name):
        self.fout.write("o {0}\n".format(name))
    
        for v in self.vertices:
            self.fout.write("v {0:.05g} {1:.05g} {2:.05g}\n".format(v[0], v[1], v[2]))
    
        for face in self.faces:
            rel = [str(x - 1 - self.numVertices) for x in face]
            self.fout.write("f {0:s}\n".format(' '.join(rel)))

        self.reset()		
