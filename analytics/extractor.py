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
def or_g(f1,f2,stream):
  s1 = f1(stream)
  s2 = f2(stream)

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
def has_hypernym(token,syn,t=wn.NOUN):
  word,pos = token
  if(pos[0] == "V"):
    t=wn.VERB
  paths = get_supertypes(word, t)
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
    if(word in ["'m", "'s"]):
      lemma = "be"
    else:
      lemma = lmtzr.lemmatize(word,wn.VERB)
  elif(pos[0] == 'N'):
    lemma = lmtzr.lemmatize(word,wn.NOUN)
  if(not lemma):
    lemma = word
  lemma_cache[key] = lemma
  return [lemma,pos]

# path -> files
def list_files(path):
  f_count = 0
  for file in glob.glob(path+"/*"):
    f_count += 1
    if(f_count%500==0): out_error("{} files".format(f_count))
    yield file

def in_range(ite):
  n = 30
  gps = each_cons(ite,n)
  for seq in gps:
    words = [[x.rstrip() for x in line.split("\t")] for line in seq]
    nouns = filter(lambda x: x[1][0] == "N", words)
    nouns = [memo_lemma(x) for x in nouns]
    people = filter(lambda x: has_hypernym(x, "person.n.01"), nouns)
    objects = filter(lambda x: has_hypernym(x, "instrumentality.n.03"), nouns)
    locations = filter(lambda x: has_hypernym(x, "building.n.01") or has_hypernym(x,"geographical_area.n.01"), nouns)
    stuff = [locations, people, objects]
    wild = ["_","*"]
    stuff = [list(itertools.chain([wild],s)) for s in stuff] # widlcard
    comb = itertools.product(*stuff)
    for c in comb:
      #print(c)
      yield [" ".join(x) for x in c]
    for i in range(n):
      gps.next() # no need to repeat window...

def person_location_filter(ite):
  for line in ite:
    word, pos = [x.rstrip() for x in line.split("\t")]
    word, pos = memo_lemma([word,pos])

    if(pos[0] == "N"):
      if(has_hypernym([word,pos],"instrumentality.n.03")):
          yield [word,"object"]

      if(has_hypernym([word,pos],"person.n.01")):
          yield [word,"person"]

      if(has_hypernym([word,pos],"building.n.01")):
          yield [word,"location"]

      if(has_hypernym([word,pos],"geographical_area.n.01")):
          yield [word,"location"]


def verb_object_filter(iter):
  lookahead = each_cons(iter,2)
  for line_seq in lookahead: #changed to enable lookahead...
    line = line_seq[0]
    word, pos = [x.rstrip() for x in line.split("\t")]
    #tagger somehow doesn't do periods...
    period = (len(word) > 1 and word[-1] == ".")
    if(period):
      word = word[:-1]
    #people subjects
    if(pos == "PRP"):
      if(word.lower() == "it"):
        yield ["it", "n"]
      yield ["s/he", "s"]

    #adjective or adjective-object
    if(pos == "JJ"):
      word2,pos2 = [x.rstrip() for x in line_seq[1].split("\t")]
      is_o2, o2 = is_object([word2,pos2])
      if(is_o2):
        lookahead.next()
        yield [word.lower()+"-"+o2, "n"]
      else:
        yield [word.lower(), "adj"]


    is_o, o = is_object([word,pos])
    if(is_o):
      word2,pos2 = [x.rstrip() for x in line_seq[1].split("\t")]
      is_o2, o2 = is_object([word2,pos2])
      if(is_o2):
        lookahead.next()
        yield [o+"-"+o2, "n"]
      else:
        yield [o,"n"]

    #verb
    if(pos[0] == "V"):
      if(pos == "VBN"):
        None
        #yield [word.lower(), "vbn"]
      else:
        word2,pos2 = [x.rstrip() for x in line_seq[1].split("\t")]
        l1, p1 = memo_lemma([word,pos])
        if(pos2 == "TO" or pos2 == "IN"):
          lookahead.next()
          yield [l1+"-"+word2.lower(),"v"]
        else:
          yield [l1,"v"]

    #punctuation (kill streams with ? !)
    if(pos == "."):
      yield [word, word]
    #kill streams with and
    if(pos == "CC"):
      yield ["&", "cc"]
    #add a period, if one was tacked on
    if(period):
      yield [".", "."]

# file -> line
def iter_lines(iter):
  for file in iter:
    if file: # Stupid None from grouper...
      with open(file,"r") as f:
        for line in f: yield line

# line -> words
def iter_words(iter):
  articles = set(["a", "the", "an"])
  for line in iter:
    for w in line.rstrip().split():
      if(not w in articles): yield w.lower()

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

def p_or_l(ite):
  for seq in ite:
    print(seq)
    seq = sorted(seq,key=lambda x:x[1], reverse=True)
    if(seq[0][1] == "person" and seq[1][1] == "object" and seq[2][1] == "location"):
      yield [" ".join(s) for s in seq]

def v_or_o(iter):
  for seq in iter:
    ok = [["s","v","n"], ["n","v","n"], ["s","v","adj"]]
    def check_ok(s,ty):
      return seq[0][1] == ty[0] and seq[1][1] == ty[1] and seq[2][1] == ty[2]
    if(any([check_ok(seq, t) for t in ok])): # v,o or o,v
      yield [" ".join(s) for s in seq]
      # v_ = [seq[0][0], "_"]
      # _o = ["_", seq[1][0]]
      # v_o = [seq[0][0], seq[1][0]]
      # yield [v_,_o,v_o]
      #for i in [v_,_o,v_o]: yield i

def s_v(iter):
  for seq in iter:
    if(seq[0][1] == "s" and seq[1][1] == "v"): # v,o or o,v
      yield [" ".join(s) for s in seq]

def possible(iter):
  for seq in iter:
    for x,y in [[x,y] for x in seq[0] for y in seq[1] if x != y]:
      yield [" ".join(x), " ".join(y)]

def with_tags(path):
  process = pipe([iter_lines, in_range, count_items], list_files(path))
  count = 0
  saved = None
  for p in process:
    count += 1
    saved = p
    #print("\t".join(p))
    # if(count % 10000 == 0):
    #   #out_error(p)
    #   out_error(print_dict(p,30))
    # if(count % 1000000 == 0):
    #   break
  print(print_dict(saved,None))


#reverb_like_thing("I go to the store.")
with_tags(sys.argv[1])
#run_tags_multi(sys.argv[1])
#list_files_multi(sys.argv[1])
