import math

epsilon = 0.00001
def feq(a, b):
    return (a > b - epsilon) and (a < b + epsilon)

def scale(v, scale):
    x, y = v
    return [x * scale, y * scale]

def lerp(a0, a1, t):
    return a0 + (a1-a0)*t
    
# Calc point by linear interpolating from v0 to v1 by t.
def lerp_pt(v0, v1, t):
    x0, y0 = v0
    x1, y1 = v1
    return [x0 + (x1-x0)*t, y0 + (y1-y0)*t]

# Calc offset to add to v0 to linear interpolate from v0 to v1 by t.
def lerp_pt_delta(v0, v1, t):
    x0, y0 = v0
    x1, y1 = v1
    return [(x1-x0)*t, (y1-y0)*t]

# Linear interpolation (lerp) with a perpendicular (perp) offset.
def lerperp(v0, v1, t, perp_t):
    x0, y0 = v0
    x1, y1 = v1
    lerp_x = x0 + (x1-x0)*t
    lerp_y = y0 + (y1-y0)*t
    x = lerp_x - (y1-y0)*perp_t
    y = lerp_y + (x1-x0)*perp_t
    #print("lerperp:", v0, v1, t, perp_t, "->", x,y)
    return [x, y]

def near(v0, v1, dist):
    x0, y0 = v0
    x1, y1 = v1
    dx = x1 - x0
    dy = y1 - y0
    return dx*dx + dy*dy < dist * dist

def dist(v0, v1):
    x0, y0 = v0
    x1, y1 = v1
    dx = x1 - x0
    dy = y1 - y0
    return math.sqrt(dx*dx + dy*dy)

def dist_pt_line(pt, line):
    line0, line1 = line
    x0, y0 = line0
    x1, y1 = line1
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

__hexXMax = math.sqrt(3) / 2

def ptInHex(size, x, y):
    # Check if point is within hexagon.
    # Assumes hexagon is centered at origin.
    # Note: scale = 1.0 in diagram.
    #
    #  1.0            _,+,_
    #           _, -'   :   `- ,_
    #  0.5   +'         :         `+
    #        |          :          |
    #        |          :          |
    #  0.0   |          + . . . . .|
    #        |                     |
    #        |                     |
    #        +,_                 _,+
    #            `- ,_     _, -'
    # -1.0             `+'
    #    
    # Upper quadrant:
    #
    #   1.0   +,_
    #         :   `- ,_
    #         :         `+  0.5
    #         :          |
    #         :          |
    #   0.0   + - - - - -+
    #          0       sqrt(3)/2
    #
    # Transform point to upper quadrant.
    tx = abs(x)
    ty = abs(y)

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
