import fileinput

# The list of approved tokens. See workflow.txt
APPROVED_LIST = "../tokens/approved-combined.tsv"


whitelist = {}
for line in open(APPROVED_LIST):
	whitelist[' '.join(line.split('\t')[:-1]).strip()]= True

def replace(word):
  singular = ["he", "she", "him", "i", "myself"]
  plural = ["they", "them", "we", "us", "ourselves"]
  if any(s == word for s in singular):
    return "the person"
  elif any(s == word for s in plural):
    return "the people"
  return word

for line in fileinput.input():
  tokens = line.split('\t')
  header = tokens[:2]
  relations = tokens[2:]
  relations = map(lambda x: replace(x.strip()), relations)
  if whitelist.get(' '.join(relations).strip()) == True:
    print  "\t".join(header + relations)
  else:
    print "NOP"
