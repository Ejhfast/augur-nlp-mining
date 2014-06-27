from __future__ import print_function
import fileinput
import sys
import warnings
import sys
import itertools
from itertools import tee, izip


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b= tee(iterable)
    next(a, None)
    return izip(a, b)


def approve(actions):
  subject_match = ["i", "you", "he", "she", "we", "they"]
  object_match = ["me", "you", "him", "his", "her", "us", "them", "#", "i", "you", "he", "she", "we", "they", "it"]
  if len(set(subject_match).intersection(actions[0].split())) > 0:
    if len(set(object_match).intersection(actions[2].split())) == 0:
      return True
  return False

#todo: make work with tsv whitelists
"""
APPROVED_LIST = "../files/approved-combined.tsv"
whitelist = {}
for line in open(APPROVED_LIST):
  whitelist[' '.join(line.split('\t')[1:-1]).rstrip()]= True
"""

#todo implement closing the file
def fillinput():
  inp = None
  inf = None

  if len(sys.argv) == 3:
    inf = open(sys.argv[2])
    inp = open(sys.argv[1])

  elif len(sys.argv) == 2:
    if '.txt' or 'approved' or 'whitelist' in sys.argv[1]:
      inf = open(sys.argv[1])
      inp = sys.stdin
    else:
      inf = sys.stdin
      inp = open(sys.argv[1])
  
  return (inp, inf)

def run():
  total = 0
  count_nop = 0
  discarded = 0

  (inp, inf) = fillinput()

  wl = inf.read().split()

  last_approved = " "

  for line1, line2 in pairwise(inp):
    
    total = total + 1
    
    [line1, line2] = map(lambda line: line.decode("ascii", "ignore").rstrip(), [line1, line2])
    [actions1, actions2] = map(lambda line: map(lambda x: ' '.join(x.split()), line.split('\t')), [line1, line2])
    [actions1, actions2] = map(lambda actions : actions[2:] if(len(actions) == 5) else actions, [actions1, actions2])
    if any(map(lambda actions: len(actions) != 3, [actions1, actions2])):
      discarded = discarded + 1
      continue
    if all(map(lambda actions: approve(actions), [actions1, actions2])):
      [verbobject1, verbobject2] = map(lambda actions:" ".join(actions[1:]).rstrip(), [actions1, actions2])
      #todo : any vs all
      if len(set(actions1[2].split()).intersection(wl)) > 0:
      #if all(map(lambda actions: len(set(actions[2].split()).intersection(wl)) > 0, [actions1, actions2])):
      #if whitelist.get(verbobject) == True:
        [output1, output2] = map(lambda verbobject: verbobject, [verbobject1, verbobject2])
        print("NOP ", count_nop)
        print(output1)
        print("NOP ", 0)
        print(output2)
        count_nop = 0
    else:
      count_nop += 1
    if(total%100000 ==0):
      print("Processed " + str(total) + " input lines. " + str(discarded) + " discarded", file=sys.stderr,  end="\r")

run()
