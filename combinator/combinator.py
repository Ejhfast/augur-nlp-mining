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

stream = iter([[1],[2],[3]])
words = iter([["i", "PRP"], ["go", "VB"], ["to", "TO"], ["the", "ART"], ["store", "NN"]])

def append_iter(v,itr):
  def thunk():
    yield v
    for i in itr: yield i
  return thunk

def comb_or(ps):
  def par(iterator):
    for p in ps:
      v,succ,rest = p(iterator)
      if(succ):
        return (v, True, rest)
      else:
        iterator = rest
    return (None, False, iterator)
  return par

def comb_then(ps,post=None):
  def par(iterator):
    parse = []
    for p in ps:
      v,succ,rest = p(iterator)
      if(not succ):
        return (None, False, rest)
      else:
        parse.append(v)
        iterator = rest
    if(post):
      parse = post(parse)
    return (parse, True, iterator)
  return par

def atom(l,can_call=False):
  if(hasattr(l,"__call__")): can_call = True
  def par(iterator):
    try:
      v = iterator.next()
      check_match = False
      if(can_call):
        check_match, new_v = l(v)
        v = new_v
      else:
        check_match = (v == l)
      if(check_match):
        return (v, True, iterator)
      else:
        iterator = itertools.chain.from_iterable([[v], iterator])
        return (None, False, iterator)
    except StopIteration:
      return (None, False, iter([]))
  return par

def skip(p):
  def par(iterator):
    v,succ,rest = p(iterator)
    if(succ):
      return (None, True, rest)
    else:
      return (None, False, rest)
  return par

def many(p):
  def par(iterator):
    results = []
    v,succ,rest = p(iterator)
    while(succ):
      if(v): results.append(v)
      iterator = rest
      v,succ,rest = p(iterator)
    return (results, True, rest)
  return par

def iter_many(p,post=None):
  def par(iterator):
    results = []
    v,succ,rest = p(iterator)
    while(succ):
      if(v):
        results.append(v)
        if(post):
          yield post(v)
        else:
          yield v
      iterator = rest
      v,succ,rest = p(iterator)
  return par

# v = atom(lambda x: (x[1][0] == "V", x))
# n = atom(lambda x: (x[1][0] == "N", x))
# adj = atom(lambda x: (x[1] == "JJ", x))
# s = atom(lambda x: (x[1] == "PRP", ["s/he", "PRP"]))
#
# adjo = comb_then([adj,n])
# nvo = comb_then([comb_or([n,s]),v,comb_or([adjo,n])])
# star = atom(lambda x: (True,x))
# filter_tokens = comb_or([v,n,adj,s,skip(star)])
# extract_relations = comb_or([nvo,skip(star)])
#
# f = iter_many(filter_tokens)
# e = iter_many(extract_relations)
#
# n = atom("n")
# many_ns = many(comb_or([atom("n"),atom("s")]))
# v_or_n = comb_or([v,n])
#
# def tokenize(iterator):
#   for l in iterator:
#     word,pos = [x.rstrip() for x in l.split("\t")]
#     yield [word,pos]

o = atom("o")
n = atom("n")
j = atom("j")
p = atom("p")
nj = comb_or([o,n,j])
nj_p = comb_then([nj,many(p)])
print(nj_p(iter("npppp")))

# parse, state, rest = mal(words)
# print(parse)
# for i in rest:
#   print(i)
