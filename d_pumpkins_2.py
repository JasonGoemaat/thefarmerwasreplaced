
# Idea is to spawn one drone per column
# Drone will manage column until everything is harvestable.
# Main drone waits for drone count to go to 0, then harvests and restarts

RUNS = 1000000000

from util import move_to_origin

def do_col():
	for i in range(get_world_size()):
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Pumpkin)
		move(North)
	
	# track lowest and highest unvarvestable
	low = 0
	high = get_world_size() - 1
	
	# loop until everything is harvestable, or there is one left
	while low <= high:
		# starting at low, move low up while we can harvest so we
		# don't check them anymore
		while low <= high and can_harvest():
			low = low + 1
			if get_pos_y() < high:
				move(North)
			
		# continue up to high and replant any dead pumpkins
		while get_pos_y() <= high:
			if get_entity_type() == Entities.Dead_Pumpkin:
				harvest()
				plant(Entities.Pumpkin)
				use_item(Items.Water)
			if get_pos_y() == high:
				break
			move(North)
				
		# now move high down as long as we can harvest		
		while low <= high and can_harvest():
			high = high - 1
			move(South)
		
		# continue down to low and replant any dead pumpkins
		while get_pos_y() >= low:
			if get_entity_type() == Entities.Dead_Pumpkin:
				harvest()
				plant(Entities.Pumpkin)
				use_item(Items.Water)
			if get_pos_y() <= low:
				break
			move(South)
			
		# last one in the column, try using fertilizer until it's good
		while low == high and (num_drones() < 8 or num_items(Items.Fertilizer) > 10):
			if can_harvest():
				return
			if get_entity_type() == Entities.Pumpkin and num_items(Items.Fertilizer) > 0:
				use_item(Items.Fertilizer)
				continue
			if get_entity_type() == Entities.Dead_Pumpkin:
				harvest()
				plant(Entities.Pumpkin)
				if num_items(Items.Fertilizer) > 0:
					use_item(Items.Fertilizer)
				else:
					use_item(Items.Water)
				
clear()

runs = 0
while RUNS < 0 or runs < RUNS:
	drones = []
	for i in range(get_world_size() - 1):
		drones.append(spawn_drone(do_col))
		move(East)
	do_col()
	move_to_origin()
	for d in drones:
		wait_for(d)
	harvest()
	# for leaderboard:
	#if num_items(Items.Pumpkin) >= 200000000:
	#	break
	runs = runs + 1
		
	