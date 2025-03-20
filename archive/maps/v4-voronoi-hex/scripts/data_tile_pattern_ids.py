# Base id for each tile pattern.
TILE_PATTERN_IDS = {
    # M = pattern id for the mirrored form of this pattern.
    #     '-' means that mirrored pattern has the same canonical form.
    # Search pattern - search for any sequence of corners to find all tiles that have
    #     that sequence.
    # Tiles = current status of tiles being created for this pattern.
    #     o = generated
    #     + = terrain complete (with rivers, cliffs and bridges)
    #     * = complete (with trees and other marks)
    #
    #              #  M   Search Pat   Tiles
    "llllll": 100, #  -   lllllllllll  *
    "lllllm": 120, #  -   lllllmlllll  
    "llllmm": 140, #  -   llllmmllllm  * o
    "lllmlm": 160, #  -   lllmlmlllml  *
    "lllmmm": 180, #  -   lllmmmlllmm  * *

    "lllmhm": 200, #  -   lllmhmlllmh  *
    "llmllm": 220, #  -   llmllmllmll  *
    "llmlmm": 240, # 260  llmlmmllmlm  
    "llmmlm": 260, # 240  llmmlmllmml  
    "llmmmm": 280, #  -   llmmmmllmmm  

    "llmmhm": 300, # 320  llmmlmllmmh  
    "llmhmm": 320, # 300  llmhmmllmhm  
    "llmhhm": 340, #  -   llmhhmllmhh  * * * * * *
    "lmlmlm": 360, #  -   lmlmlmlmlml  o
    "lmlmmm": 380, #  -   lmlmmmlmlmm  +

    "lmlmhm": 400, #  -   lmlmhmlmlmh  * * + +
    "lmmlmm": 420, #  -   lmmlmmlmmlm  
    "lmmmmm": 440, #  -   lmmmmmlmmmm  + o
    "lmmmhm": 460, # 520  lmmmhmlmmmh  +
    "lmmhmm": 480, #  -   lmmhmmlmmhm  * * o o

    "lmmhhm": 500, # 560  lmmhhmlmmhh  
    "lmhmmm": 520, # 460  lmhmmmlmhmm  +
    "lmhmhm": 540, #  -   lmhmhmlmhmh  +
    "lmhhmm": 560, # 500  lmhhmmlmhhm  
    "lmhhhm": 580, #  -   lmhhhmlmhhh  

    "mmmmmm": 600, #  -   mmmmmmmmmmm  +
    "mmmmmh": 620, #  -   mmmmmhmmmmm  
    "mmmmhh": 640, #  -   mmmmhhmmmmh  
    "mmmhmh": 660, #  -   mmmhmhmmmhm  * * o
    "mmmhhh": 680, #  -   mmmhhhmmmhh  

    "mmhmmh": 700, #  -   mmhmmhmmhmm  * *
    "mmhmhh": 720, # 740  mmhmhhmmhmh  +
    "mmhhmh": 740, # 720  mmhhmhmmhhm  
    "mmhhhh": 760, #  -   mmhhhhmmhhh  + o
    "mhmhmh": 780, #  -   mhmhmhmhmhm  *

    "mhmhhh": 800, #  -   mhmhhhmhmhh  +
    "mhhmhh": 820, #  -   mhhmhhmhhmh  * *
    "mhhhhh": 840, #  -   mhhhhhmhhhh  
    "hhhhhh": 860, #  -   hhhhhhhhhhh  * * o o

    # 900+ for special tiles
}

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
#  "lllmlm": 160, # mlm-lll   x            x
#  "lllmhm": 200, #                                     mhm-lll   x            x
#  "lmlmlm": 360, # mlm-lml   x            x
#  "lmlmmm": 380, # mlm-lmm   x   x        x   x
#                 # mlm-mml
#  "lmlmhm": 400, # mlm-lmh   x       x    x       x    mhm-lml   x            x
#                 # mlm-hml
#  "lmmlmm": 420, # mlm-mlm       x            x
#  "lmmmmm": 440, # mlm-mmm       x            x
#  "lmmhmm": 480, # mlm-mhm       x            x        mhm-mlm       x            x
#  "lmhmhm": 540, # mlm-hmh           x            x    mhm-lmh   x       x    x       x
#                 #                                     mhm-hml
#  "lmhhhm": 580, # mlm-hhh           x            x
#  "mmmmmh": 620, #                                     mhm-mmm       x            x

#  "mmmhmh": 660, #                                     mhm-mmh       x   x        x   x
#                 #                                     mhm-hmm
#  "mmhmmh": 700, #                                     mhm-mhm       x            x
#  "mhmhmh": 780, #                                     mhm-hmh           x            x
#  "mhmhhh": 800, #                                     mhm-hhh           x            x
#
# Removed tile candidates because they don't self-mirror:
#  "llmlmm": 240, # mlm-mll       x        x                                               - Mirrors with 260
#  "llmmlm": 260, # mlm-llm   x                x                                           - Mirrors with 240
#  "llmmhm": 300, #                                     mhm-llm   x                x       - Mirrors with 320
#  "llmhmm": 320, #                                     mhm-mll       x        x           - Mirrors with 300
#  "lmmmhm": 460, # mlm-mmh       x                x    mhm-lmm   x                x       X - Mirrors with 520
#  "lmmhhm": 500, # mlm-mhh       x                x                                       - Mirrors with 560
#  "lmhmmm": 520, # mlm-hmm           x        x        mhm-mml       x        x           X Y - Mirrors with 460
#  "lmhhmm": 560, # mlm-hhm           x        x                                           - Mirrors with 500
#  "mmhmhh": 720, #                                     mhm-hhm           x        x       - Mirrors with 740
#  "mmhhmh": 740, #                                     mhm-mhh       x                x   - Mirrors with 720
