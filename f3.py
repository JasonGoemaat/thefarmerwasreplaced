d1 = {'x':1,'y':2}
d2 = {'y':3,'z':4}
d3 = d1
for key in d2:
	value = d2[key]
	d3[key] = value
quick_print(d3)