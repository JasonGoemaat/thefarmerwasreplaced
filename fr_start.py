import fr_maze
import frd
import fr_cactus

def single_hay(qty):
	while num_items(Items.Hay) < qty:
		if can_harvest():
			harvest()

def single_hay_3(qty):
	while num_items(Items.Hay) < qty:
		harvest()
		move(North)
		
def single_hay_3x3(qty):
	while num_items(Items.Hay) < qty:
		if can_harvest():
			harvest()
		move(North)
		if can_harvest():
			harvest()
		move(North)
		if can_harvest():
			harvest()
		move(East)
		
def single_wood_3(qty):
	while num_items(Items.Wood) < qty:
		if can_harvest():
			harvest()
			plant(Entities.Bush)
		move(North)
		
def single_wood_3x3(qty):
	while num_items(Items.Wood) < qty:
		for i in range(3):
			if can_harvest():
				harvest()
				plant(Entities.Bush)
			if i < 2:
				move(North)
		move(East)

def single_carrot_3x3(qty):
	while num_items(Items.Carrot) < qty:
		for i in range(3):
			if can_harvest():
				harvest()
				if get_ground_type() != Grounds.Soil:
					till()
				if not plant(Entities.Carrot):
					print('oops')
			if i < 2:
				move(North)
		move(East)


def single_carrot_4x4(qty):
	while num_items(Items.Carrot) < qty:
		for i in range(4):
			if can_harvest():
				harvest()
				if get_ground_type() != Grounds.Soil:
					till()
				if not plant(Entities.Carrot):
					print('oops')
			if i < 3:
				move(North)
		move(East)
		
def single_carrot_5x5(qty):
	while num_items(Items.Carrot) < qty:
		for i in range(5):
			if can_harvest():
				harvest()
				if get_ground_type() != Grounds.Soil:
					till()
				if not plant(Entities.Carrot):
					print('oops')
			if i < 4:
				move(North)
		move(East)
		
def hay_wood_4x4(qty, wood_rows):
	while num_items(Items.Hay) < qty:
		for i in range(4):
			if can_harvest():
				harvest()
				if i < wood_rows:
					plant(Entities.Bush)
			if i < 3:
				move(North)
			else:
				move(East)

def hay_wood_5x5(qty, wood_rows):
	while num_items(Items.Hay) < qty:
		for i in range(5):
			if can_harvest():
				harvest()
				if i < wood_rows:
					plant(Entities.Bush)
			if i < 4:
				move(North)
			else:
				move(East)

def mixed_6x6(qtys, hay_rows):
	entities = [Entities.Carrot, Entities.Tree]
	def pass_till():
		for i in range(6):
			for j in range(6):
				if can_harvest():
					harvest()
				if get_pos_y() >= hay_rows:
					if get_ground_type() != Grounds.Soil:
						till()
					if (get_pos_x() + get_pos_y()) % 2 == 0:
						plant(Entities.Tree)
					else:
						plant(Entities.Carrot)
				else:
					if get_ground_type() != Grounds.Grassland:
						till()
				if j < 5:
					move(North)
				else:
					move(East)
	def pass_ready():
		for i in range(6):
			for j in range(6):
				if can_harvest():
					harvest()
					if get_pos_y() >= hay_rows:
						if (get_pos_x() + get_pos_y()) % 2 == 0:
							plant(Entities.Tree)
						else:
							plant(Entities.Carrot)
				if j < 5:
					move(North)
				else:
					move(East)
	def done():
		if num_items(Items.Hay) < qtys[0]:
			return False
		if num_items(Items.Wood) < qtys[1]:
			return False
		if num_items(Items.Carrot) < qtys[2]:
			return False
		return True
	pass_till()
	while not done():
		pass_ready()

# mixed already configured, complete more passes
def mixed_6x6_passes(passes, hay_rows):
	def pass_ready():
		for i in range(6):
			for j in range(6):
				if can_harvest():
					harvest()
					if get_pos_y() >= hay_rows:
						if (get_pos_x() + get_pos_y()) % 2 == 0:
							plant(Entities.Tree)
						else:
							plant(Entities.Carrot)
				if j < 5:
					move(North)
				else:
					move(East)
	for i in range(passes):
		pass_ready()

