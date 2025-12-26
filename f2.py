map = []

def update(map, s):
	map.append("update-" + s)


def drone():
	global map
	map.append("drone")
	update(map, "drone")
	
def run(map):
	# global map
	map.append("run()")
	update("run")
	spawn_drone(drone)
	
run()
print(map)