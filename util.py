def move_to_origin():
	while get_pos_y() > get_world_size() / 2:
		move(North)
	while get_pos_y() > 0:
		move(South)
	while get_pos_x() > get_world_size() / 2:
		move(East)
	while get_pos_x() > 0:
		move(West)