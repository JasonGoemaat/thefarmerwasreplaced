# Plant entire farm in cacti

def moveNext():
	i = get_pos_y() * get_world_size() + get_pos_x()
	m = i % (get_world_size() * 2)
	if m == get_world_size() - 1 or m == get_world_size():
		move(North)
	elif m < get_world_size():
		move(East)
	else:
		move(West)

def plantCacti():
	global first
	for y in range(get_world_size()):
		for x in range(get_world_size()):
			if first:
				till()
			plant(Entities.Cactus)
			moveNext()
			
def sortCacti():
	swapCount = 0
	for y in range(get_world_size()):
		for x in range(get_world_size()):
			realX = x
			if (y % 2) == 1:
				realX = get_world_size() - x - 1
			if y < get_world_size() - 1:
				if measure() > measure(North):
					swap(North)
					swapCount = swapCount + 1
			if realX < get_world_size() - 1:
				if measure() > measure(East):
					swap(East) 
					swapCount = swapCount + 1
			if y > 0:
				if measure() < measure(South):
					swap(South)
					swapCount = swapCount + 1
			if realX > 0:
				if measure() < measure(West):
					swap(West)
					swapCount = swapCount + 1
			moveNext()
	return swapCount

def initSoil():
	clear()
	for y in range(get_world_size()):
		for x in range(get_world_size()):
			till()
			moveNext()

first = True

def do_loop():
	global first
	while True:
		plantCacti()
		first = False
		pass_count = 0
		while True:
			swapCount = sortCacti()
			pass_count = pass_count + 1
			quick_print("Swaps:", swapCount)
			if swapCount == 0 and can_harvest():
				break
		print('Passes:', pass_count)
		harvest()
		
clear()
# initSoil()
do_loop()