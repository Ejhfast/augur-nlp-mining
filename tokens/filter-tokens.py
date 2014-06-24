import fileinput
MIN = 10

def replace(word):
	#TODO: see why this filter different from that in filter-actions.py
	singular = ["he", "she", "him", "i", "myself", "you", "me", "himself", "herself", "yourself"]
	plural = ["they", "them", "we", "us", "ourselves", "themselves"]
	if any(s == word for s in singular):
		return "the person"
	elif any(s == word for s in plural):
		return "the people"
	return word

object_match = ["the person", "the people", "it", "her",
	            "that", "this", "#", "there", "all", "'s", "the #"]

for line in fileinput.input():
	replace_pronouns = map(lambda x: ' '.join(map(lambda y: replace(y).rstrip() ,x.split(' '))), line.split('\t'))
	if not any(s == replace_pronouns[2].strip() for s in object_match) and int(replace_pronouns[3]) >= MIN:
		print '\t'.join(replace_pronouns)