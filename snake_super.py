# Complete redo: 
# https://github.com/chuyangliu/snake/blob/main/docs/algorithms.md#take-shortcust

# 1. Compute hamiltonian cycle that will vitit every plot.
# 2. Keep track of snake locations
# 3. Follow proscribed path
# 4. Allow 'shortcuts' to the apple only if it is not between the tail and head

# So what is a shortcut?   Anything that moves the furthest forward in the
#

change_hat(Hats.Top_Hat)
start_x = 30
length = 0
clear()

#hamiltonian = [] # list of dictionaries for nodes
#bylocation = {} # index into hamiltonian given (x,y) tuple
from hamiltonian_util import bylocation, hamiltonian

snake = [] # indexes into hamiltonian array of snake parts

def init_paths():
	pos = (0,0)
	index = 0
	plots = get_world_size() * get_world_size()
	# first create basic data with no shortcuts
	while index < plots:
		node = {
			"pos": pos,
			"index": index,
			"shortcuts": []
		}
		hamiltonian.append(node)
		bylocation[pos] = index
		x, y = pos
		if y == 0 and x != 0:
			# following bottom row west to origin
			node["direction"] = West
			pos = (x - 1, y)
		elif (x % 2) == 0:
			# even columns go north, east at top
			if y < get_world_size() - 1:
				node["direction"] = North
				pos = (x, y + 1)
			else:
				node["direction"] = East
				pos = (x + 1, y)
		else:
			# odd columns go south avoiding bottom row unless last column
			if y > 1 or x == get_world_size() - 1:
				node["direction"] = South
				pos = (x, y - 1)
			else:
				node["direction"] = East
				pos = (x + 1, y)
		index = index + 1
		
	# now we find shortcuts
	index = 0
	pos = (0, 0)
	def check_shortcut(pos, index, node, direction):
		def calc_next():
			if direction == North:
				return bylocation[(pos[0], pos[1]+1)]
			if direction == South:
				return bylocation[(pos[0], pos[1]-1)]
			if direction == East:
				return bylocation[(pos[0]+1, pos[1])]
			if direction == West:
				return bylocation[(pos[0]-1, pos[1])]

		# skip if we would move outside map
		if pos[0] == 0 and direction == West:
			return
		if pos[0] == get_world_size() - 1 and direction == East:
			return
		if pos[1] == 0 and direction == South:
			return
		if pos[1] == get_world_size() - 1 and direction == North:
			return

		next = calc_next()
		node["shortcuts"].append((direction, next))
		
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			pos = (x,y)
			index = bylocation[pos]
			node = hamiltonian[index]
			if node["direction"] in [North, South]:
				check_shortcut(pos, index, node, East)
				check_shortcut(pos, index, node, West)
			else:
				check_shortcut(pos, index, node, North)
				check_shortcut(pos, index, node, South)
	quick_print('hamiltonian =', hamiltonian)
	quick_print('bylocation =', bylocation)

ax, ay = 0, 0

def run():
	def better_shortcut(shortcut):
		# check if apple is between head and tail, and if
		# shortcut is between head and apple
		# case 0: head = 600, tail = 500, apple = 550
		#	apple inside the snake, no good
		# case 1: head = 600, tail = 500, apple = 700
		#	apple in front of head, shortcut between 601 and 700 good
		# case 2: head = 600, tail = 500, apple = 300
		#	shortcut leading to 601-1023 or 0-300 is good
		# case 3: head = 5, tail = 800, apple = 300
		#	I can take a shortcut if following the hamiltonian
		index = shortcut[1]
		head = snake[len(snake)-1]
		tail = snake[0] + len(hamiltonian)
		corrected_apple_index = apple_index
		if apple_index < head:
			corrected_apple_index = apple_index + len(hamiltonian)
	def shortcut_works(shortcut):
		# a shortcut is always faster than following hamiltonian
		# it works if we can take it and get to the apple without
		# hitting the snake, maybe add length in future
		index = shortcut[1]
		while index != apple_index:
			if index in snake:
				return False # would hit snake
			index = (index + 1) % len(hamiltonian)
		# made it to the apple!
		return True
		
	# init_paths() # not needed if importing from hamiltonian_util
	change_hat(Hats.Dinosaur_Hat)
	apple_pos = measure()
	apple_index = bylocation[apple_pos]
	while len(snake) < get_world_size() * get_world_size():
		index = bylocation[get_pos_x(), get_pos_y()]
		snake.append(index)
		node = hamiltonian[index]
		if index == apple_index:
			apple_pos = measure()
			apple_index = bylocation[apple_pos]
			move(node["direction"])
			continue
		direction = node["direction"]
		if direction in [North, South] and get_pos_y() == apple_pos[1]:
			for shortcut in node["shortcuts"]:
				if shortcut_works(shortcut):
					direction = shortcut[0] # is tuple (direction, index)
		elif direction == East and get_pos_y() == 1:
			for shortcut in node["shortcuts"]:
				if shortcut_works(shortcut):
					direction = shortcut[0] # is tuple (direction, index)
		elif direction in [East, West] and get_pos_x() == apple_pos[0]:
			for shortcut in node["shortcuts"]:
				if shortcut_works(shortcut):
					direction = shortcut[0] # is tuple (direction, index)
		move(direction)
		snake.pop(0)
	change_hat(Hats.Top_Hat)

run()