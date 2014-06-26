#todo keep track of counts of k and reverse sort

import fileinput

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
  APPROVED_LIST = "approved-combined.tsv"
  whitelist = {}
  for line in open(APPROVED_LIST):
    whitelist[' '.join(line.split('\t')[1:-1]).rstrip()]= True

  for line in fileinput.input():
    line = line.decode("ascii", "ignore")
    actions = line.split('\t')[2:]
    if approve(actions):
      verbobject = " ".join(actions[1:]).rstrip()
      if whitelist.get(verbobject) == True:
        output = "the person " + verbobject
        print output
    else:
      print "NOP"

run()