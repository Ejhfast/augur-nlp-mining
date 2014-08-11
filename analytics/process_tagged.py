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
import re

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
  else:
    is_object_dict[hsh] = (True, lemmatize)
    return (True, lemmatize)
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
  blacklist = ['mean','walk','see','need','ask','take','have','say', 'get', 'let', 'tell', 'think', 'know', 'go', 'saw', 'look', 'make', 'put', 'turn', 'seem', 'come', 'felt']
  lemmatize = wn.morphy(token[0].lower(),wn.VERB)
  # if(lemmatize and (not lemmatize in blacklist)):
  #   ssts = wn.synsets(lemmatize, wn.VERB)
  #   roots = [x.root_hypernyms() for x in ssts]
  #   has_act = [reduce(operator.or_, [y.name == 'act.v.01' for y in x]) for x in roots]
  #   is_there = reduce(operator.or_, has_act)
  #   if(is_there):
  #     is_action_dict[hsh] = (True, lemmatize)
  #     return (True, lemmatize)
  #   else:
  #     is_action_dict[hsh] = (False, lemmatize)
  #     return (False, lemmatize)
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
    if(f_count%1000==0): out_error("{} files".format(f_count))
    yield file

# process tokenized input
def verb_object_filter(iter):
  for line in iter:
    out = []
    qs = ["where","when","how","why","who","what"]
    for l in line:
      word,pos = l
      word = word.lower()
      #word, pos = [x.rstrip() for x in line.split("\t")]
      # if(pos == "NNP"):
      #   out.append("NNP")
      # else:
      out.append(word)
      # is_o, o = is_object([word,pos])
      # if(is_o):
      #   out.append(o+"-o")
      # is_v, v = is_action([word,pos])
      # if(is_v):
      #   out.append(v+"-v")
      # if(word.lower() in qs):
      #   out.append(word.lower()+"-q")
      # if(word.lower() == "?"):
      #  out.append("?")
    if(len(out)>1 and len(out)<10):
      #out_error(out+["?"],clear=False)
      yield " ".join(out)#sorted(out)

def in_list(iter):
  s = set([])
  with open("question-10.tsv") as f:
    for line in f:
      l,c = line.split("\t")
      s.add(l)
  for line in iter:
    if(line in s):
      yield line


# file -> line
def iter_lines(iter):
  for file in iter:
    if file: # Stupid None from grouper...
      with open(file,"r") as f:
        for line in f:
          yield [x.rstrip() for x in line.split("\t")]

def n_grams(n):
  def over(iter):
    for seq in each_cons(iter,n):
      if(len(set(seq)) > 0): # Fixme: hardcoded for bigrams
        yield seq
  return over

def in_dialog(wds):
  dialog = []
  for pos_w in wds:
    dialog = []
    if(pos_w[1] == "``"):
      pos_w = wds.next()
      while(pos_w[1] != "''"):
        dialog.append(pos_w)
        pos_w = wds.next()
      if(len(dialog)>0):
        yield dialog
        # if(dialog[-1][0] == "?"):
        #   yield dialog
    # for w in dialog:
    #   yield w

def dialog_grams(iter):
  for seq in iter:
    if(seq[0][-1] == "?"):
      yield seq

def skip_grams(n):
  def over(iter):
    for seq in each_cons(iter,n):
      head = seq[0]
      tail = seq[1:]
      for bigram in [[head,t] for t in tail]:
        if(len(set(bigram)) > 0): yield bigram
  return over

# hashable item -> table
def count_items(iter):
  table = defaultdict(int)
  for i in iter:
    table["\t".join(i)] += 1
    yield table

def with_tags(path):
  process = pipe([iter_lines, in_dialog, verb_object_filter, in_list, n_grams(2), count_items], list_files(path))
  count = 0
  saved = None
  for p in process:
    count += 1
    saved = p
    #out_error(p)
    if(count % 1000 == 0):
      out_error(print_dict(p,30))
    # if(count % 10000000 == 0):
    #   break
  print(print_dict(saved,None))

with_tags(sys.argv[1])
