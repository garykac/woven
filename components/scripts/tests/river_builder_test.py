import pytest

from river_builder import RiverBuilder

#  0      10   15   20   25   30   35   40
# 
# 10            a         b         c
#               |         |         |
#           1   |    2    |    3    |   4
#            . .|. . . . .|. . . . .|. .
#            .  |         |         |  .
# 20   ----d====e====f----g----h----i----j----
#          | .       #         |       . |
#        5 | .  6    #    7    |    8  . | 9
#          | .       #         |       . |
#          | .       #         |       . |
# 30   ----k----l----m====n====o====p====q----
#            .  |         |         |  .
#            . .|. . . . .|. . . . .|. .
#          10   |   11    |   12    |   13
#               |         |         |
# 40            r         s         t
#
# a-t are the vertices of the voronoi ridges
# 1-12 are the voronoi regions (seed ids)
# Each ridge of the voronoi is specified by identifying the regions on either
# side of the ridge.
# The dotted square border is the tile boundary (NOT part of the voronoi).
# = and # show the path of a sample river through the tile (from d fo q).

# Vertex indices.
a = 101  # [15,10]
b = 102  # [25,10]
c = 103  # [35,10]

d = 104  # [10,20]
e = 105  # [15,20]
f = 106  # [20,20]
g = 107  # [25,20]
h = 108  # [30,20]
i = 109  # [35,20]
j = 110  # [40,20]

k = 111  # [10,30]
l = 112  # [15,30]
m = 113  # [20,30]
n = 114  # [25,30]
o = 115  # [30,30]
p = 116  # [35,30]
q = 117  # [40,30]

r = 118  # [15,40]
s = 119  # [25,40]
t = 120  # [35,40]

@pytest.fixture
def single_river():
    edges = ["1-6", "8-13"]
    ridges = ["1-6", "2-6", "6-7", "7-11", "7-12", "8-12", "8-13"]
    expect = [
        [d, e, f, m, n, o, p, q],
    ]
    return (edges, ridges, expect)

@pytest.fixture
def two_rivers():
    edges = [
        "1-6", "4-8",
        "6-10", "8-13"
    ]
    ridges = [
        "1-6", "2-6", "2-7", "3-7", "3-8", "4-8",
        "6-10", "6-11", "7-11", "7-12", "8-12", "8-13",
    ]
    expect = [
        [d, e, f, g, h, i, j],
        [k, l, m, n, o, p, q],
    ]
    return (edges, ridges, expect)

class FakeVoronoi:
    def __init__(self):
        # Array of seed index pairs for each ridge.
        self.ridge_points = [
            [1,2], [2,3], [3,4],
            [1,6], [2,6], [2,7], [3,7], [3,8], [4,8],
            [5,6], [6,7], [7,8], [8,9],
            [6,10], [6,11], [7,11], [7,12], [8,12], [8,13],
            [10,11], [11,12], [12,13],
        ]
        
        # Array of vertex pairs for each ridge.
        self.ridge_vertices = [
            [a,e], [b,g], [c,i],
            [d,e], [e,f], [f,g], [g,h], [h,i], [i,j],
            [d,k], [f,m], [h,o], [j,q],
            [k,l], [l,m], [m,n], [n,o], [o,p], [p,q],
            [l,r], [n,s], [p,t], 
        ]

def checkRiver(river_info):
    (edges, ridges, expect) = river_info
    rb = RiverBuilder(edges, ridges)
    rb.buildRidgeInfo(FakeVoronoi())
    rb.buildTransitions()
    verts = rb.getRiverVertices()
    assert len(verts) == len(expect)
    for ix in range(len(expect)):
        checkVertices(verts[ix], expect[ix])

def checkVertices(verts, expect):
    for ix in range(len(expect)):
        assert verts[ix] == expect[ix]

def test_singleRiver(single_river):
    checkRiver(single_river)

def test_twoRivers(two_rivers):
    checkRiver(two_rivers)
