# set_world_size(16)
clear()
change_hat(Hats.Dinosaur_Hat)
next_x, next_y = measure()

# My theory is to get to a point where I can always move to the apple.
# I fill the left side of the map with myself (i.e. 32x32 farm I am 100 units,
# I fill the first 3 columns for 96 and 4 more), then I go to the apple, then to
# bottom and back to re-fill the first 3 columns

# do_fill, must be at position 0, 0, continue until filled >= length
def do_fill():
	global next_x
	global next_y
	global length
	filled = 0
	while filled < length - get_pos_x():
		x, y = get_pos_x(), get_pos_y()
		# pick up apples in the way
		if get_entity_type() == Entities.Apple:
			next_x, next_y = measure()
			length = length + 1
		filled = filled + 1
		if (x % 2) == 0:
			# even column, head north, if at end head east
			if y >= get_world_size() - 1:
				move(East)
				if filled >= length:
					break # ready to go right, then down for apple
				continue
			move(North)
		else:
			# odd column, head south leaving 1 gap, if at end head east
			if y < 2:
				move(East)
				continue
			move(South)

def do_find():
	# SIMPLE - at top of new column, head right to apple column
	global next_x
	global next_y
	global length
	while get_pos_x() < next_x:
		move(East)
	while get_pos_y() > 0:
		# pick up apple along the way
		if get_entity_type() == Entities.Apple:
			next_x, next_y = measure()
			length = length + 1
		move(South)
	while get_pos_x() > 0:
		# pick up apple along the way
		if get_entity_type() == Entities.Apple:
			next_x, next_y = measure()
			length = length + 1
		move(West)
		
def get_column_direction(x):
	if x % 2 == 0:
		return North
	return South
	
def get_apple_directions(x, y):
	horizontal = None
	if next_x > x:
		horizontal = East
	elif next_x < x:
		horizontal = West
	vertical = None
	if next_y > y:
		vertical = North
	elif next_y < y:
		vertical = South
	return horizontal, vertical
		
def do_advanced():
	global next_x
	global next_y
	col_v = get_column_direction(get_pos_x())
	apple_h, apple_v = get_apple_directions(get_pos_x(), get_pos_y())
	
	if apple_h == West:
		# apple is to the left, restart
		return False
	if next_y == 0:
		# apple is on bottom (path back to start), move right if needed
		# then return
		pass
	if apple_h == None: # TODO: FIX
		# apple on return path, move right to x position, then down and out
		while next_x > get_pos_x():
			move(East)
		while get_pos_y() > 0:
			move(South)
		return False # restart
	if next_x == get_pos_x():
		# is in same column
		if (get_pos_x() % 2) == 0 and get_pos_y() >= next_y:
			# same column, heading north, but apple is south, restart
			return False
		if (get_pos_x() % 2) == 0 and get_pos_y() >= next_y:
			# same column, heading south, but apple is north, restart
			return False
		while get_pos_y() != next_y:
			if (x % 2) == 0:
				move(North)
			else:
				move(South)
		return True # found apple

	# if apple is in the right North/South direction for this column,
	# move to the proper y value
	while get_pos_y() != next_y:
		if (x % 2) == 0:
			move(North)
		else:
			move(South)

	# head East if necessary to get to apple
	while get_pos_x() < next_x:
		move(East)

	# found the apple
	next_x, next_y = measure()
	length = length + 1
	return true



length = 1
while length < 30:
	if get_entity_type() == Entities.Apple:
		next_x, next_y = measure()
		length = length + 1
	do_fill()
	do_find()
		
change_hat(Hats.Carrot_Hat)
