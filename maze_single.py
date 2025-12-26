directions = [North, East, South, West]
index_deltas = [1, get_world_size(), -1, -get_world_size()]

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

clear()
substance = get_world_size()
substance = substance * 2**(num_unlocked(Unlocks.Mazes) - 1)
print(substance, 'Weird_Substance per treasure')
if num_items(Items.Weird_Substance) < substance:
	print("NOT ENOUGH SUBSTANCE")
	return
plant(Entities.Bush)
use_item(Items.Weird_Substance, substance)
initial_index = get_index()
initial_facing = -1
counter = 0
map = []
for i in range(get_world_size() * get_world_size()):
	map.append(None)

facing = 0

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
	
print("Explored map in ", counter, "moves")

# 9380.1 seconds for 295 - FULL search
def find_path(target_x, target_y):
	global index_deltas
	
	# first we do a complete search of the maze, finding the shortest
	# path to any grid square from our current position
	
	updated = [] # queue of indexes to re-check as costs were lowered
	nodes = {} # tuples with source_index, direction index used to get here, cost to get here
	index = get_index()
	nodes[index] = (-1, -1, 0)
	updated.append(index)
	while len(updated) > 0:
		current_index = updated.pop(0)
		current_node = nodes[current_index]
		moves = map[current_index]
		for i in range(4):
			if moves[i]:
				target_index = current_index + index_deltas[i]
				if target_index not in nodes or current_node[2] + 1 < nodes[target_index][2]:
					nodes[target_index] = (current_index, i, current_node[2] + 1)
					updated.append(target_index)
	
	# now we start at treasure and form a list of directions to use to get there
	path = []
	tindex = get_index(target_x, target_y)
	node = nodes[tindex]
	while node[0] >= 0:
		path.insert(0, node[1])
		node = nodes[node[0]]
	return path
	
# 4832.73 seconds for 295 - stop on treasure, 1/2 the time of full search
# 3823.04 seconds for 295 with not running update_map
# 2764.73 seconds for 295 running update_map every 20th run, but not restarting path
# 2652.23 seconds for 295, update every 10th run and now bi-directional link update
# 2740.35 seconds for 295, ditto but every 30th run
def find_path_b(target_x, target_y):
	global index_deltas
	
	treasure_index = get_index(target_x, target_y)
	updated = [] # queue of indexes to re-check as costs were lowered
	nodes = {} # tuples with source_index, direction index used to get here, cost to get here
	index = get_index()
	nodes[index] = (-1, -1, 0)
	updated.append(index)
	while len(updated) > 0:
		current_index = updated.pop(0)
		current_node = nodes[current_index]
		moves = map[current_index]
		for i in range(4):
			if moves[i]:
				next_index = current_index + index_deltas[i]
				if next_index not in nodes or current_node[2] + 1 < nodes[next_index][2]:
					nodes[next_index] = (current_index, i, current_node[2] + 1)
					
					# did we find it?
					if next_index == treasure_index:
						updated = []
						break
					if next_index in updated:
						updated.remove(next_index) # only once in list
					updated.append(next_index)
	
	# now we start at treasure and form a list of directions to use to get there
	path = []
	node = nodes[treasure_index]
	while node[0] >= 0:
		path.insert(0, node[1])
		node = nodes[node[0]]
	return path
	
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
	
treasure_count = 0
while True:
	tx, ty = measure()
	path = find_path_b(tx, ty)
	for direction in path:
		if (treasure_count % 15) < 29:
			update_map()
		move(directions[direction])
	if get_pos_x() == tx and get_pos_y() == ty:
		treasure_count = treasure_count + 1
		if treasure_count < 295:
			use_item(Items.Weird_Substance, substance)
			continue
		else:
			harvest()
			break
