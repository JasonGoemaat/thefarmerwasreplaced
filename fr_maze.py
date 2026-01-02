SIMMING = False
if SIMMING:
	unlock(Unlocks.Speed)
	unlock(Unlocks.Expand)
	unlock(Unlocks.Plant)
	unlock(Unlocks.Expand)
	unlock(Unlocks.Speed)
	unlock(Unlocks.Carrots)
	unlock(Unlocks.Expand)
	unlock(Unlocks.Grass) # double grass production
	unlock(Unlocks.Expand)
	unlock(Unlocks.Speed)
	unlock(Unlocks.Watering)
	unlock(Unlocks.Expand)
	unlock(Unlocks.Trees)
	unlock(Unlocks.Carrots)
	unlock(Unlocks.Trees) # better wood production
	unlock(Unlocks.Grass) # running low on grass
	unlock(Unlocks.Watering)
	unlock(Unlocks.Carrots)
	unlock(Unlocks.Speed)
	unlock(Unlocks.Grass)
	unlock(Unlocks.Speed)
	unlock(Unlocks.Trees)
	unlock(Unlocks.Watering) # let it build
	unlock(Unlocks.Pumpkins)
	unlock(Unlocks.Expand)
	unlock(Unlocks.Grass)
	unlock(Unlocks.Fertilizer)
	unlock(Unlocks.Trees)
	unlock(Unlocks.Carrots)
	unlock(Unlocks.Grass)
	unlock(Unlocks.Fertilizer)
	unlock(Unlocks.Sunflowers)
	unlock(Unlocks.Pumpkins)
	unlock(Unlocks.Mazes) # need 8 per maze, 2000 treasure for drones
	

# init: plant bush and use substance
# cycle: use on treasure
# 300th but not done:harvest, replant and use

