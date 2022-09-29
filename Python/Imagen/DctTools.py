
'''
Dictionary Merger


'''

import collections
import argparse
import datetime
import os
import sys

from PIL import Image, TiffImagePlugin

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
	jd = dctmrg(jd1, jd2)

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
	elif isinstance(obj, bytes):
		return  obj.decode("utf-8", "ignore")  
		return  dct.decode(errors="replace") 
	if isinstance(obj, TiffImagePlugin.IFDRational):
		#print(obj)
		return float(obj)
	else: return obj

#------------------------------------------------------------------------------------
# Dict Merger -----------------------------------------------------------------------
def dctmrg(dct='',dctnew=''):
	if isinstance(dct, dict) and isinstance(dctnew, dict):
		for key, val in dctnew.items():
			if key in dct:
				if isinstance(val, dict):
					dct[key] = dctmrg(dct[key], dctnew[key])
				else:
					dct[key] = val
			else:
				dct[key] = dctnew[key]
		return dct
	elif not isinstance(dct, dict) and isinstance(dctnew, dict):
		print('-d1 not a Dictionary: ', dct)
		return dctnew
	elif not isinstance(dctnew, dict) and isinstance(dct, dict):
		print('-d2 not a Dictionary: ', dctnew)
		return dctnew
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
