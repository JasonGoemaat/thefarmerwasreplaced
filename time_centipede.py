filename = "centipede"
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
	Items.Power: 1000000000
}

for length in lengths:
	sim_globals["MAX_LENGTH"] = length
	seconds = simulate(filename, Unlocks, sim_items, sim_globals, 0, speedup)
	bones = length * length
	bones_per_second = bones / seconds
	s = str(length) + ": " + str(bones) + " in " + str(seconds) + "s, " + str(bones_per_second) + "b/s"
	# quick_print(seconds,'for length', sim_globals["MAX_LENGTH"], 'gave ',bones,'bones at ',bones_per_second)
	outputs.append(s)
	quick_print(s)
	
quick_print("DONE")

#10: 100 in 34.53s, 2.9b/s
#50: 2500 in 179.84s, 13.9b/s
#100: 10000 in 273s, 36.63b/s
#200: 40000 in 439.53s, 91.01b/s
#300: 90000 in 679.45s, 132.46b/s
#400: 160000 in 995.2s, 160.77b/s
#500: 250000 in 1391.72s, 179.63b/s
#600: 360000 in 1826.37s, 197.11b/s
#700: 490000 in 2353.67s, 208.19b/s
#800: 640000 in 2887.8s, 221.62b/s
#900: 810000 in 3392.34s, 238.77b/s