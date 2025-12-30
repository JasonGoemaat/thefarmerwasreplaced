# Modification of snake_super4
# New hybrid method - only check hamiltonian shortcut if heading east on bottom

INPUT = 350 # sweet spot, somment for snake_sim

#hamiltonian = [] # list of dictionaries for nodes
#bylocation = {} # index into hamiltonian given (x,y) tuple
# from hamiltonian_util import bylocation, hamiltonian

# bylocation = {} # key is tuple (x,y)
byloc = []  # key is x*get_world_size() + y
directions = []
shortcut = {}
shortcut_direction = {}

def index_from_location(x, y):
	if x == 0:
		return y
	if y == 0:
		return 1024-x
	if x % 2 == 0:
		return 32 + (x-1)*31 + y-1
	return 32 + x*31 - y

def calculate_hamiltonian_directions():
	directions = []
	for i in range(31):
		directions.append(North)
	directions.append(East)
	for i in range(15):
		for j in range(30):
			directions.append(South)
		directions.append(East)
		for j in range(30):
			directions.append(North)
		directions.append(East)
	for i in range(31):
		directions.append(South)
	for i in range(31):
		directions.append(West)
	return directions
	
def calculate_shortcuts():
	global shortcut
	global shortcut_direction
	global byloc
	WORLD_SIZE = get_world_size()
	for x in range(get_world_size() - 1):
		# for y values 1 to 31 we can move east except last column
		loc = x * WORLD_SIZE
		for y in range(get_world_size() - 1):
			a = byloc[loc + y + 1]
			b = byloc[loc + WORLD_SIZE + y + 1]
			shortcut[a] = b
			shortcut_direction[a] = East
		
	for x in range(get_world_size() - 2):
		# for y value 1 we can move south to go back to origin
		loc = (x + 1) * WORLD_SIZE
		#a = index_from_location(x + 1, 1)
		#b = index_from_location(x + 1, 0)
		a = byloc[loc + 1]
		b = byloc[loc]
		shortcut[a] = b
		shortcut_direction[a] = South

def init():
	ts = get_time()
	global bylocation
	global directions
	global byloc
	WORLD_SIZE = get_world_size()
	# s = get_tick_count()
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			index = index_from_location(x, y)
			# bylocation[(x,y)] = index
			# byloc[x * WORLD_SIZE + y] = index
			byloc.append(index)
	# e = get_tick_count()
	#quick_print("bylocation:", e-s, "ticks") # ~14000 ticks

	# s = get_tick_count()
	directions = calculate_hamiltonian_directions()
	# e = get_tick_count()
	#quick_print("directions:", e-s, "ticks") # ~1100 ticks

	# s = get_tick_count()
	calculate_shortcuts()
	# e = get_tick_count()
	# quick_print("shortcuts:", e-s, "ticks") # 26369 ticks, 9023 using byloc instead
	
	#s = get_tick_count()
	#for x in range(32):
	#	for y in range(32):
	#		loc = index_from_location(x, y)
	#e = get_tick_count()
	#quick_print("non-dict location find:", e-s, "ticks") # 10825 ticks

	te = get_time()
	quick_print("init() took", te - ts, "seconds") # 3.62 seconds
	# was 8.6 seconds without byloc upgrade using x*size+y instead of tuple
	
init()

def run():
	global shortcut
	global shortcut_direction
	global directions
	global byloc
	WORLD_SIZE = get_world_size()
	change_hat(Hats.Top_Hat)
	clear()
	change_hat(Hats.Dinosaur_Hat)
	snake = []
	snake_start = 0
	ax, ay = measure()
	apple = byloc[ax * WORLD_SIZE + ay]
	head = 0
	size = len(directions)
	while True:
		snake.append(head)
		direction = directions[head]
		
		# find the apple?  get new loc and move on hamiltonian path, no snake pop
		if head == apple:
			ax, ay = measure()
			apple = byloc[ax * WORLD_SIZE + ay]
			if len(snake) - snake_start >= INPUT: # about when it starts to slow
				for dir in directions[head:get_world_size() * get_world_size()]:
					move(dir)
				break
			move(direction)
			head = (head + 1) % size
			if len(snake) > 100000:
				snake = snake[snake_start:]
				snake_start = 0
			continue
		
		if head in shortcut:
			tail = snake[snake_start]
			sh_index = shortcut[head]
			sh_dir = shortcut_direction[head]
			
			# if apple earlier than head, try to catch tail and return to origin
			if apple < head:
				# todo: keep taking shortcuts until I can't, then follow
				# hamiltonian?  some way to not have to do the previous checks
				# including check for apple since it's past the end...
				# also don't have to recalculate head every time, it moves
				# to where the shortcut is
				if tail <= head or sh_index < tail:
					move(sh_dir)
					head = sh_index
					snake_start = snake_start + 1
					continue
			elif tail <= head:
				# apple is AFTER head for sure, and tail is before,
				# so just worry about over-running apple
				if sh_index <= apple:
					move(sh_dir)
					head = sh_index
					snake_start = snake_start + 1
					continue
			else:
				# tail is later on map than head, as is apple, check both
				if sh_index <= apple and sh_index < tail:
					move(sh_dir)
					head = sh_index
					snake_start = snake_start + 1
					continue

		# following path
		move(direction)
		head = (head + 1) % size
		snake_start = snake_start + 1

	# ok, snake is at least 100 segments and we're at index 0
	# follow hamiltonian path until we cannot move
	done = False
	while not done:
		for d in directions:
			# print("(", get_pos_x(), ",", get_pos_y(), "): ", d)
			if not move(d):
				done = True
				break

	# we're full!  change hats and collect bones		
	change_hat(Hats.Top_Hat)

while True:
	run()