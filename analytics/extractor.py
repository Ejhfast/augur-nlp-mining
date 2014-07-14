from __future__ import print_function
from collections import defaultdict, Counter, deque
import multiprocessing as mp
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
def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)
def out_error(string, clear=True):
	if clear: sys.stderr.write("\x1b[2J\x1b[H")
	print(string, file=sys.stderr)

# path -> files
def list_files(path):
  f_count = 0
  for file in glob.glob(path+"/*"):
    f_count += 1
    if(f_count%1000==0): out_error("{} files".format(f_count))
    yield file

# file -> line
def iter_lines(iter):
  for file in iter:
    if file: # Stupid None from grouper...
      with open(file,"r") as f:
        for line in f: yield line

def iter_lines_single(file):
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

# hashable item -> table
def count_items(iter):
  table = defaultdict(int)
  for i in iter:
    table["\t".join(i)] += 1
    yield table

# lines -> [words] in lines with that contain word_set items
def has_words(words):
  # word_set = set(words)
  # set_len = len(word_set)
  def window(iter):
    for word_seq in iter:
      if(reduce(operator.and_, [word_seq[i] == a for i,a in enumerate(words)])):
        yield word_seq
      # if(len(word_set.intersection(set(word_seq))) >= set_len):
      #   yield word_seq
  return window

BLOCK_SIZE = 1000

def pipeline(i,file_list):
  process = pipe([iter_lines, iter_words, n_grams(3), count_items], file_list)
  inter_res = None
  for inter_res in process: pass
  out_error("Finished through: {}".format(i*BLOCK_SIZE))
  return inter_res

def list_files_multi(path):
  pool = mp.Pool(processes=4)
  file_blocks = grouper(BLOCK_SIZE,list_files(path))
  dicts = [pool.apply_async(pipeline, args=(i,f_seq)) for i,f_seq in enumerate(file_blocks)]
  out = [p.get() for p in dicts]
  out_error("Reducing dictionaries...")
  final = defaultdict(int)
  for i,d in enumerate(out):
    out_error("Merging {}".format(i))
    if d:
      for k,v in d.iteritems(): final[k] += v
  print(print_dict(final,None))

list_files_multi(sys.argv[1])
