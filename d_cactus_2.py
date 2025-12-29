RUNS = 1

# d_cactus_2 - trying to do it faster, sort vertically first,
# ensuring each column in sorted.   This lets the drones sort
# to each direction and move less and less, placing largest
# at the top, then it can be ignored, place smallest at bottom,
# then it can be ignored.   This means the drone bounces back
# and forth over a shortening path every time.
# After that, it starts new drones to sort each row horizontally.

size = min(get_world_size(), max_drones())
extra = max(0, get_world_size() - max_drones())

def init_column():
	for i in range(size):
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Cactus)
		move(North)
	
def sort_column():
	low = 0
	high = size - 1
	while low < high:
		last_swap = -1
		# move North to high - 1, move current up 1 if larger
		# will end with largest at top
		while get_pos_y() < high:
			if measure() > measure(North):
				swap(North)
				last_swap = get_pos_y()
			if get_pos_y() >= high - 1:
				break
			move(North)
		if last_swap < 0:
			break # no swaps, we're done
		high = last_swap # all higher are sorted already
		last_swap = -1
		while get_pos_y() > low:
			if measure() < measure(South):
				swap(South)
				last_swap = get_pos_y()
			if get_pos_y() <= low + 1:
				break
			move(South)
		if last_swap < 0:
			break # no swaps
		low = last_swap
	
def sort_row():
	low = 0
	high = size - 1
	while low < high:
		last_swap = -1
		# move North to high - 1, move current up 1 if larger
		# will end with largest at top
		while get_pos_x() < high:
			if measure() > measure(East):
				swap(East)
				last_swap = get_pos_x()
			if get_pos_x() >= high - 1:
				break
			move(East)
		if last_swap < 0:
			break # no swaps, we're done
		high = last_swap # all higher are sorted already
		last_swap = -1
		while get_pos_x() > low:
			if measure() < measure(West):
				swap(West)
				last_swap = get_pos_x()
			if get_pos_x() <= low + 1:
				break
			move(West)
		if last_swap < 0:
			break # no swaps
		low = last_swap
			
def move_to_origin():
	while get_pos_y() > get_world_size() / 2:
		move(North)
	while get_pos_y() > 0:
		move(South)
	while get_pos_x() > get_world_size() / 2:
		move(East)
	while get_pos_x() > 0:
		move(West)

def run():
	drones = []
	for i in range(size - 1):
		drones.append(spawn_drone(init_column))
		move(East)
	init_column()
	move_to_origin()
	for d in drones:
		wait_for(d)
		
	drones = []
	for i in range(size - 1):
		drones.append(spawn_drone(sort_column))
		move(East)
	sort_column()
	move_to_origin()
	for d in drones:
		wait_for(d)

	drones = []
	for i in range(size - 1):
		drones.append(spawn_drone(sort_row))
		move(North)
	sort_row()
	move_to_origin()
	for d in drones:
		wait_for(d)

	harvest()

clear()
runs = 0
while runs < RUNS:
	run()
	runs = runs + 1

quick_print("Cacti:", num_items(Items.Cactus))
