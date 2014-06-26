from __future__ import print_function
import fileinput
import operator
from collections import defaultdict
import sys
import os
import warnings

counts = defaultdict(int)
iters = 0
refresh_time = 500
NUM_TO_PRINT = 10

def norm((k,v)):
	tokens = k.rstrip().split('\t')
	print(k.rstrip() + '\t' + str(v))

def err((k,v)):
	tokens = k.rstrip().split('\t')
	print (map(lambda x: x.ljust(30), tokens), v, file=sys.stderr)

for line in fileinput.input():
	actions = line
	counts[actions] += 1
	val = counts[actions]
	counts.values()
	iters = iters +1
	if(iters%refresh_time == 0):
		sys.stderr.write("\x1b[2J\x1b[H")
		print ("Outputting " + str(iters) + " items", file=sys.stderr)
		c = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse= True)
		filtered =  c[:NUM_TO_PRINT]
		map(err, filtered)
		print ("--------------", file=sys.stderr)

counts = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse= True)
counts = filter(lambda (k,v): True if v >1 else False, counts)
map(norm, counts)