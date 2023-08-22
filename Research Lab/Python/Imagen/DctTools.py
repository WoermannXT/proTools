
'''
Dictionary Merger


'''

import collections
import argparse
import datetime
import os
import sys

from PIL import Image , TiffImagePlugin

def Worker(args):
	print("User Current Version:-", sys.version)
	# -- Arguments Definitions --------------------------------------------------------------------------------------------------------------
	parser = argparse.ArgumentParser(description='FileMan Link Generator')
	parser.add_argument('-d1', '--dictionary', type=str, default={'1':123, '2':234, '3':345, 'X':{'a':'abc', 'b':'bcd', 'c':'cde', }}, help='Dictionary to be updated')
	parser.add_argument('-d2', '--dictnew', type=str, default={'1':1234, '22':2234, '33':3345,  'X':{'aa':'aabc', 'bb':'bbcd', }}, help='New Dictionary to merge into the first one')

	# -- Variable Definitions --------------------------------------------------------------------------------------------------------------
	args = parser.parse_args()
	# -- Initial Setup
	jd1 = args.dictionary
	jd2 = args.dictnew

	#jd = {**jd1, **jd2}

	print(jd1)
	print(jd2)
	jd = DctMrg(jd1, jd2)

	print(dctcln(jd))

#------------------------------------------------------------------------------------
# Dict Clean up ---------------------------------------------------------------------
def dctcln(obj):
	if isinstance(obj, dict):
		for key, val in obj.items():
			obj[key] = dctcln(val)
		return obj
	elif isinstance(obj, tuple):
		return tuple(dctcln(val) for val in obj)
	elif isinstance(obj, TiffImagePlugin.IFDRational):
		return float(obj)
	elif isinstance(obj, bytes):
		#return  obj.decode("utf-8", "ignore")  
		return  obj.decode(errors="replace") 
	#elif isinstance(obj, list):
	#	return list(dctcln(val) for val in obj)
	else: 
		#print("dctcln -> non defined tyte found:", type(obj), str(obj))
		return obj

#------------------------------------------------------------------------------------
# Dict Merger -----------------------------------------------------------------------
def DctMrg(dct='',dctnew=''):
	try:
		d=dct.copy()
	except:
		d=dct
	try:
		d2=dctnew.copy()
	except:
		d2=dctnew
	if isinstance(d, dict) and isinstance(d2, dict):
		for key, val in d2.items():
			if key in d:
				if isinstance(val, dict):
					d[key] = DctMrg(d[key], d2[key])
				else:
					d[key] = val
			else:
				d[key] = d2[key]
		return d
	elif not isinstance(d, dict) and isinstance(d2, dict):
		print('-d1 not a Dictionary: ', d)
		return d2
	elif not isinstance(d2, dict) and isinstance(d, dict):
		print('-d2 not a Dictionary: ', d2)
		return d
	else:
		return {}

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	from sys import argv
	try:
		Worker(argv)
	except KeyboardInterrupt:
		pass
	exit()
