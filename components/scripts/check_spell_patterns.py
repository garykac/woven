#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from data_spell_patterns import spell_card_patterns

elem_map = {
    'a': 'air',
    'e': 'earth',
    'f': 'fire',
    'w': 'water',
}

# Spell attributes
spell_attributes = [
    'element', 'pattern', 'companion', 'id', 'set', 'category', 'flavor', 'DISABLE'
]

class CheckSpellPatterns():
    
    def __init__(self):
        self.next_id = 0
        self.name2id = {}
        self.pattern_elements = {}
        self.elements = {}
        self.pattern2id = {}
                
        self.ranges = {
            'N2': 9,
            'N3': 5,
            'E1': 9,
            'E2': 162,
            'E3': 34,
            'EE1': 7,
            'EE2': 8,
        }

        self.valid_elements = ['none', 'air', 'fire', 'earth', 'water']

        # Initialize card patterns.
        self.spellPatterns = spell_card_patterns
        
        # Dict of pattern transformations for current pattern.
        self.newPatterns = {}
        
        # Doct of all possible patterns -> canonical pattern id.
        self.patterns = {}

    #
    # DATA VALIDATION
    #
    
    def patternKey(self, pattern):
        """Convert pattern array into a simple string that can be used as a key."""
        return '/'.join([''.join(row) for row in pattern])

    def patternFromKey(self, pKey):
        return pKey.split('/')

    def calcNumThreads(self, id):
        # TODO
        return 2
        
    def checkPatterns(self, base):
        nPatterns = self.ranges[base]
        for i in range(1, nPatterns+1):
            id = f"{base}-{i}"
            self.newPatterns = {}
            self.calcNewPatterns(id)
            self.mergeNewPatterns(id)
            self.countNewPatternTransforms(id)

        self.scanForMissingPatterns()
        # Check one beyond the last to verify the ranges are correct.
        id = f"{base}-{nPatterns+1}"
        if id in self.spellPatterns:
            raise Exception("Pattern id not in valid range: {base}-{nPatterns+1}")

    def calcNewPatterns(self, id):
        if not id in self.spellPatterns:
            raise Exception("Pattern {0}: Not found".format(id))

        debug = False

        # Generate all possible permutation of the spell pattern.
        pattern = self.normalizePattern(id)
        self.addNewPatternTransforms(pattern, debug)

        pattern = self.rotateCW(pattern)
        self.addNewPatternTransforms(pattern, debug)

        pattern = self.rotateCW(pattern)
        self.addNewPatternTransforms(pattern, debug)

        pattern = self.rotateCW(pattern)
        self.addNewPatternTransforms(pattern, debug)
        
    def addNewPatternTransforms(self, pattern, debug):
        self.addNewPattern(pattern, debug)
        self.addNewPattern(self.mirrorH(pattern), debug)
        self.addNewPattern(self.mirrorV(pattern), debug)

    def addNewPattern(self, pattern, debug):
        pKey = self.patternKey(pattern)
        if not pKey in self.newPatterns:
            self.newPatterns[pKey] = 1
            if debug:
                print(pKey)
                #self.printPatInfo(pattern)

    def mergeNewPatterns(self, id):
        for p in self.newPatterns:
            if p in self.patterns:
                self.printPattern(self.patternFromKey(p))
                raise Exception(f"Pattern {p} from {id} already generated from {self.patterns[p]}")
            self.patterns[p] = id

    def countNewPatternTransforms(self, id):
        mana = 0
        transforms = 0
        tapestry = "......./......./......./...@.../......./......./......."

        foundPattern = "0"
        while foundPattern:
            foundPattern = None
            # Search for 1-mana transforms.
            for p in self.newPatterns:
                if self.canApplyPattern(tapestry, p) == 1:
                    foundPattern = p
                    mana += 1
                    break
            if not foundPattern:
                # Search for 2-mana transforms.
                for p in self.newPatterns:
                    if self.canApplyPattern(tapestry, p) == 2:
                        foundPattern = p
                        mana += 2
                        break
            if foundPattern:
                tapestry = self.applyPattern(tapestry, foundPattern)
                transforms += 1
        print(f"{id} : transforms: {transforms}, mana {mana}")

    # Can the |pattern| be applied to the current |tapestry|?
    # Return number of new mana threads it would require. 0 if it can't apply.
    def canApplyPattern(self, tapestry, pattern):
        newMana = 0
        for i in range(0, len(tapestry)):
            if tapestry[i] == '.' and pattern[i] == 'X':
                newMana += 1
        return newMana

    def applyPattern(self, tapestry, pattern):
        t = list(tapestry)
        for i in range(0, len(tapestry)):
            if tapestry[i] == '.' and pattern[i] == 'X':
                t[i] = 'X'
        return ''.join(t)

    def scanForMissingPatterns(self):
        # 7x7 array = 49 values minus the center '@' = 48
        for i in range(0, 48):
            for j in range(i+1, 48):
                line = ['.'] * 48
                line[i] = 'X'
                line[j] = 'X'
                line.insert(24, '@')
                for k in range(6):
                    line.insert(7 + k*8, '/')
                pKey = ''.join(line)
                
                if not pKey in self.patterns:
                    raise Exception(f"{pKey} not found in patterns")

    def printPatInfo(self, pattern):
        print(self.patternKey(pattern))
        self.printPattern(pattern)
        print()
    
    def printPattern(self, pattern):
        for r in pattern:
            print(' '.join(r))
    
    def normalizePattern(self, id):
        pattern = self.spellPatterns[id]['pattern']
        origin = None
        y = 0
        num_cols = 0
        threads = []
        for row in pattern:
            cells = row.split()
            if y == 0:
                num_cols = len(cells)
            if len(cells) != num_cols:
                raise Exception(f"Pattern {id}: Mismatch number of columns in pattern")

            x = 0
            for c in cells:
                if c == '@':
                    if origin != None:
                        raise Exception(f"Pattern {id}: Multiple '@'")
                    origin = (x,y)
                elif c == 'X':
                    threads.append((x,y))
                elif c != '.': 
                    raise Exception("Pattern {id}: Invalid cell: {c}")
                x += 1
            y += 1
        if len(threads) != self.calcNumThreads(id):
            raise Exception(f"Pattern {id}: Wrong number of threads: {threads}")
        if origin == None:
            raise Exception(f"Pattern {id}: Missing '@'")
            
        normPat = [["." for j in range(0,7)] for i in range(0,7)]
        normPat[3][3] = '@'
        for t in threads:
            x = t[0] - origin[0] + 3
            y = t[1] - origin[1] + 3
            normPat[y][x] = 'X'
        return normPat

    def rotateCW(self, pattern):
        return list(zip(*pattern[::-1]))
    
    def rotateCCW(self, pattern):
        return list(zip(*pattern))[::-1]
    
    def mirrorH(self, pattern):
        return [row[::-1] for row in pattern]

    def mirrorV(self, pattern):
        return pattern[::-1]

# Comparator to zero-pad the spell index so that they sort correctly.
def _pattern_sort_(x):
    (key, count) = x
    (info, element) = key.split(':')
    (eleCount, index) = info.split('-')
    return f"{eleCount}-{index.zfill(3)}:{element}"

def main():
    cpat = CheckSpellPatterns()
    cpat.checkPatterns('E2')

if __name__ == '__main__':
    main()
