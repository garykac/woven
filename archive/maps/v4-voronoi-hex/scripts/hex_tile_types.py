
type = ['l', 'm', 'h' ]

alt = {
    'l': '1',
    'm': '2',
    'h': '3',
}

def rotateString(s, n):
    if n == 0:
        return s
    return s[n:] + s[0:n]

class HexTile():
    def __init__(self):
        pass

    def isNormalized(self, pattern):
        # Check all rotated versions of the pattern
        lowVal = 400000 # Must be gt 333333
        lowIndex = -1
        for i in range(0, 6):
            pRot = rotateString(pattern, i)
            # Convert pattern to number
            pNum = int(''.join([alt[i] for i in pRot]))
            if pNum < lowVal:
                lowVal = pNum
                lowIndex = i
        # Pattern is normalized if it is the lowest numeric value.
        return lowIndex == 0

    def validPattern(self, pattern):
        p = pattern + pattern[0]
        if "hl" in p or "lh" in p:
            return False
        if not self.isNormalized(pattern):
            return False
        return True

    def analyze(self):
        num = 0
        for i0 in type:
            for i1 in type:
                for i2 in type:
                    for i3 in type:
                        for i4 in type:
                            for i5 in type:
                                pattern = ''.join([i0, i1, i2, i3, i4, i5])
                                if self.validPattern(pattern):
                                    num += 1
                                    print(pattern)
                                    if num % 5 == 0:
                                        print()

        print(num)

hex = HexTile()
hex.analyze()
