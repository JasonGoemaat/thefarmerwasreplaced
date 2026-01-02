# Modification of snake_super3
# New hybrid method - only check hamiltonian shortcut if heading east on bottom

change_hat(Hats.Top_Hat)
start_x = 30
length = 0
INPUT = 300 # sweet spot
clear()

#hamiltonian = [] # list of dictionaries for nodes
#bylocation = {} # index into hamiltonian given (x,y) tuple
from hamiltonian_util import bylocation, hamiltonian


ax, ay = 0, 0

def index_from_location(x, y):
	if x == 0:
		return y
	if y == 0:
		return 1024-x
	if x % 2 == 0:
		return 32 + (x-1)*31 + y-1
	return 32 + x*31 - y
	# column 0: 0-31
	# column 1: 32-62
	# column 2: 63-93
	# column 3: 94-124
	# column 4: 125-155
	
#good = True
#for x in range(get_world_size()):
#	for y in range(get_world_size()):
#		index = index_from_location(x, y)
#		index2 = bylocation[x,y]
#		if index != index2:
#			good = False
#if not good:
#	print('bad!')
	
east_of = {}
south_of = {}

if 1 in east_of:
	quick_print(east_of[1])

#for i in range(get_world_size() * get_world_size()):
#	# initialize to big numbers
#	east_of.append(9999)
#	south_of.append(9999)
	
for x in range(get_world_size() - 1):
	# for y values 1 to 31 we can move east except last column
	for y in range(get_world_size() - 1):
		a = index_from_location(x, y + 1)
		b = index_from_location(x + 1, y + 1)
		east_of[a] = b

for x in range(get_world_size() - 2):
	# for y value 1 we can move south to go back to origin
	a = index_from_location(x + 1, 1)
	b = index_from_location(x + 1, 0)
	south_of[a] = b

def run():
	snake = []
	# init_paths() # not needed if importing from hamiltonian_util
	change_hat(Hats.Dinosaur_Hat)
	apple_pos = measure()
	apple = bylocation[apple_pos]
	# special algorithm if snake is under 100 segments, speed up the start
	head = 0
	snake_start = 0
	while True:
		x, y = get_pos_x(), get_pos_y()
		head = bylocation[(x, y)]
		snake.append(head)
		node = hamiltonian[head]
		direction = node["direction"]
		
		# find the apple?  get new loc and move on hamiltonian path, no snake pop
		if head == apple:
			apple_pos = measure()
			apple = bylocation[apple_pos]
			if len(snake) - snake_start >= INPUT: # about when it starts to slow
				for h in hamiltonian[head:get_world_size() * get_world_size()]:
					move(h["direction"])
				break
			move(direction)
			if len(snake) > 100000:
				snake = snake[snake_start:]
				snake_start = 0
			continue
		
		tail = snake[snake_start]

		# on bottom return always go to origin		
		if y == 0:
			move(direction)
			snake_start = snake_start + 1
			continue

		if head in east_of:
			east = east_of[head]
			# if apple earlier than head, try to catch tail and return to origin
			if apple < head:
				if direction == North:
					# move east if won't overrun tail
					if tail <= head or east < tail:
						if not move(East):
							print('UH OH! snake_super4')
							move(direction)
						snake_start = snake_start + 1
						continue
				if y == 1 and direction == East and (tail < head or tail > south_of[head]):
					if not move(South):
						print('TOO BAD!')
						move(direction)
					snake_start = snake_start + 1
					continue
				move(direction)
				snake_start = snake_start + 1
				continue
			
			# apple is AFTER head for sure, see if East is shortcut
			if tail <= head:
				# tail past start, can move forward
				if direction != South and east_of[head] <= apple:
					if not move(East):
						print('OOPSIE!')
						move(direction)
					snake_start = snake_start + 1
					continue
			else:
				# tail is later on map, check it and apple
				if direction != South and east_of[head] < apple and east_of[head] < tail:
					if not move(East):
						print('DOH!')
						move(direction)
					snake_start = snake_start + 1
					continue

		move(direction)
		snake_start = snake_start + 1

	# ok, snake is at least 100 segments and we're at index 0
	# follow hamiltonian path until we cannot move
	directions = []
	for h in hamiltonian:
		directions.append(h["direction"])
	done = False
	while not done:
		for d in directions:
			# print("(", get_pos_x(), ",", get_pos_y(), "): ", d)
			if not move(d):
				done = True
				break

	# we're full!  change hats and collect bones		
	change_hat(Hats.Top_Hat)

run()