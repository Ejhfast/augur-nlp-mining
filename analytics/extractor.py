from __future__ import print_function
from collections import defaultdict
import nltk
import fileinput
import itertools
import operator
import glob
import sys

# Utils
def pipe(gens,stream):
  for g in gens: stream = g(stream)
  for i in stream: yield i
def each_cons(xs, n):
	return itertools.izip(*(itertools.islice(g, i, None) for i, g in enumerate(itertools.tee(xs, n))))
def print_dict(counts,n):
	top = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse=True)
	return "\n".join([k+"\t"+str(v) for k,v in itertools.islice(top,0,n)])
def out_error(string, clear=True):
	if clear: sys.stderr.write("\x1b[2J\x1b[H")
	print(string, file=sys.stderr)

nouns = filter(lambda x: x[1] == "N", nltk.corpus.brown.tagged_words(simplify_tags=True))
nouns = set([w[0].lower() for w in nouns])

print(nouns)
# blacklist = defaultdict(bool)
# with open('blacklist.tsv','r') as bl:
#   for line in bl:
#     word, c = line.rstrip().split("\t")
#     blacklist[word.rstrip()] = True

# path -> files
def list_files(path):
  f_count = 0
  for file in glob.glob(path+"/*"):
    f_count += 1
    if(f_count%1==0): out_error("{} files".format(f_count))
    yield file

# file -> line
def iter_lines(iter):
  for file in iter:
    with open(file,"r") as f:
      for line in f: yield line

# line -> words
def iter_words(iter):
  for line in iter:
    for w in line.rstrip().split():
      yield w.lower()

# hashable item -> table
def count_items(iter):
  table = defaultdict(int)
  for i in iter:
    table[i] += 1
    yield table

# lines -> [words] in lines with that contain word_set items
def word_window(word_set):
  def window(iter):
    for line in iter:
      words = [w.lower() for w in line.rstrip().split() if w.lower() in nouns]
      #print(nouns)
      print([line,words])
      if(len(word_set.intersection(set(words))) > 2):
        for w in words: yield w
          # if(not blacklist[w]): yield w
  return window

test_set = set(["plate","fork","napkin","chair"])

pipeline = pipe([iter_lines, word_window(test_set), count_items], list_files(sys.argv[1]))

count, last_count = 0, None
for res in pipeline:
  count += 1
  last_count = res
  if(count%10==0):
    window = print_dict(res,50)
    out_error(window)
print(print_dict(last_count,None))
