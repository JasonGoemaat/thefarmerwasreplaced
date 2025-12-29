clear()
POWER_LIMIT = -1 # for simming

# Plant entire farm in Sunflowers

def init():
	def do_init():
		for i in range(get_world_size()):
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Sunflower)
			if get_water() < 0.75:
				use_item(Items.Water)
			move(North)
	for i in range(get_world_size() - 1):
		spawn_drone(do_init)
		move(East)
	do_init()
	move(East)
	
def perform_harvest(petals):
	def do_harvest():
		for i in range(get_world_size()):
			if can_harvest() and measure() >= petals:
				harvest()
			move(North)
	for i in range(get_world_size() - 1):
		spawn_drone(do_harvest)
		move(East)
	do_harvest()
	move(East)
		

while POWER_LIMIT < 0 or num_items(Items.Power) < POWER_LIMIT:
	init()
	for i in range(9):
		perform_harvest(15-i)
