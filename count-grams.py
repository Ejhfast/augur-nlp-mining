import fileinput
import operator
from collections import defaultdict

counts = defaultdict(int)

def p((k,v)):
	print k + '\t' + str(v) 

for line in fileinput.input():
	tokens = line.split('\t')
	actions = '\t'.join(tokens)
	counts[actions] += 1
	if counts[actions] > 1:
		print actions + str(count[actions])

"""
counts = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse= True)
counts = filter(lambda (k,v): True if v >1 else False, counts)
map(p, counts)
"""