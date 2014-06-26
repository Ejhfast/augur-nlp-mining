import fileinput

for line in fileinput.input():
	actions = line.split('\t')
	if actions[0] != actions[1].rstrip():
		print line.rstrip()