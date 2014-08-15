from __future__ import print_function
from collections import defaultdict
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import itertools
import operator
import glob
import sys

#Global hashes
is_object_dict = defaultdict(tuple)
is_action_dict = defaultdict(tuple)
lemma_cache = {}
hyp_cache = {}

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
def get_supertypes(w,t=wn.NOUN):
  key = "\t".join([w,t])
  if(key in hyp_cache):
    return hyp_cache[key]
  syn = wn.synsets(w,t)
  if(len(syn) > 0):
    all_p = [s.hypernym_paths() for s in syn[:2]]
    result = itertools.chain.from_iterable(all_p)
    hyp_cache[key] = list(result)
    return result
  else:
    hyp_cache[key] = []
    return []
def has_hypernym(token,syn):
  word,pos = token
  paths = get_supertypes(word, wn.NOUN)
  return any([wn.synset(syn) in p for p in paths])
def is_object(token,typ='entity.n.01'):
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
  hypernyms = [s.lowest_common_hypernyms(wn.synset(typ)) for s in synsets]
  check_objects = [wn.synset(typ) in o for o in hypernyms]
  if(reduce(operator.or_, check_objects)):
    is_object_dict[hsh] = (True, lemmatize)
    return (True, lemmatize)
  else:
    is_object_dict[hsh] = (False, None)
    return (False, None)
def memo_lemma(token):
  word,pos = token
  if(not word): return token
  word = word.lower()
  if(word[-1] == "." and len(word) > 1):
    word = word[:-1]
  key = "\t".join([word,pos])
  lemma = None
  if(key in lemma_cache):
    return [lemma_cache[key],pos]
  if(pos[0] == 'V'):
    if(word in ["'m", "'s","'re"]):
      lemma = "be"
    else:
      lemma = lmtzr.lemmatize(word,wn.VERB)
  elif(pos[0] == 'N'):
    lemma = lmtzr.lemmatize(word,wn.NOUN)
  if(not lemma):
    lemma = word
  lemma_cache[key] = lemma
  return [lemma,pos]
