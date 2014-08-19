import nltk
import fileinput
import re
import string
import numpy as np
import sys
import json

def try1():
	line = "you " + line.lower()
	tokens = nltk.word_tokenize(line)
	tagged_tokens = nltk.pos_tag(tokens)
	tagged_tokens = filter(lambda x: False if x[1] in ["DT", "PRP","RB"] else True, tagged_tokens)
	grammar = r"""
 	 action: {<V.*>}   # chunk determiner/possessive, adjectives and nouns
 	 action2: {<action.*>{<TO>*|<JJ>*|<DT>*|<action>*|<NN>*}*}
 	"""
 	cp = nltk.RegexpParser(grammar)
	result = cp.parse(tagged_tokens)
	print line,tagged_tokens, result


"""
todos: handle "don't"
"""
def clean(line):
	#line = line.decode("ascii", "ignore")
	line = line.lower()
	tokens = nltk.word_tokenize(line)
	tagged_tokens = nltk.pos_tag(tokens)
	tokens = np.array(tokens)
	boole = np.array(map(lambda x: False if x[1] in ["DT", "PRP", '.', ] else True, tagged_tokens))
	tokens = tokens[boole]
	tokens = [tokens[0], ' '.join(list(tokens[1:]))]
	return tokens

if __name__ == '__main__':
	#j = json.load(sys.stdin)
	j = json.load(open('scraped.json','r'))
	for dic in j:
		for k, v in dic.iteritems():
			if v == ['']: continue
			print clean(k), map(lambda r: clean(r), v)