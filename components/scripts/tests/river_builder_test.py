import pytest

from river_builder import RiverBuilder

#      0    5   10   15   20   25   30   35   40   45   50
# 
# 10   ax - - - - - - a - - - - b - - - - c - - - - - - cx
#       :             |         |         |             :
#       :         1   |    2    |    3    |   4         :
#       :          . .|. . . . .|. . . . .|. .          :
#       :          .  |         |         |  .          :
# 20   dx - - - -d====e====f----g----h----i----j- - - - jx
#       :        | .       #         |       . |        :
#       :   5    | .  6    #    7    |    8  . |    9   :
#       :        | .       #         |       . |        :
#       :        | .       #         |       . |        :
# 30   kx - - - -k----l----m====n====o====p====q- - - - qx
#       :          .  |         |         |  .          :
#       :          . .|. . . . .|. . . . .|. .          :
#       :        10   |   11    |   12    |   13        :
#       :             |         |         |             :
# 40   rx - - - - - - r - - - - s - - - - t - - - - - - tx
#
# a-t are the vertices of the voronoi ridges.
# ax-tx are extra vertices that are used only to complete the outer regions.
# 1-12 are the voronoi seed ids.
#
# Each ridge of the voronoi is specified by identifying the regions on either
# side of the ridge (using seed ids). So the ridge a-e is specified as 1-2
# since 1 and 2 are the seed ids of the regions on either side of the ridge.
# The lowest numbered region is always given first.
#
# The dotted (.) square border is the tile boundary (NOT part of the voronoi).
# It acts as a clipping region for the voronoi. "River edges" are ridges where
# the river passes through this clipping boundary.
#
# = and # show the path of a sample river through the tile (from d fo q).
#
# The relevant (tile intersecting) voronoi ridges are '-' and '|'.
#
# Other (outer) voronoi edges are indicated with '- -' and ':'.
# Note that these are clipped by the tile boundary ('. . .').

# Vertex indices.
(a,b,c) = (1,2,3)
(d,e,f,g,h,i,j) = (4,5,6,7,8,9,10)
(k,l,m,n,o,p,q) = (11,12,13,14,15,16,17)
(r,s,t) = (18,19,20)
# Outside vertex indices.
(ax,cx,dx,jx,kx,qx,rx,tx) = (21,22,23,24,25,26,27,28)

@pytest.fixture
def single_river():
    edges = ["1-6", "8-13"]
    ridges = ["1-6", "2-6", "6-7", "7-11", "7-12", "8-12", "8-13"]
    lakes = []
    vertex_expect = [
        [d, e, f, m, n, o, p, q],
    ]
    loop_expect = [
        [
            [1, 6], [2, 6], [7, 6], [7, 11], [7, 12], [8, 12], [8, 13],
            [13, 8], [12, 8], [12, 7], [11, 7], [6, 7], [6, 2], [6, 1]
        ],
    ]
    return (edges, ridges, lakes, vertex_expect, loop_expect)

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
    lakes = []
    vertex_expect = [
        [d, e, f, g, h, i, j],
        [k, l, m, n, o, p, q],
    ]
    loop_expect = [
        [
            [1, 6], [2, 6], [2, 7], [3, 7], [3, 8], [4, 8],
            [8, 4], [8, 3], [7, 3], [7, 2], [6, 2], [6, 1]
        ], [
            [6, 10], [6, 11], [7, 11], [7, 12], [8, 12], [8, 13],
            [13, 8], [12, 8], [12, 7], [11, 7], [11, 6], [10, 6]
        ]
    ]
    return (edges, ridges, lakes, vertex_expect, loop_expect)

@pytest.fixture
def with_lake():
    edges = [
        "1-6",
    ]
    ridges = [
        "1-6", "2-6",
    ]
    lakes = [ 7 ]
    vertex_expect = [
        [d, e, f],
    ]
    loop_expect = [
        [
            [1, 6], [6, 2], [6, 2], [6, 1]
        ]
    ]
    return (edges, ridges, lakes, vertex_expect, loop_expect)

@pytest.fixture
def direct_into_lake():
    edges = [
        "2-3",
    ]
    ridges = [
        "2-3",
    ]
    lakes = [ 7 ]
    vertex_expect = [
        [b, g],
    ]
    loop_expect = [
        [
            [2, 3], [3, 2]
        ]
    ]
    return (edges, ridges, lakes, vertex_expect, loop_expect)

