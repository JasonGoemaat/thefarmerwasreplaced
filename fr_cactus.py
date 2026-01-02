# cactus requires 2 pumpkins at level 1
def cactus(qty = 0, max_iterations = 1000):
	clear()
	WORLD_SIZE = get_world_size()
	LIMIT = WORLD_SIZE - 1
	# COST is to plant 1 farm, 2^upgrade_level (level 2 = 4)
	PUMPKIN_COST = WORLD_SIZE * WORLD_SIZE * 2**(num_unlocked(Unlocks.Cactus))
	GAIN = WORLD_SIZE * WORLD_SIZE
	afford_iterations = num_items(Items.Pumpkin) // PUMPKIN_COST
	max_iterations = min(max_iterations, afford_iterations)
	qty_iterations = (qty + GAIN - 1) // GAIN
	if qty > 0:
		max_iterations = min(max_iterations, qty_iterations)
		if qty_iterations > afford_iterations:
			quick_print("PROBLEM!  You need", qty_iterations * PUMPKIN_COST, 'pumpkins')
	quick_print('qty:', qty_iterations, ', afford:', afford_iterations)
	
	# till if needed and plant, then sort column
	def handle_col():
		# y >= high is sorted
		# y <= low is sorted
		low = -1 # everything ABOVE high is sorted
		high = -1 # everything ON OR ABOVE high is SORTED, set first pass

		# plant and push highest item to top, swapping with below
		# the last place we swapped with below is the new high, not sure about the
		# one below we swapped with
		for i in range(WORLD_SIZE):
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Cactus)
			if i > 0 and measure(South) > measure():
				swap(South)
				high = get_pos_y()
			if i < LIMIT:
				move(North)

		while high > low:
			# move to top unsorted space
			while get_pos_y() >= high:
				move(South)
			
			# starting at one row below highest sorted spot
			last_swap = -1
			while get_pos_y() > low + 1:
				move(South) # move first, pull along lower value to north
				if measure(North) < measure():
					swap(North)
					last_swap = get_pos_y()
			if last_swap == -1:
				return # sorted!
			low = last_swap

			# starting at lowest unsorted spot
			while get_pos_y() <= low:
				move(North)
			
			last_swap = -1
			while get_pos_y() < high-1:
				move(North)
				if measure(South) > measure():
					swap(South)
					last_swap = get_pos_y()
			
			if last_swap == -1:
				return # sorted!
			
			high = last_swap

	def handle_row():
		low = -1 # everything ABOVE high is sorted
		high = WORLD_SIZE # everything ON OR ABOVE high is SORTED

		while high > low:
			while get_pos_x() <= low:
				move(East)

			last_swap = -1
			while get_pos_x() < high-1:
				move(East)
				if measure(West) > measure():
					swap(West)
					last_swap = get_pos_x()

			if last_swap == -1:
				return # sorted!
			high = last_swap

			last_swap = -1
			while get_pos_x() > low + 1:
				move(West) # move first, pull along lower value to north
				if measure(East) < measure():
					swap(East)
					last_swap = get_pos_x()
			if last_swap == -1:
				return # sorted!
			low = last_swap
				
	def do_cols():
		drones = []
		for i in range(WORLD_SIZE):
			if num_drones() < max_drones():
				drones.append(spawn_drone(handle_col))
			else:
				handle_col()
				while get_pos_y() > 0:
					move(South)
			move(East)
		while get_pos_y() > 0:
			move(South)
		while get_pos_x() > 0:
			move(West)
		for drone in drones:
			wait_for(drone)
			
	def do_rows():
		drones = []
		for i in range(WORLD_SIZE):
			if num_drones() < max_drones():
				drones.append(spawn_drone(handle_row))
			else:
				handle_row()
				while get_pos_x() > 0:
					move(West)
			move(North)
		while get_pos_y() > 0:
			move(South)
		while get_pos_x() > 0:
			move(West)
		for drone in drones:
			wait_for(drone)
			
	for i in range(max_iterations):
		do_cols()
		do_rows()
		harvest()
		if qty > 0 and qty > num_items(Items.Cactus):
			return

# run file for testing
#set_world_size(8)
#cactus()