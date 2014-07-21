from __future__ import print_function
from collections import defaultdict, Counter, deque
import multiprocessing as mp
import nltk
from nltk.corpus import wordnet as wn
import fileinput
import itertools
import operator
import glob
import sys

#Global cache for object/verb detection (speed things up a lot)
is_object_dict = defaultdict(tuple)
is_action_dict = defaultdict(tuple)

# Utils
def pipe(gens,stream):
  for g in gens: stream = g(stream)
  for i in stream: yield i
def each_cons(xs, n):
  return itertools.izip(*(itertools.islice(g, i, None) for i, g in enumerate(itertools.tee(xs, n))))
def print_dict(counts,n):
  top = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse=True)
  return "\n".join([k+"\t"+str(v) for k,v in itertools.islice(top,0,n)])
def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)
def out_error(string, clear=True):
  if clear: sys.stderr.write("\x1b[2J\x1b[H")
  print(string, file=sys.stderr)
def is_object(token):
  hsh = "\t".join(token)
  if(hsh in is_object_dict):
    return is_object_dict[hsh]
  if(token[1][0] != 'N' or token[1] == "NNP"):
    is_object_dict[hsh] = (False, None)
    return (False, None)
  lemmatize = wn.morphy(token[0].lower(),wn.NOUN)
  #blacklist = ["jenny","peter","catherine",] # names mapped to objects...
  if(not lemmatize):
    is_object_dict[hsh] = (False, None)
    return (False, None)
  synsets = wn.synsets(lemmatize)
  hypernyms = [s.lowest_common_hypernyms(wn.synset('object.n.01')) for s in synsets]
  check_objects = [wn.synset('object.n.01') in o for o in hypernyms]
  if(reduce(operator.or_, check_objects)):
    is_object_dict[hsh] = (True, lemmatize)
    return (True, lemmatize)
  else:
    is_object_dict[hsh] = (False, None)
    return (False, None)
def is_action(token):
  hsh = "\t".join(token)
  if(hsh in is_action_dict):
    return is_action_dict[hsh]
  if(token[1][0] != 'V'):
    is_action_dict[hsh] = (False, None)
    return (False, None)
  blacklist = ['have','do','be','say', 'get', 'let', 'tell', 'think', 'know', 'go', 'saw', 'look', 'make', 'put', 'turn', 'seem', 'come', 'felt']
  lemmatize = wn.morphy(token[0].lower(),wn.VERB)
  if(lemmatize in blacklist or lemmatize == None):
    is_action_dict[hsh] = (False, lemmatize)
    return (False, lemmatize)
  else:
    is_action_dict[hsh] = (True, lemmatize)
    return (True, lemmatize)


# path -> files
def list_files(path):
  f_count = 0
  for file in glob.glob(path+"/*"):
    f_count += 1
    if(f_count%100==0): out_error("{} files".format(f_count))
    yield file

# process tokenized input
def verb_object_filter(iter):
  for line in iter:
    word, pos = [x.rstrip() for x in line.split("\t")]
    is_o, o = is_object([word,pos])
    if(is_o):
      yield o+" O"
    is_v, v = is_action([word,pos])
    if(is_v):
      yield v+" A"

# file -> line
def iter_lines(iter):
  for file in iter:
    if file: # Stupid None from grouper...
      with open(file,"r") as f:
        for line in f: yield line

def n_grams(n):
  def over(iter):
    for seq in each_cons(iter,n):
      if(len(set(seq)) > 1): # Fixme: hardcoded for bigrams
        yield seq
  return over

# hashable item -> table
def count_items(iter):
  table = defaultdict(int)
  for i in iter:
    table["\t".join(i)] += 1
    yield table

def with_tags(path):
  process = pipe([iter_lines, verb_object_filter, n_grams(2), count_items], list_files(path))
  count = 0
  saved = None
  for p in process:
    count += 1
    saved = p
    if(count % 100000 == 0):
      out_error(print_dict(p,20))
    # if(count % 1000000 == 0):
    #   break
  print(print_dict(saved,None))

with_tags(sys.argv[1])
