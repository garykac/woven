# Base id for each tile pattern.
TILE_PATTERN_IDS = {
                   # M = pattern id for the mirrored form of this pattern.
                   #     '-' means that mirrored pattern has the same canonical form.
                   # Tiles = current status of tiles being created for this pattern.
                   #
                   #  M   Tiles
    "llllll": 100, #  -   *
    "lllllm": 120, #  -   
    "llllmm": 140, #  -   
    "lllmlm": 160, #  -   *
    "lllmmm": 180, #  -   *

    "lllmhm": 200, #  -   *
    "llmllm": 220, #  -   *
    "llmlmm": 240, # 260  
    "llmmlm": 260, # 240  
    "llmmmm": 280, #  -   

    "llmmhm": 300, # 320  
    "llmhmm": 320, # 300  
    "llmhhm": 340, #  -   * * * * * *
    "lmlmlm": 360, #  -   
    "lmlmmm": 380, #  -   +

    "lmlmhm": 400, #  -   +
    "lmmlmm": 420, #  -   
    "lmmmmm": 440, #  -   + o
    "lmmmhm": 460, # 520  +
    "lmmhmm": 480, #  -   o

    "lmmhhm": 500, # 560  
    "lmhmmm": 520, # 460  +
    "lmhmhm": 540, #  -   +
    "lmhhmm": 560, # 500  
    "lmhhhm": 580, #  -   

    "mmmmmm": 600, #  -   
    "mmmmmh": 620, #  -   
    "mmmmhh": 640, #  -   
    "mmmhmh": 660, #  -   +
    "mmmhhh": 680, #  -   

    "mmhmmh": 700, #  -   * +
    "mmhmhh": 720, # 740  *
    "mmhhmh": 740, # 720  
    "mmhhhh": 760, #  -   + o
    "mhmhmh": 780, #  -   

    "mhmhhh": 800, #  -   +
    "mhhmhh": 820, #  -   * *
    "mhhhhh": 840, #  -   
    "hhhhhh": 860, #  -   *

    # 900+ for special tiles
}

# Annotations:
#   * = complete
#   + = terrain complete
#   o = generated

# Capture the Toad:
#                _H_           _H_
#            _,-'   `-,_   _,-'   `-,_
#          H'           `M'           `H
#          |             |             |
#          |     34x     |     34x     |
#          |             |             |
#         _M_           _L_           _M_
#     _,-'   `-,_   _,-'   `-,_   _,-'   `-,_
#   H'           `L'           `L'           `H
#   |             |             |             |
#   |     34x     |     101     |     34x     |
#   |             |             |             |
#   H,           ,L,           ,L,           ,H
#     `-,_   _,-'   `-,_   _,-'   `-,_   _,-'
#         `M'           `L'           `M'
#          |             |             |
#          |     34x     |     34x     |
#          |             |             |
#          H,           ,M,           ,H
#            `-,_   _,-'   `-,_   _,-'
#                `H'           `H'
# To build map:
# * Place 101 in center
# * Arrange 2-6 34x tiles around the center tile

