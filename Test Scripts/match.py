from __future__ import print_function, division
import csv
import simplejson as json
import pandas as pd
import random
import unicodedata

from cogworks.tetris.game import State, Board, zoids
from cogworks.tetris import simulator
from cogworks import feature

def parse_board(rep):
    rows = len(rep)
    print(rows)
    cols = None
    for row in rep:
        if cols is None:
            cols = len(row)
        else:
            assert cols == len(row)
    board = Board(rows, cols, zero=False)
    board.heights = [0] * cols
    for r in range(0, rows):
        for c in range(0, cols):
            board.data[r, c] = bool(rep[r][c])
            if not board.heights[c] and board.data[r, c]:
                board.heights[c] = r
    return board

def gen_futures(state, zoid, move_gen):
    return [state.future(zoid, *move) for move in move_gen(state, zoid)]

def sample_tsv_lines(file_path, columns, sample_size):
    # Read the TSV file into a DataFrame
    df = pd.read_csv(file_path, sep='\t')
    
    # Sample rows
    sampled_rows = df.sample(n=sample_size)
    
    # Extract desired columns
    sampled_values = sampled_rows[columns]
    
    return sampled_values

# Example usage
file_path = 'X:\My Documents\Research\Tetris\startboards.tsv'
columns_of_interest = ['curr_zoid', 'next_zoid', 'zoid_rot', 'zoid_row', 'zoid_col','start_board']  # Specify the columns you want to extract
sample_size = 10  # Number of lines to sample

sampled_data = sample_tsv_lines(file_path, columns_of_interest, sample_size)

print(type(sampled_data.iloc[1,5]))
state = State(None, Board(20, 10))
all_zoids = {
        'I': zoids.classic.I,
        'T': zoids.classic.T,
        'L': zoids.classic.L,
        'J': zoids.classic.J,
        'O': zoids.classic.O,
        'Z': zoids.classic.Z,
        'S': zoids.classic.S
    }

#cell_value = sampled_data.at[1, 'curr_zoid']
#print(cell_value)
for index in range(sample_size):
    zoid = all_zoids[sampled_data.iloc[index, 0]]
    rot = sampled_data.iloc[index, 2]
    row = sampled_data.iloc[index, 3]
    col = sampled_data.iloc[index, 4]
   
    human_board = state.future(zoid, rot, 20-row, col)
    #print(human_board.board)
    extracted_board = sampled_data.iloc[index,5]
    clipped_board = extracted_board[1:-1]
    
    #print(repr(clipped_board))
    do_it_live = '[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 0, 0, 0, 0, 2, 2, 0, 0], [5, 5, 0, 0, 0, 6, 2, 2, 0, 0], [5, 6, 6, 6, 0, 6, 6, 6, 7, 0], [6, 6, 5, 6, 0, 3, 7, 7, 7, 0], [6, 5, 5, 4, 3, 3, 3, 5, 5, 0], [1, 6, 5, 5, 3, 4, 3, 2, 2, 0], [1, 6, 6, 6, 4, 4, 4, 2, 2, 0], [1, 3, 6, 6, 6, 4, 5, 5, 5, 0], [0, 1, 5, 4, 4, 5, 7, 7, 7, 1], [0, 1, 4, 4, 5, 5, 7, 2, 2, 1], [1, 1, 7, 7, 5, 3, 0, 2, 2, 7], [1, 6, 1, 0, 7, 7, 1, 7, 2, 2], [6, 6, 1, 5, 0, 1, 1, 3, 4, 7], [6, 6, 5, 5, 0, 1, 1, 3, 3, 5]]'
    #print(repr(do_it_live))
    do_it_live = unicodedata.normalize('NFKC', do_it_live)
    clipped_board = unicodedata.normalize('NFKC', clipped_board)

    #print('Extracted:', [hex(ord(c)) for c in clipped_board])
    #print('Manually defined:', [hex(ord(c)) for c in do_it_live])

    #extracted_board = extracted_board.strip()
    #print(len(extracted_board))
    #print(repr(extracted_board))
    #json_board = json.loads(extracted_board)
    #json_dump = json.dumps(sampled_data.iloc[index,5])
    live_board = json.loads(do_it_live)
    #print(live_board)
    #print(len(live_board))
    json_board = json.loads(clipped_board, encoding='utf-8')
    #print(clipped_board)
    #print(len(clipped_board))
    
    #model_board = parse_board(json_board)
    #print(model_board)
