def report(ticks, message):
	quick_print(ticks,'ticks:', message)
	
def time_for_loop():
	s = get_tick_count()
	for i in range(1000):
		# pass # takes 1
		pass
	e = get_tick_count()
	empty_ticks = e - s
	report(empty_ticks, '"pass" loop 1000 iterations')
	
	s = get_tick_count()
	for i in range(1000):
		move(North)
	e = get_tick_count()
	report(e - s, '"move" loop 1000 iterations')
		
	s = get_tick_count()
	for i in range(1000):
		move(North)
		move(South)
	e = get_tick_count()
	report(e - s, '"move N,S" loop 1000 iterations')

	i = 0
	s = get_tick_count()
	while i < 1000:
		move(North)
		move(South)
		i = i + 1 # extra tick, 402002 vs 400002 for above
	e = get_tick_count()
	report(e - s, '"move N,S" while loop 1000 iterations')
		
	list = []
	s = get_tick_count()
	for i in range(1000):
		list.append(i)
	e = get_tick_count()
	report(e - s, 'append 1000 times')

	s = get_tick_count()
	for i in range(1000):
		list.append(i) # 1 tick each still
	e = get_tick_count()
	report(e - s, 'append another 1000 times')

	s = get_tick_count()
	for i in range(1000):
		list.insert(0, i) # takes longer based on list length
	e = get_tick_count()
	report(e - s, 'inserting 1000 times up front') # 2500502 ticks vs 1002 for append

	s = get_tick_count()
	for i in range(1000):
		list.pop()
	e = get_tick_count()
	report(e - s, 'popping 1000 items (default)') # 1000 ticks to remove from end
	for i in range(1000):
		list.append(i)
	
	s = get_tick_count()
	for i in range(1000):
		list.pop(0)
	e = get_tick_count()
	report(e - s, 'popping 1000 items (from start)') # 2500502 ticks to remove from start
	for i in range(1000):
		list.append(i)

	quick_print('list length:', len(list))
	s = get_tick_count()
	la = list[0:1000]
	e = get_tick_count()
	report(e - s, 'slice items 0-1000 items to new list')

	quick_print('list length:', len(list))
	s = get_tick_count()
	la = list[1000:2000]
	e = get_tick_count()
	report(e - s, 'slice items 1000-1999 items to new list')

	quick_print('list length:', len(list))
	s = get_tick_count()
	la = list[2000:3000]
	e = get_tick_count()
	report(e - s, 'slice items 2000-2999 items to new list')

	quick_print('list length:', len(list))
	s = get_tick_count()
	la = list[2000:2100]
	e = get_tick_count()
	report(e - s, 'slice items 2000-2099 items to new list')
	quick_print('list length:', len(list))
	


time_for_loop()