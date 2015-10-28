import sys
import os

def fix_file_extension(html_extension):
	original_file = html_extension
	html_extension = html_extension[:-4]
	txt_extension = html_extension + "txt"
	
	os.rename(original_file,txt_extension)
	
	return txt_extension
	

def noline(data):
	fw = open(data,"rb")
	fixed_extension = fix_file_extension(data)
	fw.close()
	ftxt = open(fixed_extension, "rb")
	raw_data = ftxt.read()
	nonewline_soup = " ".join(line.strip() for line in raw_data.split("\n"))
	print nonewline_soup
	ftxt.close()
	

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print >> sys.stderr, 'SYNTAX: nonewline.py [directory]'
        sys.exit(-1)

    noline(args[0])