class FakeVoronoi:
    def __init__(self):
        # Vertices.
        (vA,vB,vC) = ([15,10],[25,10],[35,10])
        (vD,vE,vF,vG,vH,vI,vJ) = ([10,20],[15,20],[20,20],[25,20],[30,20],[35,20],[40,20])
        (vK,vL,vM,vN,vO,vP,vQ) = ([10,30],[15,30],[20,30],[25,30],[30,30],[35,30],[40,30])
        (vR,vS,vT) = ([15,40],[25,40],[35,40])

        # Seed indices.
        (s1,s2,s3,s4) = (1,2,3,4)
        (s5,s6,s7,s8,s9) = (5,6,7,8,9)
        (s10,s11,s12,s13) = (10,11,12,13)

        # Region indices.
        (r1,r2,r3,r4) = (1,2,3,4)
        (r5,r6,r7,r8,r9) = (5,6,7,8,9)
        (r10,r11,r12,r13) = (10,11,12,13)
        
        # Seed points (not used).
        self.points = []
        
        # Mapping from seed ids to region ids.
        self.point_region = list(range(0,14))

        self.vertices = [
            [0,0],  # Index 0 unused
            vA,vB,vC,
            vD,vE,vF,vG,vH,vI,vJ,
            vK,vL,vM,vN,vO,vP,vQ,
            vR,vS,vT,
        ]

        self.regions = [
            [],             # Index 0 unused
            [a,e,d,dx,ax],  # r1
            [a,b,g,f,e],    # r2
            [b,c,i,h,g],    # r3
            [c,cx,jx,j,i],  # r4
            [d,k,kx,dx],    # r5
            [d,e,f,m,l,k],  # r6
            [f,g,h,o,n,m],  # r7
            [h,i,j,q,p,o],  # r8
            [j,jx,qx,q],    # r9
            [k,l,r,rx,kx],  # r10
            [l,m,n,s,r],    # r11
            [n,o,p,t,s],    # r12
            [p,q,qx,tx,t],  # r13
        ]

        # Array of seed index pairs for each ridge.
        self.ridge_points = [
            [s1,s2], [s2,s3], [s3,s4],
            [s1,s6], [s2,s6], [s2,s7], [s3,s7], [s3,s8], [s4,s8],
            [s5,s6], [s6,s7], [s7,s8], [s8,s9],
            [s6,s10], [s6,s11], [s7,s11], [s7,s12], [s8,s12], [s8,s13],
            [s10,s11], [s11,s12], [s12,s13],
        ]
        
        # Array of vertex pairs for each ridge.
        self.ridge_vertices = [
            [a,e], [b,g], [c,i],
            [d,e], [e,f], [f,g], [g,h], [h,i], [i,j],
            [d,k], [f,m], [h,o], [j,q],
            [k,l], [l,m], [m,n], [n,o], [o,p], [p,q],
            [l,r], [n,s], [p,t], 
        ]

class FakeHexTile():
    def __init__(self):
        self.sid2region = [
            [],             # Index 0 unused
            [a,e,d,dx,ax],  # s1
            [a,b,g,f,e],    # s2
            [b,c,i,h,g],    # s3
            [c,cx,jx,j,i],  # s4
            [d,k,kx,dx],    # s5
            [d,e,f,m,l,k],  # s6
            [f,g,h,o,n,m],  # s7
            [h,i,j,q,p,o],  # s8
            [j,jx,qx,q],    # s9
            [k,l,r,rx,kx],  # s10
            [l,m,n,s,r],    # s11
            [n,o,p,t,s],    # s12
            [p,q,qx,tx,t],  # s13
        ]

def checkRiverVertices(river_info):
    (edges, ridges, lakes, vertex_expect, loop_expect) = river_info
    tile = FakeHexTile()
    rb = RiverBuilder(edges, ridges, lakes)
    rb.setVerbose(True)
    rb.setTileInfo(tile.sid2region)
    rb.buildRiverInfo(FakeVoronoi())
    rb.buildTransitions()
    verts = rb.getRiverVertices()
    assert len(verts) == len(vertex_expect)
    for ix in range(len(vertex_expect)):
        checkVertices(verts[ix], vertex_expect[ix])

def checkVertices(verts, vertex_expect):
    for ix in range(len(vertex_expect)):
        assert verts[ix] == vertex_expect[ix]

def test_riverVertices_singleRiver(single_river):
    checkRiverVertices(single_river)

def test_riverVertices_twoRivers(two_rivers):
    checkRiverVertices(two_rivers)

def test_riverVertices_lake(with_lake):
    checkRiverVertices(with_lake)

def test_riverVertices_direct_into_lake(direct_into_lake):
    checkRiverVertices(direct_into_lake)

def checkRiverBanks(river_info):
    (edges, ridges, lakes, vertex_expect, loop_expect) = river_info
    tile = FakeHexTile()
    rb = RiverBuilder(edges, ridges, lakes)
    rb.setVerbose(True)
    rb.setTileInfo(tile.sid2region)
    rb.buildRiverInfo(FakeVoronoi())

    rb.setVerbose(False)
    rb.buildTransitions()
    rb.setVerbose(True)

    loops = rb.calcRegionLoop()
    assert len(loops) == len(loop_expect)
    for ix in range(len(loop_expect)):
        checkRegions(loops[ix], loop_expect[ix])

def checkRegions(regions, region_expect):
    for ix in range(len(region_expect)):
        assert regions[ix] == region_expect[ix]

def test_riverBankRegions_singleRiver(single_river):
    checkRiverBanks(single_river)

def test_riverBankRegions_twoRivers(two_rivers):
    checkRiverBanks(two_rivers)

def test_riverBankRegions_lake(with_lake):
    checkRiverBanks(with_lake)

def test_riverBankRegions_direct_into_lake(direct_into_lake):
    checkRiverBanks(direct_into_lake)

