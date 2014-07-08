from __future__ import print_function
from nltk.corpus import names
from collections import defaultdict
import operator
import fileinput
import itertools
import sys
import re
import argparse

def check_whitelist(action_str):
  return len(whitelist.intersection(action_str.split())) > 0

# Utils
def each_cons(xs, n):
  return itertools.izip(*(itertools.islice(g, i, None) for i, g in enumerate(itertools.tee(xs, n))))
def out_error(string, clear=True): 
	if clear:
		sys.stderr.write("\x1b[2J\x1b[H")
	print(string, file=sys.stderr)
def gram_list(counts,n):
  top = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse=True)
  return "\n".join([k+"\t"+str(v) for k,v in itertools.islice(top,0,n)])

# Replace names
def pre_filter(iter):
  nameswords = set([word.lower() for word in names.words()])
  def replace(s): return ' '.join(['he' if x in nameswords else x for x in s.split()])
  for i, line in enumerate(iter):
    if(i%100000==0): out_error("Processed " + str(i) + " lines.", clear = False)
    clean = line.decode("ascii", "ignore").rstrip()
    yield [replace(c) for c in clean.split('\t')]

# Filter for persons and objects
def person_filter(iter):
  count = 0
  subjects = set(["i", "you", "he", "she", "we", "they"])
  objects = set(["me", "you", "him", "his", "her", "us", "them", "#", "i", "you", "he", "she", "we", "they", "it"])
  def subject_match(actions):
    return True if len(subjects.intersection(actions[0].split())) > 0 else False
  def object_match(actions):
    if(len(actions) < 3): return False # no object?
    return True if len(objects.intersection(actions[2].split())) == 0 else False
  def approve(actions):
    return all([subject_match(actions), object_match(actions)])
  for group in each_cons(iter, 2):
    count += 1
    if(all([approve(a) for a in group])):
      no_subjects = [" ".join(a[1:]) for a in group]
      if(any([check_whitelist(" ".join(a)) for a in group])):
        with_nops = "\tNOP 0\t".join(no_subjects).split("\t") # SO hacky...
        yield "NOP {}".format(count)
        for item in with_nops: yield item
        count = 0

def skip_grams(iter):
  n, skip = 2, 10
  for grp in each_cons(iter, 2*(n-1)+1):
    if not re.search("NOP", grp[0]):
      parsed = [int(i.split(" ")[-1]) if re.search("NOP",i) else i for i in grp]
      if reduce(operator.and_, [x < skip for x in parsed if isinstance(x,int)]):
        just_strings = [x for x in parsed if not isinstance(x,int)]
        if len(set(just_strings)) > 1: yield just_strings

def count_grams(iter):
  counts = defaultdict(int)
  for n_gram in iter:
    counts["\t".join(n_gram)] += 1
    yield counts

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('input', nargs='?', type=argparse.FileType('r'), default=open('../files/watpad.tsv'))
	parser.add_argument('whitelist', nargs='?', type=argparse.FileType('r'), default=open('../files/sampwhitelist.txt'))
	args = parser.parse_args()
	ticker, last_grams = 0, None
	whitelist = set(args.whitelist.read().split());
	pipeline = count_grams(skip_grams(person_filter(pre_filter(args.input))))
	for ngram_counts in pipeline:
  		ticker += 1
	  	last_grams = ngram_counts
	  	if(ticker%1000==0):
	  		display = gram_list(ngram_counts,50)
	  		out_error(display)
	final_output = gram_list(last_grams,None)
	print(final_output)