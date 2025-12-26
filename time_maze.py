filename = "maze_astar"
sim_globals = {"MAX_LENGTH": 10}
speedup = 1000

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

seconds = simulate(filename, Unlocks, sim_items, sim_globals, 0, speedup)
quick_print(seconds)
quick_print("DONE")
