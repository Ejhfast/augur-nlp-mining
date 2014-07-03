from nltk.corpus import names
import fileinput

nameswords = names.words()
nameswords = set(map(lambda x: x.lower(), nameswords))

for line in fileinput.input():
	line = line.decode("ascii", "ignore").rstrip()
	line = '\t'.join(map(lambda action: ' '.join(map(lambda x: 'he' if x in nameswords else x, action.split(' '))), line.split('\t')))
	print line