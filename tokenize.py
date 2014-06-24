import fileinput
import operator
from collections import defaultdict

counts = defaultdict(int)

def p((k,v)):
	#TODO: better way to do this? 
	if len(k.split('\t')) == 2:
		print "the person\t" + k + "\t" + str(v) 

#subject match
#TODO: automated subject match
subject_match = ["i", "you", "he", "she", "it", "we", "you", "they"]

#object match
#TODO: automated object match
object_match = ["me", "you", "him", "her", "us", "them", "#"]

for line in fileinput.input():
	tokens = line.split('\t')
	actions = tokens[2:]
	if any(any(r == s for r in subject_match) for s in actions[0].split(' ')):
		if not any(any(r == s for r in object_match) for s in actions[2].split(' ')):
			k = '\t'.join(actions[1:]).rstrip()
			counts[k] += 1
			p((k, 1))

counts = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse= True)
map(p, counts)