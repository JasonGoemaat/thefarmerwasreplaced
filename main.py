
clear()

for i in range(get_world_size()):
	for j in range(get_world_size()):
		move(East)
		x = get_pos_x()
		y = get_pos_y()
		index = (x + y) % get_world_size()
		if index == 0 or index == 2:
			till()
			plant(Entities.Carrot)
		elif index == 1 or index == 3:
			plant(Entities.Tree)
			use_item(Items.Water)
#		elif index == 4:
#			plant(Entities.Pumpkin)
	move(North)
while True:
	x = get_pos_x()
	y = get_pos_y()
	index = (x + y) % get_world_size()
	if can_harvest():
		harvest()
		if index == 0 or index == 2:
			plant(Entities.Carrot)
		elif index == 1 or index == 3:
			plant(Entities.Tree)
			if get_water() < 0.3:
				use_item(Items.Water)
	move(East)
	if get_pos_x() == 0:
		move(North)
