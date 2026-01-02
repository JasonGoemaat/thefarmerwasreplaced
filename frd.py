# Fastest Restart Drone-aware

def count_items():
	items = [Items.Hay, Items.Wood, Items.Carrot, Items.Cactus, Items.Gold, Items.Pumpkin, Items.Power]

def return_to_origin():
	if get_pos_x() < get_world_size() / 2:
		for i in range(get_pos_x()):
			move(West)
	else:
		for i in range(get_world_size() - get_pos_x()):
			move(East)
	if get_pos_y() < get_world_size() / 2:
		for i in range(get_pos_y()):
			move(South)
	else:
		for i in range(get_world_size() - get_pos_y()):
			move(North)

def loop_over(WORLD_SIZE, cols_per_drone, LIMIT, f):
	for i in range(cols_per_drone):
		for j in range(WORLD_SIZE):
			f()
			move(North)
		if i < LIMIT:
			move(East)
	for i in range(LIMIT):
		move(West)

# divides farm up so one drone gets X columns
# runs any function until resources are met
# function will be passed number of columns, should do 1 pass
# and return True if it was good:
#		for pumpkins, full count
#		for 
# unfortunately, each drone must check the function
# here the 
def frd_pumpkins(GOAL = 0, iterations = 1000):
	WORLD_SIZE = get_world_size()
	factor = 2**(num_unlocked(Unlocks.Pumpkins) - 1)
	GAIN = WORLD_SIZE * WORLD_SIZE * 6 * factor
	CARROT_COST = WORLD_SIZE * WORLD_SIZE * factor
	afford_iterations = num_items(Items.Carrot) // CARROT_COST
	if GOAL > 0:
		goal_iterations = (GOAL + GAIN - 1) // GAIN
		goal_cost = goal_iterations * CARROT_COST * 1.3 # factor for replanting 1/3
		if num_items(Items.Carrot) < goal_cost:
			quick_print("frd_pumpkins: have", num_items(Items.Carrot), "but need", goal_cost)
	clear()
	set_execution_speed(1)
	#return_to_origin() # not needed if clear()
	MAX_DRONES = max_drones()
	if WORLD_SIZE % MAX_DRONES != 0:
		print('UH OH! frd drones 1')
		return
	cols_per_drone = WORLD_SIZE // MAX_DRONES # must be divisible
	LIMIT = cols_per_drone - 1
	REQUIRED = cols_per_drone * WORLD_SIZE
	
	def drone_pumpkins_2():
		def handler1():
			if get_entity_type() != None:
				if can_harvest():
					harvest()
				else:
					till()
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Pumpkin)
			if get_entity_type() != Entities.Pumpkin:
				print('UH OH! Pumpkin-o!')
				
		def handler2():
			if can_harvest():
				count = count + 1
				if count >= REQUIRED:
					return True
			entity_type = get_entity_type()
			if entity_type == Entities.Dead_Pumpkin:
				harvest()
				plant(Entities.Pumpkin)
				if get_water() < 0.75:
					use_item(Items.Water)
				move(North)
				continue
			if entity_type != Entities.Pumpkin:
				# harvested early (checking measure()?)
				return

		loop_over(handler1)
	
	def drone_pumpkins():
		for i in range(cols_per_drone):
			for j in range(WORLD_SIZE):
				if get_entity_type() != None:
					if can_harvest():
						harvest()
					else:
						till()
				if get_ground_type() != Grounds.Soil:
					till()
				plant(Entities.Pumpkin)
				while get_entity_type() == Entities.Dead_Pumpkin:
					harvest()
					plant(Entities.Pumpkin)
				move(North)
			if i < LIMIT:
				move(East)
		for i in range(LIMIT):
			move(West)
			
		while True:
			count = 0
			for i in range(cols_per_drone):
				for j in range(WORLD_SIZE):
					if can_harvest():
						count = count + 1
						if count >= REQUIRED:
							return True
					entity_type = get_entity_type()
					if entity_type == Entities.Dead_Pumpkin:
						harvest()
						plant(Entities.Pumpkin)
						if get_water() < 0.75:
							use_item(Items.Water)
						move(North)
						continue
					if entity_type != Entities.Pumpkin:
						# harvested early (checking measure()?)
						return
					move(North)
				if i < LIMIT:
					move(East)
			for i in range(LIMIT):
				move(West)
	
	while GOAL <= 0 or num_items(Items.Pumpkin) < GOAL:
		remaining = WORLD_SIZE
		drones = []
		while remaining > cols_per_drone:
			drones.append(spawn_drone(drone_pumpkins))
			for i in range(cols_per_drone):
				move(East)
			remaining = remaining - cols_per_drone
		drone_pumpkins()
		return_to_origin()
		pumpkin_sw = measure() # I think sw is used when combining, like cactus
		move(South)
		move(West)
		while measure() != pumpkin_sw:
			pass
		harvest()
		move(North)
		move(East)

