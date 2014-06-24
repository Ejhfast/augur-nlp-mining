#todo keep track of counts of k and reverse sort

import fileinput

def approve(actions):
  #subject match
  #TODO: automated subject match
  subject_match = ["i", "you", "he", "she", "we", "they"]

  #object match
  #TODO: automated object match. Problems found with approach of object matching
  #object_match = ["me", "you", "him", "her", "us", "them", "#", "i", "you", "he", "she", "we", "they"]

  if any(any(r == s for r in subject_match) for s in actions[0].split(' ')):
    #if not any(any(r == s for r in object_match) for s in actions[2].split(' ')):
    return True
  return False

for line in fileinput.input():
  line = line.decode("ascii", "ignore")
  tokens = line.split('\t')
  header = tokens[:2]
  actions = tokens[2:]
  #actions = map(lambda x: replace(x.strip()), actions)
  if approve(actions):
    print "\t".join(header + actions)
  else:
    print "NOP"