def mixed_6x6_passes_report(passes, hay_rows):
	start = [num_items(Items.Hay),num_items(Items.Wood),num_items(Items.Carrot)]
	def pass_ready():
		for i in range(6):
			for j in range(6):
				if can_harvest():
					harvest()
					if get_pos_y() >= hay_rows:
						if (get_pos_x() + get_pos_y()) % 2 == 0:
							plant(Entities.Tree)
						else:
							plant(Entities.Carrot)
				if j < 5:
					move(North)
				else:
					move(East)
	for i in range(passes):
		pass_ready()
	end = [num_items(Items.Hay),num_items(Items.Wood),num_items(Items.Carrot)]
	quick_print(passes, "passes")
	quick_print('    Hay    :', (end[0]-start[0])/passes,'per pass')
	quick_print('    Wood   :', (end[1]-start[1])/passes,'per pass')
	quick_print('    Carrots:', (end[2]-start[2])/passes,'per pass')

def quick_8(passes, hay):
	for p in range(passes):
		for i in range(8):
			for j in range(8):
				if can_harvest():
					harvest()
					if i >= hay:
						plant(Entities.Bush)
				if j < 7:
					move(North)
				else:
					move(East)

HAVE_ITEMS = [Items.Hay, Items.Wood, Items.Carrot, Items.Power]
def have(qtys):
	global HAVE_ITEMS
	for i in range(len(qtys)):
		qty = qtys[i]
		if qty > 0 and num_items(HAVE_ITEMS[i]) < qty:
			return False
	return True

def mixed_8x8_passes_report(passes, hay_rows, sunflower_rows):
	items = [Items.Hay, Items.Wood, Items.Carrot, Items.Power]
	start = []
	for item in items:
		start.append(num_items(item))

	def pass_ready():
		for i in range(8):
			for j in range(8):
				if can_harvest():
					harvest()
					if get_pos_y() >= hay_rows:
						if get_ground_type() != Grounds.Soil:
							till()
						if get_pos_y() >= hay_rows + sunflower_rows:
							if (get_pos_x() + get_pos_y()) % 2 == 0:
								plant(Entities.Tree)
							else:
								plant(Entities.Carrot)
						else:
							plant(Entities.Sunflower)
					else:
						if get_ground_type() != Grounds.Grassland:
							till()
				if j < 7:
					move(North)
				else:
					move(East)
	for i in range(passes):
		pass_ready()
	end = []
	for item in items:
		end.append(num_items(item))
	quick_print(passes, "passes for mixed_8x8_passes_report")
	for i in range(len(items)):
		quick_print('    ', items[i], (end[i]-start[i])/passes,'per pass')

def mixed_8x8(qtys, hay_rows, sunflower_rows):
	def do_pass():
		for i in range(8):
			for j in range(8):
				if can_harvest():
					harvest()
					if get_pos_y() >= hay_rows:
						if get_ground_type() != Grounds.Soil:
							till()
						if get_pos_y() >= hay_rows + sunflower_rows:
							if (get_pos_x() + get_pos_y()) % 2 == 0:
								plant(Entities.Tree)
							else:
								plant(Entities.Carrot)
						else:
							plant(Entities.Sunflower)
					else:
						if get_ground_type() != Grounds.Grassland:
							till()
				if j < 7:
					move(North)
				else:
					move(East)
	while True:
		do_pass()
		if have(qtys):
			return

# same, but use a bit of fertilizer on the grass to get some seed Weird_Substance
def mixed_8x8f(qtys, hay_rows, sunflower_rows):
	def do_pass():
		for i in range(8):
			for j in range(8):
				if can_harvest():
					harvest()
					if get_pos_y() >= hay_rows:
						if get_ground_type() != Grounds.Soil:
							till()
						if get_pos_y() >= hay_rows + sunflower_rows:
							if (get_pos_x() + get_pos_y()) % 2 == 0:
								plant(Entities.Tree)
							else:
								plant(Entities.Carrot)
						else:
							plant(Entities.Sunflower)
					else:
						if get_ground_type() != Grounds.Grassland:
							till()
						if get_pos_x() in [1,4] and get_pos_y() in [1,3,5,7]:
							if num_items(Items.Fertilizer) > 0:
								use_item(Items.Fertilizer)
				if j < 7:
					move(North)
				else:
					move(East)
	while True:
		do_pass()
		if have(qtys):
			return

