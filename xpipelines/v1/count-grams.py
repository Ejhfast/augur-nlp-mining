from __future__ import print_function
import fileinput
import operator
from collections import defaultdict
import sys
import os
import warnings

refresh_time = 500
NUM_KEYS_TO_PRINT = 20
NUM_VALS_TO_PRINT = 5

def norm((k,v)):
	tokens = k.rstrip().split('\t')
	print(k.rstrip() + '\t' + str(v))

def err((k,v)):
	tokens = k.rstrip().split('\t')
	print (map(lambda x: x.ljust(40), tokens), v, file=sys.stderr)

def actionCount1():
	iters = 0
	counts = defaultdict(int)

	for line in fileinput.input():
		actions = line
		counts[actions] += 1
		iters = iters +1
		if(iters%refresh_time == 0):
			sys.stderr.write("\x1b[2J\x1b[H")
			print ("Outputting " + str(iters) + " items", file=sys.stderr)
			c = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse= True)
			filtered =  c[:NUM_KEYS_TO_PRINT]
			map(err, filtered)
			print ("--------------", file=sys.stderr)

	counts = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse= True)
	counts = filter(lambda (k,v): True if v >1 else False, counts)
	map(norm, counts)

#todo finish output printing
def actionCount2():
	iters = 0
	fcounts = defaultdict(int)
	counts = defaultdict(int)

	iters = 0
	follow = {}
	for line in sys.stdin:
		actions = line.split('\t')
		first = actions[0]
		second = actions[1].rstrip()
		if not follow.get(first):
			follow[first] = [second]
		else:
			follow[first].append(second)
		fcounts[first] += 1
		counts[line.rstrip()] += 1
		iters = iters +1
		if(iters%refresh_time == 0):
			sys.stderr.write("\x1b[2J\x1b[H")
			print ("Outputting " + str(iters) + " items", file=sys.stderr)
			c = sorted(fcounts.iteritems(), key=operator.itemgetter(1), reverse= True)
			filtered =  c[: NUM_KEYS_TO_PRINT]
			firsts = [(i[0]) for i in filtered]
			for first in firsts:
				following = set(follow[first])
				print(first.ljust(40), end='', file = sys.stderr)
				c = sorted(following, key=lambda f: counts.get(first + '\t' + f), reverse= True)
				d = map(lambda x: first + '\t' + x, c)
				d = map(lambda x: counts[x], d)
				d = d[:5]if len(d) > NUM_VALS_TO_PRINT else d
				c = c[:5] if len(c) > NUM_VALS_TO_PRINT else c
				print (c, d, file = sys.stderr)
				#print (map(lambda x: x.ljust(40), tokens), v, file=sys.stderr)
			print ("--------------", file=sys.stderr)

if(len(sys.argv) > 1 and sys.argv[1] == "2"):
	actionCount2()
actionCount1()