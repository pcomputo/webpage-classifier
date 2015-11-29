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

def review_to_words(directory):
	
	# Function to convert a raw review to a string of words
	# The input is a single string (a raw movie review), and 
	# the output is a single string (a preprocessed movie review)
	#
	# 1. Remove HTML
	count = 0
	webpages = []
	result = [y for x in os.walk(directory) for y in glob(os.path.join(x[0], '*.txt'))]
	print "Cleaning in progress..."
	for page in result:
		f = open(page,"rb")
		raw_review = f.read()
		count += 1
		print count
		print "Cleaning:",page
		review_text = BeautifulSoup(raw_review).get_text() 
		#
		# 2. Remove non-letters
		print "Removing non-letters..."		
		letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
		#
		# 3. Convert to lower case, split into individual words
		print "Converting to lower case and spliting to individual words..."
		words = letters_only.lower().split()							 
		#
		# 4. In Python, searching a set is much faster than searching
		#   a list, so convert the stop words to a set
		print "Removing stop words..."
		stops = set(stopwords.words("english"))				  
		# 
		# 5. Remove stop words
		meaningful_words = [w for w in words if not w in stops]   
		#
		# 6. Join the words back into one string separated by space, 
		# and return the result.
		f.close()
		fw = open(page,"wb")
		fw.write(" ".join( meaningful_words ))
		#print train_data_features.shape
		
		
		fw.close()
		print "Cleaned",page
		print
		#vectorizer = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None,  max_features = 5000)
		
		
		#print meaningful_words
	print "Total number of files cleaned: ",count
	
	
if __name__ == '__main__':
	args = sys.argv[1:]
	if not args:
		print >> sys.stderr, 'SYNTAX: cleanDataset.py [directory]'
		sys.exit(-1)
		
	review_to_words(args[0])
