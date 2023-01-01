import math

epsilon = 0.00001

# Floating-point equal.
def feq(a, b):
    return (a > b - epsilon) and (a < b + epsilon)

# Floating-point greater-than or equal.
def fge(a, b):
    return (a > b - epsilon)

# Floating-point less-than or equal.
def fle(a, b):
    return (a < b + epsilon)

# Floating-point equal for points.
def feq_pt(p0, p1):
    return feq(p0[0], p1[0]) and feq(p0[1], p1[1])

# Floating-point equal for lines.
def feq_line(l0, l1):
    return feq_pt(l0[0], l1[0]) and feq_pt(l0[1], l1[1])

def scale(v, scale):
    x, y = v
    return [x * scale, y * scale]

def clamp(a, min, max):
    if a < min: return min
    if a > max: return max
    return a

# Linear interpolate from |v0| to |v1| by |t|.
def lerp(a0, a1, t):
    return a0 + (a1-a0)*t
    
# Calc point by linear interpolating from |v0| to |v1| by |t|.
def lerp_pt(v0, v1, t):
    x0, y0 = v0
    x1, y1 = v1
    return [lerp(x0, x1, t), lerp(y0, y1, t)]

# Calc offset to add to |v0| to linear interpolate from |v0| to |v1| by |t|.
def lerp_pt_delta(v0, v1, t):
    x0, y0 = v0
    x1, y1 = v1
    return [(x1-x0)*t, (y1-y0)*t]

# Linear interpolation (lerp) with a perpendicular (perp) offset.
# AKA: lerpendicular, lerpinperp
def lerperp(v0, v1, t, perp_t):
    x0, y0 = v0
    x1, y1 = v1
    dx = x1 - x0
    dy = y1 - y0
    lerp_x = x0 + dx * t
    lerp_y = y0 + dy * t
    # Use (x,y) + (-dy,dx) for perpendicular line.
    x = lerp_x - dy * perp_t
    y = lerp_y + dx * perp_t
    #print("lerperp:", v0, v1, t, perp_t, "->", x,y)
    return [x, y]

# Calc point which is distance |d| along the segment from |v0| to |v1|.
# Note that |d| is an absolute distance rather than a percentage.
def pt_along_line(v0, v1, d):
    t = d / dist(v0, v1)
    return lerp_pt(v0, v1, t)

# Return True if the two points are closer than |maxDist| to each other.
# This avoids the sqrt() call, so it is more efficient than dist(v0,v1) < maxDist
def near(v0, v1, maxDist):
    x0, y0 = v0
    x1, y1 = v1
    dx = x1 - x0
    dy = y1 - y0
    return dx*dx + dy*dy < maxDist * maxDist

# Calc distance from |v0| to |v1| (always positive).
def dist(v0, v1):
    x0, y0 = v0
    x1, y1 = v1
    dx = x1 - x0
    dy = y1 - y0
    return math.sqrt(dx*dx + dy*dy)

# Calc a point on either side of the given line that is distance |d| from the line.
def perp_offset(line, d):
    v0, v1 = line
    x0, y0 = v0
    x1, y1 = v1
    dx = x1 - x0
    dy = y1 - y0
    t = d / dist(v0, v1)
    # Use (x,y) + (-dy,dx) for perpendicular line.
    x = x0 - dy
    y = y0 + dx
    return [pt_along_line(v0, [x,y], d), pt_along_line(v0, [x,y], -d)]

# Return 2 parallel lines, distance |d| on either side of the given line.
def parallel_lines(line, d):
    # Points distance |d| on either side of the line.
    pt0, pt1 = perp_offset(line, d)
    v0, v1 = line
    dx = v1[0] - v0[0]
    dy = v1[1] - v0[1]
    line0 = [pt0, [pt0[0] + dx, pt0[1] + dy]]
    line1 = [pt1, [pt1[0] + dx, pt1[1] + dy]]
    return [line0, line1]

# Return distance from |pt| to |line|.
def dist_pt_line(pt, line):
    pt0, pt1 = line
    x0, y0 = pt0
    x1, y1 = pt1
    x,y = pt
    # Handle special case of vertical lines.
    if feq(x0, x1):
        return abs(x - x0)
    # Calc Ax + By + C = 0 form of line.
    # Given 2 points: (x0,y0), (x1,y1).
    # m = (y1-y0) / (x1-x0)
    # (y - y1) = m * (x - x1)
    # y - y1 = mx - mx1
    # 0 = mx - y + y1 - mx1
    # A = m; B = -1; C = (y1 - mx1)
    m = (y1 - y0) / (x1 - x0)
    A = m
    B = -1
    C = y1 - (m * x1)
    # Distance from pt |x| to line:
    # dist = | A x + B y + C | / sqrt(A^2 + B^2)
    dist = abs(A*x + B*y + C) / math.sqrt(A*A + B*B)
    return dist

