### Starting Simulator

## Generic imports
import random

## From Simulator Specific Code
from cogworks.tetris.game import State
from cogworks.tetris.game import Board
from cogworks.tetris.game import zoids

from cogworks.tetris import features
from cogworks.tetris import simulator

from cogworks import feature

testfeatures = {
	features.landing_height: -3.383,
	features.eroded_cells: -9.277,
	features.row_trans: -2.700,
	features.col_trans: -6.786,
	features.pits: -12.668,
	features.cuml_wells: -0.396}


## Create a piece generator (can use a list here, or a generator function)

# True Random Generator Function
def zoid_gen (zoids, rng):
	while True:
		yield rng.choice(zoids)

## Create a move generator (this is where overhang detection or time pressure filtering are implemented. move_drop is basic version)

move_gen = simulator.move_drop

## Define Features

feats = testfeatures

## Define Initial State

state = State(None, Board(20,10))

## Pick a seed (if using)

seed = 10101

## Create simulator "object"

sim = simulator.simulate(state, zoid_gen(zoids.classic, random.Random(seed)), move_gen, simulator.policy_best(lambda state: sum(feature.evaluate(state, feats).values()), random.Random(-seed).choice))

## Run the simulator
# Inside this loop, print episode level data to file (take a good look at state and delta classes in game.py)

for(episode, state) in enumerate(sim, 1):
	print (episode, state.delta.zoid)
	print (state.board)
	print

	# set some kind of limit
	if episode >= 525:
		break

print (state.score())
print (state.lines_cleared(1))
print (state.lines_cleared(2))
print (state.lines_cleared(3))
print (state.lines_cleared(4))
