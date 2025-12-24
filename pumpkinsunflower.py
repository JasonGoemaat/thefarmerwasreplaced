
def calcPlant(x, y):
	if x < 8 and y < 8:
		return Entities.Pumpkin
	elif x < 2:
		return Entities.Sunflower
	elif y >= 10:
		return Entities.Grass
	elif (x + y) % 2 == 1:
		return Entities.Tree
	else:
		return Entities.Carrot
		
flag_fertilize = True
live_pumpkins = 0
sunflowers = []
sizes = [0,0,0,0,0,0,0,0,0] # 7-15

def initPlant():
	x, y = get_pos_x(), get_pos_y()
	if can_harvest():
		harvest()
	p = calcPlant(x, y)
	if p == Entities.Pumpkin or p == Entities.Carrot or p == Entities.Sunflower:
		till()
	if p != Entities.Grass:
		plant(p)
		if p == Entities.Sunflower:
			while measure() < 15:
				till()
				till()
				plant(p)
			size = measure() - 7
			sizes[size] = sizes[size] + 1
	
def moveNext():
	i = get_pos_y() * get_world_size() + get_pos_x()
	m = i % (get_world_size() * 2)
	if m == get_world_size() - 1 or m == get_world_size():
		move(North)
	elif m < get_world_size():
		move(East)
	else:
		move(West)
	
def initPlants():
	for y in range(get_world_size()):
		for x in range(get_world_size()):
			initPlant()
			moveNext()

pumpkin_count = 0

def handlePlant(harvest_pumpkins):
	global flag_fertilize
	x, y = get_pos_x(), get_pos_y()
	p = calcPlant(x, y)
	if p == Entities.Sunflower:
		size = measure() - 7 # 7 to 15 becomes 0 to 8
		if can_harvest():
			haveLarger  = False
			for i in range(8-size):
				if sizes[size+i+1] > 0:
					haveLarger = True
					break
			if not haveLarger or True:
				harvest()
				plant(Entities.Sunflower)
				while measure() < 15:
					till()
					till()
					plant(Entities.Sunflower)
				newSize = measure() - 7
				if newSize != size:
					sizes[size] = sizes[size] - 1
					sizes[newSize] = sizes[newSize] + 1
					size = newSize
		return 0
	elif p == Entities.Pumpkin:
		if harvest_pumpkins:
			if can_harvest():
				harvest()
			plant(Entities.Pumpkin)
			return 0
		else:
			if get_entity_type() == Entities.Dead_Pumpkin:
				harvest()
				plant(Entities.Pumpkin)
				return 0
			if can_harvest():
				return 1
		return 0
	if can_harvest():
		harvest()
		if p != Entities.Grass:
			plant(p)
			if flag_fertilize and (get_pos_x() == (get_world_size() - 1)):
				use_item(Items.Fertilizer)
		return 0
	return 0
			
	
def doPass():
	global pumpkin_count
	harvest_pumpkins = False
	if pumpkin_count == 64:
		harvest_pumpkins = True
	pumpkin_count = 0
	for y in range(get_world_size()):
		for x in range(get_world_size()):		
			pumpkin_count += handlePlant(harvest_pumpkins)
			moveNext()

clear()			
initPlants()
while True:
	doPass()
	