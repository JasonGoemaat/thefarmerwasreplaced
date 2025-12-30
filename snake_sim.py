sim_globals = {"INPUT": 10}
speedup = 100000
seed = 9999

# inputs = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
inputs = [300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450]
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
	for i in range(len(inputs)):
		sim_globals["INPUT"] = inputs[i]
		seconds = simulate(filename, Unlocks, sim_items, sim_globals, seed, speedup)
		print(filename, i, ':', inputs[i], '-', seconds, 'seconds')

time_trial("snake_super5")


# sweet spot around 100 when speed is maxxed:
# snake_super3 0 : 50 - 1422.6 seconds
# snake_super3 1 : 100 - 1196.37 seconds
# snake_super3 2 : 200 - 1434.26 seconds
# snake_super3 0 : 60 - 1350.55 seconds
# snake_super3 1 : 70 - 1287.66 seconds
# snake_super3 2 : 80 - 1238.05 seconds
# snake_super3 3 : 90 - 1218.67 seconds
# snake_super3 4 : 100 - 1196.37 seconds
# snake_super3 5 : 110 - 1205.7 seconds
# snake_super3 6 : 120 - 1209.96 seconds
# snake_super3 7 : 130 - 1212.66 seconds
# snake_super3 8 : 140 - 1197.58 seconds

# Not popping helped, sweet spot moved to around 300:
# snake_super4 0 : 100 - 1072.81 seconds
# snake_super4 1 : 150 - 971.09 seconds
# snake_super4 2 : 200 - 942.4 seconds
# snake_super4 3 : 250 - 908.5 seconds
# snake_super4 4 : 300 - 894.68 seconds
# snake_super4 5 : 350 - 900.3 seconds
# snake_super4 6 : 400 - 920.47 seconds
# snake_super4 7 : 450 - 954.68 seconds

#snake_super5 0 : 100 - 1002.23 seconds
#snake_super5 1 : 150 - 938.48 seconds
#snake_super5 2 : 200 - 893.3 seconds
#snake_super5 3 : 250 - 858.55 seconds
#snake_super5 4 : 300 - 848.05 seconds
#snake_super5 5 : 350 - 852.54 seconds
#snake_super5 6 : 400 - 851.99 seconds
#snake_super5 7 : 450 - 878 seconds
#snake_super5 8 : 500 - 912.03 seconds
#snake_super5 9 : 550 - 970.51 seconds
