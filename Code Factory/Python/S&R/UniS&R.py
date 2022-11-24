
'''
Search and Replace Script to to 
Note:
If no Destinatin is defined, the source will be replaced!
For Help use:
python.exe '.\UniS&R.py' -h
Example:
python.exe '.\UniS&R.py' -s .\Driver\org\ -d .\Driver\out\ -c .\Driver\Config.txt -m .*S_7$

'''

import argparse
import datetime
import os
import unicodedata
import re
import string


def Worker(args):

	parser = argparse.ArgumentParser(description='FileMan Link Generator')
	parser.add_argument('-s', '--Source', default='', type=str, help='Data File to apply S&R to')
	parser.add_argument('-d', '--Destination', default='', type=str, help='Directory to search for files')
	parser.add_argument('-c', '--Config', default='Config.txt', type=str, help='Configuration File for S&R')
	parser.add_argument('-m', '--RegExMatch', default='.*', type=str, help='Optional: Regular Expression to match filename (including folder). Only if Directory is selected')

	args = parser.parse_args()
	src = args.Source
	dst = args.Destination
	match = args.RegExMatch
	conf = args.Config

	print('Source: ', src)
	print('Destination: ', dst)
	print('Match: ', match)
	print('Config File: ', conf)

	if dst == '':
		dst = src

	if dst == src:
		input("No Destination configured! Source will be replaced without backup!")
		input("Press Enter to continue or Cntr+C to exit...")

	if os.path.isfile(src):
		file = src
		SaR(file, conf, dst)

	elif os.path.isdir(src):
		ConfPat = re.compile(match)
		for path, subdirs, files in os.walk(src):
			for name in files:
			#try:
				file = os.path.join(path, name)

				match = ConfPat.match(file)
				if match:
					#print(path)
					#print(subdirs)
					#input("Press Enter to continue or Cntr+C to exit...")

					mydst = file.replace(src, dst)
					dstPath, xyz = os.path.split(os.path.abspath(mydst))
					if not os.path.exists(dstPath):
						os.makedirs(dstPath)

					print('File: ', file)
					print('Dest: ', mydst)
					#input("Press Enter to continue or Cntr+C to exit...")

					SaR(file, conf, mydst)
			#except:
			#	print('Error looping through files!')
	else:
		print('Source does not exist!')

def SaR(fname, conf, dst):

	#Load Data File
	with open(fname, 'r', encoding='utf-8', errors='ignore') as f:	#, encoding='utf-8'
		myData = f.read()

	#Load Config
	ConfPat = re.compile('(?P<S>.*)\{\|(?P<C>\w*)\|\}(?P<R>.*)')
	with open(conf, 'r', encoding='utf-8', errors='ignore') as myConf:		#, encoding='utf-8', errors='ignore'
		while True:
			# Get next line from file
			line = myConf.readline()
			match = ConfPat.match(line)
			if match:
				#print(line)
				s = match.group('S')
				r = match.group('R')
				c = match.group('C')
				#print('  Search: ',s ,'  Replace: ', r,'  Config: ', c )
				if c == 'regex':
					myData = re.sub(s, r, myData)				
				else:
					myData = myData.replace(s, r)

			#print(match)

			# end reached
			if not line:
				break
	#print(myData)
	with open(dst, 'w', encoding='utf-8') as f:
		f.write(myData)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	from sys import argv
	try:
		Worker(argv)
	except KeyboardInterrupt:
		pass
	#exit()