def frd_mix(hay, sunflowers, qty, use_weird = False):
	clear()
	WORLD_SIZE = get_world_size()
	MAX_DRONES = max_drones()
	if WORLD_SIZE % MAX_DRONES != 0:
		print('UH OH! Drone')
		return
	DRONE_COLS = WORLD_SIZE // MAX_DRONES # must be divisible
	LIMIT = DRONE_COLS - 1
	MIX_START = hay + sunflowers
	
	def is_done():
		for k in qty:
			if qty[k] >= num_items(k):
				return False
		return True

	def drone_run():
		while True:
			for i in range(DRONE_COLS):
				x = get_pos_x()
				for j in range(WORLD_SIZE):
					y = get_pos_y()
					if can_harvest():
						harvest()
						if y > hay:
							if get_ground_type() != Grounds.Soil:
								till()
							if y < MIX_START:
								plant(Entities.Sunflower)
							else:
								if (x + y) % WORLD_SIZE == 0:
									plant(Entities.Carrot)
								else:
									plant(Entities.Tree)
						if use_weird:
							if (get_pos_x() % 3) == 1 and (get_pos_y() % 3) == 1:
								use_item(Items.Weird_Substance)
					move(North)
				if i < LIMIT:
					move(East)
			for i in range(LIMIT):
				move(West)
			if is_done():
				return
		
	remaining = WORLD_SIZE
	drones = []
	while remaining > DRONE_COLS:
		drones.append(spawn_drone(drone_run))
		for i in range(DRONE_COLS):
			move(East)
		remaining = remaining - DRONE_COLS
	drone_run()
	for drone in drones:
		wait_for(drone)

def cactus(qty):
	# Plant entire farm in cacti
	WORLD_SIZE = get_world_size()
	MAX_DRONES = max_drones()
	
	def init():
		def do_init():
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Cactus)
		drones = []
		for i in range(WORLD_SIZE):
			if num_drones() < MAX_DRONES:
				drones.append(spawn_drone(do_init))
			else:
				do_init()
			move(East)
	
	have_swapped = False
	
	def perform_pass(main_direction, plant_flag):
		swaps_d = 0
		other_direction = North
		if main_direction == West:
			other_direction = South
	
		def do_pass(drone_index, direction):
			swaps_b = 0
	
			# move in direction and swap all around to help
			def do_direction(direction, last):
				swaps_a = 0
				x, y = get_pos_x(), get_pos_y()
				# swap all directions if helping
				if y > 0 and measure(South) != None and measure(South) > measure():
					swap(South)
					swaps_a = swaps_a + 1
				if x > 0 and measure(West) != None and measure(West) > measure():
					swap(West)
					swaps_a = swaps_a + 1
				if y < size - 1 and measure(North) < measure():
					swap(North)
					swaps_a = swaps_a + 1
				if x < size - 1 and measure(East) < measure():
					swap(East)
					swaps_a = swaps_a + 1
				if not last:
					move(direction)
				return swaps_a
				
			def do_my_pass():
				swaps_c = 0
				for i in range(size):
					if plant_flag:
						if get_ground_type() != Grounds.Soil:
							till()
						plant(Entities.Cactus)
						if i < size - 1:
							move(direction)
					else:
						swaps_c = swaps_c + do_direction(direction, i == (size - 1))
				return swaps_c
				
			return do_my_pass
	
		drones = []
		for i in range(size - 1):
			drones.append(spawn_drone(do_pass(i, other_direction)))
			move(main_direction)
		swaps_d = do_pass(size - 1, other_direction)()
		# note, no last move, we will end in opposite corner
			
		for d in drones:
			swaps_d = swaps_d + wait_for(d)
		
		if plant_flag or swaps_d > 0:
			# print(swaps_d, "swaps")
			return False
	
		return True
	
	clear()
	outer_direction = East
	while True:
		perform_pass(outer_direction, True)
		while True:
			if outer_direction == East:
				outer_direction = West
			else:
				outer_direction = East
			if perform_pass(outer_direction, False):
				harvest()
				break
		if outer_direction == East:
			outer_direction = West
		else:
			outer_direction = East
			
	
# frd_pumpkins()