# Return the 2 t values for the intersection between the 2 lines.
def line_intersection_t(line1, line2):
    pt1a, pt1b = line1
    pt2a, pt2b = line2

    pt1ax, pt1ay = pt1a
    pt1bx, pt1by = pt1b
    pt2ax, pt2ay = pt2a
    pt2bx, pt2by = pt2b

    # Intersection point for line1:
    #   x = (1 - t1) * pt1ax + t1 * pt1bx
    #   y = (1 - t1) * pt1ay + t1 * pt1by
    # Intersection point for line2:
    #   x = (1 - t2) * pt2ax + t2 * pt2bx
    #   y = (1 - t2) * pt2ay + t2 * pt2by
    #
    # x = x
    # (1 - t1) * pt1ax + t1 * pt1bx = (1 - t2) * pt2ax + t2 * pt2bx
    # pt1ax - t1 * pt1ax + t1 * pt1bx = (1 - t2) * pt2ax + t2 * pt2bx
    # t1 * (pt1bx - pt1ax) = (1 - t2) * pt2ax + t2 * pt2bx - pt1ax
    # t1 = ((1 - t2) * pt2ax + t2 * pt2bx - pt1ax) / (pt1bx - pt1ax)
    # t1 = (pt2ax - t2 * pt2ax + t2 * pt2bx - pt1ax) / (pt1bx - pt1ax)
    # t1 = (t2 * (pt2bx - pt2ax) + pt2ax - pt1ax) / (pt1bx - pt1ax)
    #
    # y = y
    # t1 = (t2 * (pt2by - pt2ay) + pt2ay - pt1ay) / (pt1by - pt1ay)

    # x = x
    # (1 - t1) * pt1ax + t1 * pt1bx = (1 - t2) * pt2ax + t2 * pt2bx
    # (1 - t1) * pt1ax + t1 * pt1bx = pt2ax - t2 * pt2ax + t2 * pt2bx
    # (1 - t1) * pt1ax + t1 * pt1bx - pt2ax = t2 * (pt2bx - pt2ax) 
    # t2 = ((1 - t1) * pt1ax + t1 * pt1bx - pt2ax) / (pt2bx - pt2ax)
    # t2 = (pt1ax - t1 * pt1ax + t1 * pt1bx - pt2ax) / (pt2bx - pt2ax)
    # t2 = (t1 * (pt1bx - pt1ax) + pt1ax - pt2ax) / (pt2bx - pt2ax)
    #
    # y = y
    # t2 = (t1 * (pt1by - pt1ay) + pt1ay - pt2ay) / (pt2by - pt2ay)

    pt1dx = pt1bx - pt1ax
    pt1dy = pt1by - pt1ay
    pt2dx = pt2bx - pt2ax
    pt2dy = pt2by - pt2ay
    pt21adx = pt2ax - pt1ax
    pt21ady = pt2ay - pt1ay
    pt12adx = pt1ax - pt2ax
    pt12ady = pt1ay - pt2ay

    # t1 = t1
    # (t2 * (pt2bx - pt2ax) + pt2ax - pt1ax) / (pt1bx - pt1ax)
    #    = (t2 * (pt2by - pt2ay) + pt2ay - pt1ay) / (pt1by - pt1ay)
    # (t2 * pt2dx + pt21adx) / pt1dx = (t2 * pt2dy + pt21ady) / pt1dy
    # (t2 * pt2dx + pt21adx) * pt1dy = (t2 * pt2dy + pt21ady) * pt1dx
    # t2 * pt2dx * pt1dy + pt21adx * pt1dy
    #    = t2 * pt2dy * pt1dx + pt21ady * pt1dx
    # t2 * pt2dx * pt1dy - t2 * pt2dy * pt1dx
    #    = pt21ady * pt1dx - pt21adx * pt1dy
    # t2 * (pt2dx * pt1dy - pt2dy * pt1dx) = pt21ady * pt1dx - pt21adx * pt1dy
    # t2 = (pt21ady * pt1dx - pt21adx * pt1dy) / (pt2dx * pt1dy - pt2dy * pt1dx)
    if feq((pt2dx * pt1dy - pt2dy * pt1dx), 0):
        print("uh oh", line1, line2)
    t2 = (pt21ady * pt1dx - pt21adx * pt1dy) / (pt2dx * pt1dy - pt2dy * pt1dx)

    # t2 = t2
    # (t1 * (pt1bx - pt1ax) + pt1ax - pt2ax) / (pt2bx - pt2ax)
    #    = (t1 * (pt1by - pt1ay) + pt1ay - pt2ay) / (pt2by - pt2ay)
    # (t1 * pt1dx + pt12adx) / pt2dx = (t1 * pt1dy + pt12ady) / pt2dy
    # (t1 * pt1dx + pt12adx) * pt2dy = (t1 * pt1dy + pt12ady) * pt2dx
    # t1 * pt1dx * pt2dy + pt12adx * pt2dy
    #    = t1 * pt1dy * pt2dx + pt12ady * pt2dx
    # t1 * pt1dx * pt2dy - t1 * pt1dy * pt2dx
    #    = pt12ady * pt2dx - pt12adx * pt2dy
    # t1 * (pt1dx * pt2dy - pt1dy * pt2dx) = pt12ady * pt2dx - pt12adx * pt2dy
    # t1 = (pt12ady * pt2dx - pt12adx * pt2dy) / (pt1dx * pt2dy - pt1dy * pt2dx)
    if feq((pt1dx * pt2dy - pt1dy * pt2dx), 0):
        print("uh oh", line1, line2)
    t1 = (pt12ady * pt2dx - pt12adx * pt2dy) / (pt1dx * pt2dy - pt1dy * pt2dx)

    # Alternate way to calculate t1.
    #t1 = (t2 * pt2dx + pt21adx) / pt1dx
    #print(t1, lerp_pt(pt1a, pt1b, t1))
    #print(t2, lerp_pt(pt2a, pt2b, t2))
    return (t1, t2)

