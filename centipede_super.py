# Idea: snake in columns, following a path that lets us guarantee
# a return, but zipping over when there is room to complete.

# Base would be starting at (0,0), moving up column 0 to (0,31),
# moving over to (1,31), down to (1,1) leaving the bottom row empty
# for return, over to (2,1), up to (2,31), over to (3,31), down to
# (3,1), etc.   At the end we will move over from (30,31) to (31,31),
# then ALL the way down to (31,0) and back over to (0,0), repeat...

# But especially early on that is very wasteful.  Say the apple is at
# (8,4) and our length is 1.  We analyze and see that (8,4) gives us
# columns 9-31 to play with.  That's 23 columns times 31 for fill, plus
# 31 for return to the start from the end.  So if we get to the apple,
# we have 23*31+31-1 or 744 length to play with and when we return to
# (0,0), the tail will be on the apple. Actually since 8 is an even
# column and we're going up, that would give us an extra 32-4 or 28,
# so if we can get to the apple and our length is 793 (23*31+31-1+28),
# we can follow secure path and return to the origin when the tail
# is over the old apple.

# So first step is to start at origin
# 1. Continue secure path UNTIL we can move over and be assured
# 	 that there is enough room to return to origin if we follow the
#	 safe path from the apple forward
# 2. If we can move directly horizontal taking #1 into consideration,
#	 we do it, otherwise follow the safe path
# 3. If apple is in the wrong vertical direction for our current column,
#	 we can move over a column if the safe distance is > 31 more than needed
# 4. If the apple is on the bottom row, return at the bottom of our
#	 safe path when we will get to the origin with no tail

# Possible idea:
# 1. Till the field and plant all sunflowers in all but the first 2 columns
# 2. At some THRESHOLD of empty space, harvest the next 2 columns at a time

change_hat(Hats.Top_Hat)
start_x = 30
length = 0
clear()

def prepare_field():
	global start_x
	drones = []
	def plant_sunflowers():
		for i in range(get_world_size()):
			if can_harvest():
				harvest()
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Sunflower)
			if i < get_world_size() - 1:
				move(North)
	for x in range(start_x):
		drones.append(spawn_drone(plant_sunflowers))
		move(East)
	for drone in drones:
		wait_for(drone)

ax, ay = 0, 0

def run():
	global length
	global start_x
	global ax
	global ay
	prepare_field()
	change_hat(Hats.Dinosaur_Hat)
	ax, ay = measure()
	
	def check_apple(direction):
		global ax
		global ay
		if ax == get_pos_x() and ay == get_pos_y():
			length = length + 1
			ax, ay = measure()
		move(direction)
	
	while start_x >= 0:
		while length + 1 < (32 - start_x) * 32:
			while get_pos_x() < get_world_size() - 1:
				check_apple(North)
			check_apple(East)
			while get_pos_x() > 1:
				check_apple(South)
			if get_pos_x() < get_world_size() - 1:
				check_apple(East)
			else:
				check_apple(South)
				while get_pos_x() > start_x:
					check_apple(West)
		start_x = start_x - 2
		move(West)
		move(West)
				
run()