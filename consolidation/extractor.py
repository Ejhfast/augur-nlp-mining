from __future__ import print_function
from collections import defaultdict, Counter, deque
import multiprocessing as mp
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import fileinput
import itertools
import operator
import os
from stream_util import *

def wedge(tick):
  d=os.getpid()
  def cl(ite):
    count = 0
    for i in ite:
      if(count%tick==0): out_error("{}: {}".format(d,count))
      count += 1
      yield i
  return cl

# path -> files
def list_files(path):
  f_count = 0
  for file in glob.glob(path+"/*"):
    f_count += 1
    #if(f_count%100==0): out_error("{} files".format(f_count))
    yield file

def in_range(syns,n):
  funcs = [(lambda x,z=y: any([has_hypernym(x,i) for i in z])) for y in syns]
  def cl(ite):
    gps = each_cons(ite,n)
    for seq in gps:
      words = [[x.rstrip() for x in line.split("\t")] for line in seq]
      nouns = filter(lambda x: x[1][0] == "N", words)
      nouns = [memo_lemma(x) for x in nouns]
      stuff = [filter(f,nouns) for f in funcs]
      wild = ["_","*"]
      stuff = [list(itertools.chain([wild],s)) for s in stuff] # widlcard
      comb = itertools.product(*stuff)
      for c in comb:
        if(not all([a == c[0] for a in c])):
          yield [x[0] for x in c]
      for i in range(n):
        gps.next() # no need to repeat window...
  return cl

def relation_filter(iter):
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
        continue #yield ["it", "n"]
      yield ["s/he", "s"]
      continue

    if(has_hypernym([word,pos], "person.n.01")):
      p, ps = memo_lemma([word,pos])
      if(not p in ["have"]):
        yield [p,"p"]
        continue

    #adjective or adjective-object
    if(pos == "JJ"):
      word2,pos2 = [x.rstrip() for x in line_seq[1].split("\t")]
      is_o2, o2 = is_object([word2,pos2])
      if(is_o2):
        lookahead.next()
        yield [word.lower()+"-"+o2, "n"]
      else:
        yield [word.lower(), "adj"]
      continue

    is_o, o = is_object([word,pos])
    if(is_o):
      word2,pos2 = [x.rstrip() for x in line_seq[1].split("\t")]
      is_o2, o2 = is_object([word2,pos2])
      if(is_o2):
        lookahead.next()
        yield [o+"-"+o2, "n"]
      else:
        yield [o,"n"]
      continue

    #verb
    if(pos[0] == "V"):
    #if(has_hypernym([word,pos],"act.v.01") or has_hypernym([word,pos],"move.v.02")):
      word2,pos2 = [x.rstrip() for x in line_seq[1].split("\t")]
      l1, p1 = memo_lemma([word,pos])
      if(pos2 == "TO" or pos2 == "IN"):
        lookahead.next()
        yield [l1+"-"+word2.lower(),"v"]
      else:
        yield [l1,"v"]
      continue

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

def valid_relations(iter):
  for seq in iter:
    ok = [["p","v","n"], ["n","v","n"], ["p","v","adj"],
          ["n","v","p"], ["p","v","p"], ["s","v","n"], ["s","v","p"]]
    def check_ok(s,ty):
      return seq[0][1] == ty[0] and seq[1][1] == ty[1] and seq[2][1] == ty[2]
    if(any([check_ok(seq, t) for t in ok])): # v,o or o,v
      yield [" ".join(s) for s in seq]

def subject_match_subject(it):
  for seq in it:
    #if(seq[0][0].split(" ")[-1] == "p" and seq[1][0].split(" ")[-1] == "p"):
    if(seq[0][0] == seq[1][0]):  
      yield seq

def string_gram(iter):
  for seq in iter:
      yield ["\t".join(s) for s in seq]

def extract(ite):
  saved = None
  print(ite)
  for i in ite:#wedge(name,10,ite):
    saved=i
  return saved

def ret(proc,fs):
  saved=None
  for i in proc("",files=fs): saved=i
  return saved

def do_parallel(path,proc,chunksize=1000):
  cpus = mp.cpu_count()
  pool = mp.Pool(cpus)
  files = list_files(path)
  chunks = grouper(chunksize,files)
  comp = [pool.apply_async(ret, args=(proc,fs)) for fs in chunks]
  results = [r.get() for r in comp]
  final_dict = defaultdict(int)
  for r in results:
    if r:
      for k,v in r.iteritems():
        final_dict[k] += v
  print(print_dict(final_dict,None))

def do_print(process):
  count = 0
  saved = None
  for p in process:
    count += 1
    saved = p
    if(count % 100 == 0):
      out_error(print_dict(p,30))
  print(print_dict(saved,None))

def scene_context(path,files=None):
  if(not files):
    files = list_files(path)
  fs = [["building.n.01","geographical_area.n.01"], ["person.n.01"], ["instrumentality.n.03"]]
  return pipe([iter_lines, in_range(fs,30), count_items], files)

def rel_grams(path,files=None):
  if(not files):
    files = list_files(path)
  process = pipe([wedge(500), iter_lines, relation_filter, n_grams(3),
                  valid_relations, count_items], files)
  return process

def bi_rel_grams(path,files=None):
  if(not files):
    files = list_files(path)
  process = pipe([wedge(500), iter_lines, relation_filter, n_grams(3),
                  valid_relations, n_grams(2), subject_match_subject, string_gram,
                  count_items], files)
  return process

#do_print(bi_rel_grams(sys.argv[1]))
do_parallel(sys.argv[1], bi_rel_grams)
