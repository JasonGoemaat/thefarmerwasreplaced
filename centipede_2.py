# set_world_size(16)
clear()
change_hat(Hats.Dinosaur_Hat)
next_x, next_y = measure()

# My theory is to get to a point where I can always move to the apple.
# I fill the left side of the map with myself (i.e. 32x32 farm I am 100 units,
# I fill the first 3 columns for 96 and 4 more), then I go to the apple, then to
# bottom and back to re-fill the first 3 columns

filled = 0
length = 1

# do_fill, follow fill pattern, filling columns from left, until we can get
# to the apple and wind up home without eating our tail.
def do_fill():
	global next_x
	global next_y
	global length
	global filled
	while True:
		# pick up apples in the way
		if get_pos_x() == next_x and get_pos_y() == next_y:
			next_x, next_y = measure()
			length = length + 1
		filled = filled + 1
		if (get_pos_x() % 2) == 0:
			# even column, head north, if at end head east
			if get_pos_y() >= get_world_size() - 1:
				move(East)
				if filled >= length:
					break # ready to go right, then down for apple
				continue
			move(North)
		else:
			# odd column, head south leaving 1 gap, if at end head east
			if get_pos_y() < 2:
				move(East)
				continue
			move(South)
			
		# see if we can shortcut to it, if at least 1 to the right and
		# enough left to get there and return to the start with an empty filled
		def home_in():
			global next_x
			global next_y
			global filled
			global length
			moves_to_apple = abs(next_x - get_pos_x()) + abs(next_y - get_pos_y())
			moves_to_home = next_x + next_y
			if next_x > get_pos_x() + 1 and (moves_to_apple + moves_to_home + length) > filled + 5:
				move(East)
				filled = filled - 1
				while get_pos_y() != next_y:
					if get_pos_y() > next_y:
						move(South)
					else:
						move(North)
					if filled > 0:
						filled = filled - 1
				while get_pos_x() < next_x:
					move(East)
					if filled > 0:
						filled = filled - 1
				next_x, next_y = measure()
				length = length + 1
				return True
			return False
		if home_in():
			while home_in():
				pass
			while get_pos_y() > 0:
				move(South)
				if get_pos_x() == next_x and get_pos_y() == next_y:
					next_x, next_y = measure()
					length = length + 1
			while get_pos_x() > 0:
				move(West)
				if get_pos_x() == next_x and get_pos_y() == next_y:
					next_x, next_y = measure()
					length = length + 1
		break
		
length = 1
while length < 300:
	if get_entity_type() == Entities.Apple:
		next_x, next_y = measure()
		length = length + 1
	do_fill()
		
change_hat(Hats.Carrot_Hat)
