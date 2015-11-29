import sys
import re
import os
from glob import glob

from bs4 import BeautifulSoup
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.ensemble import RandomForestClassifier

import urllib
import urllib2



def vectorization(directory):
	print "Preparing vectorizer"
	vectorizer = TfidfVectorizer(token_pattern=r'\b[a-z]{2,}\b', max_df=0.3, min_df=2, sublinear_tf=True)
	result = [(x,y) for x in os.walk(directory) for y in glob(os.path.join(x[0], '*.txt'))]
	#print result
	ls = []
	y_train = []
	for (cat,page) in result:
		fp = open(page,"rb")
		cleaned_data = fp.read()
		fp.close()
		ls.append(cleaned_data)
		y_train.append(cat[0].split('/')[-2])
		
	print "Vectorization in progress..."	
	X_train = vectorizer.fit_transform(ls)
	print set(y_train)
	print "Vectorization completed!"
	
	
	testClassifiers(X_train, y_train)
	Initialize a Random Forest classifier with 100 trees
	print "Preparing training"
	forest = RandomForestClassifier(n_estimators = 100)
	
	print "Training in progress..."
	forest = forest.fit(X_train.toarray(), y_train)
	
	print "Training completed!"
	
	print "Preparing classification"
	#result = forest.predict(test_data_features)
	print "Classification completed!"
	
	
if __name__ == '__main__':
	args = sys.argv[1:]
	if not args:
		print >> sys.stderr, 'SYNTAX: trainingAndTesting.py [directory]'
		sys.exit(-1)
		
	vectorization(args[0])
