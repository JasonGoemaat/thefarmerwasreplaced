map = []
map_dict = {}
visited = set()
DIRECTIONS = [North, East, South, West]

def get_index(x, y, direction):
	if direction == 0:
		y = y + 1
		if y >= get_world_size():
			return None
	if direction == 1:
		y = y - 1
		if y < 0:
			return None
	if direction == 2:
		x = x + 1
		if x >= get_world_size():
			return None
	if direction == 3:
		x = x - 1
		if x < 0:
			return None
	return x * get_world_size() + y
						
def update_map(map, map_dict, visited):
	index = get_index(get_pos_x(), get_pos_y(), None)
	if index == None:
		print('uh, oh!')
		return None, -1, False
	if index in visited:
		print('old')
		return map[index], index, False
#	moves = map[index]
#	if moves != None:
#		# other drone has handled this
#		return moves, index, False
	visited.add(index)
	moves = [can_move(North), can_move(East), can_move(South), can_move(West)]
	map[index] = moves
	map_dict[index] = moves
	return moves, index, True
		
def do_drone(direction, map, map_dict, visited):
	def handler():
		while True:
			# start with move, drone spawned on top of other drone and we know we can,
			# will keep moving in that direction while able
			if not move(DIRECTIONS[direction]):
				return # hit a wall
			moves, index, updated = update_map(map, map_dict, visited)
			if not updated:
				print('been there')
				return
			
			# spawn drones to the left and right
			left = (direction + 1) % 4
			if moves[left]:
				spawn_drone(do_drone(left, map, map_dict, visited))
			right = (direction + 3) % 4
			if moves[right]:
				spawn_drone(do_drone(right, map, map_dict, visited))
	return handler
						
def init_map(map, map_dict, visited):
	size = get_world_size()
	for i in range(size*size):
		map.append(None)
	moves, index, updated = update_map(map, map_dict, visited)
	for i in range(4):
		if moves[i]:
			spawn_drone(do_drone(i, map, map_dict, visited))
	while num_drones() > 1:
		do_a_flip()
	print("map", map)
	print("map_dict", map_dict)
	print("visited", visited)
	print("done initializing")
		
def run(map, map_dict, visited):
	clear()
	substance = get_world_size()
	# substance = 5 # smaller for testing
	substance = substance * 2**(num_unlocked(Unlocks.Mazes) - 1)
	print(substance)
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substance)
	init_map(map, map_dict, visited)
	print(map)
	
run(map, map_dict, visited)	
	