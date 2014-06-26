from __future__ import print_function
import fileinput
import sys
import warnings

def approve(actions):
  subject_match = ["i", "you", "he", "she", "we", "they"]
  object_match = ["me", "you", "him", "his", "her", "us", "them", "#", "i", "you", "he", "she", "we", "they", "it"]
  if len(set(subject_match).intersection(actions[0].split())) > 0:
    if len(set(object_match).intersection(actions[2].split())) == 0:
      return True
  return False


def run():
  total = 0
  count_nop = 0
  discarded = 0
  APPROVED_LIST = "../files/approved-combined.tsv"
  whitelist = {}
  for line in open(APPROVED_LIST):
    whitelist[' '.join(line.split('\t')[1:-1]).rstrip()]= True

  for line in fileinput.input():
    total = total + 1
    line = line.decode("ascii", "ignore").rstrip()
    actions = map(lambda x: ' '.join(x.split()), line.split('\t'))
    if(len(actions) == 5):
      actions = actions[2:]
    if(len(actions) != 3):
      discarded = discarded + 1
      continue
    if approve(actions):
      verbobject = " ".join(actions[1:]).rstrip()
      if whitelist.get(verbobject) == True:
        output = "the person " + verbobject
        print("NOP ", count_nop)
        print(output)
        count_nop = 0
    else:
      count_nop += 1
    if(total%100000 ==0):
      print("Processed " + str(total) + " input lines. " + str(discarded) + " discarded", file=sys.stderr,  end="\r")

run()
