from __builtins__ import *

# One drone per column, grass, carrot, tree

clear()
change_hat(Hats.Brown_Hat)

grass = 10
sunflowers = 5
mix = get_world_size() - grass - sunflowers

def do_plant(entity):
	if get_ground_type() != Grounds.Soil:
		till()
	if can_harvest():
		harvest()
	if get_entity_type() != entity:
		plant(entity)
	if get_water() < 0.75:
		use_item(Items.Water)

def do_plot():
	x, y = get_pos_x(), get_pos_y()
	if y < grass:
		if can_harvest():
			harvest()
	elif y < grass + sunflowers:
		do_plant(Entities.Sunflower)
	else:
		if (x + y) % 4 == 0:
			do_plant(Entities.Tree)
		else:
			do_plant(Entities.Carrot)

def do_column():
	while True:
		for i in range(get_world_size()):
			do_plot()
			move(North)

usable_columns = min(get_world_size(), max_drones())
for i in range(usable_columns - 1):
	spawn_drone(do_column)
	move(East)
do_column()

