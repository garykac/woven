
def calcSortedId(id0, id1):
    if int(id0) < int(id1):
        return f"{id0}-{id1}"
    return f"{id1}-{id0}"

def calcSortedIdFromPair(seeds):
    (seedA, seedB) = seeds
    return calcSortedId(seedA, seedB)
