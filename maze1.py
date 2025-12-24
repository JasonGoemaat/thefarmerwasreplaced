clear()
substance = get_world_size()
# substance = 5 # smaller for testing
substance = substance * 2**(num_unlocked(Unlocks.Mazes) - 1)
print(substance)

while True:
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substance)
	tx, ty = measure()
	x, y = get_pos_x(), get_pos_y()
	
	directions = [North, East, South, West]
	facing = 0
	
	while x != tx or y != ty:
		left = (facing + 3) % 4
		if can_move(directions[left]):
			# turn left if we can
			facing = left
		while move(directions[facing]) != True:
			# turn right until we can move
			facing = (facing + 1) % 4
		x, y = get_pos_x(), get_pos_y()
		
	harvest()