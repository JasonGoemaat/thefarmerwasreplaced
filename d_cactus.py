# Plant entire farm in cacti

size = min(get_world_size(), max_drones())
extra = max(0, get_world_size() - max_drones())

def init():
	def do_init():
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Cactus)
	for i in range(size - 1):
		spawn_drone(do_init)
	do_init()
	for i in range(extra):
		move(North)
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
