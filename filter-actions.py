#todo keep track of counts of k and reverse sort

import fileinput

def approve(actions):
  #subject match
  #TODO: automated subject match
  subject_match = ["i", "you", "he", "she", "we", "they"]

  #object match
  #TODO: automated object match. Problems found with approach of object matching
  #object_match = ["me", "you", "him", "her", "us", "them", "#", "i", "you", "he", "she", "we", "they"]

  #TODO explore if the same subject or different subject match in actions[0] and actions[2]
  #Todo replace proper nouns with pronoun
  if any(any(r == s for r in subject_match) for s in actions[0].split(' ')):
    #if not any(any(r == s for r in object_match) for s in actions[2].split(' ')):
    return True
  return False

for line in fileinput.input():
  line = line.decode("ascii", "ignore")
  actions = line.split('\t')
  actions = map(lambda x: x.strip(), actions)
  if approve(actions):
    print "\t".join(actions)
  else:
    print "NOP"