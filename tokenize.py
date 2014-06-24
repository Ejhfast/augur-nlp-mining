import fileinput
import operator
from collections import defaultdict

counts = defaultdict(int)

def p((k,v)):
	print "the person\t" + k + "\t" + str(v) 

pronouns = ["he","she","you","i","we","they"]
for line in fileinput.input():
	tokens = line.split('\t')
	actions = tokens[2:]
	if any(s == actions[0] for s in pronouns):
		counts['\t'.join(actions[1:]).rstrip()] += 1

#TODO reverse?
counts = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse= True)
map(p, counts)