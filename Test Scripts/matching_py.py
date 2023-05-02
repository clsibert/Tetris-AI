from __future__ import print_function, division
import csv
import json
import random
import sys

from cogworks.tetris.game import State, Board, zoids
from cogworks.tetris import features, simulator
from cogworks import feature

# Parses a Board from its JSON representation
def parse_board(rep):
    rows = len(rep)
    cols = None
    for row in rep:
        if cols is None:
            cols = len(row)
        else: assert cols == len(row)

    board = Board(rows, cols, zero=False)
    board.heights = [0] * cols

    for r in range(0, rows):
        for c in range(0, cols):
            board.data[r,c] = bool(rep[r][c])
            if not board.heights[c] and board.data[r,c]:
                board.heights[c] = r

    return board

# Prints all board arguments next to each other
def print_spliced(*states):
    # Prints the boards
    print('\n'.join('\t'.join(x) for x in zip(*[str(state.board).split('\n') for state in states])))

    # Prints the scores underneath them
    print('\t'.join('{:{width}d}'.format(state.score(), width=state.board.cols()) for state in states))

# Generates a list of possible immediate futures from a state, given a zoid and move_gen
def gen_futures(state, zoid, move_gen):
    return [state.future(zoid, *move) for move in move_gen(state, zoid)]

straightdrop = {
	features.landing_height: -3.383,
	features.eroded_cells: -9.277,
	features.row_trans: -2.700,
	features.col_trans: -6.786,
	features.pits: -12.668,
	features.cuml_wells: -0.396}

with open("test2.tsv", 'r') as file:
    reader = csv.DictReader(file, dialect='excel-tab')
    state = State(None, Board(20, 10))
      
    # Read the input file
    for line in (line for line in reader if line["event_type"] == 'EP_SUMM'):
        # Parse the zoid
        zoid = {
            'I': zoids.classic.I,
            'T': zoids.classic.T,
            'L': zoids.classic.L,
            'J': zoids.classic.J,
            'O': zoids.classic.O,
            'Z': zoids.classic.Z,
            'S': zoids.classic.S
        }[line["curr_zoid"]]

        # Parse the move
        rot = int(line["zoid_rot"])
        row = int(line["zoid_row"])
        col = int(line["zoid_col"])

        # Apply the move to the tracking state (retains history)
        ours = state.future(zoid, rot, 20 - row, col)
        # Create a new Board (no history) from the log
        # It has full lines, so clear those to match ours
        theirs = parse_board(json.loads(line["board_rep"][1:-1]))
        theirs.clear(theirs.full())
        # our board and theirs should element-wise match here
        assert ours.board == theirs

        feats = straightdrop
        # Generate the possible states for the current zoid
        possible = gen_futures(state, zoid, simulator.move_drop)
        possible = [(sum(feature.evaluate(s, feats).values()), s) for s in possible]
        # Order them (ascending order) according to some criteria (key=function of state):
        
        possible.sort(key=lambda x: -x[0])
        scores, possible = zip(*possible)
        print(zoid, '->', {"rot": rot, "row": row, "col": col})
        # Print the previous and next state
        
        
        #state = board before move is made
        #ours = what human did
        #possible = list of possible moves
        #possible[0] SHOULD BE what the model chooses
        
        print_spliced(state, ours)
        
        print(possible[0].board)
        print(scores)
        
        if possible[0].board == ours.board:
            print("Match")
        
        # Print the top five moves, according to criteria
        print_spliced(*possible[:5])
        print()

        # Update state to maintain history
        state = ours
