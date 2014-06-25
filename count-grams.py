import fileinput
import operator
from collections import defaultdict
from sys import stdout

counts = defaultdict(int)
iters = 0
refresh_time = 1000
NUM_TO_PRINT = 20

def p((k,v)):
	stdout.write("%s\n" % k)

#todo: move this conditional to skip-gram
def removeSameAction((k,v)):
	spl = k.split('\t')
	if spl[0] != spl[1].rstrip():
		return True
	return False

for line in fileinput.input():
	tokens = line.split('\t')
	actions = '\t'.join(tokens)
	counts[actions] += 1
	val = counts[actions]
	counts.values()
	iters = iters +1
	if(iters%refresh_time == 0):
		stdout.flush()
		stdout.write("===============================\n")
		c = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse= True)
		iters = 0
		bound = NUM_TO_PRINT
		filtered =  c[:bound]
		while(True):
			filtered = filter(removeSameAction, filtered)
			if len(filtered) == NUM_TO_PRINT:
				break
			filtered.append(c[bound])
			bound = bound+1
		map(p, filtered)
		stdout.write("===============================\n")

"""
counts = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse= True)
counts = filter(lambda (k,v): True if v >1 else False, counts)
map(p, counts)
"""