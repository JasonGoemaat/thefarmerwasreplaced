# set_world_size(16)
clear()
change_hat(Hats.Dinosaur_Hat)
next_x, next_y = measure()

# My theory is to get to a point where I can always move to the apple.
# I fill the left side of the map with myself (i.e. 32x32 farm I am 100 units,
# I fill the first 3 columns for 96 and 4 more), then I go to the apple, then to
# bottom and back to re-fill the first 3 columns

# do_fill, must be at position 0, 0, will end up on top of a column
def do_fill():
	global next_x
	global next_y
	global length
	filled = 0
	while True:
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

length = 1
while length < 30:
	if get_entity_type() == Entities.Apple:
		next_x, next_y = measure()
		length = length + 1
	do_fill()
	do_find()
		
change_hat(Hats.Carrot_Hat)
