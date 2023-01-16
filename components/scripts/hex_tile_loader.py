import re

from data_tile_pattern_ids import TILE_PATTERN_IDS
from hex_tile import VoronoiHexTile

class VoronoiHexTileLoader():
    def __init__(self, options):
        self.options = options

    def process(self):
        # Load data from file.
        if self.options['load']:
            self.processTileData(self.options['load'])
            return

        self.processTile(None, None, None, None)

    def processTile(self, terrainData, riverData, cliffData, overlayData):
        options = self.options.copy()

        id = options['id']
        pattern = options['pattern']
        seed = options['seed']
        if id is None:
            idString = "???"
        else:
            idString = f"{id}"
        print(f"Tile {idString} - pattern {pattern} - seed {seed}")

        if id:
            # Verify the that id matches the correct range for this pattern.
            # Note that the 0th value of each range is unused.
            patternBaseId = TILE_PATTERN_IDS[pattern]
            if id <= patternBaseId or id >= patternBaseId+20:
                print(f"WARNING: Id {options['id']} does not match pattern range {patternBaseId}+")
        
        v = VoronoiHexTile(options)
        v.init()
        v.setTerrainData(terrainData)
        v.setRiverData(riverData)
        v.setCliffData(cliffData)
        v.setOverlayData(overlayData)

        if options['anim']:
            v.cleanupAnimation()

        v.generate()
        while v.update():
            v.generate()
        if not v.successfulTileGeneration:
            print(f"Tile generation failed for pattern {pattern} with seed {options['seed']}")
            v.printIteration("Final")
        v.plot()

        if v.successfulTileGeneration and (self.options['verbose'] or not id or not seed):
            v.writeTileData()

        if options['export-3d']:
	        v.writeObject3d()
    
        if options['anim']:
            v.exportAnimation()

    def processTileData(self, file):
        header = True
        
        # If |id| is set on the command line, then only generate that map tile from
        # the data file.
        select_id = None
        if self.options['id']:
            select_id = self.options['id']

        with open(file) as f:
            pattern = None
            seed = None
            center = None
            terrain_data = None
            river_data = None
            cliff_data = None
            overlay_data = None

            last_id = None
            for line in f:
                if header:
                    header = False
                    continue
                # Id, RowType
                data = line.rstrip().split(',')
                id = int(data.pop(0))
                rowType = data.pop(0)
                
                # Skip over non-matching id if we're only processing a specific one.
                if select_id and id != select_id:
                    continue
                
                if last_id and id != last_id:
                    if rowType != "INFO":
                        raise Exception(f"Expected INFO as first line of new tile {id}. Found {rowType}")

                    # Write out previous tile.
                    self.options['id'] = last_id
                    self.options['pattern'] = pattern
                    self.options['seed'] = seed
                    self.options['center'] = center
                    if active:
                        self.processTile(terrain_data, river_data, cliff_data, overlay_data)

                    pattern = None
                    seed = None
                    center = None
                    terrain_data = None
                    river_data = None
                    cliff_data = None
                    overlay_data = None

                if rowType == "INFO":
                    active = True
                    status = data.pop(0)
                    if status != "_":
                        active = False
                    pattern = data.pop(0)
                    seed = int(data.pop(0))
                    center = data.pop(0)
                    if center == "AVG":
                        center = None
                elif rowType == "TERRAIN":
                    # |terrain_data| is an array of 'l', 'm', 'h'.
                    terrain_data = data
                elif rowType == "RIVER":
                    # |river_data| is an array of river segments identified as
                    # "<c1>-<c2>" pairs where <c1> and <c2> identify the 2 cells on
                    # either side of the river segment.
                    river_data = data
                elif rowType == "BRIDGE":
                    if not overlay_data:
                        overlay_data = {}
                    # Bridge |overlay_data| is an array of edges that should have a bridge.
                    # Each bridge is a set of "<c1>-<c2>" pairs with an optional
                    # "(<x> <y>)" offset to shift the location along the edge.
                    overlay_data['bridge'] = data
                elif rowType == "LAKE":
                    if not overlay_data:
                        overlay_data = {}
                    # Lake |overlay_data| is an array of region ids that are lakes.
                    overlay_data['lake'] = data
                elif rowType == "CLIFF":
                    # |cliff_data| is an array of cliff segments identified as
                    # "<c1>-<c2>" pairs where <c1> and <c2> identify the 2 cells on
                    # either side of the cliff segment. Segments may be followed by '*'
                    # to indicate that they are the end of a cliff.
                    cliff_data = data
                elif rowType == "MARK":
                    if not overlay_data:
                        overlay_data = {}
                    # Star |overlay_data| is an array of cells that should be marked with
                    # an icon. Each cell index may have an optional "(<x> <y>)" offset to
                    # shift the icon from the cell's seed location.
                    overlay_data['mark'] = data
                elif rowType == "TREE":
                    if not overlay_data:
                        overlay_data = {}
                    # Tree |overlay_data| is an array of cells and tree types. Each cell
                    # index may have an optional "(<x> <y>)" offset to shift the icon
                    # from the cell's seed location.
                    overlay_data['tree'] = data
                else:
                    raise Exception(f"Unrecognized row type: {rowType}")
                last_id = id

            # Write out final tile.
            self.options['id'] = last_id
            self.options['pattern'] = pattern
            self.options['seed'] = seed
            self.options['center'] = center
            if active:
                self.processTile(terrain_data, river_data, cliff_data, overlay_data)

