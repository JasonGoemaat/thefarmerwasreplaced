# Idea is to spawn one drone per column
# Drone will manage column until everything is harvestable.
# Main drone waits for drone count to go to 0, then harvests and restarts

def do_init():
	def init_column():
		for i in range(get_world_size()):
			till()
			move(North)
	
	for i in range(get_world_size() - 1):
		if spawn_drone(init_column):
			move(East)
	init_column()

def do_col():
	for i in range(get_world_size()):
		plant(Entities.Pumpkin)
		move(North)
	
	while True:
		count = 0
		for i in range(get_world_size()):
			if get_entity_type() == Entities.Dead_Pumpkin:
				harvest()
				plant(Entities.Pumpkin)
			else:
				if can_harvest():
					count = count + 1
			move(North)
		if count == get_world_size():
			break
	
clear()
do_init()

while True:
	for i in range(get_world_size()):
		if spawn_drone(do_col):
			move(East)
	do_col()
	while num_drones() > 1:
		for i in range(get_world_size()):
			move(East)
	harvest()
		
