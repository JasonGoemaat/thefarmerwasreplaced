special_item = Items.Weird_Substance # None, Items.Fertilizer, Items.Weird_Substance
clear()
change_hat(Hats.Brown_Hat)
sunflower_columns = 10
preferences = []
for i in range(get_world_size()):
	for j in range(get_world_size()):
		preferences.append(Entities.Grass)

from __builtins__ import *

def do_plant(entity):
	if get_ground_type() != Grounds.Soil:
		till()
	if can_harvest():
		harvest()
	if get_entity_type() != entity:
		plant(entity)
		if (get_pos_x() % 3) == 1 and (get_pos_y() % 3) == 1:
			use_item(Items.Fertilizer)
			
	if get_water() < 0.75:
		use_item(Items.Water)

def get_entity():
	global preferences
	global sunflower_columns
	x, y = get_pos_x(), get_pos_y()
	if x < sunflower_columns:
		return Entities.Sunflower
	index = get_pos_x() * get_world_size() + get_pos_y()
	return preferences[index]

def do_plot():
	global special_item
	entity = get_entity()
	if get_water() < 0.5 and entity != Entities.Grass:
		use_item(Items.Water)
	if not can_harvest():
		return
	harvest()
	if entity == Entities.Grass:
		if get_ground_type() != Grounds.Grassland:
			till()
		return
	if entity == Entities.Bush:
		plant(Entities.Bush)
		return
	if get_ground_type() != Grounds.Soil:
		till()
	plant(entity)
	if special_item != None and (get_pos_x() % 3) == 1 and (get_pos_y() % 3) == 1:
		use_item(special_item)
		
def do_column():
	global preferences
	while True:
		for i in range(get_world_size()):
			do_plot()
			if get_pos_x() >= sunflower_columns:
				entity, (x, y) = get_companion()
				index = x * get_world_size() + y
				preferences[index] = entity
			move(North)

usable_columns = min(get_world_size(), max_drones())
for i in range(usable_columns - 1):
	spawn_drone(do_column)
	move(East)
do_column()

