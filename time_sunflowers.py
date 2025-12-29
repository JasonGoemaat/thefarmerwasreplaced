sim_globals = {"MAX_LENGTH": 10}
speedup = 1000

lengths = [10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900]
outputs = []

sim_items = {
	Items.Carrot: 1000000000,
	Items.Wood: 1000000000,
	Items.Hay: 1000000000,
	Items.Pumpkin: 1000000000,
	Items.Cactus: 1000000000,
	Items.Bone: 1000000000,
	Items.Weird_Substance: 1000000000,
	Items.Gold: 1000000000,
	Items.Water: 1000000000,
	Items.Fertilizer: 1000000000,
	Items.Power: 1000
}

def time_trial(filename):
	seconds = simulate(filename, Unlocks, sim_items, sim_globals, 0, speedup)
	print(filename, seconds)

time_trial("sunflower_1")
time_trial("sunflower_2")