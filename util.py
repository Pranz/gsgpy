

def generic_index(p, ls):
	i = 0
	while i < len(ls):
		if p(ls[i]):
			return i
		i += 1