def mixed_8x8w(qtys, hay_rows, sunflower_rows):
	def do_pass():
		for i in range(8):
			for j in range(8):
				if can_harvest():
					harvest()
					if get_pos_y() >= hay_rows:
						if get_ground_type() != Grounds.Soil:
							till()
						if get_pos_y() >= hay_rows + sunflower_rows:
							if (get_pos_x() + get_pos_y()) % 2 == 0:
								plant(Entities.Tree)
							else:
								plant(Entities.Carrot)
						else:
							plant(Entities.Sunflower)
					else:
						if get_ground_type() != Grounds.Grassland:
							till()
						if i in [1,3] and j in [1,3,5]:
							if num_items(Items.Fertilizer) > 0:
								use_item(Items.Fertilizer)
							elif num_items(Items.Weird_Substance) > 0:
								use_item(Items.Weird_Substance)
				if j < 7:
					move(North)
				else:
					move(East)
	while True:
		do_pass()
		if have(qtys):
			return
			

def pumpkins(qty):
	WORLD_SIZE = get_world_size()
	LAST = WORLD_SIZE - 1
	LIMIT = WORLD_SIZE * WORLD_SIZE
	def do_plant():
		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE):
				if get_ground_type() != Grounds.Soil:
					till()
				plant(Entities.Pumpkin)
				if j < LAST:
					move(North)
				else:
					move(East)
	def replant():
		count = 0
		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE):
				if can_harvest():
					count = count + 1
				elif get_entity_type() == Entities.Dead_Pumpkin:
					harvest()
					plant(Entities.Pumpkin)
					use_item(Items.Water)
				if j < LAST:
					move(North)
				else:
					move(East)
		return count
	for i in range(qty):
		do_plant()
		while replant() < LIMIT:
			pass
		harvest()

single_hay(20)
unlock(Unlocks.Speed)
single_hay(30)
unlock(Unlocks.Expand)
single_hay_3(70) # enough to unlock bush
unlock(Unlocks.Plant)
single_wood_3(20) # enough to speed up drone or expand

# 129.3 seconds, have 3 hay only - expand is better first
#unlock(Unlocks.Speed)
#single_wood_3(20) # enough to expand to 3x3
#unlock(Unlocks.Expand)

# 129.2 seconds, slightly better, have 20 hay and .1 sec
unlock(Unlocks.Expand)
single_wood_3x3(20) # enough to expand to 3x3
unlock(Unlocks.Speed)

# Carrots - 50 wood
single_wood_3x3(50) # enough to unlock carrots
unlock(Unlocks.Carrots)

# Possible unlocks:
# Expand to 4x4 - 30 wood, 20 carrots
# Speed - 50 wood, 50 carrots
# Double hay - 300

# Need SOME hay to plant carrots, wood also
# going for expand, carrots take longer to grow than 
single_hay_3x3(15) # 20 hay for 20 carrots, wood will get 9
single_wood_3x3(49) # need 20 for 20 carrots, plus 30 for speed
single_carrot_3x3(20)

# 31 wood, 20 carrots, expand to 4x4 (clears to hay)
unlock(Unlocks.Expand)

# 300 hay plus 1 wood row, gives 118 wood
hay_wood_4x4(300, 1)
unlock(Unlocks.Grass) # double grass production
hay_wood_4x4(300, 3) # keep it up, need 100 grass and 150+100 wood
# 206 hay, 303 wood, 1 carrot

# Speed - 50 wood, 50 carrot
# Expand - 100 wood, 50 carrot
single_carrot_4x4(100)
unlock(Unlocks.Expand)
unlock(Unlocks.Speed)

hay_wood_5x5(300, 4)
# 300h, 252w, 1c
unlock(Unlocks.Watering)
unlock(Unlocks.Expand)
single_carrot_5x5(70) # 70 to unlock Trees
unlock(Unlocks.Trees)

