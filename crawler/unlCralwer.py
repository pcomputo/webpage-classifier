#!/usr/bin/env python


from bs4 import BeautifulSoup
import sys
import urllib
import urllib2
import json
from nltk.corpus import stopwords
import urlparse
import re

package = ""
visited = set()
unvisited = set()
count = 0

cachedStopWords = stopwords.words("english")

#Entry point
def CrawlPage (url):
    global package
    package = url

#Cleans the soup
def cleanSoup(soup):
    cleanedHtml_soup = soup.get_text()
    nonewline_soup = " ".join(line.strip() for line in cleanedHtml_soup.split("\n"))
    lowercase_soup = nonewline_soup.lower()
    meaningful_soup = ' '.join([word for word in lowercase_soup.split() if word not in cachedStopWords])
    
    #print meaningful_soup
    #return soup

def fix_url(url):
	if url[-1] == '/': 
		url = url[:-1]

	return url
	
def is_valid_webpage(url):
	extensions_notincluded = ('pdf','png','jpg','zip','tar','exe', 'ppt', 'doc')
	
	return not url[-3:] in extensions_notincluded

def is_valid_url(url):
	regUNL = re.compile('http://(?:www\.)?(cse.unl.edu/*)')
	
	return regUNL.search(url)
        
                  
#Creates the soup
def createSoup(url):
    global visited
    global unvisited
    global count
    
    fixed_url = fix_url(url)
    if is_valid_url(fixed_url) and not (fixed_url in visited):
    	print "Now crawling: ", fixed_url
    	try:
        	response = urllib.urlopen(fixed_url)
    	except urllib.error.HTTPError as e:
        	print( "HTTPError with: ", fixed_url, "\t", e )
        	return None
    
    	#print "BOW for: %s",url  
    	the_page = response.read()
    	soup = BeautifulSoup(the_page)  
    	cleanSoup(soup)
    	visited.add(fixed_url)
        print "Crawled: ", fixed_url
        count = count + 1
        print count
    
    	for link in soup.find_all('a'):
			href = link.get('href')
			if href:
				print href
				fixed_href = fix_url(href)
				if is_valid_url(fixed_href) and is_valid_webpage(fixed_href) and not (fixed_href in visited) and not (fixed_href in unvisited):
					print "Added to unvisited: ",fixed_href
					unvisited.add(fixed_href)
					createSoup(fixed_href)

    #for unvisitedpage in unvisited:
    	#if unvisitedpage not in visited:
			#createSoup(unvisitedpage)
    
if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print >> sys.stderr, 'SYNTAX: unlCrawler.py [webpage]'
        sys.exit(-1)

    createSoup(args[0])
