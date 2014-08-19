from nltk.tag.stanford import NERTagger
import nltk.data
import fileinput

st = NERTagger('./stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz', './stanford-ner/stanford-ner.jar');
sent_detector = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
for line in fileinput.input():
    sents = sent_detector.tokenize(line.strip());
    for sent in sents:
    	st.tag(sent.split());