from nltk.tag.stanford import POSTagger
import os

class Tagger():
	def __init__(self):
		self.st = POSTagger(os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + '/stanford-pos/models/english-bidirectional-distsim.tagger'), os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + '/stanford-pos/stanford-postagger.jar')); 

	def tag(self, line):
		return self.st.tag(line.split());

if __name__ == '__main__':
	t = Tagger();
	print t.tag('What is the airspeed of an unladen swallow ?')