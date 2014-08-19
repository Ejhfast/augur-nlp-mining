from __future__ import print_function
from collections import defaultdict, Counter, deque
import multiprocessing as mp
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import fileinput
import itertools
import operator
import glob
import sys
from combinator import *

#Global hashes
is_object_dict = defaultdict(tuple)
is_action_dict = defaultdict(tuple)
lemma_cache = {}

lmtzr = WordNetLemmatizer()

# Utils
def pipe(gens,stream):
  for g in gens: stream = g(stream)
  for i in stream: yield i
def each_cons(xs, n):
	return itertools.izip(*(itertools.islice(g, i, None) for i, g in enumerate(itertools.tee(xs, n))))
def print_dict(counts,n):
	top = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse=True)
	return "\n".join([k+"\t\t"+str(v) for k,v in itertools.islice(top,0,n)])
def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)
def out_error(string, clear=True):
	if clear: sys.stderr.write("\x1b[2J\x1b[H")
	print(string, file=sys.stderr)
def memo_lemma(token):
  word,pos = token
  if(not word): return token
  word = word.lower()
  key = "\t".join([word,pos])
  lemma = None
  if(key in lemma_cache):
    return [lemma_cache[key],pos]
  if(pos[0] == 'V'):
    lemma = lmtzr.lemmatize(word,wn.VERB)
  elif(pos[0] == 'N'):
    lemma = lmtzr.lemmatize(word,wn.NOUN)
  if(not lemma):
    lemma = word
  lemma_cache[key] = lemma
  return [lemma,pos]
def is_object(token):
  hsh = "\t".join(token)
  if(hsh in is_object_dict):
    return is_object_dict[hsh]
  if(token[1][0] != 'N' or token[1] == "NNP"):
    is_object_dict[hsh] = (False, None)
    return (False, None)
  lemmatize = wn.morphy(token[0].lower(),wn.NOUN)
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
  blacklist = [] #['see','have','do','be','say', 'get', 'let', 'tell', 'think', 'know', 'go', 'saw', 'look', 'make', 'put', 'turn', 'seem', 'come', 'felt']
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
    if(f_count % 1 == 0): out_error("{} files".format(f_count))
    yield file

# file -> line
def iter_tokens(iter):
  for file in iter:
    if file: # Stupid None from grouper...
      with open(file,"r") as f:
        for line in f:
          word, pos = [x.rstrip() for x in line.split("\t")]
          word = word.lower()
          if(word[-1] == "."):
            yield [word[:-1], pos]
            yield [".", "."]
          else:
            yield [word, pos]

def f_tokens(ite):
  for tk in ite:
    word,pos = tk
    if(pos[0] == "N" or pos[0] == "V" or pos == "JJ" or pos == "PRP"):
      yield memo_lemma(tk)
    elif(pos[0] == "."):
      yield tk

def n_grams(n):
  def over(iter):
    for seq in each_cons(iter,n):
        yield seq
  return over

def skip_grams2(n):
  def over(iter):
    for seq in each_cons(iter,n):
      for s in [[seq[0],i] for i in seq if i != seq[0]]: yield s
  return over

# hashable item -> table
def count_items(iter):
  table = defaultdict(int)
  for i in iter:
    table["\t\t".join(i)] += 1
    yield table

def possible(iter):
  for seq in iter:
    for x,y in [[x,y] for x in seq[0] for y in seq[1] if x != y]:
      yield [" ".join(x), " ".join(y)]

v = atom(lambda x: (x[1][0] == "V", x))
n = atom(lambda x: (x[1][0] == "N", memo_lemma(x)))
adj = atom(lambda x: (x[1] == "JJ", x))
end = atom(lambda x: ((x[1] == "."), x))
s = atom(lambda x: (x[1] == "PRP", ["s/he", "PRP"]))

adjo = comb_then([adj,n], lambda x: [x[0][0] + "_" + x[1][0], "NJJ"])
nvo = comb_then([comb_or([n,s]),v,comb_or([adjo,n])])
star = atom(lambda x: (True,x))
filter_tokens = comb_or([v,n,adj,s,end,skip(star)])
extract_relations = comb_or([nvo,skip(star)])

f = iter_many(filter_tokens)
e = iter_many(extract_relations, lambda x: [" ".join(y) for y in x])

def with_skip(f): return iter_many(comb_or([f,skip(star)]))

def with_tags(path):
  process = pipe([iter_tokens, f_tokens, with_skip(adjo)], list_files(path))
  count = 0
  saved = None
  for p in process:
    count += 1
    saved = p
    print(p)
    #print("\t".join(p))
    # if(count % 10000 == 0):
    #   #out_error(p)
    #   out_error(print_dict(p,30))
    # if(count % 1000000 == 0):
    #   break
  #print(print_dict(saved,None))


#reverb_like_thing("I go to the store.")
with_tags(sys.argv[1])
#run_tags_multi(sys.argv[1])
#list_files_multi(sys.argv[1])
