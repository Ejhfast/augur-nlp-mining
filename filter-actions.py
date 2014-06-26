from __future__ import print_function
import fileinput
import sys
import warnings
def approve(actions):
  #subject match
  #TODO: automated subject match
  subject_match = ["i", "you", "he", "she", "we", "they"]

  #object match
  #TODO: automated object match. Problems found with approach of object matching
  object_match = ["me", "you", "him", "her", "us", "them", "#", "i", "you", "he", "she", "we", "they"]

  #TODO explore if the same subject or different subject match in actions[0] and actions[2]
  #Todo replace proper nouns with pronoun
  if len(set(subject_match).intersection(actions[0].split(' '))) > 0:
    if len(set(object_match).intersection(actions[2].split(' '))) == 0:
      return True
  return False


def run():
  total = 0
  count_nop = 0
  discarded = 0
  APPROVED_LIST = "files/approved-combined.tsv"
  whitelist = {}
  for line in open(APPROVED_LIST):
    whitelist[' '.join(line.split('\t')[1:-1]).rstrip()]= True

  for line in fileinput.input():
    total = total + 1
    line = line.decode("ascii", "ignore")
    actions = line.split('\t')
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
