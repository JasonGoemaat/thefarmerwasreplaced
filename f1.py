clear()

def do_sunflowers_simple():
	for i in range(get_world_size()):
		till()
		plant(Entities.Sunflower)
		use_item(Items.Water)
		move(North)
	while (True):
		if can_harvest():
			harvest()
			plant(Entities.Sunflower)
			if get_water() < 0.5:
				use_item(Items.Water)
		move(North)
		
def do_sunflowers():
	def is_largest():
		size = measure()
		largest = True
		for i in sizes:
			if i > size:
				largest = False
				break
		return largest
	sizes = []
	for i in range(get_world_size()):
		till()
		plant(Entities.Sunflower)
		sizes.append(measure())
		move(North)
	while True:
		if can_harvest() and is_largest():
			harvest()
			plant(Entities.Sunflower)
			i = get_pos_y()
			sizes[i] = measure()
		move(North)
				
def do_grass():
	while True:
		for i in range(get_world_size()):
			harvest()
			move(North)

def do_carrot_wood():
	plants = [Entities.Carrot, Entities.Tree]
	flavor = get_pos_x() % 2
	y = 0
	for i in range(get_world_size()):
		till()
		plant(plants[(y + flavor) % 2])
		use_item(Items.Water)
		y = (y + 1) % get_world_size()
		move(North)
	while True:
		if can_harvest():
			harvest()
			plant(plants[(y + flavor) % 2])
			if get_water() < 0.5:
				use_item(Items.Water)
		y = (y + 1) % get_world_size()
		move(North)
	
spawn_drone(do_sunflowers_simple)
move(East)
spawn_drone(do_sunflowers_simple)
move(East)

for i in range(5):
	spawn_drone(do_grass)
	move(East)
	
for i in range(8):
	spawn_drone(do_carrot_wood)
	move(East)
		
do_carrot_wood()