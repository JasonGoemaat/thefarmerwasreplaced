def calcPlant(x, y):
	if x < 6 and y < 6:
		return Entities.Pumpkin
	elif x < 6 or y >= 6:
		return Entities.Grass
	elif (x + y) % 2 == 1:
		return Entities.Tree
	else:
		return Entities.Carrot
		
live_pumpkins = 0

def initPlant():
	x, y = get_pos_x(), get_pos_y()
	if can_harvest():
		harvest()
	p = calcPlant(x, y)
	if p == Entities.Pumpkin or p == Entities.Carrot:
		till()
	if p != Entities.Grass:
		plant(p)
	
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
	x, y = get_pos_x(), get_pos_y()
	p = calcPlant(x, y)
	if p == Entities.Pumpkin:
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
		return 0
	return 0
			
	
def doPass():
	global pumpkin_count
	harvest_pumpkins = False
	if pumpkin_count == 36:
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