# Futball
#                _b_           _b_           _b_
#            _,-'   `-,_   _,-'   `-,_   _,-'   `-,_
#          c'           `a'           `a'           `c
#          |             |             |             |
#          |     mhm     |     mlm     |     mhm     |
#          |             |             |             |
#         _M_           _M_           _M_           _M_
#     _,-'   `-,_   _,-'   `-,_   _,-'   `-,_   _,-'   `-,_
#   L'           `H'           `L'           `H'           `L
#   |             |             |             |             |
#   |     34x     |     34x     |     34x     |     34x     |
#   |             |             |             |             |
#   L,           _H_           _L_           _H_           ,L
#     `-,_   _,-'   `-,_   _,-'   `-,_   _,-'   `-,_   _,-'
#         `M'           `M'           `M'           `M'
#          |             |             |             |
#          |     mhm     |     mlm     |     mhm     |
#          |             |             |             |
#          c,           ,a,           ,a,           ,c
#            `-,_   _,-'   `-,_   _,-'   `-,_   _,-'
#                `b'           `b'           `b'
# To build map:
# * Place 4 34x tiles in a line with L-L edge in center
# * Add a mlm tile above and below the L-L edge
# * Add mhm tiles that match the mlm tiles
#
# This is an analysis of all the MLM and MHM tiles. Since in this map we don't care about
# the 'b' and 'c' vertices, we want to maximize the tiles that make it easy to match
# the 'a' vertices with the placed MLM tile.
#
# Removing the MLM or MHM from the beginning and looking at the other 3 vertices, we have
# the following possibilities:
#   lll                  mll                  hll  X
#   llm                  mlm                  hlm  X
#   llh  X               mlh  X               hlh  X
#   lml                  mml                  hml
#   lmm                  mmm                  hmm
#   lmh                  mmh                  hmh
#   lhl  X               mhl  X               hhl  X
#   lhm  X               mhm                  hhm
#   lhh  X               mhh                  hhh
# 
# X = invalid ('h' cannot be next to 'l')
# Pattern counts (for left/right side match):
#    l-- 5     --l 5
#    m-- 7     --m 7
#    h-- 5     --h 5
#  
#                                      mlm                                 mhm
#                            l-- m-- h--  --l --m --h            l-- m-- h--  --l --m --h
#  "lllmlm": 160, # mlm-lll   x            x                                               X
#  "lllmhm": 200, #                                     mhm-lll   x            x
#  "llmlmm": 240, # mlm-mll       x        x                                               - Mirrors with 260
#  "llmmlm": 260, # mlm-llm   x                x                                           - Mirrors with 240
#  "llmmhm": 300, #                                     mhm-llm   x                x       - Mirrors with 320
#  "llmhmm": 320, #                                     mhm-mll       x        x           - Mirrors with 300
#  "lmlmlm": 360, # mlm-lml   x            x
#  "lmlmmm": 380, # mlm-lmm   x   x        x   x                                           X Y
#                 # mlm-mml
#  "lmlmhm": 400, # mlm-lmh   x       x    x       x    mhm-lml   x            x           X Y
#                 # mlm-hml
#  "lmmlmm": 420, # mlm-mlm       x            x
#  "lmmmmm": 440, # mlm-mmm       x            x
#  "lmmmhm": 460, # mlm-mmh       x                x    mhm-lmm   x                x       X - Mirrors with 520
#  "lmmhmm": 480, # mlm-mhm       x            x        mhm-mlm       x            x       X
#  "lmmhhm": 500, # mlm-mhh       x                x                                       - Mirrors with 560
#  "lmhmmm": 520, # mlm-hmm           x        x        mhm-mml       x        x           X Y - Mirrors with 460
#  "lmhmhm": 540, # mlm-hmh           x            x    mhm-lmh   x       x    x       x   X Y
#                 #                                     mhm-hml
#  "lmhhmm": 560, # mlm-hhm           x        x                                           - Mirrors with 500
#  "lmhhhm": 580, # mlm-hhh           x            x
#  "mmmmmh": 620, #                                     mhm-mmm       x            x

#  "mmmhmh": 660, #                                     mhm-mmh       x   x        x   x   X Y
#                 #                                     mhm-hmm
#  "mmhmmh": 700, #                                     mhm-mhm       x            x
#  "mmhmhh": 720, #                                     mhm-hhm           x        x       - Mirrors with 740
#  "mmhhmh": 740, #                                     mhm-mhh       x                x   - Mirrors with 720
#  "mhmhmh": 780, #                                     mhm-hmh           x            x
#  "mhmhhh": 800, #                                     mhm-hhh           x            x   X
#
# Sum rows with 'X' at eng:   3   3   3    3   3   3              3   3   3    3   3   3
#
# Sum rows with 'Y' at eng:   2   1   3    2   2   2              2   2   2    3   1   2
