filename = "d_cactus_2"
sim_globals = {}
speedup = 1000

sim_items = {
	Items.Carrot: 1000000,
	Items.Wood: 1000000,
	Items.Hay: 1000000,
	Items.Pumpkin: 1000000,
	Items.Cactus: 0,
	Items.Bone: 1000000,
	Items.Weird_Substance: 1000000,
	Items.Gold: 0,
	Items.Water: 1000000,
	Items.Fertilizer: 1000000,
	Items.Power: 10000
}

ITERATIONS = 10
total_seconds = 0
for i in range(ITERATIONS):
	seconds = simulate(filename, Unlocks, sim_items, sim_globals, i, speedup)
	quick_print(i, ':', seconds)
	total_seconds = total_seconds + seconds
quick_print("DONE, average", total_seconds / ITERATIONS, 'seconds')
