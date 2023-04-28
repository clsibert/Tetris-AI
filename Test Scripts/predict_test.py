from simulator_API import *
from simulator import TetrisSimulator
from tetris_cpp import *
from boards import print_board, all_zoids
import sys


data = open("reg_best_full_game.tsv", "rU")
outfile = open("reg_best_game_predictionsMMShort", "w")

CERLscore = {"landing_height": -152.3582,
                   "eroded_cells": 25.0868439339,
                   "row_trans": -162.330389078,
                   "col_trans": -383.049691756,
                   "pits": -498.471504549,
                   "cuml_wells": 3.59862230086}
                   
MMLong = {"landing_height": -0.4,
                   "eroded_cells": 1,
                   "row_trans": -0.6,
                   "col_trans": -1,
                   "pits": -0.8,
                   "cuml_wells": -0.4}
                   
MMShort = {"landing_height": -0.1,
                   "eroded_cells": 0,
                   "row_trans": -0.1,
                   "col_trans": 0.1,
                   "pits": -1,
                   "cuml_wells": 0.01}
                   
header = data.readline()
header = header.rstrip().split('\t')


board_ix = header.index('board_rep') 
zoid_rot_ix = header.index('zoid_rot') 
zoid_col_ix = header.index('zoid_col') 
zoid_row_ix = header.index('zoid_row') 
curr_zoid_ix = header.index('curr_zoid') 
ep_num_ix = header.index('episode_number')

out_header = ""
out_header += ("episode_number" + "\t")
out_header += ("zoid" + "\t")
out_header += ("move_row" + "\t")
out_header += ("move_col" + "\t")
out_header += ("move_rot" + "\t")
out_header += "move_score"

outfile.write(out_header + "\n")

lines = data.readlines()
for x in range(len(lines)):
    line = lines[x]
    if x == 0:
        player_board = [[0]*10 for i in range(20)]
    else:
        prev_line = lines[x - 1]
        prev_line = prev_line.rstrip().split('\t')
        player_board = eval(eval(prev_line[board_ix]))
    line = line.rstrip().split('\t')
    
    if line[curr_zoid_ix] != 'NA':
    	player_zoid = line[curr_zoid_ix]

    working_controller = MMShort
    working_features = MMShort.keys()
    
    sim = TetrisSimulator(controller=working_controller)
    sim.space = tetris_cow2.convert_old_board(player_board)
    sim.curr_z = all_zoids[player_zoid]


    feats = get_features(player_board, player_zoid, working_controller)
    
    for f in feats:
        lh_val = f['features']['landing_height'] * working_controller['landing_height']
        ec_val = f['features']['eroded_cells'] * working_controller['eroded_cells']
        rt_val = f['features']['row_trans'] * working_controller['row_trans']
        ct_val = f['features']['col_trans'] * working_controller['col_trans']
        pit_val = f['features']['pits'] * working_controller['pits']
        wells_val = f['features']['cuml_wells'] * working_controller['cuml_wells']
        move_score = lh_val + ec_val + rt_val + ct_val + pit_val + wells_val
        
        out_line = ""
        out_line += (str(line[ep_num_ix]) + "\t")
        out_line += (str(f['zoid']) + "\t")
        out_line += (str(f['row']) + "\t")
        out_line += (str(f['col']) + "\t")
        out_line += (str(f['orient']) + "\t")
        out_line += str(move_score)
        
        outfile.write(out_line + "\n")
        
