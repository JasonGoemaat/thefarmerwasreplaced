# filenames = ["maze_astar_original", "maze_astar_forward", "maze_astar_nopop"]
# filenames = ["maze_astar_nopop","maze_astar_nopop_uns"]
filenames = ["maze_astar_nopop"]

sim_globals = {"MAX_LENGTH": 10}
speedup = 100000
set_world_size(8)

sim_items = {
	Items.Carrot: 1000000,
	Items.Wood: 1000000,
	Items.Hay: 1000000,
	Items.Pumpkin: 1000000,
	Items.Cactus: 1000000,
	Items.Bone: 1000000,
	Items.Weird_Substance: 1000000,
	Items.Gold: 0,
	Items.Water: 1000000,
	Items.Fertilizer: 1000000,
	Items.Power: 10000
}

for filename in filenames:
	seconds = simulate(filename, Unlocks, sim_items, sim_globals, 0, speedup)
	quick_print(filename, seconds)

quick_print("DONE")
