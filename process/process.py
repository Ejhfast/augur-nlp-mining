from __future__ import print_function
from nltk.corpus import names
from collections import defaultdict
import operator
import fileinput
import itertools
import sys
import re


# Adding the whitelist as a second argument screws up fileinput
with open("../files/sampwhitelist.txt") as file:
  whitelist = set(file.read().split())

def check_whitelist(action_str):
  return len(whitelist.intersection(action_str.split())) > 0

# Utils
def each_cons(xs, n):
  return itertools.izip(*(itertools.islice(g, i, None) for i, g in enumerate(itertools.tee(xs, n))))
def status(i):
  if (i%100000==0):
    print("Processed " + str(i) + " items.", file=sys.stderr)
def gram_list(counts,n):
  top = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse=True)
  return "\n".join([k+"\t"+str(v) for k,v in itertools.islice(top,0,n)])

# Replace names
def pre_filter(iter):
  nameswords = names.words()
  nameswords = set(map(lambda x: x.lower(), nameswords))
  def replacements(action):
    return ' '.join(['he' if x in nameswords else x for x in action.split()])
  for i, line in enumerate(iter):
    status(i)
    line = line.decode("ascii", "ignore").rstrip()
    line = '\t'.join([replacements(action) for action in line.split('\t')])
    yield line

# Filter for persons and objects
def person_filter(iter):
  count = 0
  subjects = set(["i", "you", "he", "she", "we", "they"])
  objects = set(["me", "you", "him", "his", "her", "us", "them", "#", "i", "you", "he", "she", "we", "they", "it"])
  def subject_match(actions):
    if len(subjects.intersection(actions[0].split())) > 0: return True
    else: return False
  def object_match(actions):
    if(len(actions) < 3): return False # no object?
    if len(objects.intersection(actions[2].split())) == 0: return True
    return False
  def approve(actions):
    return all([subject_match(actions), object_match(actions)])
  for group in each_cons(iter, 2):
    count += 1
    two_actions = [i.split('\t') for i in group]
    if(all([approve(a) for a in two_actions])):
      no_subjects = [" ".join(a[1:]) for a in two_actions]
      if(any([check_whitelist(" ".join(a)) for a in two_actions])):
        with_nops = "\tNOP 0\t".join(no_subjects).split("\t") # SO hacky...
        yield "NOP {}".format(count)
        for item in with_nops: yield item
        count = 0

def skip_grams(iter):
  n, skip = 2, 10
  for grp in each_cons(iter, 2*(n-1)+1):
    if not re.search("NOP", grp[0]):
      parsed = [int(i.split(" ")[-1]) if re.search("NOP",i) else i for i in grp]
      if reduce(lambda x, y: x & y, [x < skip for x in parsed if isinstance(x,int)]):
        strings = [x for x in parsed if not isinstance(x,int)]
        if len(set(strings)) > 1:
          yield strings

def count_grams(iter):
  counts = defaultdict(int)
  for n_gram in iter:
    counts["\t".join(n_gram)] += 1
    yield counts

if __name__ == "__main__":
	ticker, last_grams = 0, None
	pipeline = count_grams(skip_grams(person_filter(pre_filter(fileinput.input()))))
	for counts in pipeline:
	  ticker += 1
	  last_grams = counts
	  if(ticker%1000==0):
	    display = gram_list(counts,50)
	    sys.stderr.write("\x1b[2J\x1b[H")
	    print(display, file=sys.stderr)

	final_output = gram_list(last_grams,None)
	print(final_output)
