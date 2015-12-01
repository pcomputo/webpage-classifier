import sys
import re
import os
from glob import glob

from bs4 import BeautifulSoup
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing
from sklearn import svm
from sklearn.ensemble import GradientBoostingClassifier

import urllib
import urllib2



def vectorization(directory):
	print "Preparing vectorizer"
	vectorizer = TfidfVectorizer(min_df=2, max_df = 0.95, sublinear_tf = True)
	
	result = [(x,y) for x in os.walk(directory) for y in glob(os.path.join(x[0], '*.txt'))]
	#print result
	ls = []
	y = []
	for (cat,page) in result:
		fp = open(page,"rb")
		cleaned_data = fp.read()
		fp.close()
		ls.append(cleaned_data)
		y.append(cat[0].split('/')[-2])
		
	print "Vectorization in progress..."	
	X = vectorizer.fit_transform(ls)
	print y[:10]
	le = preprocessing.LabelEncoder()
	y1 = le.fit_transform(y)
	print "Vectorization completed!"
	#print (vectorizer.stop_words_)
	
	#testClassifiers(X_train, y_train)
	X_train, X_test, y_train, y_test = train_test_split(X, y1, test_size=0.33, random_state=42)
	print len(y_test)
	
	#Initialize a Random Forest classifier with 100 trees
	print "Preparing training"
	#forest = RandomForestClassifier(n_estimators = 100)
	clf = svm.SVC()
	print "Training in progress..."
	#forest = forest.fit(X_train.toarray(), y_train)
	clf.fit(X_train, y_train) 
	
	print "Training completed!"
	
	print "Preparing classification"
	result = clf.predict(X_test)
	print len(result)
	print "Classification completed!"
	count = np.count_nonzero(result == y_test)
	print count
	
	#print "Confusion Matrix : "
	#print metrics.confusion_matrix(y_train, result)
	
	#print score(X_test, y_test)
	
if __name__ == '__main__':
	args = sys.argv[1:]
	if not args:
		print >> sys.stderr, 'SYNTAX: trainingAndTesting.py [directory]'
		sys.exit(-1)
		
	vectorization(args[0])
