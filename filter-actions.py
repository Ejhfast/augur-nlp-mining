#todo keep track of counts of k and reverse sort

import fileinput

def approve(actions):
  #subject match
  #TODO: automated subject match
  subject_match = ["i", "you", "he", "she", "it", "we", "you", "they"]

  #object match
  #TODO: automated object match
  object_match = ["me", "you", "him", "her", "us", "them", "#"]

  if any(any(r == s for r in subject_match) for s in actions[0].split(' ')):
    if not any(any(r == s for r in object_match) for s in actions[2].split(' ')):
      #k = '\t'.join(actions[1:]).rstrip()
      return True
  return False

def replace(word):
  singular = ["he", "she", "him", "i", "myself", "you", "me", "himself", "herself", "yourself"]
  plural = ["they", "them", "we", "us", "ourselves", "themselves"]
  if any(s == word for s in singular):
    return "the person"
  elif any(s == word for s in plural):
    return "the people"
  return word

for line in fileinput.input():
  line = line.decode("ascii", "ignore")
  tokens = line.split('\t')
  header = tokens[:2]
  actions = tokens[2:]
  actions = map(lambda x: replace(x.strip()), actions)
  if approve(actions):
    print "\t".join(header + actions)
  else:
    print "NOP"