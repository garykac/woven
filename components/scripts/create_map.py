import getopt
import os
import sys

from hex_tile_loader import VoronoiHexTileLoader

MAP_OUTPUT_DIR = "../maps"
MAP_TEMPLATE_DIR = os.path.join(MAP_OUTPUT_DIR, 'templates')

OPTIONS = {
    'anim': {'type': 'bool', 'default': False,
             'desc': "Generate animation plots"},
    'bleed': {'type': 'bool', 'default': False,
              'desc': "Create output for printing (with bleed and no tile outline)"},
    'bw': {'type': 'bool', 'default': False,
           'desc': "Black & white SVG output"},
    'center': {'type': 'string', 'default': None,
               'desc': "Terrain type for center of tile: l, m, h"},
    'debug': {'type': 'int', 'default': -1,
              'desc': "Log debug info for given region id"},
    'export-3d': {'type': 'bool', 'default': False,
                 'desc': "Export .obj"},
    'export-pdf': {'type': 'bool', 'default': False,
                   'desc': "Export .pdf from .svg"},
    'export-png': {'type': 'bool', 'default': True,
                   'desc': "Export .png from .svg"},
    'id': {'type': 'int', 'default': None,
           'desc': "Process only this tile id (used with --load)"},
    'iter': {'type': 'int', 'default': 500,
             'desc': "Max iterations"},
    'load': {'type': 'string', 'default': None,
             'desc': "Load data from file"},
    'pattern': {'type': 'string', 'default': "llllll",
                'desc': "Edge pattern ([lmh] x6)"},
    'random-terrain-fill': {'type': 'bool', 'default': False,
                            'desc': "True to fill interior cells with random terrain"},
    'seed': {'type': 'int', 'default': None,
             'desc': "Random seed"},
    'show-seed-ids': {'type': 'bool', 'default': False,
                      'desc': "Show the seed id layer"},
    'size': {'type': 'int', 'default': 80,
             'desc': "Size of hex side (mm)"},
    'texture-fill': {'type': 'bool', 'default': False,
                     'desc': "True to fill regions with texture"},
    'verbose': {'type': 'bool', 'short': 'v', 'default': False,
                'desc': "Display progress during processing"},
}

def usage():
    print("python create-map.py <options>")
    for o in OPTIONS:
        opt = OPTIONS[o]
        print("  ", o, end=' ')
        if opt['type'] == 'int':
            print("<int>", end=' ')
        elif opt['type'] == 'string':
            print("<str>", end=' ')
        print("-", opt['desc'])
    sys.exit(0)

def parse_options():
    option_defs = {}
    option_defs.update(OPTIONS)
    short_opts = ""
    long_opts = []
    for opt,info in option_defs.items():
        if 'short' in info:
            short_opts += info['short']
            if info['type'] != 'bool':
                short_opts += ':'
        long_opt = opt
        if info['type'] != 'bool':
            long_opt += '='
        long_opts.append(long_opt)

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        usage()

    options = {}
    for opt,info in option_defs.items():
        options[opt] = info['default']

    for opt,arg in opts:
        # Build list of short and fullname for this option.
        for opt_name, opt_info in option_defs.items():
            option_flags = []
            if 'short' in opt_info:
                option_flags.append(f"-{opt_info['short']}")
            option_flags.append(f"--{opt_name}")

            # If matches this option.
            if opt in option_flags:
                type = opt_info['type']
                if type == 'bool':
                    options[opt_name] = True
                elif type == 'int':
                    options[opt_name] = int(arg)
                else:
                    options[opt_name] = str(arg)

    # Non-public options.
    options['outdir_svg'] = os.path.join(MAP_OUTPUT_DIR, "map-svg")
    options['outdir_png'] = os.path.join(MAP_OUTPUT_DIR, "map-png")
    options['outdir_png_id'] = os.path.join(MAP_OUTPUT_DIR, "map-png-id")
    options['outdir_pdf'] = os.path.join(MAP_OUTPUT_DIR, "map-pdf")
    options['map_obj_template'] = os.path.join(MAP_TEMPLATE_DIR, 'map-obj-template.svg')
    options['anim_subdir'] = "anim"  # Subdirectory of png output dir

    options['origin'] = [0, 0]
    options['write_output'] = True
    options['verbose_iteration'] = options['verbose']

    # Calc the neighbor edges for 3d output.
    options['calc_neighbor_edges'] = False

    # Internal options (don't edit manually).
    # True if we're processing one of the neighbor tiles.
    options['_neighbor_tile'] = False
    # Current edge to export (if exporting 3d).
    options['_export_3d_edge'] = None
    # Used when generating mirrored 3d neighbors of the current tile.
    options['_allow_non_canonical_pattern'] = False

    return options

def main():
    options = parse_options()

    loader = VoronoiHexTileLoader(options)
    loader.process()

if __name__ == '__main__':
    main()