# trying out mixed crops, rows of hay and mixed
clear()
mixed_6x6([0,250,0], 1) # 250 wood to double carrot production
unlock(Unlocks.Carrots)
# mixed_6x6([0,500,500], 1) # 500 carrots for speed and 500 wood for grass
unlock(Unlocks.Trees) # better wood production
mixed_6x6_passes(2, 1)
unlock(Unlocks.Grass) # running low on grass
mixed_6x6_passes(1, 1)
unlock(Unlocks.Watering)
mixed_6x6_passes(4, 1) # 13-20 hay,f 260 wood, 50 carrots per pass
unlock(Unlocks.Carrots)
mixed_6x6_passes(4, 4)
unlock(Unlocks.Speed)
mixed_6x6_passes_report(10, 1) # enough wood to boost hay production
unlock(Unlocks.Grass)
# 1200 grass to double wood production
mixed_6x6([1200,0,0],3)
unlock(Unlocks.Speed)
unlock(Unlocks.Trees)
unlock(Unlocks.Watering) # let it build
mixed_6x6([0,500,200],3) # unlock pumpkins
unlock(Unlocks.Pumpkins)
mixed_6x6([0,300,300],3) # enough for some pumpkin runs
clear()
pumpkins(6)
unlock(Unlocks.Expand)
quick_8(5, 4) # quick get some hay and wood so I can plant enough carrots
unlock(Unlocks.Grass)
unlock(Unlocks.Fertilizer)
mixed_8x8([5000],4,0) # [hay,wood,carrot,power],hay,sunflower - 4800 hay to upgrade trees
unlock(Unlocks.Trees)
mixed_8x8([0,6400],4,0) # 6250 wood to upgrade carrots
unlock(Unlocks.Carrots)
mixed_8x8([0,12700],4,0) # 12500 wood to upgrade grass
unlock(Unlocks.Grass)
mixed_8x8([0,2500],4,0) # 1250 to upgrade ferilizer
unlock(Unlocks.Fertilizer)
unlock(Unlocks.Sunflowers)
unlock(Unlocks.Pumpkins)
mixed_8x8f([],4,0) # one pass to use some ferilizer
mixed_8x8([],4,0) # one pass collects some weird substance
while num_items(Items.Weird_Substance) < 3400: # 1000 unlock, 2400 for 300 runs
	mixed_8x8w([],2,1)
unlock(Unlocks.Trees)
unlock(Unlocks.Carrots)
unlock(Unlocks.Watering)
unlock(Unlocks.Fertilizer)
unlock(Unlocks.Watering)
unlock(Unlocks.Fertilizer)
unlock(Unlocks.Pumpkins)
unlock(Unlocks.Pumpkins)
unlock(Unlocks.Mazes) # need 8 per maze, 2000 treasure for drones
fr_maze.mazes(10000) # enough for drone farming, but maybe should get more?
unlock(Unlocks.Megafarm)
unlock(Unlocks.Megafarm)
frd.frd_mix(2,1,{Items.Carrot: 20000}, True)
frd.frd_pumpkins(8000) # 8000 pumpkins for expand to 12x12
unlock(Unlocks.Expand)
frd.frd_pumpkins(5000) # 5000 for cactus
unlock(Unlocks.Cactus)

#items = frd.count_items()
frd.frd_mix(2,4,{Items.Carrot: 20000, Items.Wood: 63000})
#frd.report_item_gain(items)

unlock(Unlocks.Watering)
unlock(Unlocks.Fertilizer)
unlock(Unlocks.Grass)

frd.frd_pumpkins(84000) # cactus and expand, costs carrots
unlock(Unlocks.Cactus)
unlock(Unlocks.Expand)
unlock(Unlocks.Trees)
frd.frd_mix(2,4,{Items.Wood: 20000}, True)
# 63.4k, cost 16 substance, get 64 gold each run, 4800 substance -> 

frd.frd_mix(2,4,{Items.Carrot: 15000}, True)
frd.frd_pumpkins(51128) # need 48128 for 12000 cactus and 3000 for polyculture
unlock(Unlocks.Polyculture)
fr_cactus.cactus(12000) # 6 hours
unlock(Unlocks.Mazes)

# wait for maze, cactus improves it
fr_maze.mazes(32000) # full run 300, 2h13, 76.8k, 1h13 for 32k, double drones


# frd.frd_pumpkins(5000) # 5000 pumpkins for cactus upgrade
# unlock(Unlocks.Mazes) # 12000 cacti required
# unlock(Unlocks.Cactus) # 5000 pumpkins required
for u in Unlocks:
	cost = get_cost(u)
	if len(cost) > 0:
		quick_print(u, cost, len(cost))

quick_print("DONE")