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
	
good = True
for x in range(get_world_size()):
	for y in range(get_world_size()):
		index = index_from_location(x, y)
		index2 = bylocation[x,y]
		if index != index2:
			good = False
if not good:
	print('bad!')

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
		tail = snake[0]
		apple = apple_index
		if apple < head:
			apple = apple + len(hamiltonian)
		if tail > head:
			# tail is after head, wrapping around
			# head < shortcut < apple < tail
			if shortcut[1] <= head or shortcut[1] >= apple or apple > tail:
				return False
			return True
		# head is after tail, so no wrapping...
		# if apple after head, shortcut after head and before apple
		if apple > head:
			if shortcut[1] > head and shortcut[1] <= apple:
				return True
			return False
		# apple is before head, must be before tail
		if apple > tail:
			return False
		# shortcut must be after head or before apple
		if shortcut[1] > head or shortcut[1] <= apple:
			return True
		return False
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
			if apple_pos == None:
				break
			apple_index = bylocation[apple_pos]
			move(node["direction"])
			continue
		direction = node["direction"]
		if direction in [North, South]:
			for shortcut in node["shortcuts"]:
				if better_shortcut(shortcut):
					direction = shortcut[0] # is tuple (direction, index)
		elif direction == East and get_pos_y() == 1:
			for shortcut in node["shortcuts"]:
				if better_shortcut(shortcut):
					direction = shortcut[0] # is tuple (direction, index)
		elif direction in [East, West] and get_pos_x() == apple_pos[0]:
			for shortcut in node["shortcuts"]:
				if better_shortcut(shortcut):
					direction = shortcut[0] # is tuple (direction, index)
		move(direction)
		snake.pop(0)
	change_hat(Hats.Top_Hat)

run()