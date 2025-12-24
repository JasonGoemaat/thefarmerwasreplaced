# Idea is to spawn one drone per column
# Drone will manage column until everything is harvestable.
# Main drone waits for drone count to go to 0, then harvests and restarts

size = min(max_drones(), get_world_size())
over = max(0, get_world_size() - size)

def do_init():
	global size
	global over
	def init_column():
		for i in range(size):
			till()
			move(North)
		for i in range(over):
			harvest()
			move(North)
	
	for i in range(size - 1):
		if spawn_drone(init_column):
			move(East)
	init_column()

def do_col():
	global size
	global over
	for i in range(size):
		plant(Entities.Pumpkin)
		move(North)
	for i in range(over):
		harvest()
		move(North)
	
	while True:
		count = 0
		for i in range(size):
			if get_entity_type() == Entities.Dead_Pumpkin:
				harvest()
				plant(Entities.Pumpkin)
			else:
				if can_harvest():
					count = count + 1
			move(North)
		for i in range(over):
			harvest()
			move(North)
		if count == size:
			break
	
clear()
do_init()

while True:
	while get_pos_x() != 0:
		move(East) # back to west edge
	for i in range(size - 1):
		if spawn_drone(do_col):
			move(East)
	do_col()
	while get_pos_x() != 0:
		move(East) # back to west edge
	while num_drones() > 1:
		do_a_flip() # wait until all drones are done
	harvest()
		
	