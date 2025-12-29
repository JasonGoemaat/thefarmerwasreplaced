clear()
POWER_LIMIT = -1

# Plant entire farm in Sunflowers

def run():
	def do_sunflowers():
		for i in range(get_world_size()):
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Sunflower)
			use_item(Items.Water)
			move(North)
		while POWER_LIMIT < 0 or num_items(Items.Power) < POWER_LIMIT:
			if can_harvest():
				harvest()
				plant(Entities.Sunflower)
				if get_water() < 0.75:
					use_item(Items.Water)
			move(North)
								
	for i in range(get_world_size() - 1):
		spawn_drone(do_sunflowers)
		move(East)
	do_sunflowers()

run()