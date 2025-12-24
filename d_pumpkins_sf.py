# Idea is to spawn one drone per column
# Drone will manage column until everything is harvestable.
# Main drone waits for drone count to go to 0, then harvests and restarts

sunflowers = 2 # sunflower rows above pumpkins
mix = 2 # mix of carrots/trees above sunflowers
pumpkins = min(max_drones(), get_world_size() - sunflowers - mix)
grass = max(0, get_world_size() - pumpkins - sunflowers - mix) # remaining is grass at top
flag_water = True

parts = (pumpkins, sunflowers, grass)

def do_water():
	global flag_water
	if not flag_water:
		return
	if get_water() < 0.7:
		use_item(Items.Water)
		
def moveto(x, y):
	if get_pos_x() > x and get_pos_x() - x <= get_world_size() / 2:
		while get_pos_x() != x:
			move(West)
	else:
		while get_pos_x() != x:
			move(West)
	if get_pos_y() > y and get_pos_y() - y <= get_world_size() / 2:
		while get_pos_y() != y:
			move(South)
	else:
		while get_pos_y() != y:
			move(North)
			
# Idea is to spawn one drone per column
# Drone will manage column until everything is harvestable.
# Main drone waits for drone count to go to 0, then harvests and restarts

def do_mix(flag_init):
	types = [Entities.Tree, Entities.Carrot]
	type = types[(get_pos_x() + get_pos_y()) % 2]
	if flag_init:
		till()
		plant(type)
		do_water()
	if can_harvest():
		harvest()
		plant(type)
		do_water()
	move(North)

def do_init():
	global parts
	pumpkins, sunflowers, grass = parts
	def init_column():
		for i in range(pumpkins):
			till()
			do_water()
			move(North)
		for i in range(sunflowers):
			till()
			do_water()
			move(North)
		for i in range(mix):
			do_mix(True)
		for i in range(grass):
			harvest()
			move(North)
	
	for i in range(pumpkins - 1):
		if spawn_drone(init_column):
			move(East)
	init_column()
	moveto(0, 0)

def do_col():
	global parts
	pumpkins, sunflowers, grass = parts
	
	for i in range(pumpkins):
		plant(Entities.Pumpkin)
		do_water()
		move(North)
	for i in range(sunflowers):
		plant(Entities.Sunflower)
		do_water()
		move(North)
	for i in range(mix):
		do_mix(False)
	for i in range(grass):
		if can_harvest():
			harvest()
		move(North)
	
	while True:
		count = 0
		for i in range(pumpkins):
			if get_entity_type() == Entities.Dead_Pumpkin:
				harvest()
				plant(Entities.Pumpkin)
				do_water()
			else:
				if can_harvest():
					count = count + 1
			move(North)
		for i in range(sunflowers):
			if can_harvest():
				harvest()
				plant(Entities.Sunflower)
				do_water()
			move(North)
		for i in range(mix):
			do_mix(False)
		for i in range(grass):
			if can_harvest():
				harvest()
			move(North)
		if count == pumpkins:
			break
	
clear()
do_init()

while True:
	for i in range(pumpkins - 1):
		if spawn_drone(do_col):
			move(East)
	do_col()
	moveto(0, 0)
	while num_drones() > 1:
		do_a_flip() # wait until all drones are done
	harvest()
		
	