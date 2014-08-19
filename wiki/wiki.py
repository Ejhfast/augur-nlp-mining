from nltk.tag.stanford import NERTagger
import nltk.data
import fileinput

st = NERTagger('/Users/Phoenix/Documents/CURIS/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz', '/Users/Phoenix/Documents/CURIS/stanford-ner/stanford-ner.jar');
sent_detector = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
for line in fileinput.input():
	sent = sent_detector.tokenize(line.strip())
	tagged = [st.tag(s) for s in sent]
	print tagged