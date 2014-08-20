""" 

Experiment to investigate how well a "at home" 
vs "at dinner" classifier works with the dataset.

Supply two sets of wordlists to run

"""
import fileinput
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
import numpy as np

if __name__ == "__main__":
	#get features to create training set
	dinnerList = [''.join([i for i in r.replace('\t', ' ') if not i.isdigit()]).rstrip()  for r in open("dinner-output.txt")]
	workList = [''.join([i for i in r.replace('\t', ' ') if not i.isdigit()]).rstrip()  for r in open("work-output.txt")]
	vectorizer = CountVectorizer(min_df=3, stop_words = 'english')
	train = vectorizer.fit_transform(workList + dinnerList)
	labels = np.zeros(train.shape[0])
	labels[:len(workList)] = 0
	labels[len(workList):] = 1

	#fit the model
	clf = svm.SVC()
	clf.fit(train, labels);

	#testing
	testList = [''.join([i for i in r.replace('\t', ' ') if not i.isdigit()]).rstrip()  for r in open("test-output.txt")]
	test = vectorizer.transform(testList)
	output =  clf.predict(test)
	print "dinner" if (np.sum(np.array(output)))/(1.0*output.shape[0]) > 0.5 else "work"