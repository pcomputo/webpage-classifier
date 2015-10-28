import sys
import re
import os
from glob import glob

from bs4 import BeautifulSoup
from nltk.corpus import stopwords

import urllib
import urllib2

def review_to_words(directory):
    
    # Function to convert a raw review to a string of words
    # The input is a single string (a raw movie review), and 
    # the output is a single string (a preprocessed movie review)
    #
    # 1. Remove HTML
    count = 0
    result = [y for x in os.walk(directory) for y in glob(os.path.join(x[0], '*.txt'))]
    for page in result:
    	f = open(page,"rb")
    	raw_review = f.read()
    	review_text = BeautifulSoup(raw_review).get_text() 
    	#
    	# 2. Remove non-letters        
    	letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    	#
    	# 3. Convert to lower case, split into individual words
    	words = letters_only.lower().split()                             
    	#
    	# 4. In Python, searching a set is much faster than searching
    	#   a list, so convert the stop words to a set
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
    	fw.close()
    	count += 1
    	#print meaningful_words
    print count
    	#return( " ".join( meaningful_words ))
    
if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print >> sys.stderr, 'SYNTAX: cleanDataset.py [directory]'
        sys.exit(-1)
        
    review_to_words(args[0])