# run mazes starting with a new one:
#	GOAL: If set, stop when gold gets this high
#	LOOPS: How many oops of TREASURES to repeat, restarting maze each time
#	TREASURES: repeat same maze until this many treasures have been found
def mazes(GOAL = 0, LOOPS = 1, TREASURES = 300):
	directions = [North, East, South, West]
	index_deltas = [1, get_world_size(), -1, -get_world_size()]
	substance = get_world_size()
	substance = substance * 2**(num_unlocked(Unlocks.Mazes) - 1)
	TREASURE_VALUE = substance * get_world_size()
	if num_items(Items.Weird_Substance) < substance or (GOAL > 0 and num_items(Items.Gold) > GOAL):
		return False

	# start off with new maze, repeat until 300 treasures, or GOAL hit
	def maze_to_treasures():
		treasures = 0
		map = []
		for i in range(get_world_size() * get_world_size()):
			map.append(None)
		clear()
		plant(Entities.Bush)
		use_item(Items.Weird_Substance, substance)

		def create_map():
			facing = 0
			initial_index = get_index()
			initial_facing = -1
		
			counter = 0
			while True:
				index = get_index()
				moves = [can_move(North), can_move(East), can_move(South), can_move(West)]
				map[index] = moves
				if counter > 0 and index == initial_index and facing == initial_facing:
					break # explored entire maze
				counter = counter + 1
				left = (facing + 3) % 4
				if can_move(directions[left]):
					# turn left if we can
					facing = left
				while not can_move(directions[facing]):
					# turn right until we can move 
					facing = (facing + 1) % 4
				if initial_index == index:
					if initial_facing == -1:
						initial_facing = facing # first path we followed
					elif initial_facing == facing:
						break # would repeat first ever move
				move(directions[facing])

		# look at current position and find places we can move, if
		# different than stored in map, update map and return true
		def update_map():
			index = get_index()
			moves = [can_move(North), can_move(East), can_move(South), can_move(West)]
			m = map[index]
			updated = False
			for i in range(4):
				if m[i] != moves[i]:
					map[index] = moves
					other_index = index + index_deltas[i]
					map[other_index][(i + 2) % 4] = True
					updated = True
			return updated

	# 2074.61 updating every time - BEST
		# 2101.8 updating every 5th time
		# 2379.96 updating every 10th time I think
		# 3053.2 updating AND restarting if updated every time
		def find_path_astar(map, target_x, target_y):
			global index_deltas
			
			treasure_index = get_index(target_x, target_y)
			open = [] # queue of indexes to re-check as costs were lowered
			closed = set() # set of nodes we've visited
			nodes = {} # tuples with source_index, direction index used to get here, cost to get here
			index = get_index()
			h = calculate_h(index, target_x, target_y)
		
			# f is estimated total cost for sorting, f = g + h
			# g is actual cost to get here when we visit
			# h is estimated cost from here to target
			nodes[index] = [-1, -1, h, 0, h] # source, direction, f, g, h
			open.append(index)
			open_index = 0
			
			def enqueue_node(index, cost):
				for i in range(len(open) - open_index):
					if nodes[open[i + open_index]][2] >= cost:
						open.insert(i + open_index, index)
						return
				open.append(index)
				
			while open_index < len(open):
				# current_index = open.pop(0) # smallest estimated distance
				current_index = open[open_index]
				open_index = open_index + 1
				closed.add(current_index)
				current_node = nodes[current_index]
				moves = map[current_index]
				next_cost = current_node[3] + 1
				x, y = index_to_xy(current_index)
				# quick_print("Handling index", current_index, "at", x, ",", y)
				for i in range(4):
					if moves[i]:
						next_index = current_index + index_deltas[i]
						nx, ny = index_to_xy(next_index)
						if next_index in closed:
							# quick_print("  ", directions[i], "(", next_index, ") at", nx, ",", ny, "is CLOSED")
							continue
						if next_index not in nodes:
							# quick_print("  ", directions[i], "(", next_index, ") at", nx, ",", ny, "- adding to nodes")
							h = calculate_h(current_index, target_x, target_y)
							nodes[next_index] = [current_index, i, h + next_cost, next_cost, h] # source, direction, f, g, h
							if next_index == treasure_index:
								open = []
								break
							enqueue_node(next_index, h + next_cost)
							continue
						if next_cost < nodes[next_index][3]:
							# quick_print("  ", directions[i], "(", next_index, ") at", nx, ",", ny, "- updating cost")
							nodes[next_index][3] = next_cost
							nodes[next_index][2] = next_cost + nodes[next_index][4]
						# else:
							# quick_print("  ", directions[i], "(", next_index, ") at", nx, ",", ny, "- not cheaper")
					# else:
						# quick_print("  ", directions[i], "- CANNOT MOVE")

			
			# now we start at treasure and form a list of directions to use to get there
			path = []
			node = nodes[treasure_index]
			while node[0] >= 0:
				# path.insert(0, node[1]) # TOO EXPENSIVE?
				path.append(node[1])
				node = nodes[node[0]]
			return path

		def find_treasure():
			tx, ty = measure()
			path = find_path_astar(map, tx, ty)
			path_length = len(path)
			for i in range(path_length - 1, -1, -1):
				update_map()
				move(directions[path[i]])
		#	for direction in path:
		#		update_map()
		#		move(directions[direction])

		create_map()
		treasures = 0
		while True:
			find_treasure()
			if GOAL > 0 and num_items(Items.Gold) + TREASURE_VALUE >= GOAL:
				break
			use_item(Items.Weird_Substance, substance)
			treasures = treasures + 1
			if treasures >= TREASURES:
				break
		harvest() # final harvest will clear area/reset maze

	for i in range(LOOPS):
		maze_to_treasures()
		
def reverse(l):
	n = []
	for i in l:
		n.insert(0, i)
	return n

def get_index(x = None, y = None):
	if x == None:
		x = get_pos_x()
	if y == None:
		y = get_pos_y()
	return x * get_world_size() + y

def index_to_xy(index):
	return index // get_world_size(), index % get_world_size()

# for A* algorithm, taxi distance to treasure
def calculate_h(index, target_x, target_y):
	x = index / get_world_size()
	y = index % get_world_size()
	dx = abs(target_x - x)
	dy = abs(target_y - y)
	return dx + dy

	
			