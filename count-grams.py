import fileinput
import operator
from collections import defaultdict

counts = defaultdict(int)

def p((k,v)):
	print k + '\t' + str(v) 

for line in fileinput.input():
	tokens = line.split('\t')
	actions = '\t'.join(tokens[:-1])
	counts[actions] += 1

counts = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse= True)
counts = filter(lambda (k,v): True if v >1 else False, counts)
map(p, counts)