# Calculate 2x signed area of the region defined by the vertices.
def _signedArea2(verts):
    # Algorithm:
    #   Calculate the signed area.
    #   Sum (x2 - x1)(y2 + y1) for each segment.
    # Positive = clockwise, Negative = counter-clockwise.
    #   Divide by 2 to get area.
    # Example:
    #  5 +
    #    |
    #  4 +              ,C,
    #    |            ,'   `,
    #  3 +          ,'       `,
    #    |        ,'           `,
    #  2 +       A - - - - - - - B
    #    |
    #  1 +
    #    |
    #  0 +---+---+---+---+---+---+---+---+
    #    0   1   2   3   4   5   6   7   8
    #  A = (2,2)  B = (6,2)  C = (4,4)
    # For [A, B, C]:
    #   Calc A->B, B->C and C->A
    #   = (6-2)(2+2) + (4-6)(4+2) + (2-4)(2+4)
    #   = 16 + -12 + -12
    #   = -8 (counter-clockwise)
    # For [A, C, B]:
    #   Calc A->C, C->B and B->A
    #   = (4-2)(4+2) + (6-4)(2+4) + (2-6)(2+2)
    #   = 12 + 12 + -16
    #   = 8 (clockwise)
    # Area = 8 / 2 = 4
    area2 = 0.0
    numVerts = len(verts)
    for i in range(0, numVerts):
        pt1 = verts[i]
        pt2 = verts[(i+1) % numVerts]
        area2 += (pt2[0] - pt1[0]) * (pt2[1] + pt1[1])
    # The sign of area2 indicates the direction of the points.
    # The actual area can be obtained by dividing |area2| by 2.
    return area2

# Return true if the points are in clockwise order.
def isClockwise(verts):
    # No need to divide by 2 since we don't need the area, just the sign.
    return fge(_signedArea2(verts), 0.0)

def area(self, verts):
    # Divide the absolute value by 2 to get the area.
    return abs(_signedArea2(verts)) / 2;

__hexXMax = math.sqrt(3) / 2

# Return True if |pt| is within a hexagon of size |size|, centered at the origin.
# size - size of hexagon (from center to vertex)
# pt - point to check
def ptInHex(size, pt):
    x, y = pt
    # Check if point is within hexagon.
    # Assumes hexagon is centered at origin.
    # Note: scale = 1.0 in diagram.
    #
    #  1.0             _+_
    #              _,-' : `-,_
    #          _,-'     :     `-,_
    #  0.5   +'         :         `+
    #        |          :          |
    #        |          :          |
    #  0.0   |          + . . . . .|
    #        |                     |
    #        |                     |
    # -0.5   +,                   ,+
    #          `-,_           _,-'
    #              `-,_   _,-'
    # -1.0             `+'
    #    
    # Upper quadrant:
    #
    #   1.0   +_
    #         : `-,_
    #         :     `-,_
    #         :         `+  0.5
    #         :          |
    #         :          |
    #   0.0   + . . . . .|
    #         0       sqrt(3)/2
    #
    # Transform point to upper quadrant.
    tx = abs(x)
    ty = abs(y)

    # Check if |pt| is outside the hexagon's right edge.
    if tx > (size * __hexXMax):
        return False
            
    # Equation for sloped line defined by (0, 1) and (sqrt(3)/2, 0.5):
    # y = m * x + b
    # m = (y2 - y1) / (x2 - x1)
    #   = (0.5 - 1.0) / (sqrt(3)/2 - 0)
    #   = -0.5 / (sqrt(3)/2)
    #   = -0.5 * 2 / sqrt(3)
    #   = -1 / sqrt(3)
    m = -1 / math.sqrt(3)
    # b = 1 (y-axis intercept, needs to be scaled by size)
    b = size
        
    # Use tx and solve for y. If ty is below the line, then it is inside
    # the hex.
    yEdge = m * tx + b
    return ty < yEdge
